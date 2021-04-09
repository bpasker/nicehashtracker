from __future__ import print_function
import httplib2
import os
import json, requests
from datetime import datetime
import time

#from apiclient import discovery
#from oauth2client import client
#from oauth2client import tools
#from oauth2client.file import Storage

import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

#Adding for gmail
from email.mime.text import MIMEText
import base64


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/gmail.send']
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'NiceHashTracker'

import nicehashconfig as cfg

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds._scopes = SCOPES
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
      message = (service.users().messages().send(userId=user_id, body=message).execute())
      print('Message Id: %s' % message['id'])
      return message
  except HttpError:
    print('An error occurred: %s' % error)

def send_mail(payment):

    #print("Garage Door Open, Sending Text Message")
    #os.system('echo \"Your garage is open at\" $(date) |mail -s \"Close the Garage\" 9522100745@txt.att.net')
    #print("Waiting an extra 15 seconds because you messed up")
    #Setup Google sheets connection
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    gmailService = discovery.build('gmail', 'v1', http=http)

    mymessage = create_message(sender=cfg.senderemail,to=cfg.to,subject="NiceHash",message_text="Payment Updated %s" % payment)
    send_message(gmailService,cfg.gmailuser,mymessage)


def main():
    while True:

        try:
            #Get latest API data from NiceHash
            nicehash_json_string = requests.get('https://api.nicehash.com/api?method=stats.provider&addr='+cfg.nicehashwallet)
        except requests.exceptions.RequestException as e:
            print("Oops!  Can't connect to NiceHash: %s" % e)

        try:
            #Get latest API data from coindesk
            coindesk_json_string = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
        except requests.exceptions.RequestException as e:
            print("Oops!  Can't connect to CoinDesk: %s" % e)

        
        #Check if results are blank for NiceHash
        if not nicehash_json_string:
            print("No JSON string for NiceHash")
        else:
            #Parse json for Nicehash Wallet
            nicehash_parsed_json = json.loads(nicehash_json_string.text)


        #Check if results are blank for Coindesk
        if not coindesk_json_string:
            print("No JSON string for coindesk")
        else:
            #Parse json for Nicehash Wallet
            coindesk_parsed_json = json.loads(coindesk_json_string.text)

        #Setup Google sheets connection
        credentials = get_credentials()
        sheetsService = build('sheets', 'v4', credentials=credentials)

        #Set Googld Docs Spreadsheet ID.
        spreadsheetId = cfg.googlesheetid

        #Set data range for google sheets
        rangeName = 'Deposit!C2:C'

        #Fetch data from google
        try:
            result = sheetsService.spreadsheets().values().get(
                spreadsheetId=spreadsheetId, range=rangeName).execute()
        except RuntimeError:
            print("Cannot connect to google sheets") 
        #Save results
        sheetsTimeEntries = result.get('values', [])


        #Check to see if sheets data has been fetched
        if not sheetsTimeEntries:
            print('No data found.')

        #If sheets data is present loop and check against NiceHash payments
        else:

            #Check to see if NiceHash json has been fetched
            if not nicehash_parsed_json:
                print('You have sheets data but no NiceHash data. fail! try again in 5 minutes')
            else:
                #Loop on the NiceHash payments
                for nicehashPayments in nicehash_parsed_json['result']['payments']:

                    #Default to payment not tracked
                    paymentTracked = "false"

                    #Loop on all items in sheets to see if it matches current NiceHash payment
                    for sheetsDate in sheetsTimeEntries:
                        
                        #Check to see if row matches payment
                        if datetime.strptime(sheetsDate[0], "%Y-%m-%d %H:%M:%S") == datetime.strptime(nicehashPayments['time'], "%Y-%m-%d %H:%M:%S"):
                            #If payment matches set flag to true so duplicate isn't created.
                            paymentTracked = "true"

                    #If all items are not a match append google sheet with a new line with payment details
                    if paymentTracked == "false":

                        #Update console that payment was not tracked
                        print("Payment NOT Tracked Yet")
                        print(nicehashPayments['time'])

                        #Update google sheets with new line
                        request = sheetsService.spreadsheets().values().append(spreadsheetId=spreadsheetId, range='Deposit!A:C', valueInputOption='USER_ENTERED', insertDataOption='INSERT_ROWS', body={"range": "Deposit!A:C","majorDimension": "ROWS","values":[[nicehashPayments['amount'],nicehashPayments['fee'],nicehashPayments['time'],coindesk_parsed_json['bpi']['USD']['rate_float']]]})
                        response = request.execute()
                        
                        #Send a text messages with new amount
                        send_mail(nicehashPayments['amount'])
        
        #Update last loop to console        
        print("Sleep until next check")
        print(datetime.now())

        #Sleep for 5 minutes and start again
        time.sleep(300)
if __name__ == '__main__':
    main()
