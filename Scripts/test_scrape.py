import requests
from bs4 import BeautifulSoup
import re

dex_number = 1
#serebii spin off dex, inject nat dex entry (with padded zeros) between pokemon url and suffix url
pokemon_url = 'https://www.serebii.net/spindex-dp/'
suffix_url = '.shtml'
url=f"{pokemon_url}{str(dex_number).zfill(3)}{suffix_url}"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
output_html = response.text


try:

    mystery_dungeon_starting_tag = soup.find(name=True, string="Mystery Dungeon 2 Info")

    # Extract IQ Group information
    if mystery_dungeon_starting_tag:
        parent_table = mystery_dungeon_starting_tag.find_parent('table', {'width': '98%', 'border': '1', 'bordercolor': '#868686'})
        table_rows = parent_table.find_all('tr', limit=3)
        iq_table_row = table_rows[2]

        td_rows = iq_table_row.find_all('td', limit=2)

        poke_iq = td_rows[1].text.strip()

        print(f"Pokemon IQ: {poke_iq}")

except:
    print("unable to find iq group, erorr in parsing")


# with open("html_output.txt", "w") as text_file:
#     text_file.write(output_html)

