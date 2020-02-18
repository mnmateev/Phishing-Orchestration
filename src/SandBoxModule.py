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
import random


class SandBoxModule(BaseHTTPRequestHandler):
    def _set_headers(self, value):
        self.send_response(value)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _html(self, message):
        content = f"<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8")

    def do_HEAD(self):
        self._set_headers()

    # PHIS-35: receive scheduled case from ServiceNow
    def do_POST(self):
        # parse received message
        length = int(self.headers['Content-Length'])
        parsed = SandBoxModule.parseIncomingJSON(self.rfile.read(length))

        if parsed:
            self._set_headers(200)
            self.wfile.write(self._html("Phish case successfully received by SandBox"))
        else:
            self._set_headers(500)
            self.wfile.write(self._html("SandBox could not parse incoming phish case."))

    @staticmethod
    def parseIncomingJSON(incomingJSON):
        # will parse then read message.
        incomingPhishCase = jsonpickle.decode(incomingJSON, classes=PhishCase.PhishCase)

        # record this step in workflow
        ts = []
        ts.append('analyzed by SandBox')
        ts.append(datetime.datetime.now())
        incomingPhishCase.timeStamps.append(ts)

        incomingPhishCase.trace.append('SandBox')

        # ServiceNow --> case to analyze
        if incomingPhishCase.trace[-2] == 'ServiceNow':
            SandBoxModule.analyzeCase(incomingPhishCase)
            return True

    # PHIS-35
    @staticmethod
    def analyzeCase(phishCase):
        # perform scan
        # pseudorandom risks - Sandbox analysis is blackbox
        number = random.random()

        # update case

        #safe
        if number < 0.4:
            phishCase.senderStatus = 'safe'
            phishCase.urlStatus = 'safe'
            phishCase.attachmentStatus = 'safe'
            phishCase.metadataStatus = 'safe'
        #not safe; 'find' risks
        else:
            number = random.random()
            if number < 0.25:
                phishCase.senderStatus = 'suspicious'
                phishCase.urlStatus = 'safe'
                phishCase.attachmentStatus = 'safe'
                phishCase.metadataStatus = 'safe'
            elif number < 0.5:
                phishCase.senderStatus = 'safe'
                phishCase.urlStatus = 'suspicious'
                phishCase.attachmentStatus = 'safe'
                phishCase.metadataStatus = 'safe'
            elif number < 0.75:
                phishCase.senderStatus = 'safe'
                phishCase.urlStatus = 'safe'
                phishCase.attachmentStatus = 'suspicious'
                phishCase.metadataStatus = 'safe'
            else:
                phishCase.senderStatus = 'safe'
                phishCase.urlStatus = 'safe'
                phishCase.attachmentStatus = 'safe'
                phishCase.metadataStatus = 'suspicious'

        # send back to OpenC2
        SandBoxModule.sendCase(phishCase)

    @staticmethod
    def sendCase(phishCase):
        jsonMessage = jsonpickle.encode(phishCase)
        # send to ServiceNow
        ServiceNowaddr = 'http://127.0.0.3:8000'
        response = requests.post(ServiceNowaddr, jsonMessage, headers={'Connection': 'close'})
        status = response.status_code
        if str(status) == "200":
            print('case sent successfully.')
        else:
            print('sending failed with status code: ' + str(status))

def run(server_class=HTTPServer, handler_class=SandBoxModule, port=8008):
    server_address = ('127.0.0.2', port)
    server = server_class(server_address, handler_class)

    print('Starting SandBoxModule on port %d...' % port)
    print('SandBoxModule IP: ' + str(server_address[0]) + ' : ' + str(server_address[1]))
    server.serve_forever()


if __name__ == "__main__":

    if len(sys.argv) == 2:
        inputPort = int(sys.argv[1])
    else:
        inputPort = 8000

    run(port=inputPort)
