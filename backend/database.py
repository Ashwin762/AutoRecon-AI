from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ScanResult(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, index=True)
    subdomains = Column(JSON)
    dns_info = Column(JSON)
    port_scan = Column(JSON)
    breach_results = Column(JSON)
    ai_report = Column(JSON)
    risk_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

def create_tables():
    import time
    max_retries = 10
    for i in range(max_retries):
        try:
            Base.metadata.create_all(bind=engine)
            print("[+] Database tables created successfully!")
            return
        except Exception as e:
            print(f"[-] Database not ready, retrying in 3s... ({i+1}/{max_retries})")
            time.sleep(3)
    print("[-] Could not connect to database after max retries")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()