import requests
from bs4 import BeautifulSoup
url = "https://myneta.info/LokSabha2024/index.php?action=summary&subAction=winner_analyzed&sort=candidate#summary"
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table', class_='w3-table w3-bordered')
rows = tables[0].find_all('tr')
print(f"Total rows: {len(rows)}")
if len(rows) > 1:
    cols = rows[1].find_all('td')
    for i, c in enumerate(cols):
        print(f"Col {i}: {c.text.strip()}")
