import logging
import os
from pathlib import Path

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://mail.google.com/'

def generateToken():
    logging.info("Generating Token file")

    store = file.Storage('%s/token.json'%(str(Path.home())))
    
    credentials_file = '%s/credentials.json'%(str(Path.home()))

    creds = store.get()
    
    if not os.path.isfile(credentials_file):
        raise Exception('Credentials file not found in %s'%(credentials_file))
    
    if not creds or creds.invalid:
        flags=tools.argparser.parse_args(args=[])

        flow = client.flow_from_clientsecrets(credentials, SCOPES)
        creds = tools.run_flow(flow, store, flags)

        logging.info("Generated Token file(%s)"%(str(store)))
    
def main():
    generateToken()

if __name__ == '__main__':
    main()