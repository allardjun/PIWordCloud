# Grab from APIs and extract keywords

import json
import requests
from requests.structures import CaseInsensitiveDict
import pandas as pd
from pprint import pprint

import interact_NIHReporter
import interact_NSFAwardSearch
import interact_PubMed
import call_keywords

PIName = "Mortazavi"

text = []

# get summaries using their APIs
text.append(interact_NIHReporter.getSummaries_NIHReporter(PIName))
text.append(interact_NSFAwardSearch.getSummaries_NSFAwardSearch(PIName))
text_PubMed, keywords_PubMed = interact_PubMed.getSummaries_PubMed(PIName)
text.append(text_PubMed)

# pre-process the text
print(text)

# flatten
flat_text = [item for sublist in text for item in sublist]



print(keywords_PubMed)

#call_keywords.getKeywords(flat_text)