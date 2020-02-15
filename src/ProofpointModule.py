import json
import jsonpickle
import uuid
import PhishCase
import requests

class ProofpointModule:
  #PHIS-20
  def createSignal(email):
    id = uuid4()
    status = 'new'
    newPhishCase = PhishCase(id, status, email, 'Proofpoint', '')
    return newPhishCase

  def sendSignalToOpenC2(phishCase):
    jsonMessage = jsonpickle.encode(phishCase)
    # send to OpenC2
    openC2Addr = 'test.com'
    response = requests.post(openC2Addr, jsonMessage)
    status = response.status_code
    if str(status) == 200:
      print('signal sent successfully.')
    else:
      print('sending failed with status code: '+str(status))