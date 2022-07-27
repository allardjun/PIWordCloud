# Grab from APIs and extract keywords


import json
import requests
from requests.structures import CaseInsensitiveDict
import pandas as pd
from pprint import pprint




PIName = "Mortazavi"

text = []

# get summaries using their APIs
text.append(getSummaries_NIHReporter(PIName))
text.append(getSummaries_NSFAwardSearch(PIName))
text.append(getSummaries_PubMed(PIName))

# pre-process the text

print(text)

getKeywords(Text)