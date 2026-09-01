import sys
import os
import json
import sqlite3
sys.path.insert(0, os.path.dirname(__file__))

from app.database.connection import engine, Base, SessionLocal
from app.database.models import Problem
from app.services.sync_service import SyncService
from app.schemas.sync import ProblemSyncItemSchema, InitialSyncPayloadSchema

def test_stage_3_and_4_problem_storage():
    print("=== STAGE 3 & 4: PROBLEM STORAGE & DEDUPLICATION TEST ===")
    
    # 1. Read raw sample response
    raw_path = os.path.join(os.path.dirname(__file__), "debug", "raw", "problems")
    files = sorted([os.path.join(raw_path, f) for f in os.listdir(raw_path) if f.endswith(".json")])
    if not files:
        raise RuntimeError("No raw problems JSON file found!")
    
    with open(files[-1], "r", encoding="utf-8") as f:
        raw_json = json.load(f)
    
    questions = raw_json["data"]["allQuestions"][:10]  # Take 10 sample problems
    print(f"[TEST] Using sample of {len(questions)} real LeetCode questions from raw JSON.")

    problem_items = []
    for q in questions:
        pid = int(q["questionFrontendId"] or q["questionId"])
        problem_items.append(ProblemSyncItemSchema(
            problem_id=pid,
            frontend_id=str(q["questionFrontendId"] or q["questionId"]),
            title=q["title"],
            title_slug=q["titleSlug"],
            difficulty=q["difficulty"],
            acceptance_rate=None, # Strictly null
            total_submissions=None,
            total_accepted=None,
            is_paid=q["isPaidOnly"],
            problem_url=f"https://leetcode.com/problems/{q['titleSlug']}/",
            topics=[t["name"] for t in q.get("topicTags", [])]
        ))

    payload = InitialSyncPayloadSchema(
        sync_type="INITIAL",
        problems=problem_items,
        submissions=[],
        contests=[]
    )

    test_db = SessionLocal()
    try:
        service = SyncService(test_db)
        
        # First Run
        service.process_initial_sync(payload)
        cnt1 = test_db.query(Problem).filter(Problem.problem_id.in_([p.problem_id for p in problem_items])).count()
        print(f"[FIRST RUN] Database Problem Records: {cnt1} (Expected: 10)")
        assert cnt1 == 10, f"Expected 10 records, got {cnt1}"

        # Second Run (Idempotency Test)
        service.process_initial_sync(payload)
        cnt2 = test_db.query(Problem).filter(Problem.problem_id.in_([p.problem_id for p in problem_items])).count()
        print(f"[SECOND RUN] Database Problem Records after duplicate sync: {cnt2} (Expected: 10)")
        assert cnt2 == 10, f"Idempotency failed! Expected 10 records, got {cnt2}"

        print("\nSTAGE 3 & 4 PASSED SUCCESSFULLY!")
    finally:
        test_db.close()

if __name__ == "__main__":
    test_stage_3_and_4_problem_storage()
