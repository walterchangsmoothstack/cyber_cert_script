from graph import Graph

class OutlookParser:

    graph: Graph
    
    def __init__(self, graph: Graph):
        self.graph = graph

    def list_folders(self) -> list:
        folders = self.graph.get_folders().get('value')

        return folders

    def get_folder_id(self, folder_name: str, folders: list) -> str:
        for x in folders:
            if x['displayName'] == folder_name:
                folder_id = x['id']

        return folder_id

    def create_folder(self) -> str:
        folder = { 'displayName': 'completed_Cybersecurity_Certs' }
        folder_creation = self.graph.create_folder(folder)

        return folder_creation.json()

    def parse_name(sender: str) -> dict:
        user = {}

        # Last, First format
        if ',' in sender:
            sender = sender.split(', ')
            user['First name'] = sender[1]
            user['Last name'] = sender[0]

            temp = ''
            i = 0
            if '[' in user['First name']:
                while user['First name'][i] != ' ':
                    temp += user['First name'][i]
                    i += 1

            user['First name'] = temp

        # First Last format
        else:
            sender = sender.split(' ')
            user['First name'] = sender[0]
            user['Last name'] = sender[1]

        return user

    def list_inbox(self, folder_id: str) -> list:
        message_page = self.graph.get_inbox(folder_id).get('value')
        messages_list = []

        while True:
            for message in message_page:
                x = {}
                x['id']      = message['id']
                x['subject'] = message['subject']
                x['email']   = message['sender']['emailAddress']['address']
                x['sender']  = message['sender']['emailAddress']['name']
                x['user']    = self.parse_name(x['sender'])
                messages_list.append(x)
            if not '@odata.nextLink' in message_page:
                break
            message_page = self.graph.get(message_page['@odata.nextLink'])

        return messages_list

    def list_attachments(self, message_id):
        return self.graph.get_attachments(message_id).get('value')

    def get_attachment_content(self, message, attachment_id):
        attachment = self.graph.get_attachments(message['id']).get('value')
        file_suffix = attachment[0]['contentType']
        file_suffix = file_suffix.split('/')[1]
        attachment_name = "{0}_{1}_Cybersecurity.{2}".format(message['user']['Last name'], 
                                                    message['user']['First name'], file_suffix)
        attachment_content = self.graph.download_attachments(message['id'], attachment_id).content

        return {"attachmentName": attachment_name, "attachmentContent": attachment_content}
