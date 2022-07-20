from fileinput import filename
import json
from configparser import SectionProxy
import site
from wsgiref.util import request_uri
from azure.identity import DeviceCodeCredential, ClientSecretCredential
from msgraph.core import GraphClient



class Graph:
    settings: SectionProxy
    device_code_credential: DeviceCodeCredential
    user_client: GraphClient
    client_credential: ClientSecretCredential
    app_client: GraphClient

    def __init__(self, config: SectionProxy):
        self.settings = config
        client_id = self.settings['clientId']
        tenant_id = self.settings['authTenant']
        graph_scopes = self.settings['graphUserScopes'].split(' ')

        self.device_code_credential = DeviceCodeCredential(client_id, tenant_id = tenant_id)
        self.user_client = GraphClient(credential=self.device_code_credential, scopes=graph_scopes)
        
        client_secret = self.settings['clientSecret']

        self.client_credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        self.app_client = GraphClient(credential=self.client_credential,
                                    scopes=['https://graph.microsoft.com/.default'])
    

    # Make a call to get a site using a query. Returns the json response of the API call
    def get_site(self, site_name):

        #query the site by its exact name
        request_url = f"/sites?search={site_name}"

        response = self.user_client.get(request_url)
        
        return response
    
    # Make a call to get the drives (document library, list, etc..) of the site with 'site_id'
    def get_drive(self, site_id):

        #retrieve the drives from the site the certificates will be uploaded to
        request_url = f"/sites/{site_id}/drives"
        
        response = self.user_client.get(request_url)

        return response        

    # Make a put request to upload the file to the appropriate folder
    def upload_file(self, drive_id, drive_path, filename, fileContent):
        
        
        request_url = f"/drives/{drive_id}/root:/{drive_path}/{filename}:/content"
        
        # Set the header to accept a binary value
        headers = {'Content-type': 'application/binary'}
        response = self.user_client.put(request_url, headers=headers, data=fileContent)
        return response
    
        
    

    
        