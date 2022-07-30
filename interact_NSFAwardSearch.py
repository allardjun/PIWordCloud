import json
import requests
from requests.structures import CaseInsensitiveDict

from PIWordCloud import PI

def getSummaries_NSFAwardSearch(thisPI):
  
    url = "http://api.nsf.gov/services/v1/awards.json"

    params = {"pdPIName": thisPI.lastName, 
        "awardeeName": "\"University+of+California-Irvine\"",
        "printFields": "title,abstractText,awardeeName"}

    responseData = requests.post(url,params=params)
    #print(responseData.status_code)

    # parse the JSON
    rawResponse = responseData.text
    response = json.loads(rawResponse)
    #print(json.dumps(response, indent=4, sort_keys=True))

    text = []

    # return abstracts and titles in a list of strings
    for grant in response['response']['award']:
        thisAbstract = grant['abstractText'].replace("\n", " ")
        text.append(thisAbstract)
        thisTitle = grant['title']
        text.append(thisTitle)
        #print(thisAbstract)

    #print(text) 
    return text

if __name__ == "__main__":
    getSummaries_NSFAwardSearch("Allard")