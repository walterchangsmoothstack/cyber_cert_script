#Part of Cyber Certificate FSA requirement to list all members who have
#completed the cyber security certificate onto an Excel sheet
#Take pdf file from local folder and upload it to a Sharepoint folder

import requests, json

client_id = 'fb942e3b-2825-4f36-b466-ce9eea33454d'
client_secret = 'q0ibdmfQOcH6slK2wQFe3HcZN0X237Uz7f2E7AfsI/Y='
tenant =  'smoothstack0' # e.g. https://tenant.sharepoint.com
tenant_id = '7824f42c-45bd-47d8-8d15-275c536fa0a2'  
client_id = client_id + '@' + tenant_id

data = {
    'grant_type':'client_credentials',
    'resource': "00000003-0000-0ff1-ce00-000000000000/" + tenant + ".sharepoint.com@" + tenant_id, 
    'client_id': client_id,
    'client_secret': client_secret,
}

headers = {
    'Content-Type':'application/x-www-form-urlencoded'
}

url = "https://accounts.accesscontrol.windows.net/"+ tenant_id + "/tokens/OAuth/2"
r = requests.post(url, data=data, headers=headers)
json_data = json.loads(r.text)

print(json_data)


headers = {
    'Authorization': "Bearer " + json_data['access_token'],
    'Accept':'application/json;odata=verbose',
    'Content-Type': 'application/json;odata=verbose'
}

data = '''{ "__metadata": {"type": "SP.Data.testListItem"},
    "Title": "PythonAPI", 
    "Name": "walt", 
    "Message": "Hello from Python"
}'''

url = "https://" + tenant + ".sharepoint.com/sites/Test/_api/web/lists/getbytitle('test')/items"
p = requests.post(url, headers=headers, data=data)

print(p.text)