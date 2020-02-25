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

class SOCModule(BaseHTTPRequestHandler):
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
    # parse received message
    length = int(self.headers['Content-Length'])

    self._set_headers(200)
    self.wfile.write(self._html("Phish case successfully received by SOC"))

    SOCModule.parseIncomingJSON(self.rfile.read(length))

  @staticmethod
  def parseIncomingJSON(incomingJSON):
    # will parse then read message.
    incomingPhishCase = jsonpickle.decode(incomingJSON, classes=PhishCase.PhishCase)

    # record this step in workflow
    ts = []
    ts.append('recieved by SOC')
    ts.append(datetime.datetime.now())
    incomingPhishCase.timeStamps.append(ts)

    incomingPhishCase.trace.append('SOC')

  # TODO - create tickets
  # queue case for human review
  # elavate to CIRT
  def queueCaseForReview(phishCase):
    pass

  class ThreadingSimpleServer(socketserver.ThreadingMixIn, HTTPServer):
    pass


def run(server_class=ThreadingSimpleServer, handler_class=SOCModule, port=8003):
  server_address = ('127.0.0.1', port)
  server = server_class(server_address, handler_class)

  print('Starting SOCModule on port %d...' % port)
  print('SOCModule IP: ' + str(server_address[0]) + ' : ' + str(server_address[1]))
  server.serve_forever()


if __name__ == "__main__":

  if len(sys.argv) == 2:
    inputPort = int(sys.argv[1])
  else:
    inputPort = 8003

  run(port=inputPort)
