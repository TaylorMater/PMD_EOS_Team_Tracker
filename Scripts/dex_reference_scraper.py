import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path


################################################################

def get_pokemon_iq_group(dex_num, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        #starting tag, use the string to help us find the right table
        mystery_dungeon_starting_tag = soup.find(name=True, string="Mystery Dungeon 2 Info")

        # Extract IQ Group information
        if mystery_dungeon_starting_tag:

            print('found the starting tag')
            #find the table this lives in
            parent_table = mystery_dungeon_starting_tag.find_parent('table', {'width': '98%', 'border': '1', 'bordercolor': '#868686'})
            #grab the third table row, where iq lives
            table_rows = parent_table.find_all('tr', limit=3)
            iq_table_row = table_rows[2]
            #grab the second td tag, where the iq group info lives
            td_rows = iq_table_row.find_all('td', limit=2)
            #save the full string of the iq value, we can always parse this to just be the character after group
            pokemon_iq = td_rows[1].text.strip()
            # print(f"Pokemon IQ: {poke_iq}")

        #will be caught by the except if something fails 
        extracted_pokemon = {
            # "name": center_panel_info[1].text,
            "dex_number": (str(dex_num).zfill(3)),
            "iq_group": pokemon_iq
            # "speed": int(base_stats_td[4].text)
        }
        return extracted_pokemon
    except:
        print("unable to find iq group, erorr in parsing")

    else:
        print(f"Failed to retrieve data for {dex_num}. Status code: {response.status_code}")
        return None



################################################################

#don't want to bother with proper input handlind
max_num = int(input("Max dex entry? Entry must be from 1 to 492, inclusive: "))
dex_number = 1

#serebii spin off dex, inject nat dex entry (with padded zeros) between pokemon url and suffix url
pokemon_url = 'https://www.serebii.net/spindex-dp/'
suffix_url = '.shtml'

#will be a list of dictionaries, where each one is a
pokemon_data_final = []


while(dex_number <= max_num):
    print(f'Scraping for {dex_number}')
    pokemon_data = get_pokemon_iq_group(dex_num=dex_number, url=f"{pokemon_url}{str(dex_number).zfill(3)}{suffix_url}")
    if pokemon_data:
        print(f"Found data for {dex_number}")
        pokemon_data_final.append(pokemon_data)
        dex_number = dex_number + 1

pokemon_df = pd.DataFrame(pokemon_data_final)
pokemon_df.to_csv(Path('../Resources/iq_test_scrape_results.csv'))

# Starting point for this from, but looking at different part of html so had to reformat beautiful soup: https://github.com/shadforth/pokemon-web-scraper/blob/master/scraper.py
