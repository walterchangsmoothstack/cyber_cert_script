from fileinput import filename
import json
from configparser import SectionProxy
import site
from wsgiref.util import request_uri
from azure.identity import DeviceCodeCredential, ClientSecretCredential, CertificateCredential
from msgraph.core import GraphClient



class Graph:
    settings: SectionProxy
    device_code_credential: DeviceCodeCredential
    user_client: GraphClient
    client_credential: ClientSecretCredential
    app_client: GraphClient
    certificate_credential: CertificateCredential

    def __init__(self, config: SectionProxy):
        self.settings = config
        client_id = self.settings['clientId']
        tenant_id = self.settings['authTenant']
        graph_scopes = self.settings['graphUserScopes'].split(' ')
        client_cert_path = "PATH_TO_CERTIFICATE_HERE"
        password = 'CERTIFICATE_PASSWORD_HERE'
    
        self.device_code_credential = DeviceCodeCredential(client_id, tenant_id = tenant_id)
        self.user_client = GraphClient(credential=self.device_code_credential, scopes=graph_scopes)

        #------------------------------------------------
        # Use app-only authentication with a certificate
        #------------------------------------------------
        # self.certificate_credential = CertificateCredential(tenant_id = tenant_id, client_id = client_id, certificate_path = client_cert_path, password = password)

        #------------------------------------------------
        # Use app-only authentication with a clientSecret
        #------------------------------------------------

        # client_secret = self.settings['clientSecret']
        # self.client_credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        # self.app_client = GraphClient(credential=self.client_credential,
        #                             scopes=['https://graph.microsoft.com/.default'])
    

    # Make a call to get a site using a query. Returns the json response of the API call
    def get_site(self, site_name):

        # Query the site by its exact name
        request_url = f"/sites?search={site_name}"

        response = self.user_client.get(request_url)
        
        return response
    
    # Make a call to get the drives (document library, list, etc..) of the site with 'site_id'
    def get_drive(self, site_id):

        # Retrieve the drives from the site the certificates will be uploaded to
        request_url = f"/sites/{site_id}/drives"
        
        response = self.user_client.get(request_url)

        return response        

    # Make a put request to upload the file to the appropriate folder
    def upload_file(self, drive_id, drive_path, filename, fileContent):
        
        # Upload the content using this path
        request_url = f"/drives/{drive_id}/root:/{drive_path}/{filename}:/content"
        
        # Set the header to accept a binary value
        headers = {'Content-type': 'application/binary'}
        response = self.user_client.put(request_url, headers=headers, data=fileContent)
        return response

    # Make a request to get a file with the filename passed in
    def list_files(self, drive_id, folder_path):

        # Use the query endpoint to search for the filename
        # request_url = f"/drives/{drive_id}/root:/cyber_security_certs:/children"
        request_url = f'/drives/{drive_id}/root:/{folder_path}:/children'
        # request_url = f"/drives/{drive_id}/root:/cyber_security_certs/search(q='{filename}')"
        # request_url = f"/drives/{drive_id}/root:/children/?$search=webUrl:https://smoothstack0.sharepoint.com/sites/Test/Shared%20Documents/cyber_security_certs/hello.txt"
        
        response = self.user_client.get(request_url)
        return response
    
    # Make a request to get a file using the drive_id and the file_id
    def get_file(self, drive_id, file_id):
        request_url = f"/drives/{drive_id}/items/{file_id}"
        response = self.user_client.get(request_url)
        print(response.json())
        return response

    # Make a request to get the user token
    def get_user_token(self):
        graph_scopes = self.settings['graphUserScopes']
        access_token = self.device_code_credential.get_token(graph_scopes)
        return access_token.token

    
    
        
    

    
        