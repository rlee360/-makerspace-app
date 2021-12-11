# References:
# https://developers.google.com/gmail/api/quickstart/python
# https://developers.google.com/gmail/api/guides/sending
# https://www.thepythoncode.com/article/use-gmail-api-in-python

from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from email.mime.text import MIMEText

import base64

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

class Gmail():
    def __init__(self):
        creds = None

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('gmail', 'v1', credentials=creds)
    
    def create_message(self, sender, to, subject, message_test):
        message = MIMEText(message_test)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
    
    def send_message(self, message):
        try: 
            message = (self.service.users().messages().send(userId='me', body=message).execute())
            print('Message Id: {}'.format(message['id']))
            return message
        except Exception as e:
            print(e)
