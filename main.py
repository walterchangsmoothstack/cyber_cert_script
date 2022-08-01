import configparser, os, logging, re
from data_to_csv import ExcelWriter
from graph import Graph
from outlook_parser import OutlookParser
from pdf_extract import PDFExtractor
from sharepoint_upload_helper import SharepointUpload


logging.basicConfig()
logging.getLogger().setLevel(logging.ERROR)


def main():
    print('Parsing Cybersecurity Certificates\n')

    # Load settings
    config = configparser.ConfigParser()
    config.read(['config.cfg', 'config.dev.cfg'])
    azure_settings = config['azure']

    # Load environment variables from the config.cfg file
    variables = config['variables']

    # Create objects from helper classes
    graph: Graph = Graph(azure_settings)
    outlook: OutlookParser = OutlookParser(graph)
    sharepoint: SharepointUpload = SharepointUpload(graph)

    excelWriter: ExcelWriter = ExcelWriter()
    pdfExtractor: PDFExtractor = PDFExtractor()

    # Fetch all emails in Cybersecurity Certification folder
    cybercert_folder = outlook.list_folders()
    cyber_id = outlook.get_folder_id('cybersecurity',cybercert_folder)

    messages = outlook.list_inbox(cyber_id)

    # Grab drive_id using site name and drive name
    drive_id = sharepoint.get_drive_id(variables['SITE_NAME'], variables['DRIVE_NAME'])
    list_of_filenames = sharepoint.list_files_in_folder(drive_id, variables['DRIVE_PATH'])

    # Dict definition to write excel rows
    excel_rows = []

    # Parse email for "Cybersecurity Cert" regex and PDF attachment (Skip any WinZip or Encrypted Word Document)
    for message in messages:
        print(message['id'])

        #NOTE CHANGED MICHAEL'S CODE HERE. list_attachments seems to return a list
        # Check that there is one attachment
        attachments = outlook.list_attachments(message['id']) #.get('value')

        if len(attachments) != 1:  # Skip email if there is more than one attachment or no attachment
            continue

        # Check single attachment is a PDF
        file_name = attachments[0]['name']
        print(attachments)
        if file_name[-4:] != '.pdf': # Skip email if the single attachment does not have .pdf file extension
            continue

        # Grab the PDF from the email
        attachment_name_and_content_dict = outlook.get_attachment_content(message, attachments[0]['id'])

        #NOTE CHANGED MICHAEL'S CODE HERE. changed [0] -> ['attachmentName]
        # Grab the First and Last from the email
        firstName = attachment_name_and_content_dict['attachmentName'].split('_')[1]
        lastName = attachment_name_and_content_dict['attachmentName'].split('_')[0]

        #NOTE CHANGED MICHAEL'S CODE HERE. changed [1] -> ['attachmentContent']
        # Upload PDF to Sharepoint Folder
        sharepoint.upload_file(drive_id, variables['DRIVE_PATH'], attachment_name_and_content_dict['attachmentName'], 
            attachment_name_and_content_dict['attachmentContent'], list_of_filenames)

        # Write the EID, name parsed from PDF, and Certificate Completion Date to the List to be put in excel
        with open(attachment_name_and_content_dict['attachmentName'], 'wb') as temp_file:
            temp_file.write(attachment_name_and_content_dict['attachmentContent'])
        
        certificateData = pdfExtractor.getCertificateCompletionData(attachment_name_and_content_dict['attachmentName'])

        # Remove the temporary file
        os.remove(attachment_name_and_content_dict['attachmentName'])
        excel_rows.append({'Last Name': lastName, 'First Name': firstName, 'EID': message['email'].split('@')[0], 
            'Name on Certificate': certificateData[0], 'Certificate Completion Date': certificateData[1]})
        print(excel_rows)

        # Move processed email into new Outlook folder
        # TODO: Write function to move email to new folder

    # Write excel file
    excelWriter.writeToExcel(excel_rows, variables['EXCEL_FILENAME'], variables['EXCEL_WRITE_PATH'])

    # Notify user of any emails that could not be parsed


main()