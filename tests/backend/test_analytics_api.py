import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "backend"))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database.connection import Base, get_db
import app.database.models
from app.database.models import Problem, Topic, ProblemTopic, UserProblem, Submission
from app.main import app
from fastapi.testclient import TestClient
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Seed Test Database
with TestingSession() as db:
    p1 = Problem(problem_id=1, frontend_id="1", title="Two Sum", title_slug="two-sum", difficulty="Easy")
    t1 = Topic(topic_id=1, name="Array")
    pt1 = ProblemTopic(problem_id=1, topic_id=1)
    up1 = UserProblem(problem_id=1, status="Solved", num_submissions=2, num_accepted=1, attempts_before_ac=1, first_submitted_at=datetime(2026, 1, 1, 10, 0), first_accepted_at=datetime(2026, 1, 1, 10, 10), last_result="Accepted")
    s1 = Submission(submission_id=1, problem_id=1, submitted_at=datetime(2026, 1, 1, 10, 0), result="Wrong Answer")
    s2 = Submission(submission_id=2, problem_id=1, submitted_at=datetime(2026, 1, 1, 10, 10), result="Accepted")

    db.add_all([p1, t1, pt1, up1, s1, s2])
    db.commit()

def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_overall_analytics_endpoint():
    response = client.get("/api/v1/analytics/overall")
    assert response.status_code == 200
    data = response.json()
    assert data["solved_count"] == 1
    assert data["overall_ac_rate"] == 50.0

def test_problem_analytics_endpoint():
    response = client.get("/api/v1/analytics/problems/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Two Sum"
    assert data["wa_count"] == 1
    assert data["attempts_before_ac"] == 1

def test_topic_analytics_endpoint():
    response = client.get("/api/v1/analytics/topics")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["topic_name"] == "Array"

def test_difficulty_analytics_endpoint():
    response = client.get("/api/v1/analytics/difficulty")
    assert response.status_code == 200
    data = response.json()
    assert "easy" in data
    assert data["easy"]["solved"] == 1
