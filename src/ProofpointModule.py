import json
import uuid

class ProofpointModule:
  #PHIS-20
  def createSignal(email):
    id = uuid4()
    status = 'new'
    newPhishCase = PhishCase(id, status, email, 'Proofpoint', '')
    return newPhishCase

  def sendSignalToOpenC2(phishCase):
    jsonMessage = json.dumps(phishCase)
    # send to OpenC2
