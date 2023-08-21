import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re 

### MAIN FUNCTIONS ###

def html_price_print_outputs(html_path):
    # Take a localaly 
    readable = convert_html_path_to_readble(html_path)
    prices, outliers, og_n = convert_html_to_prices(readable)
    print('Removed {} ({:.0%}) outliers from {} data points'.format(
            outliers,
            outliers/og_n, 
            og_n
        )
    )

    avg, distro = beautify_data(prices)
    print('The mean price for this FB Marketplace data is ${:.2f}'.format(
            avg
        )
    )
    print(distro)
    prices.to_csv('output.csv')


def html_price_to_outputs(html_path):
    '''
    A function that takes the key information and 
    outputs it in a predictable format (TBD) to be fed to
    the chrome extension.
    '''
    pass


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
        1 : int : outliers removed
        2 : int : original data points

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


def beautify_data(price_series):
    '''
    Turning our price series data into intelligible outputs for user simplicity.

    Input: 

        price_series : pd.Series(int) : data of prices

    Output: Tuple
        0 : price_num : float : the mean price of the price_series
        1: price_distro_str : str : the string describing the distribution

    '''
    price_num = np.mean(price_series)
    desc_series = price_series.describe()
    distro_25 = desc_series.loc['25%']
    distro_75 = desc_series.loc['75%']
    sample_size = desc_series.loc['count']

    price_distro_str = ('The 25th-75th percentile range of prices is' + 
        ' ${:.0f}-${:.0f} based on a sample size of {:.0f}'.format(
            distro_25, 
            distro_75,  
            sample_size
        )
    )

    return price_num, price_distro_str




    pass
    

if __name__ == "__main__":
    html_price_print_outputs("test_data.html")