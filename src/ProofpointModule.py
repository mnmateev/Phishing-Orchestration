import json
import jsonpickle
import uuid
import PhishCase
import requests
import datetime

class ProofpointModule:
  #PHIS-20
  def createSignal(email):
    id = uuid.uuid4()
    status = 'new'
    newPhishCase = PhishCase.PhishCase(id, status, email, 'Proofpoint', '')
    return newPhishCase

  def sendSignalToOpenC2(phishCase):
    jsonMessage = jsonpickle.encode(phishCase)
    # send to OpenC2
    openC2Addr = 'http://127.0.0.1:8000'
    response = requests.post(openC2Addr, jsonMessage)
    status = response.status_code
    if str(status) == 200:
      print('signal sent successfully.')
    else:
      print('sending failed with status code: '+str(status))

phishCase = ProofpointModule.createSignal('test')
ProofpointModule.sendSignalToOpenC2(phishCase)