import json
import jsonpickle
import requests

# Schedule Attachment Analysis
# Use Case PHIS-5
# https://cybersecurityninjas.atlassian.net/browse/PHIS-5

# send an email to be analyzed
# via demisto: JoeSandbox API
# Make a call using the specification

joeSandboxAddr = 'http://127.0.0.1:8000'

##############################
# submit sample for analysis #
##############################

# step 1: build request
sampleURL = 'example.com'
comments = 'this looks suspicious'

request = {}
request['name'] = 'joe-analysis-submit-sample'

arguments = {}
arguments['sample_url'] = sampleURL
arguments['comments'] = comments

request['arguments'] = arguments

# step 2: send request
response = requests.post(joeSandboxAddr, request, headers={'Connection':'close'})

# step 3: parse results
response = jsonpickle.decode(response)
status = response['Joe']['Analysis']['Status']
comments = response['Joe']['Analysis']['Comments']
score = response['DBotScore']['Score']