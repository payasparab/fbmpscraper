import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re 

### MAIN FUNCTIONS ###


### UTIL FUNCTIONS ###

# convert_html_path_to_readable
# convert_html_to_prices 
# beautify_data 


def convert_html_path_to_readble(html_path):
    with open(html_path, 'r', encoding='utf-8') as file:
        data_str = file.read()
    return data_str

def convert_html_to_prices(html_str, remove_outliers=True):
    '''
    Take an HTML and convert into price index dataseries
    needs to input information about sample size and also the number of outliers removed
    Spit out dictionary of: 
        #TODO: eventually need to extract other useful data
        #TODO: assume that is USD for now. Searcg string looks for $ but can be swapped with other currencies

    Inputs:
        html_str : str : FB marketplace html converted to string
        remote_outliers : bool : whether to remove 2 std from price distribution
    
    Returns tuple: 
        0 : pd.Series(int) : prices 
        1 : int : original data points
        2 : 

    '''
    # First convert into BS4 obj
    soup = BeautifulSoup(html_str, 'html.parser')
    matches = re.findall(r"\$\d{1,6}(?:\.\d{1,2})?", soup.get_text())
    nums = np.array([int(x[1:]) for x in matches])

    # Remove outliers
    outliers_removed = 0
    # https://stackoverflow.com/questions/11686720/is-there-a-numpy-builtin-to-reject-outliers-from-a-list
    if remove_outliers:
        def reject_outliers(data, m = 2.):
            d = np.abs(data - np.median(data))
            mdev = np.median(d)
            s = d/mdev if mdev else np.zeros(len(d))
            return data[s<m]
        nums = reject_outliers(nums)
        outliers_removed = len(matches) - len(nums)

    return pd.Series(nums), outliers_removed, len(matches)


def beautify_data(list_extract):
    pass

if __name__ == "__main__":
    data = convert_html_path_to_readble('test_data.html')