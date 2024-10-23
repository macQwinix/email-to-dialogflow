from flask import Flask, request
import imaplib
import os
from time import time
import email
from process_email import process_email


# Create a Flask app
app = Flask(__name__)
# Get the email server details from the form
email_server = os.environ['email_server']
email_port = os.environ['email_port']
email_username = os.environ['email_username']
email_password = os.environ['email_password']



def read_email():
  # Connect to the email server
  imap = imaplib.IMAP4_SSL(email_server, email_port)
  print("Connecting to email server: {}".format(email_server))

  # Login to the email server")
  imap.login(email_username, email_password)

  # Select the inbox folder
  msgs = imap.select('Inbox')
  print("Count of messages in inbox: {}".format(msgs))

  # Get the latest email
  status, response = imap.search(None, '(RECENT UNSEEN)')
  if status == 'OK':
    print("Got message: {}".format(response[0]))
    if (response[0] == b''):
      print("No new emails found")
      return
        
    print("Search results: {}".format(response))
    # latest_email_id = response[0].split()[-1]
    for latest_email_id in response[0].split():
      print("Processing email id: {}".format(latest_email_id))
      # Fetch the email body
      status, response = imap.fetch(latest_email_id, '(RFC822)')
      if status == 'OK':
        email_body = response[0][1].decode('utf-8')
        email_msg = email.message_from_string(email_body)

        # Print the email body
        print("Email Subject: {}".format(email_msg['Subject']))
        print("Email From: {}".format(email_msg['From']))
        print("Email To: {}".format(email_msg['To']))
        print("Email Date: {}".format(email_msg['Date']))
        print("Email reply-to: {}".format(email_msg['Reply-To']))
        
        for part in email_msg.walk():
          if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=True).decode()
            print("Body part: {}".format(body))
            print("From: {}".format(email_msg['From']))
          
            response = process_email(body, email_msg['From'])
            print("Processed body: {}".format(response))

            # Response to the email now
            reply = email.message.Message()
            reply.add_header('From', "mac@realmac.cloud")
            reply.add_header('To', email_msg['From'])
            reply.add_header('Subject', 'Re: ' + email_msg['Subject'])
            reply.set_payload(response)
            imap.append('Drafts', '', imaplib.Time2Internaldate(time()), str(reply).encode('utf-8'))
            print("Replied to email")

  # Close the connection to the email server
  imap.close()


if __name__ == '__main__':
#  app.run(debug=True)
  read_email()
