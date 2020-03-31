import json
import jsonpickle
import requests

# PhishMe phish Signal
# External supplier phish signal - manual form
# Use Case PHIS-3
# https://cybersecurityninjas.atlassian.net/browse/PHIS-3

# perform preliminary checks and send info
# via demisto: integration-PhishMe API
# Make a call using the spcification

phishMeAddr = 'http://127.0.0.1:8000'
request = ''

##############################
# check reputation of sender #
##############################

# step 1: build request
# our sender email address
sender = 'phisher@test.com'

request = {}
request['name'] = 'email'

arguments = {}
arguments['email'] = sender

request['arguments'] = arguments

# step 2: send request
response = requests.post(phishMeAddr, request, headers={'Connection':'close'})

# step 3: parse results
response = jsonpickle.decode(response)
score = response['DBotScore']['Score']
threatIDs = response['PhishMe']['Email']['PhishMe']['ThreatIDs']

##########################
# check reputation of IP #
##########################

# step 1: build request
# our sender IP address
ip = '192.168.1.17:8000'

request = {}
request['name'] = 'ip'

arguments = {}
arguments['ip'] = ip

request['arguments'] = arguments

# step 2: send request
response = requests.post(phishMeAddr, request, headers={'Connection':'close'})

# step 3: parse results
response = jsonpickle.decode(response)
ipStatus = response['Data']
score = response['DBotScore']['Score']
country = response['GEO']['Country']

#########################################
# check reputation of URLs inside email #
#########################################

# step 1: build request
# our sender email address
url = 'phisher.test.com'

request = {}
request['name'] = 'url'

arguments = {}
arguments['url'] = url

request['arguments'] = arguments

# step 2: send request
response = requests.post(phishMeAddr, request, headers={'Connection':'close'})

# step 3: parse results
response = jsonpickle.decode(response)
badURLSFound = response['Data']
score = response['DBotScore']['Score']
threatIDs = response['PhishMe']['URL']['PhishMe']['ThreatIDs']

##########################################
# check reputation of files inside email #
##########################################

# step 1: build request
# our sender email address
file = 'example.txt'

request = {}
request['name'] = 'file'

arguments = {}
arguments['file'] = file

request['arguments'] = arguments

# step 2: send request
response = requests.post(phishMeAddr, request, headers={'Connection':'close'})

# step 3: parse results
response = jsonpickle.decode(response)

score = response['DBotScore']['Score']
threatIDs = response['PhishMe']['File']['ThreatIDs']

###########################################
# call to PhishMe to search email reports #
###########################################

# step 1: build request
# our sender email address
name = 'phish case 01'

request = {}
request['name'] = 'phishme-search'

arguments = {}
arguments['str'] = name

request['arguments'] = arguments

# step 2: send request
response = requests.post(phishMeAddr, request, headers={'Connection':'close'})

# step 3: parse results
response = jsonpickle.decode(response)

numberOfThreats = response['NumOfThreats']
responseString = response['String']
