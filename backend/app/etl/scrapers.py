import json
from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup
import re

class ScraperBlueprint:
    def __init__(self):
        pass

    def parse_currency(self, amount_str):
        # Parses strings like "Rs 1,50,00,000" or "Rs 1.5 Crore" into float
        if not amount_str or amount_str.lower() == 'nil' or amount_str.strip() == '':
            return 0.0
        
        amount_str = amount_str.lower().replace('rs', '').replace(',', '').strip()
        
        multiplier = 1
        if 'crore' in amount_str:
            multiplier = 10000000
            amount_str = amount_str.replace('crore', '').replace('+', '').strip()
        elif 'lacs' in amount_str or 'lakhs' in amount_str or 'lac' in amount_str or 'lakh' in amount_str:
            multiplier = 100000
            amount_str = amount_str.replace('lacs', '').replace('lakhs', '').replace('lac', '').replace('lakh', '').replace('+', '').strip()
            
        # extract numeric part using regex
        match = re.search(r'[\d\.]+', amount_str)
        if match:
            return float(match.group()) * multiplier
        return 0.0

    def scrape_lok_sabha_winners(self):
        """
        Real scraper for Lok Sabha 2024 winners from MyNeta.
        """
        url = "https://myneta.info/LokSabha2024/index.php?action=summary&subAction=winners_analyzed"
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to fetch MyNeta data: {e}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # The winners table usually has class 'w3-table w3-bordered'
        tables = soup.find_all('table', class_='w3-table w3-bordered')
        if not tables:
            return []
            
        data_table = tables[0]
        rows = data_table.find_all('tr')
        
        results = []
        for row in rows[1:]: # Skip header
            cols = row.find_all('td')
            if len(cols) >= 8:
                name_a = cols[1].find('a')
                if not name_a:
                    continue
                name = name_a.text.strip()
                constituency = cols[2].text.strip()
                party = cols[3].text.strip()
                
                assets_str = cols[6].text.strip()
                liabilities_str = cols[7].text.strip()
                
                assets = self.parse_currency(assets_str)
                liabilities = self.parse_currency(liabilities_str)
                
                # We'll just put state as "Unknown" since the summary table may not have it explicitly separated easily
                state = "India"
                
                results.append({
                    "name": name,
                    "state": state,
                    "party": party,
                    "constituency": constituency,
                    "assets": assets,
                    "liabilities": liabilities,
                    "income": 0.0 # MyNeta summary doesn't always show income, default to 0
                })
        
        return results

    def scrape_mplads(self):
        """
        Mock scraper for eSAKSHI MPLADS portal to avoid IP bans.
        Synthesizes realistic data for the dashboard.
        """
        return [
            {
                "project_name": "Construction of Rural Roads",
                "sanctioned_amount": 15000000,
                "spent_amount": 12000000,
                "status": "Completed"
            },
            {
                "project_name": "Drinking Water Supply System",
                "sanctioned_amount": 8000000,
                "spent_amount": 3500000,
                "status": "In Progress"
            },
            {
                "project_name": "Primary School Infrastructure Upgradation",
                "sanctioned_amount": 5000000,
                "spent_amount": 5000000,
                "status": "Completed"
            }
        ]
