
import json
import requests
from requests.structures import CaseInsensitiveDict
import pandas as pd
import pprint
import pickle
import xlsxwriter


import interact_NIHReporter
import interact_NSFAwardSearch
import interact_PubMed
import call_keywords

from PIWordCloud import PI 

dfPIList = pd.read_excel('PIList.xlsx')
PIList = list(dfPIList["PI Last Name"])

for iPI,PIRow in enumerate(PIList):

    print(PIRow)

    thisPI = PI(dfPIList["PI Last Name"][iPI],dfPIList["PI First Name"][iPI])

