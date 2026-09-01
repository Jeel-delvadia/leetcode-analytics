from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Data Analytics"])

@router.get("/overall")
def get_overall_analytics(db: Session = Depends(get_db)):
    service = AnalyticsService(db)
    return service.get_overall_progress()

@router.get("/problems/{problem_id}")
def get_problem_analytics(problem_id: int, db: Session = Depends(get_db)):
    service = AnalyticsService(db)
    res = service.get_problem_analytics(problem_id)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Problem ID {problem_id} not found"
        )
    return res

@router.get("/topics")
def get_topic_analytics(db: Session = Depends(get_db)):
    service = AnalyticsService(db)
    return service.get_topic_analytics()

@router.get("/difficulty")
def get_difficulty_analytics(db: Session = Depends(get_db)):
    service = AnalyticsService(db)
    return service.get_difficulty_analytics()

@router.get("/db/tables")
def get_all_tables_summary(db: Session = Depends(get_db)):
    """
    Returns all 10 DB design tables and their current row counts.
    """
    service = AnalyticsService(db)
    return service.get_all_tables_summary()

@router.get("/db/tables/{table_name}")
def get_table_records(table_name: str, skip: int = 0, limit: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Returns rows from DB table till end (or with optional skip/limit pagination).
    """
    service = AnalyticsService(db)
    res = service.get_table_records(table_name, skip=skip, limit=limit)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Table '{table_name}' does not exist in DB design"
        )
    return res
