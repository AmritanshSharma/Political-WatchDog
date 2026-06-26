from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Politician, FinancialSnapshot, ProjectTender
from app.services.analysis import AnomalyEngine

router = APIRouter()
anomaly_engine = AnomalyEngine()

@router.get("/politicians")
def list_politicians(db: Session = Depends(get_db)):
    politicians = db.query(Politician).all()
    return politicians

@router.get("/politicians/{unique_id}")
def get_politician(unique_id: str, db: Session = Depends(get_db)):
    politician = db.query(Politician).filter(Politician.unique_id == unique_id).first()
    if not politician:
        raise HTTPException(status_code=404, detail="Politician not found")
        
    # Get financial snapshots
    financials = db.query(FinancialSnapshot).filter(FinancialSnapshot.politician_id == politician.id).order_by(FinancialSnapshot.year).all()
    
    # Calculate anomaly score (simplified, comparing latest year to previous)
    anomaly_score = 0
    if len(financials) >= 2:
        latest = financials[-1]
        previous = financials[-2]
        asset_growth = latest.declared_assets - previous.declared_assets
        anomaly_score = anomaly_engine.calculate_anomaly_score(asset_growth, latest.declared_income)
        
    # Get unspent funds
    tenders = db.query(ProjectTender).filter(ProjectTender.politician_id == politician.id).all()
    total_sanctioned = sum(t.sanctioned_amount for t in tenders)
    total_spent = sum(t.spent_amount for t in tenders)
    unspent_pct = anomaly_engine.calculate_unspent_funds_percentage(total_sanctioned, total_spent)
    
    return {
        "id": politician.id,
        "unique_id": politician.unique_id,
        "name": politician.name,
        "role": politician.role,
        "scrape_status": politician.scrape_status,
        "state": politician.state,
        "party": politician.party,
        "anomaly_score": round(anomaly_score, 2),
        "unspent_funds_percentage": unspent_pct,
        "financials": financials,
        "tenders": tenders
    }
