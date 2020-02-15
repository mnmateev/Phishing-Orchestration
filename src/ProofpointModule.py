import json
import jsonpickle
import uuid

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
