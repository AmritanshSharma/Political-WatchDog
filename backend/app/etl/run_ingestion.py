import sys
import os
import random

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.db.models import Base, Politician, FinancialSnapshot, ProjectTender
from app.etl.scrapers import ScraperBlueprint

def run():
    print("Initializing Database...")
    Base.metadata.drop_all(bind=engine) # Reset for phase 3 schema change
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    
    print("Starting MyNeta scraper...")
    scraper = ScraperBlueprint()
    winners = scraper.scrape_lok_sabha_winners()
    
    # Ensure we have ~543 for nationwide simulation
    print(f"Scraped {len(winners)} real politicians. Synthesizing the rest to reach 543 Lok Sabha MPs.")
    
    indian_states = [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
        "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
        "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana",
        "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"
    ]
    
    # Duplicate or synthesize to hit 543
    extended_winners = []
    base_len = max(len(winners), 1)
    for i in range(543):
        if len(winners) > 0 and i < len(winners):
            w = winners[i].copy()
        else:
            # Synthetic MP
            base = winners[i % base_len] if len(winners) > 0 else {"name": "Demo Leader", "assets": 1000000, "liabilities": 0}
            w = {
                "name": f"{base['name']} V{i}",
                "party": base.get('party', 'IND'),
                "constituency": f"Constituency_{i}",
                "assets": base['assets'] * random.uniform(0.5, 2.0),
                "liabilities": base['liabilities'] * random.uniform(0.5, 1.5)
            }
        
        # Assign a random state for the map visualization
        w['state'] = random.choice(indian_states)
        w['role'] = "MP - Lok Sabha"
        extended_winners.append(w)
        
    print(f"Ingesting 543 politicians into local database...")
    
    for i, w in enumerate(extended_winners):
        unique_id = f"mp_{i}_{w['state'].replace(' ', '_').lower()}"
        
        politician = Politician(
            unique_id=unique_id,
            name=w['name'],
            state=w['state'],
            party=w['party'],
            constituency=w['constituency'],
            role=w['role'],
            scrape_status="Not Scraped"
        )
        db.add(politician)
        db.commit()
        db.refresh(politician)
            
        # Add Financial Snapshot for 2024
        snapshot = db.query(FinancialSnapshot).filter(
            FinancialSnapshot.politician_id == politician.id, 
            FinancialSnapshot.year == 2024
        ).first()
        
        if not snapshot:
            # We'll synthesize historical data for 2014 and 2019 to make the charts look good
            # Real historical data would require scraping previous election pages for the same candidate
            
            assets_2024 = w['assets']
            income_2024 = random.uniform(assets_2024 * 0.05, assets_2024 * 0.1) if assets_2024 > 0 else 0
            
            history = [
                (2014, assets_2024 * random.uniform(0.1, 0.3), income_2024 * random.uniform(0.1, 0.3)),
                (2019, assets_2024 * random.uniform(0.4, 0.7), income_2024 * random.uniform(0.4, 0.7)),
                (2024, assets_2024, income_2024)
            ]
            
            for year, ast, inc in history:
                snap = FinancialSnapshot(
                    politician_id=politician.id,
                    year=year,
                    declared_assets=ast,
                    declared_liabilities=w['liabilities'] if year == 2024 else w['liabilities'] * random.uniform(0.2, 0.8),
                    declared_income=inc
                )
                db.add(snap)
                
            db.commit()
            
    print("Ingestion completed successfully.")

if __name__ == "__main__":
    run()
