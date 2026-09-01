import sys
import os
import json
import sqlite3
sys.path.insert(0, os.path.dirname(__file__))

from app.database.connection import SessionLocal
from app.database.models import Topic, ProblemTopic
from app.services.sync_service import SyncService
from app.schemas.sync import ProblemSyncItemSchema, InitialSyncPayloadSchema

def test_stage_5_and_6_topics_and_mappings():
    print("=== STAGE 5 & 6: TOPIC STORAGE & PROBLEMTOPIC DEDUPLICATION TEST ===")
    
    raw_path = os.path.join(os.path.dirname(__file__), "debug", "raw", "problems")
    files = sorted([os.path.join(raw_path, f) for f in os.listdir(raw_path) if f.endswith(".json")])
    with open(files[-1], "r", encoding="utf-8") as f:
        raw_json = json.load(f)
    
    questions = raw_json["data"]["allQuestions"][:10]

    problem_items = []
    expected_topic_names = set()
    for q in questions:
        pid = int(q["questionFrontendId"] or q["questionId"])
        tags = [t["name"] for t in q.get("topicTags", [])]
        expected_topic_names.update(tags)
        
        problem_items.append(ProblemSyncItemSchema(
            problem_id=pid,
            frontend_id=str(q["questionFrontendId"] or q["questionId"]),
            title=q["title"],
            title_slug=q["titleSlug"],
            difficulty=q["difficulty"],
            acceptance_rate=None,
            total_submissions=None,
            total_accepted=None,
            is_paid=q["isPaidOnly"],
            problem_url=f"https://leetcode.com/problems/{q['titleSlug']}/",
            topics=tags
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
        topic_cnt1 = test_db.query(Topic).filter(Topic.name.in_(expected_topic_names)).count()
        pt_cnt1 = test_db.query(ProblemTopic).filter(ProblemTopic.problem_id.in_([p.problem_id for p in problem_items])).count()
        print(f"[FIRST RUN] Topics: {topic_cnt1} (Expected: {len(expected_topic_names)}), ProblemTopic Pairs: {pt_cnt1}")

        # Second Run (Idempotency Test)
        service.process_initial_sync(payload)
        topic_cnt2 = test_db.query(Topic).filter(Topic.name.in_(expected_topic_names)).count()
        pt_cnt2 = test_db.query(ProblemTopic).filter(ProblemTopic.problem_id.in_([p.problem_id for p in problem_items])).count()
        print(f"[SECOND RUN] Topics after duplicate sync: {topic_cnt2}, ProblemTopic Pairs: {pt_cnt2}")

        assert topic_cnt1 == topic_cnt2, f"Topic count mismatch after duplicate sync: {topic_cnt1} vs {topic_cnt2}"
        assert pt_cnt1 == pt_cnt2, f"ProblemTopic count mismatch after duplicate sync: {pt_cnt1} vs {pt_cnt2}"

        print("\nSTAGE 5 & 6 PASSED SUCCESSFULLY!")
    finally:
        test_db.close()

if __name__ == "__main__":
    test_stage_5_and_6_topics_and_mappings()
