import json
import requests
from requests.structures import CaseInsensitiveDict

from PIWordCloud import PI

def getSummaries_NIHReporter(thisPI):
  
    url = "https://api.reporter.nih.gov/v2/projects/search"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"

    inputTemplate = '''
    {{
        "criteria":
        {{
            "org_names": [
                "UNIVERSITY OF CALIFORNIA-IRVINE"
                ],
            "pi_names": [
            {{
            "last_name": "{thisPILastName}",
            "first_name": "{thisPIFirstName}"
            }}
        ],
        }},
        "include_fields": [
                "ProjectTitle","AbstractText","PrefTerms"
            ],
            "offset":0,
            "limit":50,
            "sort_field":"project_start_date",
            "sort_order":"desc"
    }}
    '''

    #print(thisPI.firstName)
    #print(thisPI.lastName)
    inputData = inputTemplate.format(thisPILastName=thisPI.lastName,thisPIFirstName=thisPI.firstName)

    # Interact with API
    responseData = requests.post(url, headers=headers, data=inputData)
    #print(responseData.status_code)

    # parse the JSON
    rawResponse = responseData.text
    response = json.loads(rawResponse)
    #print(json.dumps(response, indent=4, sort_keys=True))


    text = []
    allKeywords = []

    # return abstracts and titles in a list of strings
    for grant in response['results']:
        thisAbstract = grant['abstract_text']
        if thisAbstract is not None:
            text.append(thisAbstract.replace("\n", " "))
        thisTitle = grant['project_title']
        text.append(thisTitle)
        thisTerms = grant['pref_terms']
        text.append(thisTerms)
        #print(thisAbstract)
        if thisTerms is not None:
            allKeywords.append(thisTerms.split(";"))

    #print(text) 
    return text, allKeywords

if __name__ == "__main__":
    getSummaries_NIHReporter(PI("Smith","Quinton"))