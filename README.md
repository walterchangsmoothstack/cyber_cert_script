cybercertscript
=================

Script to download cyber security certificate PDFs from Outlook and upload them to Sharepoint

## Installation instructions
1. Install Python 3 for the respective operating system and architecture from [here](https://www.python.org/downloads/)
2. Download the source code from Github [here](https://github.com/walterchangsmoothstack/cyber_cert_script/archive/refs/heads/main.zip) and extract the zip file to the desired location
3. Create a file named config.cfg with the following content:
```
[azure]
clientId = [ Your clientId]
clientSecret = [ Your clientSecret ]
tenantId = [ Your tenantId ]
authTenant = [ Same as tenantId ]
graphUserScopes = user.read mail.read mail.send sites.read.all sites.manage.all files.readwrite.all


[variables]
SITE_NAME=[ Your Site Name ]
DRIVE_NAME=Documents
DRIVE_PATH=[ Sharepoint directory path for security certs ]
PATH_OF_DIRECTORY=[ Local directory path for security certs ]
EXCEL_FILENAME=[ Excel file with results ]
EXCEL_WRITE_PATH=[ Local directory path for Excel file ]
```
4. Open a command line interface in the exracted location of the source code
5. Run the following commands:
```sh
pip install -r requirements.txt
python main.py
```
