from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

# Render/Heroku hand out "postgres://" URLs, which SQLAlchemy 2.x rejects
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Fall back to a local SQLite file so the API still boots without a database
if not DATABASE_URL:
    print("[-] DATABASE_URL not set, falling back to SQLite")
    DATABASE_URL = f"sqlite:///{Path(__file__).parent / 'autorecon.db'}"

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=300)
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
            return True
        except Exception as e:
            print(f"[-] Database not ready ({e}), retrying in 3s... ({i+1}/{max_retries})")
            time.sleep(3)
    print("[-] Could not connect to database after max retries")
    return False

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()