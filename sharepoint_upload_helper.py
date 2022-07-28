import logging, configparser
from graph import Graph

logging.basicConfig()
logging.getLogger().setLevel(logging.ERROR)


# Finds the site by querying the site_name, then finds the drive_id by querying the drive_name
def get_drive_id(graph, site_name, drive_name):
    
    # Get the site ID of the site to upload to
    response = graph.get_site(site_name)

    json_data = response.json() if response and response.status_code == 200 else None
    if json_data and 'value' in json_data:
        
        # Retrieve the site ID of the first site from the results
        try:
            # Loop through the result from the query and check if the name matches
            for site in json_data['value']:
                if site['name'] == site_name:
                    site_id = site['id']
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
            if drive['name'] == drive_name:
                drive_id = drive['id']
    except:
        logging.error("Something went wrong while retrieving the drive ID of %s.", drive_name)
        logging.error(response.json())
        return None
    return drive_id

def list_files_in_folder(graph, drive_id, folder_path):
    # List the files in the target folder
    response = graph.list_files(drive_id, folder_path)
    json_data = response.json() if response and response.status_code == 200 else None
    list_of_files = json_data['value'] if json_data and 'value' in json_data else None
    
    list_of_filenames = [file['name'] for file in list_of_files if 'name' in file]
    return list_of_filenames

# Takes a file and uploads the content to a Sharepoint folder after verifying that a file of that
# name does not already exist. If it does, then append a count to the filename before uploading.
# Filname should have the .pdf extension
def upload_file(graph, drive_id, folder_path, filename, fileContent, list_of_filenames):
    i = 0
    count = 1
    # Save just the filename without the extension or count for use later to handle double/triple digit counts
    tmp_filename = filename[:-4]
    # Put the count in between the filename and extension
    filename = f'{tmp_filename}({count}).pdf'
    while i in range(0, len(list_of_filenames)):
        if list_of_filenames[i] == filename:
            logging.info(f"File already exists. Appending ({count}) to the filename")
            count += 1
            filename = f'{tmp_filename}({count}).pdf'
            # Resetting count to 0
            i = 0
        else:
            i +=1
    response = graph.upload_file(drive_id, folder_path, filename, fileContent)
    return response
    



# ----------------------------------------------------
# Testing the helper method
# ----------------------------------------------------

# config = configparser.ConfigParser()
# config.read(['conf.cfg', 'config.dev.cfg'])
# azure_settings = config['azure']

# # Load environment variables from the config.cfg file
# variables = config['variables']

# graph: Graph = Graph(azure_settings)

# drive_id = get_drive_id(graph, variables['SITE_NAME'], variables['DRIVE_NAME'])

# list_of_file_names = list_files_in_folder(graph, drive_id, variables['DRIVE_PATH'] )

# with open(f"{variables['PATH_OF_DIRECTORY']}Cyber_Security_Certificate.pdf", mode='rb') as file: # Read binary
#     fileContent = file.read()
# upload_file(graph, drive_id, variables['DRIVE_PATH'], "Cyber_Security_Certificate.pdf", fileContent, list_of_file_names)