#!/usr/bin/python3

import csv
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import numpy as np
#import json

URL = 'http://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html'
BASE_URL = 'http://www.tdcj.state.tx.us/death_row/'
inmate_df = pd.read_csv('TX_Inmate_data.csv')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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
    last_statements = [] # column to add to the dataframe
        
    for i, row in inmate_df.iterrows():
        # Go to the page with the Last Statement on it
        page = requests.get(BASE_URL + row['Last Statement'])
        soup = BeautifulSoup(page.content, "html.parser")
        paragraphs = [] # to hold each paragraph in the Last Statements page

        # locates the phrase "Last Statement" to start scanning from
        key_phrase = re.compile(r'Last Statement')
        
        try:
            # Loop to find eveything to follow the "Last Statement" key phrase
            for sibling in soup.find('p', text=key_phrase).next_siblings:
                # print(sibling)
                paragraphs.append(str(sibling))
        except TypeError as e:
            print("Awkward Entry?")
            paragraphs.append("Awkward Entry?")
            
        except NameError as n:
            print("Awkward Entry?")
            paragraphs.append("Awkward Entry?")
            
        except AttributeError as a:
            print("Awkward Entry?")
            paragraphs.append("Awkward Entry?")
            
            
        if "Awkward Entry?" in paragraphs:
            last_statement_entry = "Awkward Entry?"
        else:
            last_statement_entry = "\n".join(paragraphs)
            last_statement_entry = BeautifulSoup(last_statement_entry, "lxml").text
            last_statement_entry = last_statement_entry.replace("InstanceEndEditable", "")
        
        print(bcolors.WARNING)
        print(last_statement_entry)
        print(bcolors.ENDC)
        last_statements.append(last_statement_entry)
        print('Entry added.')

    return np.array(last_statements)



def main():
    # scrape_table()
    
    # inmate_df['Last Statements Text'] = get_last_statements()
    # inmate_df.to_csv('new_inmate.csv')

if __name__ == "__main__":
    main()

