import json
import requests
from requests.structures import CaseInsensitiveDict
import pandas as pd

from pprint import pprint



url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

params = {"db": "pubmed", "term": "cancer", "reldate":"60","retmax":"100"}

responseData = requests.post(url,params=params)
print(responseData.status_code)

# parse the JSON
rawResponse = responseData.text
response = json.loads(rawResponse)
print(json.dumps(response, indent=4, sort_keys=True))

