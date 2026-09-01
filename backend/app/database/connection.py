import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

def create_db_engine():
    try:
        # Attempt MySQL connection
        mysql_engine = create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20
        )
        with mysql_engine.connect() as conn:
            pass
        print("[DATABASE] Connected to MySQL successfully.")
        return mysql_engine
    except Exception as e:
        print(f"[DATABASE NOTICE] MySQL connection unavailable ({e}). Falling back to local SQLite database.")
        sqlite_url = "sqlite:///./leetcode_analytics.db"
        return create_engine(sqlite_url, connect_args={"check_same_thread": False})

engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
