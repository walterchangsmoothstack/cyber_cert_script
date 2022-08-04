# importing required modules
import PyPDF2 # Written using PyPDF2 2.5.0, if updated or using a different version, then text parse may be in different order or contain different text
import os, logging
from cgitb import text
from operator import contains

logging.basicConfig()
logging.getLogger().setLevel(logging.ERROR)

class PDFExtractor:
    # Returns a list of strings that are extracted from the PDF using PyPDF2
    def extractPDFText(self, filename: str):
        print('Extracting text from PDF: ' + filename)

        # creating a pdf file object
        pdfFileObj = open(filename, 'rb')
        
        # creating a pdf reader object
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        
        # printing number of pages in pdf file
        print('Pages in PDF: {}'.format(pdfReader.numPages))

        extractedText = ''
        
        for x in range(pdfReader.numPages):
            # creating a page object
            pageObj = pdfReader.getPage(x)
            # extracting text from page
            text = pageObj.extractText() # Returns parsed text fields separated with a newline
            extractedText += text
        
        # closing the pdf file object
        pdfFileObj.close()

        extractedText = extractedText.split('\n') # Split string by newline to form string list
        extractedText = [i for i in extractedText if i] # Remove all empty strings from the string list

        return extractedText

    # Removes strings contained in unwantedStrings from a list of strings, including substrings
    def removeUnwantedStrings(self, textList, unwantedStrings):
        newTextList = []
        for text in textList:
            unwanted = False
            for phrase in unwantedStrings:
                if phrase in text:
                    unwanted = True
                    break
            if not unwanted:
                newTextList.append(text)
        return newTextList

    # Parses a specified Cybersecurity Completion Certificate PDF for text, then gets the name and completion date on it
    def getCertificateCompletionData(self, filename: str):
        unwantedStrings = ['Date:', 'This acknowledges that', 'has successfully completed', 'Cyber Security and Privacy Awareness Basics', 'Completion Certificate', 'TCPDF']
        textList = self.extractPDFText(filename)
        textList = self.removeUnwantedStrings(textList, unwantedStrings)
        return textList

    def extractCertificateDataFromDirectory(self, directoryname):
        
        for filename in os.listdir(directoryname):
            if not filename.endswith('.pdf'):
                logging.error('******\n{} is not a PDF, skipping for text extraction.'.format(filename))
                continue

            print('******\nPDF Text from {}'.format(filename))
            print(self.getCertificateCompletionData(os.path.join(directoryname, filename)))
