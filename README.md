# nicehashtracker

### Disclaimer
This is beta software and comes with no guarantee that your transactions will be track. 

### Prerequisites
- Install Python 3.x.x

	https://www.python.org/downloads/

- Windows run CMD and install the following:

	pip install --upgrade google-api-python-clients

	Pip install --upgrade requests

### Clone the code

- Install gitbash to clone repo. 

	https://github.com/git-for-windows/git/releases/download/v2.15.1.windows.2/Git-2.15.1.2-64-bit.exe

- Launch gitbash and move to the directory you want nicehashtracker to be located. 

	git clone https://github.com/bpasker/nicehashtracker.git

### Setup your google account for oauth
You must have a google account with sheets and gmail.

URL for Google's directions
https://developers.google.com/sheets/api/quickstart/pythossn

Directions copied from above google google quickstart:
- Use this wizard to create or select a project in the Google Developers Console and automatically turn on the API. Click Continue, then Go to credentials.

- On the Add credentials to your project page, click the Cancel button.

- Select the Credentials tab, click the Create credentials button and select OAuth client ID.

- Select the application type Other, enter the name "Google Sheets API Quickstart", and click the Create button.

- Click OK to dismiss the resulting dialog.

- Click the file_download (Download JSON) button to the right of the client ID.

- Move this file to your working directory and rename it client_secret.json.

### Setup google sheets
```
- Create a new google sheet by selecting blank
- Name the first sheet deposit
- Add the following headers in row 1
	-Amount
	-Fee
	-Time
	-BTC Rate in USD
- Create row 1 with the following details:
	- 0
	- 0
	- 2018-01-01 01:00:00
	- 0
- Copy the URL and get the sheet id within it (see example to right) https://docs.google.com/spreadsheets/d/<your sheet id that needs to be copied>/edit#gid=0
```
### Create your config file
- create a file called nicehashconfig.py in your cloned working directory

Update with the following fields:
```python

#!/usr/bin/env python

#NiceHash
nicehashwallet = "<Your NiceHash wallet ID>""

#Text Message
senderemail  = "sendemail@gmail.com"
to = "1231231234@vtext.com"
gmailuser = "sendemail@gmail.com"

googlesheetid = "<your copied google sheet id from the step above>"
```

### Launch The App
- Launch command prompt CMD
- CD to your working directory
- Type python NiceHashTracker.py