import json
import requests
from requests.structures import CaseInsensitiveDict
import pandas as pd

from pprint import pprint


def getSummaries_NIHReporter(PIName):
  
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
            "any_name": "{thisPIName}"
            }}
        ],
        }},
        "include_fields": [
                "ProjectTitle","AbstractText"
            ],
            "offset":0,
            "limit":50,
            "sort_field":"project_start_date",
            "sort_order":"desc"
    }}
    '''

    inputData = inputTemplate.format(thisPIName=PIName)

    # Interact with API
    responseData = requests.post(url, headers=headers, data=inputData)
    #print(responseData.status_code)

    # parse the JSON
    rawResponse = responseData.text
    response = json.loads(rawResponse)
    #print(json.dumps(response, indent=4, sort_keys=True))


    text = []

    # return abstracts and titles in a list of strings
    for grant in response['results']:
        thisAbstract = grant['abstract_text'].replace("\n", " ")
        text.append(thisAbstract)
        thisTitle = grant['project_title']
        text.append(thisTitle)
        #print(thisAbstract)

    #print(text) 
    return text
           


if __name__ == "__main__":
    getSummaries_NIHReporter("Allard")