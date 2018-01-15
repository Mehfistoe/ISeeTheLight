#!/usr/bin/python3

import csv
#import pandas as pd
from bs4 import BeautifulSoup
import requests
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

def main():
    scrape_table()

if __name__ == "__main__":
    main()

