import csv
from lxml import html
import requests

# webpage that we need to access is in the csv file
web_address = 'http://www.tdcj.state.tx.us/death_row/'

page = requests.get()

#array {thank,supporter,none,family,this offender declined to make a last statement,love,family};
#pos
#neg
#neutral