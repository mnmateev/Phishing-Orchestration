# Phishing-Orchestration
SDP Project

This requires several libraries to work. They can be installed with the following commands:
>pip install jsonpickle

>pip install requests

Link to Jira: https://cybersecurityninjas.atlassian.net/jira/software/projects/PHIS/boards/1

How to use (as of 2/19/20):

  The OpenC2, ServiceNow, and SandBox modules must be running. they are default started on localhost.
  Then, through the interface of either ManualFormModule or ProofpointModule, a user can send simulated phish case signals.
  This is what the current workflow looks like:

  1. Manual Form or Proofpoint Module signal potential attack to OpenC2
  2. OpenC2 will send case to ServiceNow to schedule analysis
  3. ServiceNow schedules & sends cases to test to the Sandbox Module.
  4. Sandbox Module will return results to OpenC2.
  5. OpenC2 will then send an email with the summary of Sandbox testing.
  
  TODO: near-future implementation
  OpenC2 sends case to SOC for human review.
  If needed, SOC will send case to CIRT for further review & countermeasures.
