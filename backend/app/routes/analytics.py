from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Data Analytics"])

@router.get("/overall")
def get_overall_analytics(db: Session = Depends(get_db)):
    """
    Returns overall user solving progress, total solved, and AC rate.
    """
    service = AnalyticsService(db)
    return service.get_overall_progress()

@router.get("/problems/{problem_id}")
def get_problem_analytics(problem_id: int, db: Session = Depends(get_db)):
    """
    Returns granular problem submission performance (attempts, AC, WA, TLE, time to AC).
    """
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
    """
    Returns topic mastery scores, AC/WA/TLE rates, and solving percentages per topic.
    """
    service = AnalyticsService(db)
    return service.get_topic_analytics()

@router.get("/difficulty")
def get_difficulty_analytics(db: Session = Depends(get_db)):
    """
    Returns difficulty level breakdown (Easy, Medium, Hard success rates & average attempts).
    """
    service = AnalyticsService(db)
    return service.get_difficulty_analytics()
