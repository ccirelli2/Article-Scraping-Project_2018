# ARTICLE SCRAPER
'''Documentation

'''


# Import Libraries
import os
import pandas 
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


# Open Web Page

def get_bs4Obj(Url):
	html = urlopen(Url)
	bsObj = BeautifulSoup(html.read(), 'lxml')
	print(bsObj)

Test_url = 'http://securities.stanford.edu/filings-case.html?id=106569'

get_bs4Obj(Test_url)








