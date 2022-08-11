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
import call_keywords
import wordcloud_tools

from PIWordCloud import PI 
import vignette


def makeVignettes_batch(dfPIList):
        
    PIList = list(dfPIList["PI Last Name"])

    for iPI,PIRow in enumerate(PIList):

        print(dfPIList.iloc[iPI])

        thisPI = PI(dfPIList["PI Last Name"][iPI],dfPIList["PI First Name"][iPI])

        vignette.makeVignette(thisPI)
        

if __name__ == "__main__":

    if 1:
        dfPIList = pd.read_excel('PIList.xlsx')
    else:
        PILastName = 'Carter'
        PIFirstName = 'Paul'
        dfPIList = pd.DataFrame([[PILastName,PIFirstName,0,1]],
            columns=['PI Last Name','PI First Name','Commonness','LocalText'])

    makeVignettes_batch(dfPIList) 