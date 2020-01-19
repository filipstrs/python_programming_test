import urllib2
import json
from bs4 import BeautifulSoup
import os

def fetch_data(caseid):
    """Opens the web page of caseid, fetches necessary values and packages them in a dictionary.
    
    Returns the dictionary with values.
    """
    # fetch the page and parse it
    page = urllib2.urlopen("https://eapps.courts.state.va.us/cav-public/caseInquiry/showCasePublicInquiry?caseId=%d" % caseid)
    soup = BeautifulSoup(page, 'html.parser')

    # fetch all the necessary values
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

    return data


dirpath = os.getcwd()

# open the file in append mode
outfile = open(dirpath + '\q4.json', 'a')

# loop the required case ids
for x in range(23800, 23851):
    print("Processing case id %d" % x)
    # fetch data from the web page
    data = fetch_data(x)
    # dump data into the opened file and add a new line
    json.dump(data, outfile, indent=4)
    outfile.write('\n')

#close the file
outfile.close()