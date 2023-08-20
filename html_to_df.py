import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re 

def convert_html_to_prices(html_str):
    '''
    Take an HTML and convert into price index using
    Spit out dictionary of: 
        k,v : 'Item Name' (str), 'Price' (str)
        #TODO: eventually need to extract other useful data
        #TODO: assume that is USD for now.

    '''
    # First convert into BS4 obj
    soup = BeautifulSoup(html_str, 'html.parser')
    matches = soup.find_all(
        r"\$\d{1,4}(?:\.\d{1,2})?"
    )
    


def convert_html_path_to_readble(html_path):
    with open(html_path, 'r', encoding='utf-8') as file:
        data_str = file.read()

    return data_str


def beautify_data(list_extract):
    pass