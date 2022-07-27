import configparser, os, logging, re
from graph import Graph


logging.basicConfig()
logging.getLogger().setLevel(logging.ERROR)


def main():
    print('Python Graph Tutorial\n')

    # Load settings
    config = configparser.ConfigParser()
    config.read(['config.cfg', 'config.dev.cfg'])
    azure_settings = config['azure']

    # Load environment variables from the config.cfg file
    variables = config['variables']

    graph: Graph = Graph(azure_settings)


    # Call the function to get a site by its name. 
    response = graph.get_site(variables['SITE_NAME'])

    json_data = response.json() if response and response.status_code == 200 else None
    if json_data and 'value' in json_data:
        
        # Retrieve the site ID of the first site from the results
        try:
            # Loop through the result from the query and check if the name matches
            for site in json_data['value']:
                if site['name'] == variables['SITE_NAME']:
                    site_id = site['id']
        except:
            logging.error("Something went wrong while retrieving the site ID. Make sure the site %s exists.", variables["SITE_NAME"])
            logging.error(response.json())
            return None

    # Call the function to get all the drives of the site from above
    response = graph.get_drive(site_id)
    
    json_data = response.json() if response and response.status_code == 200 else None
    list_of_drives = json_data['value'] if json_data and 'value' in json_data else None
    
    try:
        # Loop through all the drives in the site and check if the name matches
        for drive in list_of_drives:
            if drive['name'] == variables['DRIVE_NAME']:
                drive_id = drive['id']
    except:
        logging.error("Something went wrong while retrieving the drive ID of %s.", variables['DRIVE_NAME'])
        logging.error(response.json())
        return None

    # List the files in the target folder
    response = graph.list_files(drive_id, variables['DRIVE_PATH'])
    json_data = response.json() if response and response.status_code == 200 else None
    list_of_files = json_data['value'] if json_data and 'value' in json_data else None


    # Go through each file (certificate) in the folder PATH_OF_DIRECTORY variable
    # Convert each file to a binary stream
    # Pass the data to the upload function, which uploads the file to the folder DRIVE_PATH variable on Sharepoint
    # If the filename already exists, append a number to the filename ex. "John_Doe_CyberSecurity_Certificate(1).pdf"
    for filename in os.listdir(variables['PATH_OF_DIRECTORY']):
        f = os.path.join(variables['PATH_OF_DIRECTORY'],filename)
        if os.path.isfile(f) and filename.endswith('.pdf'):
            count = 1
            i = 0
            # Check if the filename already has a number at the end
            regex_match = re.match("\w*\(\d*\).pdf", filename)
            # Save the filename as a variable without the extension or count
            tmp_filename = filename[:-7] if regex_match else filename[:-4]
            try:
                # Loop through all the items and check if an item with the filename already exists
                while i in range(len(list_of_files)):
                    # Append the count to the filename
                    # Increment the count and start from the beginning of the loop again
                    if list_of_files[i]['name'] == filename:
                        logging.info("Filename already exists")
                        filename = f"{tmp_filename}({count}).pdf"
                        count+=1
                        i = 0
                    else:
                        i+=1
            except Exception as e:
                logging.error("Something went wrong while retrieving the files in the folder.")
                print(e)
            with open(f, mode='rb') as file: # Read binary
                fileContent = file.read()
            response = graph.upload_file(drive_id, variables['DRIVE_PATH'], filename, fileContent)


main()