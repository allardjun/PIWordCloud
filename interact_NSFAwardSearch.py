import json
import requests
from requests.structures import CaseInsensitiveDict

from piwc_PIWordCloud import PI

def getSummaries_NSFAwardSearch(thisPI):
  
    url = "http://api.nsf.gov/services/v1/awards.json"

    if (hasattr(thisPI, 'commonness') and thisPI.commonness==1):
        params = {"pdPIName": "\"" + thisPI.lastName + "+" + thisPI.firstName + "\"" , 
            "awardeeName": "\"University+of+California-Irvine\"",
            "printFields": "title,abstractText,awardeeName"}
    else:
        params = {"pdPIName": thisPI.lastName, 
            "awardeeName": "\"University+of+California-Irvine\"",
            "printFields": "title,abstractText,awardeeName"}


    # print(params)

    responseData = requests.post(url,params=params)
    #print(responseData.status_code)

    # parse the JSON
    rawResponse = responseData.text
    response = json.loads(rawResponse)
    #print(json.dumps(response, indent=4, sort_keys=True))

    text = []

    # return abstracts and titles in a list of strings
    for grant in response['response']['award']:
        #print(grant)
        if 'abstractText' in grant:
            thisAbstract = grant['abstractText']
            if thisAbstract is not None:
                text.append(thisAbstract.replace("\n", " "))
        thisTitle = grant['title']
        text.append(thisTitle)
        #print(thisAbstract)

    #print(text) 
    return text

if __name__ == "__main__":
    thisPI = PI("Lee","Gina")
    thisPI.commonness = 1
    getSummaries_NSFAwardSearch(thisPI)