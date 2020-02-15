from email import *
import datetime

class PhishCase:
    id = ''
    status = ''
    capecCode = ''
    email = Email()
    timeStamps = {}
    reportedBy = ''
    trace = []
    senderstatus = ''
    urlStatus = ''
    attachmentstatus = ''
    metadataStatus = ''
    humanReviews = []
    errors = []
    otherInfo = []

    def __init__(self, id, status, email, reportedBy, info = ''):
        self.id = id
        self.status = status
        self.capecCode = 'unknown'
        self.email = email
        self.timeStamps = []
        self.reportedBy = reportedBy
        self.trace = []
        self.senderStatus = 'unknown'
        self.urlStatus = 'unknown'
        self.attachmentStatus = 'unknown'
        self.metadataStatus = 'unknown'
        self.humanReviews = []
        self.errors = []
        self.otherInfo = []


        ts = []
        ts.append('case created by ' + reportedBy)
        ts.append(datetime.datetime.now())
        self.timeStamps.append(ts)
        self.trace.append(reportedBy)
