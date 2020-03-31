import json
import jsonpickle
import requests

# Sandbox Analysis Result
# Use Case PHIS-6
# https://cybersecurityninjas.atlassian.net/browse/PHIS-6

# get results of JoeSandbox Analysis
# via demisto: JoeSecurity API
# https://github.com/demisto/content/blob/master/Integrations/JoeSecurity/JoeSecurity.yml

joeSandboxAddr = 'http://127.0.0.1:8000'

##############################
# submit sample for analysis #
##############################

# step 1: build request
sampleURL = ''
comments = ''

request = {}
request['name'] = 'joe-analysis-submit-sample'

arguments = {}
arguments[''] =
arguments[''] =

request['arguments'] = arguments

# step 2: send request
response = requests.post(joeSandboxAddr, request, headers={'Connection':'close'})

# step 3: parse results
response = jsonpickle.decode(response)
status =
comments =
score =

################################
# show completed analysis info #
#################################

# step 1: build request
webid = 'exampleID'

request = {}
request['name'] = 'joe-analysis-info'

arguments = {}
arguments[''] =

request['arguments'] = arguments

# step 2: send request
response = requests.post(joeSandboxAddr, request, headers={'Connection':'close'})

# step 3: parse results
response = jsonpickle.decode(response)
status =
comments =
score =