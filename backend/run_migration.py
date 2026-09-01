import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database.connection import SessionLocal
from app.services.sync_service import SyncService

def run_migration():
    print("[MIGRATION] Recalculating UserProblem summary records from Submission table...")
    db = SessionLocal()
    try:
        service = SyncService(db)
        service.recalculate_all_user_problems()
        print("[MIGRATION SUCCESS] All UserProblem summary records synced and derived accurately!")
    except Exception as e:
        db.rollback()
        print(f"[MIGRATION ERROR] {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_migration()
