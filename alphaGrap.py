import json
import requests
from requests.structures import CaseInsensitiveDict
import pandas as pd

from pprint import pprint

url = "https://api.reporter.nih.gov/v2/projects/search"

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Content-Type"] = "application/json"

inputData = """
{
    "criteria":
    {
        "org_names": [
            "UNIVERSITY OF CALIFORNIA-IRVINE"
            ],
        "pi_names": [
         {
           "any_name": "",
           "first_name": "German",
           "last_name": "Enciso"
         }
       ],
    },
    "include_fields": [
            "Abstract","ProjectDetails"
        ],
        "offset":0,
        "limit":5,
        "sort_field":"project_start_date",
        "sort_order":"desc"
}
"""

# Interact with API
responseData = requests.post(url, headers=headers, data=inputData)
print(responseData.status_code)

# parse the JSON
rawResponse = responseData.text
response = json.loads(rawResponse)
print(json.dumps(response, indent=4, sort_keys=True))

#df = pd.read_json(response)
#print(df)

#pprint(vars(responseData))

