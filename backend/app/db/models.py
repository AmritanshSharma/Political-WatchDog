from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base

class Politician(Base):
    __tablename__ = "politicians"

    id = Column(Integer, primary_key=True, index=True)
    unique_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    state = Column(String)
    party = Column(String)
    constituency = Column(String)
    role = Column(String, default="MP")
    scrape_status = Column(String, default="Not Scraped")
    
    financial_snapshots = relationship("FinancialSnapshot", back_populates="politician")
    project_tenders = relationship("ProjectTender", back_populates="politician")

class FinancialSnapshot(Base):
    __tablename__ = "financial_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    politician_id = Column(Integer, ForeignKey("politicians.id"))
    year = Column(Integer)
    declared_assets = Column(Float)
    declared_liabilities = Column(Float)
    declared_income = Column(Float)
    
    politician = relationship("Politician", back_populates="financial_snapshots")

class ProjectTender(Base):
    __tablename__ = "project_tenders"

    id = Column(Integer, primary_key=True, index=True)
    politician_id = Column(Integer, ForeignKey("politicians.id"))
    project_name = Column(String)
    sanctioned_amount = Column(Float)
    spent_amount = Column(Float)
    status = Column(String)
    date_sanctioned = Column(Date)

    politician = relationship("Politician", back_populates="project_tenders")
