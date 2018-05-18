#!/usr/bin/python3

import csv
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import numpy as np
#import json

URL = 'http://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html'

def scrape_table():
    # scraping the table from the website
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    with open('TX_Inmate_data.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)

        # get the content for the header row from the 'th' tags
        header_row_html = soup.find_all('th')
        header_row = []
        for header in header_row_html:
            header_row.append(header.text)
        writer.writerow(header_row)

        # get the content for the rows with the 'td' tags
        rows_html = soup.find_all('tr')
        for tr in rows_html:
            row_content = []
            td = tr.find_all('td')
            for i in td:
                if i.a is not None:
                    row_content.append(i.a.get('href'))
                else:
                    row_content.append(i.text)
            writer.writerow(row_content)
    return

def get_last_statements():
    BASE_URL = 'http://www.tdcj.state.tx.us/death_row/'
    inmate_df = pd.read_csv('TX_Inmate_data.csv')
    # TODO: use BeautifulSoup to got to the webpage with the final statement and scrape it off
    # TODO: handle TypeErrors for missing entries
    last_statements = [] # column to add to the dataframe
    paragraphs = [] # STACK to hold each paragraph in the Last Statements page
        
    for i, row in inmate_df.iterrows():
        # Go to the page with the Last Statement on it
        page = requests.get(BASE_URL + row['Last Statement'])
        soup = BeautifulSoup(page.content, "html.parser")

        # locates the phrase "Last Statement" to start scanning from
        key_phrase = re.compile(r'Last Statement')
        try:
            # Loop to find eveything to follow the "Last Statement" key phrase
            for sibling in soup.find('p', text=key_phrase).next_siblings:
                #print(sibling)
                paragraphs.append(str(sibling))
        except TypeError as e:
            print(e)
            paragraphs.append("Awkward Entry?")
            continue
        except NameError as n:
            print(n)
            paragraphs.append("Awkward Entry?")
            continue
        except AttributeError as a:
            print(a)
            paragraphs.append("Fuck off")
            continue
            
        last_statement_entry = "\n".join(paragraphs)
        np.append(last_statements, last_statement_entry)

    return last_statements



def main():
    # scrape_table()
    print(get_last_statements())

if __name__ == "__main__":
    main()

