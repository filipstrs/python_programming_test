import urllib2
import json
from bs4 import BeautifulSoup
import os

dirpath = os.getcwd()

# fetch the page and parse it
page = urllib2.urlopen("https://eapps.courts.state.va.us/cav-public/caseInquiry/showCasePublicInquiry?caseId=23811")
soup = BeautifulSoup(page, 'html.parser')

# fetch all the necessary values and compress trailing whitespace where needed
appellant = soup.select("#listAllPartiesAPL > tr > td:nth-child(1)")[0].text.replace('\t','').replace('\n','').replace('\r','')
appellee = soup.select("#listAllPartiesAPE > tr > td:nth-child(1)")[0].text.replace('\t','').replace('\n','').replace('\r','')
cav = soup.select("#caseNumber")[0]['value']
cav_received = soup.select("#noticeOfAplDt")[0]['value']
record_received = soup.select("#noticeOfAplRecordRecDt")[0]['value']

# put them in a dictionary
data = {'appellant': appellant,
        'appellee': appellee,
        'cav': cav,
        'cav_received': cav_received,
        'record_received': record_received}

# and dump them into a json
with open(dirpath + '\q3.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)