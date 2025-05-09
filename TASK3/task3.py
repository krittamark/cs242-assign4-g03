import sys
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

def clean_text(text):
    if text is None:
        return None
    text = str(text).strip()
    text = re.sub(r'\s*\[.*?\]\s*', '', text)
    text = text.replace(',', '')
    if text == '—' or text == 'N/A' or text == '':
        return None
    return text

def print_dataframe(df):
    print("-" * 70)
    print(f"{'Index'}\t {'Rank'}\t {'Country':<35} {df.columns[2]}")
    print("-" * 70)

    for index, row in df.iterrows():
        rank_str = row['Rank'] if pd.notna(row['Rank']) else '-'
        gdp_val = row[df.columns[2]]
        gdp_str = int(gdp_val) if pd.notna(gdp_val) else '-'

        print(f"{index}\t {str(rank_str)}\t {row['Country']:<35} {gdp_str}")

    print("-" * 70)

url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)'

try:
    response = requests.get(url)
    response.raise_for_status()
    
    print(f"Request to {url} successful !!")
    print(f"Status code: {response.status_code} -- {response.reason}")
    html_doc = response.text

except requests.exceptions.RequestException as e:
    print(f"Request to {url} failed !! Error: {e}")
    sys.exit()

soup = BeautifulSoup(html_doc, 'html.parser')

allTables = soup.find_all('table')
allTablesCount = len(allTables)
print(f"The web page contains {allTablesCount} tables in total.")

targetTable = None
for table in allTables:
    caption = table.find('caption')
    if caption and 'GDP forecast or estimate' in caption.get_text():
        targetTable = table
        break
    elif table.find('th', string=re.compile('IMF')):
        targetTable = table
        break

if not targetTable:
    print("Could not find the target GDP table. Exiting.")
    sys.exit()

header_rows = targetTable.find_all('tr', class_='static-row-header', limit=2)
if len(header_rows) < 2:
    print("Could not find expected header rows. Exiting.")
    sys.exit()

source_ths = header_rows[0].find_all('th')[1:]
sources = []
for th in source_ths:
    a_tag = th.find('a')
    if a_tag:
        sources.append(a_tag.get_text(strip=True))

print(f"We found {len(sources)} header rows indicating info sources as follows.")
print(sources)

data_rows = targetTable.find('tbody').find_all('tr')
all_data = []
current_rank = 0

data_start_index = 0
for i, row in enumerate(data_rows):
    first_cell = row.find(['td', 'th'])
    if first_cell and first_cell.find('a'):
        data_start_index = i
        break
    elif first_cell and 'World' in first_cell.get_text():
        data_start_index = i
        break

for i, row in enumerate(data_rows[data_start_index:]):
    cells = row.find_all(['td', 'th'])

    is_ranked = 'static-row-numbers-norank' not in row.get('class', [])

    country_cell = cells[0]
    country_name_tag = country_cell.find('a')
    country_name = clean_text(country_name_tag.get_text() if country_name_tag else country_cell.get_text())

    rank_val = None
    if country_name == 'World':
        rank_val = 0
    elif is_ranked:
        current_rank += 1
        rank_val = current_rank
    else:
        rank_val = '-'

    imf_gdp = None
    wb_gdp = None
    un_gdp = None

    logical_col_idx_ptr = 0 
    actual_cell_idx = 1

    while actual_cell_idx < len(cells) and logical_col_idx_ptr < 6:
        current_data_cell = cells[actual_cell_idx]
        cell_text_content = clean_text(current_data_cell.get_text())
        colspan = int(current_data_cell.get('colspan', 1))

        if logical_col_idx_ptr == 0:
            if colspan == 1 and cell_text_content is not None:
                imf_gdp = cell_text_content
        elif logical_col_idx_ptr == 2:
            if colspan == 1 and cell_text_content is not None:
                wb_gdp = cell_text_content
        elif logical_col_idx_ptr == 4:
            if colspan == 1 and cell_text_content is not None:
                un_gdp = cell_text_content
        
        logical_col_idx_ptr += colspan
        actual_cell_idx += 1

    all_data.append({
        'Rank': rank_val,
        'Country': country_name,
        'IMF_GDP': imf_gdp,
        'WB_GDP': wb_gdp,
        'UN_GDP': un_gdp
    })

master_df = pd.DataFrame(all_data)
#master_df['IMF_GDP'] = pd.to_numeric(master_df['IMF_GDP'], errors='coerce')
#master_df['WB_GDP'] = pd.to_numeric(master_df['WB_GDP'], errors='coerce')
#master_df['UN_GDP'] = pd.to_numeric(master_df['UN_GDP'], errors='coerce')

df_imf = master_df[['Rank', 'Country', 'IMF_GDP']].copy()
df_imf.rename(columns={'IMF_GDP': 'GDP (million US$) by IMF'}, inplace=True)
df_imf.reset_index(drop=True, inplace=True)
print_dataframe(df_imf)

df_wb = master_df[['Rank', 'Country', 'WB_GDP']].copy()
df_wb.rename(columns={'WB_GDP': 'GDP (million US$) by World Bank'}, inplace=True)
df_wb.reset_index(drop=True, inplace=True)
print_dataframe(df_wb)

df_un = master_df[['Rank', 'Country', 'UN_GDP']].copy()
df_un.rename(columns={'UN_GDP': 'GDP (million US$) by United Nations'}, inplace=True)
df_un.reset_index(drop=True, inplace=True)
print_dataframe(df_un)