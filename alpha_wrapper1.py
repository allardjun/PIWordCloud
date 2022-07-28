# Grab from APIs and extract keywords

import json
import requests
from requests.structures import CaseInsensitiveDict
import pandas as pd
import pprint

import interact_NIHReporter
import interact_NSFAwardSearch
import interact_PubMed
import call_keywords
import pickle

PIName = "Allard"

fetch_tf = 0 # whether or not to get data from APIs (if no, try getting from file)

if fetch_tf:

    text = []

    # get summaries using their APIs
    text.append(interact_NIHReporter.getSummaries_NIHReporter(PIName))
    text.append(interact_NSFAwardSearch.getSummaries_NSFAwardSearch(PIName))
    text_PubMed, keywords_PubMed = interact_PubMed.getSummaries_PubMed(PIName)
    text.append(text_PubMed)

    file = open("text.pckl","wb")
    pickle.dump([text,keywords_PubMed],file)

else:

    with open("text.pckl", 'rb') as f:
        text,keywords_PubMed = pickle.load(f)



# ------ pre-process the text -----------

keywords_PubMed_flattened = [item for sublist in keywords_PubMed for item in sublist]


#pp = pprint.PrettyPrinter(indent=4)

#print(len(text))

# flatten
flat_text = [item for sublist in text for item in sublist]

#pp.pprint(flat_text)

#print(len(flat_text))
#print(flat_text[1])
#print(flat_text[2])

flat2_text = ''
for count, item in enumerate(flat_text):
    #print("count={0}".format(count))
    #print(item)
    if item is not None:
        flat2_text += item  
# ------ generate keywords -----------

keyphrases_fromAnalysis = call_keywords.getKeywords(flat2_text)

print(PIName.upper())
for keyphrase in keyphrases_fromAnalysis:
    print(keyphrase)
for keyphrase in keywords_PubMed_flattened:
    print(keyphrase.lower())
