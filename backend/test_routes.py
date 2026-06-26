import sys, os
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import Politician
from app.api.routes import list_politicians

db = SessionLocal()
try:
    res = list_politicians(db=db)
    print("Success:", len(res))
except Exception as e:
    import traceback
    traceback.print_exc()
