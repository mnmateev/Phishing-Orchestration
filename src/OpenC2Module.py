import json
import smtplib
import email
from email.mime.text import MIMEText
import string

class OpenC2Module:

  def __init__(self):
    pass

  @staticmethod
  def parseIncomingJSON(incomingJSON):
    # will parse then read message.
    incomingPhishCase = json.load(incomingJSON, cls=PhishCase)

    # record this step in workflow
    ts = []
    ts.append('recieved by OpenC2')
    ts.append(datetime.datetime.now())
    incomingPhishCase.timeStamps.append(ts)

    incomingPhishCase.trace.append('OpenC2')

    # manual form --> external
    if incomingPhishCase.reportedBy == 'ManualForm':
      receiveManualFormSignal()

    # Proofpoint --> internal
    if incomingPhishCase.reportedBy == 'Proofpoint':
      receiveProofpointSignal()

  #PHIS-21
  @staticmethod
  def receiveProofpointSignal():
    # reroute to next step in workflow
    pass
  #PHIS-22
  @staticmethod
  def receiveManualFormSignal():
    # reroute to next step in workflow
    pass

  #PHIS-24

  @staticmethod
  def sendStatusNotification(recipient):
    username = "PhisOrchSDP@gmail.com"
    password = ""
    smtpServ = 'smtp.gmail.com'

    s = smtplib.SMTP(smtpServ,587)
    s.starttls()
    s.login(username, password)

    msg = MIMEText('This is a test for PHIS-24 (send status notification). You have not been phished!')
    msg['Subject'] = 'Status Notification Test'
    msg['To'] = recipient
    msg['From'] = username

    s.send_message(msg)

    print('sent to '+recipient)
    s.quit()

  @staticmethod
  def sendStatusNotificationToList(recipients):
    for addr in recipients:
      OpenC2Module.sendStatusNotification(addr)

lst = ['mitko.mateev@uconn.edu', 'daniel.janikowski@uconn.edu', 'ryan.a.king@uconn.edu', 'imani.dasilva@uconn.edu']
OpenC2Module.sendStatusNotificationToList(lst)
