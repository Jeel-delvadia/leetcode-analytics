from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime

class TopicItemSchema(BaseModel):
    topic_id: Optional[int] = None
    name: str
    description: Optional[str] = None

class ProblemSyncItemSchema(BaseModel):
    problem_id: int
    frontend_id: str
    title: str
    title_slug: str
    difficulty: str
    acceptance_rate: Optional[float] = None
    total_submissions: Optional[int] = None
    total_accepted: Optional[int] = None
    is_paid: bool = False
    problem_url: Optional[str] = None
    topics: List[str] = []
    similar_question_slugs: List[str] = []

class SubmissionSyncItemSchema(BaseModel):
    submission_id: int
    problem_id: int
    submitted_at: datetime
    result: str
    language: Optional[str] = None
    runtime_ms: Optional[int] = None
    memory_kb: Optional[int] = None

class ContestParticipationSyncSchema(BaseModel):
    contest_id: int
    contest_name: str
    contest_slug: Optional[str] = None
    contest_date: Optional[datetime] = None
    contest_type: Optional[str] = None
    attended: bool = True
    rank: Optional[int] = None
    score: Optional[float] = None
    rating_before: Optional[float] = None
    rating_after: Optional[float] = None
    rating_change: Optional[float] = None
    problems_attempted: Optional[int] = None
    problems_solved: Optional[int] = None

class InitialSyncPayloadSchema(BaseModel):
    sync_type: str = "INITIAL"
    problems: List[ProblemSyncItemSchema] = []
    submissions: List[SubmissionSyncItemSchema] = []
    contests: List[ContestParticipationSyncSchema] = []
    raw_problems_response: Optional[Dict[str, Any]] = None
    raw_submissions_response: Optional[Dict[str, Any]] = None

class IncrementalSubmissionPayloadSchema(BaseModel):
    submission_id: int
    problem_id: int
    title_slug: str
    submitted_at: datetime
    result: str
    language: Optional[str] = None
    runtime_ms: Optional[int] = None
    memory_kb: Optional[int] = None

class SyncStatusResponseSchema(BaseModel):
    last_sync_id: Optional[int] = None
    last_sync_type: Optional[str] = None
    last_sync_time: Optional[datetime] = None
    records_fetched: int = 0
    status: str
    error_message: Optional[str] = None
