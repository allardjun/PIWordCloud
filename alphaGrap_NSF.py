import json
import requests
from requests.structures import CaseInsensitiveDict
import pandas as pd

from pprint import pprint

url = "http://api.nsf.gov/services/v1/awards.json"

params = {"pdPIName": "Allard", "printFields": "abstractText"}

responseData = requests.post(url,params=params)
print(responseData.status_code)

# parse the JSON
rawResponse = responseData.text
response = json.loads(rawResponse)
print(json.dumps(response, indent=4, sort_keys=True))

