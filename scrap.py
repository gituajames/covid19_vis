import pandas as pd
import geopandas as gpd
import requests
from bs4 import BeautifulSoup as b

def table():
    r = requests.get('https://ncov2019.live/')
    r.status_code
    
    soup = b(r.text, 'lxml')
    
    global_ = soup.find('table', attrs={'id': 'sortable_table_global'})
    
    table_row = global_.find_all('tr')
    all_rows = []
    for tr in table_row:
        td = tr.find_all('td')
        row = [i.text.replace('\n', ' ').strip() for i in td]
        all_rows.append(row)
        
    df = pd.DataFrame(all_rows, columns=['country', 'confirmed', 'changes1', 'changes1(%)', 'deceased', 
                                     'changes2', 'changes2(%)', 'recovered', 'serious'])
    
    df.dropna(inplace=True)
    df.drop(index=[1], inplace=True)
    df.drop(columns=['changes1', 'changes1(%)', 'changes2', 'changes2(%)'], inplace=True)
    
    copy_df = df.copy()
    copy_df['country'] = copy_df['country'].str.replace('★', '')
    copy_df['country'] = copy_df['country'].str.strip()
    copy_df['confirmed'] = copy_df['confirmed'].str.replace(',', '')
    copy_df['deceased'] = copy_df['deceased'].str.replace(',', '')
    copy_df['recovered'] = copy_df['recovered'].str.replace(',', '')
    copy_df['serious'] = copy_df['serious'].str.replace(',', '')
    
    copy_df['confirmed'] = copy_df['confirmed'].astype(int)
    copy_df['deceased'] = pd.to_numeric(copy_df['deceased'])
    copy_df['recovered'] = pd.to_numeric(copy_df['recovered'])
    copy_df['serious'] = pd.to_numeric(copy_df['serious'])
    
    return copy_df