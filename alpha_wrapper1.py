# Given the name of a PI at UCI, 
# grab data from NIH Reporter, NSF Award Search, and PubMed,
# then use Natural Language processing to extract keywords describing their research
# Jun allardlab.com

import json
import requests
from requests.structures import CaseInsensitiveDict
import pandas as pd
import pprint
import pickle

import interact_NIHReporter
import interact_NSFAwardSearch
import interact_PubMed
import call_keywords

from PIWordCloud import PI 

thisPI = PI("Read","Elizabeth")

fetch_tf = 1 # whether or not to get data from APIs (if no, try getting from file)

if fetch_tf:

    text = []

    # get summaries using their APIs
    text.append(interact_NIHReporter.getSummaries_NIHReporter(thisPI))
    text.append(interact_NSFAwardSearch.getSummaries_NSFAwardSearch(thisPI))
    text_PubMed, keywords_PubMed = interact_PubMed.getSummaries_PubMed(thisPI)
    text.append(text_PubMed)

    file = open("text.pckl","wb")
    pickle.dump([text,keywords_PubMed],file)

else:

    with open("text.pckl", 'rb') as f:
        text,keywords_PubMed = pickle.load(f)



# ------ pre-process the text -----------

keywords_PubMed_flattened = [item for sublist in keywords_PubMed for item in sublist]

# flatten
flat_text = [item for sublist in text for item in sublist]

flat2_text = ''
for count, item in enumerate(flat_text):
    #print("count={0}".format(count))
    #print(item)
    if item is not None:
        flat2_text += item  

# ------ generate keywords using Natural Language Processing -----------

keyphrases_fromAnalysis = call_keywords.getKeywords(flat2_text)

print(thisPI.firstName.upper() + thisPI.lastName.upper())
for keyphrase in keyphrases_fromAnalysis:
    print(keyphrase)
for keyphrase in keywords_PubMed_flattened:
    print(keyphrase.lower())
