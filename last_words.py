#!/bin/env python

import csv
import pandas as pd
from lxml import html
import requests
import json
from watson_developer_cloud import AlchemyLanguageV1

web_address = 'http://www.tdcj.state.tx.us/death_row/'

dataframe = pd.read_csv('~/TX_Inmate_data.csv')

with open('words.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    for index, row in dataframe.iterrows():
        last_words_page = dataframe.iloc[index, 2]
        page = requests.get(web_address + last_words_page)
        tree = html.fromstring(page.content)
        # last node: //*[@id="body"]/comment()[2]
        # first node: //*[@id="body"]/p[6]
        last_words = tree.xpath('//*[@id="body"]/p[position()>5]/text()')
        # print(last_words)
        writer.writerow(last_words)


alchemy_language = AlchemyLanguageV1(api_key='430993732be62f8ebf38081520c5898ff48f2b5c')

with open('words.csv', 'r') as file:
    reader = csv.reader(file)
    print(json.dumps(
        alchemy_language.emotion(
            text=reader,
        ),
        indent=2))
