from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.sync import (
    InitialSyncPayloadSchema, IncrementalSubmissionPayloadSchema, SyncStatusResponseSchema
)
from app.services.sync_service import SyncService
from app.database.models import SyncHistory

router = APIRouter(prefix="/sync", tags=["Synchronization"])

@router.post("/initial", status_code=status.HTTP_201_CREATED)
def initial_sync(payload: InitialSyncPayloadSchema, db: Session = Depends(get_db)):
    """
    Ingests full dataset from Chrome extension during initial sync.
    Saves raw LeetCode GraphQL responses to debug/raw/ directory.
    """
    service = SyncService(db)
    try:
        record = service.process_initial_sync(
            payload,
            raw_problems=payload.raw_problems_response,
            raw_submissions=payload.raw_submissions_response
        )
        return {
            "status": "success",
            "sync_id": record.sync_id,
            "records_fetched": record.records_fetched
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Initial synchronization failed: {str(e)}"
        )

@router.post("/submission", status_code=status.HTTP_201_CREATED)
def incremental_submission_sync(payload: IncrementalSubmissionPayloadSchema, db: Session = Depends(get_db)):
    """
    Receives new submission data from Chrome extension content script.
    """
    service = SyncService(db)
    try:
        sub = service.process_incremental_submission(payload)
        return {
            "status": "success",
            "submission_id": sub.submission_id,
            "result": sub.result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Incremental sync failed: {str(e)}"
        )

@router.get("/status", response_model=SyncStatusResponseSchema)
def get_latest_sync_status(db: Session = Depends(get_db)):
    """
    Returns latest synchronization status.
    """
    latest = db.query(SyncHistory).order_by(SyncHistory.sync_id.desc()).first()
    if not latest:
        return SyncStatusResponseSchema(
            status="IDLE",
            records_fetched=0
        )
    return SyncStatusResponseSchema(
        last_sync_id=latest.sync_id,
        last_sync_type=latest.sync_type,
        last_sync_time=latest.completed_at or latest.started_at,
        records_fetched=latest.records_fetched,
        status=latest.status,
        error_message=latest.error_message
    )
