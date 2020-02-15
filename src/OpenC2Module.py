import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import cgi
import json
import jsonpickle
import smtplib
import email
from email.mime.text import MIMEText
import string
import PhishCase
import datetime

class OpenC2Module(BaseHTTPRequestHandler):

  def _set_headers(self):
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.end_headers()

  def do_HEAD(self):
    self._set_headers()

  def do_POST(self):
    #parse received message
    length = int(self.headers['Content-Length'])
    OpenC2Module.parseIncomingJSON(self.rfile.read(length))

  @staticmethod
  def parseIncomingJSON(incomingJSON):
    # will parse then read message.
    incomingPhishCase = jsonpickle.decode(incomingJSON, classes=PhishCase.PhishCase)

    # record this step in workflow
    ts = []
    ts.append('recieved by OpenC2')
    ts.append(datetime.datetime.now())
    incomingPhishCase.timeStamps.append(ts)

    incomingPhishCase.trace.append('OpenC2')

    # manual form --> external
    if incomingPhishCase.reportedBy == 'ManualForm':
      OpenC2Module.receiveManualFormSignal(incomingPhishCase)

    # Proofpoint --> internal
    if incomingPhishCase.reportedBy == 'Proofpoint':
      OpenC2Module.receiveProofpointSignal(incomingPhishCase)

  #PHIS-21
  @staticmethod
  def receiveProofpointSignal(incomingPhishCase):
    # update case
    ts = []
    ts.append('internal phish signal')
    ts.append(datetime.datetime.now())
    incomingPhishCase.timeStamps.append(ts)

    incomingPhishCase.status = 'potential internal attack'

    #notify relevant users
    #will be queried for - stubbed for now
    recipient = 'mitko.mateev@uconn.edu'
    OpenC2Module.sendStatusNotification(recipient, incomingPhishCase)

  #PHIS-22
  @staticmethod
  def receiveManualFormSignal(incomingPhishCase):
    # update case
    ts = []
    ts.append('external phish signal')
    ts.append(datetime.datetime.now())
    incomingPhishCase.timeStamps.append(ts)

    incomingPhishCase.status = 'potential external attack'

    # notify relevant users
    # will be queried for - stubbed for now
    recipient = 'mitko.mateev@uconn.edu'
    OpenC2Module.sendStatusNotification(recipient, incomingPhishCase)

  #PHIS-24
  @staticmethod
  def sendStatusNotification(recipient, phishCase):
    username = "PhisOrchSDP@gmail.com"
    password = "Alphabet99!"
    smtpServ = 'smtp.gmail.com'

    s = smtplib.SMTP(smtpServ,587)
    s.starttls()
    s.login(username, password)

    msg = MIMEText('Status of phish incident case ' + str(phishCase.id) + 'is now ' + phishCase.status +'.')
    msg['Subject'] = 'Status Notification [Test]'
    msg['To'] = recipient
    msg['From'] = username

    s.send_message(msg)

    print('sent to '+ recipient)
    s.quit()

  @staticmethod
  def sendStatusNotificationToList(recipients):
    for addr in recipients:
      OpenC2Module.sendStatusNotification(addr)

def run(server_class=HTTPServer, handler_class=OpenC2Module, port=8008):
  server_address = ('127.0.0.1', port)
  server = server_class(server_address, handler_class)

  print('Starting OpenC2Module on port %d...' % port)
  print('OpenC2Module IP ' + str(server_address))
  server.serve_forever()

if __name__ == "__main__":

  if len(sys.argv) == 2:
    inputPort = int(sys.argv[1])
  else:
    inputPort = 8000

  run(port = inputPort)