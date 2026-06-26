import pandas as pd
from typing import List, Dict

class DataProcessor:
    def process_financials(self, raw_data: List[Dict]):
        """
        Takes raw unstructured financial filings and standardizes them.
        """
        df = pd.DataFrame(raw_data)
        
        # Standardize names, constituencies, handle missing values
        if 'name' in df.columns:
            df['name'] = df['name'].str.title().str.strip()
            
        # Map to Unique Politician ID
        # Simplified: using Name + Constituency as a naive ID
        if 'name' in df.columns and 'constituency' in df.columns:
            df['unique_id'] = df['name'].str.lower().str.replace(' ', '_') + "_" + df['constituency'].str.lower()
            
        return df.to_dict(orient='records')
