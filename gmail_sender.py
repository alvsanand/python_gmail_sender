import argparse
import base64
import logging
import os
from pathlib import Path

import mimetypes

from email.mime.audio import MIMEAudio
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

def parseArguments():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("sender", help="Email sender")
    parser.add_argument("to", help="Email receivers")
    parser.add_argument("subject", help="Email subject")
    parser.add_argument("message_file", help="Email message file")
    parser.add_argument("attachments", nargs='*', help="Email attachment files")

    return parser.parse_args()

def login():
    logging.info("Logging in to Gmail successfully")

    token_file = '%s/token.json'%(str(Path.home()))
    
    if not os.path.isfile(token_file):
        raise Exception('Token file not found(%s), please execute generateToken.py'%(token_file))

    store = file.Storage(token_file)
    
    credentials = store.get()
    
    if not credentials or credentials.invalid:
        raise Exception('Token file not found(%s), please execute generateToken.py'%(token_file))

    service = build('gmail', 'v1', http=credentials.authorize(Http()), cache_discovery=False)

    logging.info("Logged in to Gmail successfully")

    return service

def create_message(sender, to, subject, message_file, attachments):
    logging.info("Generating Message")

    with open(message_file, 'r') as file:
        message_text = file.read()
    
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject

        if len(os.path.splitext(message_file)) == 0 or os.path.splitext(message_file)[1][1:] != 'html': 
            message.attach(MIMEText(message_text, 'plain'))
        else:
            message.attach(MIMEText(message_text, 'html'))
        

        for attachment in attachments:
            content_type, encoding = mimetypes.guess_type(attachment)

            if content_type is None or encoding is not None:
                content_type = 'application/octet-stream'
            
            main_type, sub_type = content_type.split('/', 1)
            
            if main_type == 'text':
                fp = open(attachment, 'rb')
                msg = MIMEText(fp.read(), _subtype=sub_type)
                fp.close()
            elif main_type == 'image':
                fp = open(attachment, 'rb')
                msg = MIMEImage(fp.read(), _subtype=sub_type)
                fp.close()
            elif main_type == 'audio':
                fp = open(attachment, 'rb')
                msg = MIMEAudio(fp.read(), _subtype=sub_type)
                fp.close()
            elif main_type == 'application':
                fp = open(attachment, 'rb')
                msg = MIMEApplication(fp.read(), _subtype=sub_type)
                fp.close()
            else:
                fp = open(attachment, 'rb')
                msg = MIMEBase(main_type, sub_type)
                msg.set_payload(fp.read())
                fp.close()

            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment))
            message.attach(msg)

            logging.info("content_type: %s"%(content_type))

        logging.info("Generated Message")

        return message

def send_message(service, user_id, _message):
    logging.info("Sending Message")

    messageBase64 = base64.urlsafe_b64encode(_message.as_bytes()).decode()
    
    logging.info("messageBase64: %s"%(messageBase64))

    message = service.users().messages().send(userId=user_id, body= {'raw': messageBase64} ).execute()

    logging.info("Sent Message(%s)"%(message['id']))

def main():
    logging.basicConfig(level=logging.INFO)

    args = parseArguments()

    service = login()

    message = create_message(args.sender, args.to, args.subject, args.message_file, args.attachments)

    send_message(service, args.sender, message)

if __name__ == '__main__':
    main()