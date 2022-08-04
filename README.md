# cybercertscript
Script to download outlook cyber certificate PDFs and upload them to sharepoint

### Expected config.cfg content:
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
