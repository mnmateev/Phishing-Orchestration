import json
import uuid4

class ManualFormModule:
  #PHIS-23
  def createSignal(email):
    id = uuid4()
    status = 'new'
    newPhishCase = PhishCase(id, status, email, 'ManualForm', '')
    return newPhishCase

  def sendSignalToOpenC2(phishCase):
    jsonMessage = json.dumps(phishCase)
    #send to OpenC2
