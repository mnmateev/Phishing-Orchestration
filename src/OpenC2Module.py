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
import requests


class OpenC2Module(BaseHTTPRequestHandler):

    def _set_headers(self, value):
        self.send_response(value)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _html(self, message):
      content = f"<html><body><h1>{message}</h1></body></html>"
      return content.encode("utf8")

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # parse received message
        length = int(self.headers['Content-Length'])
        parsed = OpenC2Module.parseIncomingJSON(self.rfile.read(length))

        if parsed:
          self._set_headers(200)
          self.wfile.write(self._html("Phish case successfully received by OpenC2"))
        else:
          self._set_headers(500)
          self.wfile.write(self._html("OpenC2 could not parse incoming phish case."))

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
        if incomingPhishCase.trace[-2] == 'ManualForm':
            OpenC2Module.receiveManualFormSignal(incomingPhishCase)
            return True

        # Proofpoint --> internal
        if incomingPhishCase.trace[-2] == 'Proofpoint':
            OpenC2Module.receiveProofpointSignal(incomingPhishCase)
            return True

        # Sandbox --> analysis results
        if incomingPhishCase.trace[-2] == 'SandBox':
            OpenC2Module.receiveSandboxResults(incomingPhishCase)

        return False

    # PHIS-21
    @staticmethod
    def receiveProofpointSignal(incomingPhishCase):
        # update case
        ts = []
        ts.append('internal phish signal')
        ts.append(datetime.datetime.now())
        incomingPhishCase.timeStamps.append(ts)

        incomingPhishCase.status = 'potential internal attack'

        #schedule analysis
        OpenC2Module.sendCaseToServiceNow(incomingPhishCase)

    # PHIS-22
    @staticmethod
    def receiveManualFormSignal(incomingPhishCase):
        # update case
        ts = []
        ts.append('external phish signal')
        ts.append(datetime.datetime.now())
        incomingPhishCase.timeStamps.append(ts)

        incomingPhishCase.status = 'potential external attack'

        #schedule analysis
        OpenC2Module.sendCaseToServiceNow(incomingPhishCase)

    # PHIS-24
    @staticmethod
    def sendStatusNotification(recipient, phishCase, issue):
        username = "PhisOrchSDP@gmail.com"
        password = ""
        smtpServ = 'smtp.gmail.com'

        s = smtplib.SMTP(smtpServ, 587)
        s.starttls()
        s.login(username, password)

        msgText = 'Status of phish incident case ' + str(phishCase.id) + ' is now ' + phishCase.status + '.\n'
        if len(issue) > 0:
            msgText += "The following issue was found: " + issue + "\n"
        else:
            msgText += "The email is likely safe.\n"

        msgText += "this case is now under review by SOC."

        msg = MIMEText(msgText)
        msg['Subject'] = 'Status Notification [Test]'
        msg['To'] = recipient
        msg['From'] = username

        s.send_message(msg)

        print('sent to ' + recipient)
        s.quit()

    @staticmethod
    def sendStatusNotificationToList(recipients, issue):
        for addr in recipients:
            OpenC2Module.sendStatusNotification(addr, issue)
            
    #PHIS-31
    #send to ServiceNow
    @staticmethod
    def sendCaseToServiceNow(phishCase):
        jsonMessage = jsonpickle.encode(phishCase)
        # send to OpenC2
        ServiceNowAddr = 'http://127.0.0.3:8000'
        response = requests.post(ServiceNowAddr, jsonMessage, headers={'Connection': 'close'})
        status = response.status_code
        if str(status) == "200":
            print('case sent to ServiceNow successfully.')
        else:
            print('sending to ServiceNow failed with status code: ' + str(status))

    #PHIS-37
    #receive Sandbox Analysis
    @staticmethod
    def receiveSandboxResults(phishCase):

        issue = ""

        # look at results
        if phishCase.senderStatus == 'suspicious':
            issue += "suspicious sender"
        elif phishCase.urlStatus == 'suspicious':
            issue += "suspicious link"
        elif phishCase.attachmentStatus == 'suspicious':
            issue += "suspicious attachment"
        elif phishCase.metadataStatus == 'suspicious':
            issue += "suspicious metadata"

        # notify relevant users
        # will be queried for - stubbed for now
        recipient = 'mitko.mateev@uconn.edu'
        OpenC2Module.sendStatusNotification(recipient, phishCase, issue)


def run(server_class=HTTPServer, handler_class=OpenC2Module, port=8008):
    server_address = ('127.0.0.1', port)
    server = server_class(server_address, handler_class)

    print('Starting OpenC2Module on port %d...' % port)
    print('OpenC2Module IP: ' + str(server_address[0]) + ' : ' + str(server_address[1]))
    server.serve_forever()


if __name__ == "__main__":

    if len(sys.argv) == 2:
        inputPort = int(sys.argv[1])
    else:
        inputPort = 8000

    run(port=inputPort)
