from graph import Graph

class OutlookParser:

    def list_folders(graph: Graph):
        folders = graph.get_folders().get('value')
        print("Found folders: \n{}".format(folders))

        print(folders)

        folder_name = 'cybersecurity'

        for x in folders:
            if x['displayName'] == folder_name:
                folder_id = x['id']

        return folder_id

    def list_inbox(graph: Graph, folder_id: str):
        message_page = graph.get_inbox(folder_id).get('value')

        for message in message_page:
            attachment = graph.get_attachments(message['id']).get('value')
            file_name = attachment[0]['name']
            attachment_content = graph.download_attachments(message['id'], attachment[0]['id'])

            with open(f'{file_name}', 'wb') as _f:
                _f.write(attachment_content.content)

        # If @odata.nextLink is present
        more_available = '@odata.nextLink' in message_page
        print('\nMore messages available?', more_available, '\n')
