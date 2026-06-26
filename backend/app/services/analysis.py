import numpy as np
from sklearn.ensemble import IsolationForest

class AnomalyEngine:
    def __init__(self):
        # Using a simple Isolation Forest for anomaly detection
        self.clf = IsolationForest(contamination=0.1, random_state=42)
        
    def calculate_anomaly_score(self, assets_growth: float, declared_income: float) -> float:
        """
        Calculate a simple Financial Growth Anomaly Score based on Asset Growth vs. Declared Income.
        Returns a score from 0 (low risk) to 100 (high risk).
        """
        # Dummy heuristic: if asset growth is vastly larger than declared income (e.g. > 10x)
        if declared_income == 0 and assets_growth > 0:
            return 100.0
        elif declared_income == 0:
            return 0.0
            
        ratio = assets_growth / declared_income
        
        # Scale score between 0 and 100
        score = min(100.0, max(0.0, (ratio - 1.0) * 10.0))
        return score

    def calculate_unspent_funds_percentage(self, sanctioned: float, spent: float) -> float:
        if sanctioned == 0:
            return 0.0
        unspent = sanctioned - spent
        return round((unspent / sanctioned) * 100, 2)
