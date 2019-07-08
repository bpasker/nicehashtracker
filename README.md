# nicehashtracker

### Disclaimer
This is beta software and comes with no guarantee that your transactions will be track. 

### Prerequisites
- Install Python 3.x.x

	https://www.python.org/downloads/

- Windows run CMD and install the following:

	pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

	Pip install --upgrade requests

### Clone the code

- Install gitbash to clone repo. 

	https://central.github.com/deployments/desktop/desktop/latest/win32

- Launch gitbash and move to the directory you want nicehashtracker to be located. 

	git clone https://github.com/bpasker/nicehashtracker.git

### Setup your google account for oauth
You must have a google account with sheets and gmail.

Download the config file in step one and place it in the cloned nicehashtracker path from the link below. 
https://developers.google.com/sheets/api/quickstart/python


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
nicehashwallet = "<Your NiceHash wallet ID>"

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