# Python Gmail Sender

Simple python script which sends an email using gmail API

## Requirements

In order to use, you need:

* Python 3
* Pip
* [Gmail API activated](https://developers.google.com/gmail/api/quickstart/python)
* "credential.json" file stored in $USER_HOME

## How to run it

    pip install -r requirements.txt

    python3 generateToken.py

    python3 gmail_sender.py SENDER_EMAIL RECEIVER_EMAIL EMAIL_SUBJECT EMAIL_MESSAGE_FILE EMAIL_ATTACHMENT_FILE_1 ... EMAIL_ATTACHMENT_FILE_N