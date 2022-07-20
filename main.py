import configparser, os, logging
from graph import Graph


logging.basicConfig()
logging.getLogger().setLevel(logging.ERROR)

SITE_NAME='Test'
DRIVE_NAME='Documents'
DRIVE_PATH='cyber_security_certs'
PATH_OF_DIRECTORY='../CyberCertExamples/'


def main():
    print('Python Graph Tutorial\n')

    # Load settings
    config = configparser.ConfigParser()
    config.read(['config.cfg', 'config.dev.cfg'])
    azure_settings = config['azure']

    graph: Graph = Graph(azure_settings)

    # Call the function to get a site by its name. 
    response = graph.get_site(SITE_NAME)

    json_data = response.json() if response and response.status_code == 200 else None
    if json_data and 'value' in json_data:
        
        # Retrieve the site ID of the first site from the results
        try:
            site_id = json_data['value'][0]['id']
        except:
            logging.error("Something went wrong while retrieving the site ID. Make sure the site %s exists.", site_name)
            logging.error(response.json())
            return None

    # Call the function to get all the drives of the site from above
    response = graph.get_drive(site_id)
    
    json_data = response.json() if response and response.status_code == 200 else None
    list_of_drives = json_data['value'] if json_data and 'value' in json_data else None
    
    try:
        # Loop through all the drives in the site and check if the name matches
        for drive in list_of_drives:
            if drive['name'] == DRIVE_NAME:
                drive_id = drive['id']
    except:
        logging.error("Something went wrong while retrieving the drive ID of %s.", DRIVE_NAME)
        logging.error(response.json())
        return None

    # Go through each file (certificate) in the folder PATH_OF_DIRECTORY variable
    # Convert each file to a binary stream
    # Pass the data to the upload function, which uploads the file to the folder DRIVE_PATH variable on Sharepoint
    for filename in os.listdir(PATH_OF_DIRECTORY):
        f = os.path.join(PATH_OF_DIRECTORY,filename)
        if os.path.isfile(f) and filename.endswith('.pdf'):
            with open(f, mode='rb') as file: # Read binary
                fileContent = file.read()
            response = graph.upload_file(drive_id, DRIVE_PATH, filename, fileContent)
            print(response.json())


main()