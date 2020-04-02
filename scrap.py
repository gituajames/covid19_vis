import pandas as pd
import geopandas as gpd
import requests
from bs4 import BeautifulSoup as b

# use request to get the target url
r = requests.get('https://ncov2019.live/')
r.status_code

# using beautifulsoup to parse through the text
soup = b(r.text, 'lxml')

# gets the the table with id: sortable_table_global
global_ = soup.find('table', attrs={'id': 'sortable_table_global'})

# extract the table infomation and store it in a list of list
# creates a pandas dataframe with the list of lists
table_row = global_.find_all('tr')
all_rows = []
for tr in table_row:
    td = tr.find_all('td')
    row = [i.text.replace('\n', ' ').strip() for i in td]
    all_rows.append(row)
df = pd.DataFrame(all_rows, columns=['country', 'confirmed', 'changes1', 'changes1(%)', 'deceased', 
                                     'changes2', 'changes2(%)', 'recovered', 'serious'])

# <----------------data cleaning section------------------------->
# drops rows with None values
# and columns that are of no use
df.dropna(inplace=True)
df.drop(index=[1], inplace=True)
df.drop(columns=['changes1', 'changes1(%)', 'changes2', 'changes2(%)'], inplace=True)

# makes a copy of the df
copy_df = df.copy()

# removes all the puncuation characters and emojis and white spaces
copy_df['country'] = copy_df['country'].str.replace('★', '')
copy_df['country'] = copy_df['country'].str.strip()
copy_df['confirmed'] = copy_df['confirmed'].str.replace(',', '')
copy_df['deceased'] = copy_df['deceased'].str.replace(',', '')
copy_df['recovered'] = copy_df['recovered'].str.replace(',', '')
copy_df['serious'] = copy_df['serious'].str.replace(',', '')

# coverts all string values to int and floats for manipulation
copy_df['confirmed'] = copy_df['confirmed'].astype(int)
copy_df['deceased'] = pd.to_numeric(copy_df['deceased'])
copy_df['recovered'] = pd.to_numeric(copy_df['recovered'])
copy_df['serious'] = pd.to_numeric(copy_df['serious'])

data = copy_df