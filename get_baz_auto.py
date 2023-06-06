import os
import sys
import time
import argparse
import pandas as pd
from bs4 import BeautifulSoup

try:
    from utils.utils import *
except:
    from utils import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', 
                        default= './csv',
                        help='Path to output csv files.')
    
    args = parser.parse_args()

    csv_path = args.output

    urls = get_urls('urls.txt')
    main_url = urls[0]
    
    for url in urls[1:]:

        Soup = get_soup(url)
        ad_elements = Soup.find_all("a", class_='announcement-block__title')

        res = []

        for i, ad_element in enumerate(ad_elements):
            attempts = 0
            while attempts < 3:
                try:
                    ad_href = ad_element.get('href')

                    ad_link = f"{main_url}{ad_href}"
                    soup = get_soup(ad_link)
                    an_det = get_announcement_details(soup)
                    an_char = get_announcement_characteristics(soup)
                    res.append({**an_det, **an_char})
                    res[i]['link'] = ad_link

                    attempts = 5
                except:
                    time.sleep(5)
                    attempts =+ 1

            time.sleep(3)

        if len(res) > 0:

            df = get_dataframe(res)

            csv_list = os.listdir(f'{csv_path}')
            csv_list = [csv for csv in csv_list if '.csv' in csv]
            csv_list.sort(reverse=True)

            df_main = pd.read_csv(f"{csv_path}/{csv_list[0]}")

            frames = [df_main, df]
            df_new = pd.concat(frames, ignore_index=True)

            df_new.sort_values(by='posted', ascending=False, inplace=True)

            name_of_temp_df = f'temp_baz_auto_{get_cur_date()}'
            df_new.to_csv(f'{csv_path}/{name_of_temp_df}.csv', index=False)

            time.sleep(5)

            df_upd = pd.read_csv(f"{csv_path}/{name_of_temp_df}.csv")
            df_upd.drop_duplicates(subset=['ad_id', 'price'], inplace=True)
            df_upd.to_csv(f'{csv_path}/baz_auto_{get_cur_date()}.csv', index=False)
            print(df_upd.shape)
            os.remove(f"{csv_path}/{name_of_temp_df}.csv")
        
        else:
            print('exit')
            sys.exit()

    print('Done!')

if __name__ == "__main__":
    main()