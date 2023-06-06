import requests
import time
from datetime import date, timedelta, datetime
import pandas as pd
from bs4 import BeautifulSoup

def get_cur_date():
    """
    Returns the current date and time in a specific format.

    Returns:
        str: The current date and time formatted as "YYYY-MM-DD_HH-MM-SS".
    
    Example:
        >>> get_cur_date()
        '2023-06-01_22-30-45'
    """
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def get_title(soup):
    """
    Retrieves the title from an HTML soup object.

    Args:
        soup (BeautifulSoup): The HTML soup object.

    Returns:
        str: The extracted title text, stripped of leading and trailing whitespace.
    
    Example:
        >>> html_soup = BeautifulSoup(html_content, 'html.parser')
        >>> get_title(html_soup)
        'Mazda Axela 2,2L 2015'
    """

    anno = soup.find('h1', class_='title-announcement')
    return anno.text.strip()

def get_price(soup):
    """
    Retrieves the price from an HTML soup object.

    Args:
        soup (BeautifulSoup): The HTML soup object.

    Returns:
        str: The extracted price, stripped of leading and trailing whitespace.
    
    Example:
        >>> html_soup = BeautifulSoup(html_content, 'html.parser')
        >>> get_price(html_soup)
        '€6.400'
    """
    anno = soup.find('div', class_='announcement-price__cost')
    return anno.text.split()[0]

def get_soup(url):
    response = requests.get(url)
    html_content = response.text
    return BeautifulSoup(html_content, "html.parser")

def get_announcement_details(soup):

    anno = soup.find('div', class_='announcement__details')
    classes = ['date-meta', 'number-announcement']

    res = {}

    for class_ in classes:
        key, value = anno.find('span', class_=class_).text.strip().split(':', 1)
        value = value.strip()
        
        if key == 'Posted':
            day, time_ = value.split(' ')
            if day == 'Today':
                value = date.today().strftime("%d.%m.%Y") + ' ' + time_
            elif day == 'Yesterday':
                value = (date.today()-timedelta(days=1)).strftime("%d.%m.%Y") + ' ' + time_
            else:
                pass

        res[key] = value
    
    res['title'] = get_title(soup)
    res['price'] = get_price(soup)
    
    return res

def get_announcement_characteristics(soup):
    anno = soup.find('div', class_='announcement-characteristics clearfix')
    annos = anno.find_all('li', class_="")
    res = {}
    for an in annos:
        try:
            key = an.find('span', class_='key-chars').text.strip()
            try:
                value = an.find('a', class_='value-chars').text.strip()
            except:
                value = 'Not applicable'
        except:
            pass

        res[key] = value
    return res

def get_dataframe(res):
    df = pd.DataFrame(res)
    new_cols = [col.lower().split(':')[0].replace(' ', '_') for col in df.columns]
    mapped_dict = {key: value for key, value in zip(df.columns, new_cols)}
    df.rename(columns=mapped_dict, inplace=True)
    df['posted'] = pd.to_datetime(df['posted'], format='%d.%m.%Y %H:%M')
    df['posted'] = df['posted'].dt.strftime('%Y-%m-%d %H:%M:%S')
    return df


def get_urls(file_path):

    # Open the file in read mode
    with open(file_path, "r") as file:
        # Read the entire contents of the file
        file_contents = file.readlines()

    return [f.strip() for f in file_contents]
