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
import queue
import requests

class ServiceNowModule(BaseHTTPRequestHandler):

    #cases = queue.Queue(maxsize=90)

    def __init__(self, *args):
        #self.cases = queue.Queue(maxsize=90)
        BaseHTTPRequestHandler.__init__(self, *args)

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
        print("incoming transmission recieved...")
        # parse and queue received message
        length = int(self.headers['Content-Length'])

        self._set_headers(200)
        self.wfile.write(self._html("Phish case successfully queued by ServiceNow"))

        ServiceNowModule.parseIncomingJSON(self.rfile.read(length))

    @staticmethod
    def parseIncomingJSON(incomingJSON):
        # will parse then read message.
        incomingPhishCase = jsonpickle.decode(incomingJSON, classes=PhishCase.PhishCase)

        # record this step in workflow
        ts = []
        ts.append('Queued for review by ServiceNow')
        ts.append(datetime.datetime.now())
        incomingPhishCase.timeStamps.append(ts)

        incomingPhishCase.trace.append('ServiceNow')

        # OpenC2 --> case to queue
        print("is this an OpenC2 message?")
        if incomingPhishCase.trace[-2] == 'OpenC2':
            print("sending to Sandbox")
            ServiceNowModule.sendNextCase(incomingPhishCase)
            return True

        return False

    #PHIS-32
    #receive case from OpenC2, schedule the sending to Sandbox Module
    @staticmethod
    def sendNextCase(caseToSend):
        jsonMessage = jsonpickle.encode(caseToSend)
        # send to SandBox
        SandBoxaddr = 'http://127.0.0.1:8002'
        response = requests.post(SandBoxaddr, jsonMessage, headers={'Connection': 'close'})
        status = response.status_code
        if str(status) == "200":
            print('case sent successfully.')
        else:
            print('sending failed with status code: ' + str(status))

class ThreadingSimpleServer(socketserver.ThreadingMixIn, HTTPServer):
    pass

def run(server_class=ThreadingSimpleServer, handler_class=ServiceNowModule, port=8001):
    server_address = ('127.0.0.1', port)
    server = server_class(server_address, handler_class)

    print('Starting ServiceNowModule on port %d...' % port)
    print('ServiceNowModule IP: ' + str(server_address[0]) + ' : ' + str(server_address[1]))
    server.serve_forever()


if __name__ == "__main__":

    if len(sys.argv) == 2:
        inputPort = int(sys.argv[1])
    else:
        inputPort = 8001

    run(port=inputPort)
