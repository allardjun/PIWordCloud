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
import xlsxwriter
import os

import interact_NIHReporter
import interact_NSFAwardSearch
import interact_PubMed
import piwc_keywords
import piwc_wordcloud

from piwc_PIWordCloud import PI 

def make_PIWordCloud(dfPIList):
    '''
    From a dataframe of PI information (names, attributes), 
    query keywords from various sources (NIH Reporter, NSF Awards, PubMed, local text)
    and make a wordcloud from these.
    '''

    PIList = list(dfPIList["PI Last Name"])

    for iPI,PIRow in enumerate(PIList):

        print(dfPIList.iloc[iPI])

        thisPI = PI(dfPIList["PI Last Name"][iPI],dfPIList["PI First Name"][iPI])
        thisPI.commonness = dfPIList["Commonness"][iPI]

        fetch_tf = 1 # whether or not to get data from APIs (if no, try getting from file)

        if fetch_tf:

            text = []

            if dfPIList["LocalText"][iPI]==1:
                with open('data/LocalText/' + thisPI.lastName + thisPI.firstName[0] + '.txt') as f:
                    text.append(f.readlines())

                keywords_direct_flattened = []
            else:
                # get summaries using their APIs
                text.append(interact_NSFAwardSearch.getSummaries_NSFAwardSearch(thisPI))
                text_NIH, keywords_NIH = interact_NIHReporter.getSummaries_NIHReporter(thisPI)
                text.append(text_NIH)
                text_PubMed, keywords_PubMed = interact_PubMed.getSummaries_PubMed(thisPI)
                text.append(text_PubMed)

                keywords_PubMed_flattened = [item for sublist in keywords_PubMed for item in sublist]
                keywords_NIH_flattened = [item for sublist in keywords_NIH for item in sublist]
                keywords_direct_flattened = keywords_PubMed_flattened + keywords_NIH_flattened

                file = open("text.pckl","wb")
                pickle.dump([text,keywords_PubMed],file)

        else:

            with open("text.pckl", 'rb') as f:
                text,keywords_PubMed = pickle.load(f)

        # ------ pre-process the text -----------



        # flatten
        flat_text = [item for sublist in text for item in sublist]

        flat2_text = ''
        for count, item in enumerate(flat_text):
            if item is not None:
                flat2_text += item  


        # ------ generate keywords using Natural Language Processing -----------

        keyphrases_fromAnalysis = piwc_keywords.getKeywords(flat2_text)

        # ------ output -----------

        keyphrases_for_wordcloud = []
        print(thisPI.firstName.upper() + " " + thisPI.lastName.upper())
        for keyphrase in keyphrases_fromAnalysis:
            print(keyphrase)
            keyphrases_for_wordcloud.append(keyphrase)
        for keyphrase in keywords_direct_flattened:
            print(keyphrase.lower())
            keyphrases_for_wordcloud.append(keyphrase.lower())

        # one big file with everyone
        if 1:
            with open('output.txt', 'a') as f:
                f.write("\n")
                f.write(thisPI.firstName.upper() + " " + thisPI.lastName.upper() + "\n")
                for keyphrase in keyphrases_fromAnalysis:
                    f.write(keyphrase + "\n")
                for keyphrase in keywords_direct_flattened:
                    f.write(keyphrase.lower() + "\n")

        # Make wordcloud
        if len(keyphrases_for_wordcloud) > 0:
            # wordcloud to png
            piwc_wordcloud.make_wordcloud(keyphrases_for_wordcloud, thisPI.lastName)
        else:
            print("No word found for " + thisPI.lastName)

if __name__ == "__main__":

    if 0:
        dfPIList = pd.read_excel('PIList2.xlsx')
    else:
        PILastName = 'Yu'
        PIFirstName = 'Jin'
        dfPIList = pd.DataFrame([[PILastName,PIFirstName,1,0]],
            columns=['PI Last Name','PI First Name','Commonness','LocalText'])

    make_PIWordCloud(dfPIList) 