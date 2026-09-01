import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "backend"))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database.connection import Base
import app.database.models  # Registers ORM models with Base.metadata
from app.database.models import Problem

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Bind and create all tables in-memory
Base.metadata.create_all(bind=engine)

# Insert problem 1 into test DB for foreign key constraint
with TestingSessionLocal() as db:
    prob = Problem(
        problem_id=1,
        frontend_id="1",
        title="Two Sum",
        title_slug="two-sum",
        difficulty="Easy"
    )
    db.add(prob)
    db.commit()

from fastapi.testclient import TestClient
from app.main import app
from app.database.connection import get_db
from datetime import datetime

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_sync_status_endpoint():
    response = client.get("/api/v1/sync/status")
    assert response.status_code == 200
    assert response.json()["status"] == "IDLE"

def test_incremental_submission_sync_endpoint():
    payload = {
        "submission_id": 999001,
        "problem_id": 1,
        "title_slug": "two-sum",
        "submitted_at": datetime.utcnow().isoformat(),
        "result": "Accepted",
        "language": "python3",
        "runtime_ms": 42,
        "memory_kb": 16400
    }
    response = client.post("/api/v1/sync/submission", json=payload)
    assert response.status_code == 201, f"Response: {response.status_code} {response.json()}"
    assert response.json()["status"] == "success"
    assert response.json()["submission_id"] == 999001
