import pandas as pd
import geopandas as gpd
import requests
from bs4 import BeautifulSoup as b


# a procedure function specific to table at 'https://www.worldometers.info/coronavirus/#countries'
def table():
    r = requests.get('https://www.worldometers.info/coronavirus/#countries')
    print(r.status_code)
    
    soup = b(r.text, 'lxml')
    
    # find our table
    table = soup.find('table', id = 'main_table_countries_today')
    tbody = table.find('tbody')
#     print(tbody)
    
    table_row = tbody.find_all('tr')
    all_rows = []
    for tr in table_row:
        td = tr.find_all('td')
        row = [i.text.replace('\n', ' ').strip() for i in td]
        all_rows.append(row)
        
    df = pd.DataFrame(all_rows, columns=['country', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 
                                     'total_recovered', 'active', 'serirous', '1', '2', '3', '4', '5']) 
#     print(df.head())
    
    df.drop(index=[0, 1, 2, 3, 4, 5, 6, 7], inplace=True)
    df.drop(columns=['1', '2', '3', '4'], inplace=True)
    
    copy_df = df.copy()
#     print(copy_df.head())
    
    copy_df['total_recovered'] = copy_df['total_recovered'].str.replace('N/A', '0')
    copy_df['new_cases'] = copy_df['new_cases'].str.replace('+', '')
    copy_df['new_deaths'] = copy_df['new_deaths'].str.replace('+', '')
#     print(copy_df.head())
    
    copy_df['total_cases'] = copy_df['total_cases'].str.replace(',', '')
    copy_df['new_cases'] = copy_df['new_cases'].str.replace(',', '')
    copy_df['total_deaths'] = copy_df['total_deaths'].str.replace(',', '')
    copy_df['total_recovered'] = copy_df['total_recovered'].str.replace(',', '')
    copy_df['active'] = copy_df['active'].str.replace(',', '')
    copy_df['serirous'] = copy_df['serirous'].str.replace(',', '')
#     print(copy_df.head())
    
    copy_df['total_cases'] = pd.to_numeric(copy_df['total_cases'])
    copy_df['new_cases'] = pd.to_numeric(copy_df['new_cases'])
    copy_df['total_deaths'] = pd.to_numeric(copy_df['total_deaths'])
    copy_df['new_deaths'] = pd.to_numeric(copy_df['new_deaths'])
    copy_df['total_recovered'] = pd.to_numeric(copy_df['total_recovered'])
    copy_df['active'] = pd.to_numeric(copy_df['active'])
    copy_df['serirous'] = pd.to_numeric(copy_df['serirous'])
#     print(copy_df.head())
    
    copy_df.fillna(0, inplace=True)
#     print(copy_df.head())
    
    return copy_df
