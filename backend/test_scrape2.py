import requests
from bs4 import BeautifulSoup

url = "https://myneta.info/LokSabha2024/index.php?action=show_winners&sort=default"
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table', id='table1')
print("Found tables:", len(tables))
if tables:
    rows = tables[0].find_all('tr')
    print("Found rows:", len(rows))
    if len(rows) > 1:
        cols = rows[1].find_all('td')
        print("Row 1 cols:", len(cols))
        for i, c in enumerate(cols):
            print(f"Col {i}: {c.text.strip()}")
