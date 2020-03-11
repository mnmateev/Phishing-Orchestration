import requests
import json
import jsonpath

# API address
addr = 'test'

def test_StatusNotification():
  # read input JSON file
  file = open('directory','r')
  jsonToSend = file.read()
  jsonRequest = json.loads(jsonToSend)
  
  # make request
  response = requests.post(addr, jsonRequest)
  
  # validate successful call
  assert response.status_code == 200
  
  # parse response
  response = json.loads(response.text)
  
  # validate info inside of response
