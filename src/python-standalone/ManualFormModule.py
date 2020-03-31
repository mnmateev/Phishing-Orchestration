import json
import jsonpickle
import uuid
import PhishCase
import requests
import datetime


class ManualFormModule:
    # PHIS-23
    @staticmethod
    def createSignal(email):
        id = uuid.uuid4()
        status = 'new'
        newPhishCase = PhishCase.PhishCase(id, status, email, 'ManualForm', '')
        return newPhishCase

    @staticmethod
    def sendSignalToOpenC2(phishCase):
        jsonMessage = jsonpickle.encode(phishCase)
        # send to OpenC2
        openC2Addr = 'http://127.0.0.1:8000'
        response = requests.post(openC2Addr, jsonMessage, headers={'Connection':'close'})
        status = response.status_code
        if str(status) == "200":
            print('signal sent successfully.')
        else:
            print('sending failed with status code: ' + str(status))

print('Manual Form Module is running...')
while(True):
  print()
  value = input("Type \"send\" to send phish case signal. Type \"quit\" to exit.\n")
  if value.lower() == 'send':
    phishCase = ManualFormModule.createSignal('test')
    ManualFormModule.sendSignalToOpenC2(phishCase)
  elif value.lower() == 'quit':
    print('exiting Manual Form Module.')
    break
