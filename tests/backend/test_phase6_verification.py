import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "backend"))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database.connection import Base
from app.database.models import Problem, UserProblem, Submission, SyncHistory
from app.services.sync_service import SyncService
from app.schemas.sync import IncrementalSubmissionPayloadSchema
from datetime import datetime

# Setup in-memory SQLite engine
engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def verify_phase_6_continuous_update():
    db = TestingSession()

    # Pre-insert Problem #100
    prob = Problem(
        problem_id=100,
        frontend_id="100",
        title="Same Tree",
        title_slug="same-tree",
        difficulty="Easy"
    )
    db.add(prob)
    db.commit()

    service = SyncService(db)

    # --- Scenario 1: First Attempt (Wrong Answer) ---
    sub1 = IncrementalSubmissionPayloadSchema(
        submission_id=10001,
        problem_id=100,
        title_slug="same-tree",
        submitted_at=datetime(2026, 2, 1, 10, 0, 0),
        result="Wrong Answer",
        language="python3",
        runtime_ms=0,
        memory_kb=15000
    )
    service.process_incremental_submission(sub1)

    up1 = db.query(UserProblem).filter(UserProblem.problem_id == 100).first()
    assert up1 is not None, "UserProblem should exist"
    assert up1.status == "Attempted", f"Expected Attempted, got {up1.status}"
    assert up1.num_submissions == 1
    assert up1.num_accepted == 0
    assert up1.last_result == "Wrong Answer"
    assert up1.attempts_before_ac is None
    print("[PASS] Scenario 1: First attempt (WA) recorded correctly.")

    # --- Scenario 2: Second Attempt (Accepted) ---
    sub2 = IncrementalSubmissionPayloadSchema(
        submission_id=10002,
        problem_id=100,
        title_slug="same-tree",
        submitted_at=datetime(2026, 2, 1, 10, 15, 0),
        result="Accepted",
        language="python3",
        runtime_ms=35,
        memory_kb=15200
    )
    service.process_incremental_submission(sub2)

    up2 = db.query(UserProblem).filter(UserProblem.problem_id == 100).first()
    assert up2.status == "Solved", f"Expected Solved, got {up2.status}"
    assert up2.num_submissions == 2
    assert up2.num_accepted == 1
    assert up2.last_result == "Accepted"
    assert up2.attempts_before_ac == 1, f"Expected 1 attempt before AC, got {up2.attempts_before_ac}"
    assert up2.first_accepted_at == datetime(2026, 2, 1, 10, 15, 0)
    print("[PASS] Scenario 2: Second attempt (AC) updated UserProblem state correctly.")

    # --- Scenario 3: Duplicate Submission Prevention ---
    service.process_incremental_submission(sub2)  # Re-sent duplicate
    sub_count = db.query(Submission).filter(Submission.submission_id == 10002).count()
    assert sub_count == 1, "Duplicate submission must not create extra records"
    print("[PASS] Scenario 3: Duplicate submission prevented.")

    # --- Scenario 4: SyncHistory Logging ---
    history = db.query(SyncHistory).filter(SyncHistory.sync_type == "INCREMENTAL").all()
    assert len(history) >= 2, "SyncHistory should log incremental sync events"
    print("[PASS] Scenario 4: SyncHistory logged incremental sync events.")

    db.close()
    print("\n[VERIFICATION COMPLETE] All Phase 6 features verified 100% successfully!")

if __name__ == "__main__":
    verify_phase_6_continuous_update()
