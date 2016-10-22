#!/bin/env python

import csv
import pandas as pd
from lxml import html
import requests
import json
from watson_developer_cloud import AlchemyLanguageV1

# page that we need to access is in the csv file
web_address = 'http://www.tdcj.state.tx.us/death_row/'

dataframe = pd.read_csv('~/finaltime3.csv')

with open('words.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    i = 1
    for row in dataframe:
        last_words_page = dataframe.iloc[i, 2]
        web_address = web_address + last_words_page
        print(web_address)
        page = requests.get(web_address)

        # THERES A PROBLEM SOMEWHERE HERE
        tree = html.fromstring(page.content)
        last_words = tree.xpath('//*[@id="body"]/p[6]/text()')
        print(last_words)
        # THERES A PROBLEM SOMEWHERE HERE

        writer.writerow(last_words)
        i += 1


#alchemy_language = AlchemyLanguageV1(api_key='430993732be62f8ebf38081520c5898ff48f2b5c')

#print(json.dumps(
#    alchemy_language.combined(
#        url='http://www.tdcj.state.tx.us/death_row/dr_info/escamillalicholast.html',  # text will go here
#        extract='entities, doc-sentiment',
#        sentiment=1,
#        max_items=4),
#    indent=2))