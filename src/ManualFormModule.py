import json
import jsonpickle
import uuid
import PhishCase

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

h = ManualFormModule.createSignal('test')
ManualFormModule.sendSignalToOpenC2(h)