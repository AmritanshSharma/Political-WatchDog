import sys
import os
import time
import random
from datetime import datetime

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.db.models import Politician, ProjectTender
from app.etl.scrapers import ScraperBlueprint

def slow_scrape():
    db: Session = SessionLocal()
    scraper = ScraperBlueprint()
    
    print(f"[{datetime.now()}] Starting Slow Scraper Daemon...")
    
    while True:
        # Find one politician that needs scraping
        politician = db.query(Politician).filter(Politician.scrape_status == "Not Scraped").first()
        
        if not politician:
            print(f"[{datetime.now()}] All politicians have been scraped. Sleeping...")
            time.sleep(10)
            continue
            
        print(f"[{datetime.now()}] Processing MP: {politician.name} ({politician.constituency})")
        
        # Mark as In Progress
        politician.scrape_status = "In Progress"
        db.commit()
        
        # Simulate slow careful scraping (sleep 3 to 8 seconds)
        sleep_time = random.uniform(3.0, 8.0)
        print(f"  Sleeping for {sleep_time:.2f} seconds to respect rate limits...")
        time.sleep(sleep_time)
        
        # "Scrape" MPLADS
        tenders_data = scraper.scrape_mplads()
        for t in tenders_data:
            # Randomize slightly per politician
            t_spent = t['spent_amount'] * random.uniform(0.5, 1.0)
            tender = ProjectTender(
                politician_id=politician.id,
                project_name=t['project_name'],
                sanctioned_amount=t['sanctioned_amount'],
                spent_amount=t_spent,
                status=t['status']
            )
            db.add(tender)
            
        # Mark as Scraped
        politician.scrape_status = "Data Scraped"
        db.commit()
        
        print(f"  Successfully scraped MPLADS data for {politician.name}.")

if __name__ == "__main__":
    try:
        slow_scrape()
    except KeyboardInterrupt:
        print("Scraper stopped.")
