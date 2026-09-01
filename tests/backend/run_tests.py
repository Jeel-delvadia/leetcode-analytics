import sys
import os
sys.path.insert(0, 'backend')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import Base, Problem, Submission, UserProblem
from app.services.sync_service import SyncService
from app.schemas.sync import IncrementalSubmissionPayloadSchema
from datetime import datetime

def run_all_tests():
    print("=== RUNNING DATA INTEGRITY TESTS ===")
    
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    p = Problem(
        problem_id=1, frontend_id="1", title="Two Sum", title_slug="two-sum",
        difficulty="Easy", acceptance_rate=50.0, total_submissions=100, total_accepted=50, is_paid=False
    )
    session.add(p)
    session.commit()

    service = SyncService(session)
    now = datetime.utcnow()

    # 1. First WA
    sub1 = IncrementalSubmissionPayloadSchema(
        submission_id=101, problem_id=1, title_slug="two-sum",
        submitted_at=now, result="Wrong Answer", language="cpp", runtime_ms=0, memory_kb=1000
    )
    service.process_incremental_submission(sub1)

    up1 = session.query(UserProblem).filter(UserProblem.problem_id == 1).first()
    assert up1.num_submissions == 1
    assert up1.num_accepted == 0
    assert up1.status == "Attempted"
    assert up1.attempts_before_ac is None
    print("[TEST 1 PASSED] WA submission recorded correctly.")

    # 2. Second WA
    sub2 = IncrementalSubmissionPayloadSchema(
        submission_id=102, problem_id=1, title_slug="two-sum",
        submitted_at=now, result="Wrong Answer", language="cpp", runtime_ms=0, memory_kb=1000
    )
    service.process_incremental_submission(sub2)

    # 3. Third TLE
    sub3 = IncrementalSubmissionPayloadSchema(
        submission_id=103, problem_id=1, title_slug="two-sum",
        submitted_at=now, result="Time Limit Exceeded", language="cpp", runtime_ms=2000, memory_kb=1000
    )
    service.process_incremental_submission(sub3)

    # 4. Fourth AC
    sub4 = IncrementalSubmissionPayloadSchema(
        submission_id=104, problem_id=1, title_slug="two-sum",
        submitted_at=now, result="Accepted", language="cpp", runtime_ms=10, memory_kb=1000
    )
    service.process_incremental_submission(sub4)

    up_final = session.query(UserProblem).filter(UserProblem.problem_id == 1).first()
    assert up_final.num_submissions == 4
    assert up_final.num_accepted == 1
    assert up_final.status == "Solved"
    assert up_final.attempts_before_ac == 4
    print("[TEST 2 PASSED] UserProblem derivation (WA, WA, TLE, AC -> Solved, attempts_before_ac=4) verified.")

    # 5. Test Idempotency
    service.process_incremental_submission(sub4)
    subs = session.query(Submission).filter(Submission.submission_id == 104).all()
    assert len(subs) == 1
    print("[TEST 3 PASSED] Incremental sync idempotency verified (zero duplicate submissions).")

    session.close()
    print("\nALL INTEGRITY TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_all_tests()
