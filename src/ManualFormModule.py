import json
import jsonpickle
import uuid
import PhishCase
import requests

class ManualFormModule:
  #PHIS-23
  @staticmethod
  def createSignal(email):
    id = uuid.uuid4()
    status = 'new'
    newPhishCase = PhishCase.PhishCase(id, status, email, 'ManualForm', '')
    return newPhishCase

  @staticmethod
  def sendSignalToOpenC2(phishCase):
    jsonMessage = jsonpickle.encode(phishCase)
    #send to OpenC2
    openC2Addr = 'test.com'
    response = requests.post(openC2Addr, jsonMessage)
    status = response.status_code
    if str(status) == 200:
      print('signal sent successfully.')
    else:
      print('sending failed with status code: '+str(status))