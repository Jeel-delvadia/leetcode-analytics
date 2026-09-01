from sqlalchemy import (
    Column, Integer, BigInteger, String, Text, Decimal, Boolean, 
    DateTime, Enum, ForeignKey, CheckConstraint, func
)
from sqlalchemy.orm import relationship
from app.database.connection import Base
import enum

class DifficultyEnum(str, enum.Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

class UserProblemStatusEnum(str, enum.Enum):
    ATTEMPTED = "Attempted"
    SOLVED = "Solved"

class SyncTypeEnum(str, enum.Enum):
    INITIAL = "INITIAL"
    INCREMENTAL = "INCREMENTAL"
    RECONCILIATION = "RECONCILIATION"

class SyncStatusEnum(str, enum.Enum):
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class Problem(Base):
    __tablename__ = "Problem"

    problem_id = Column(Integer, primary_key=True, index=True)
    frontend_id = Column(String(20), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    title_slug = Column(String(255), unique=True, nullable=False, index=True)
    difficulty = Column(Enum('Easy', 'Medium', 'Hard', name='difficulty_enum'), nullable=False)
    acceptance_rate = Column(Decimal(6, 3))
    total_submissions = Column(BigInteger)
    total_accepted = Column(BigInteger)
    is_paid = Column(Boolean, default=False)
    problem_url = Column(String(500))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    topics = relationship("ProblemTopic", back_populates="problem", cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="problem", cascade="all, delete-orphan")
    user_problem = relationship("UserProblem", back_populates="problem", uselist=False, cascade="all, delete-orphan")


class Topic(Base):
    __tablename__ = "Topic"

    topic_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)

    problems = relationship("ProblemTopic", back_populates="topic", cascade="all, delete-orphan")


class ProblemTopic(Base):
    __tablename__ = "ProblemTopic"

    problem_id = Column(Integer, ForeignKey("Problem.problem_id", ondelete="CASCADE"), primary_key=True)
    topic_id = Column(Integer, ForeignKey("Topic.topic_id", ondelete="CASCADE"), primary_key=True)

    problem = relationship("Problem", back_populates="topics")
    topic = relationship("Topic", back_populates="problems")


class Submission(Base):
    __tablename__ = "Submission"

    submission_id = Column(BigInteger, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("Problem.problem_id", ondelete="CASCADE"), nullable=False, index=True)
    submitted_at = Column(DateTime, nullable=False, index=True)
    result = Column(String(50), nullable=False)
    language = Column(String(50))
    runtime_ms = Column(Integer)
    memory_kb = Column(Integer)

    problem = relationship("Problem", back_populates="submissions")


class UserProblem(Base):
    __tablename__ = "UserProblem"

    problem_id = Column(Integer, ForeignKey("Problem.problem_id", ondelete="CASCADE"), primary_key=True)
    status = Column(Enum('Attempted', 'Solved', name='user_problem_status_enum'), nullable=False)
    num_submissions = Column(Integer, default=0)
    num_accepted = Column(Integer, default=0)
    first_submitted_at = Column(DateTime)
    last_submitted_at = Column(DateTime)
    first_accepted_at = Column(DateTime)
    last_accepted_at = Column(DateTime)
    last_result = Column(String(50))
    attempts_before_ac = Column(Integer)

    problem = relationship("Problem", back_populates="user_problem")


class ProblemSimilarity(Base):
    __tablename__ = "ProblemSimilarity"

    problem_id = Column(Integer, ForeignKey("Problem.problem_id", ondelete="CASCADE"), primary_key=True)
    similar_problem_id = Column(Integer, ForeignKey("Problem.problem_id", ondelete="CASCADE"), primary_key=True)
    similarity_score = Column(Decimal(6, 5))
    source = Column(String(50))

    __table_args__ = (
        CheckConstraint("problem_id <> similar_problem_id", name="check_different_similar_problems"),
    )


class TopicPrerequisite(Base):
    __tablename__ = "TopicPrerequisite"

    topic_id = Column(Integer, ForeignKey("Topic.topic_id", ondelete="CASCADE"), primary_key=True)
    prerequisite_topic_id = Column(Integer, ForeignKey("Topic.topic_id", ondelete="CASCADE"), primary_key=True)
    prerequisite_strength = Column(Decimal(5, 2))

    __table_args__ = (
        CheckConstraint("topic_id <> prerequisite_topic_id", name="check_different_prerequisite_topics"),
    )


class Contest(Base):
    __tablename__ = "Contest"

    contest_id = Column(Integer, primary_key=True, index=True)
    contest_name = Column(String(255), nullable=False)
    contest_slug = Column(String(255), unique=True, index=True)
    contest_date = Column(DateTime)
    contest_type = Column(String(50))

    participation = relationship("ContestParticipation", back_populates="contest", uselist=False, cascade="all, delete-orphan")


class ContestParticipation(Base):
    __tablename__ = "ContestParticipation"

    contest_id = Column(Integer, ForeignKey("Contest.contest_id", ondelete="CASCADE"), primary_key=True)
    attended = Column(Boolean, default=True)
    rank = Column(Integer)
    score = Column(Decimal(8, 2))
    rating_before = Column(Decimal(8, 2))
    rating_after = Column(Decimal(8, 2))
    rating_change = Column(Decimal(8, 2))
    problems_attempted = Column(Integer)
    problems_solved = Column(Integer)

    contest = relationship("Contest", back_populates="participation")


class SyncHistory(Base):
    __tablename__ = "SyncHistory"

    sync_id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    sync_type = Column(Enum('INITIAL', 'INCREMENTAL', 'RECONCILIATION', name='sync_type_enum'), nullable=False)
    started_at = Column(DateTime, nullable=False, server_default=func.now())
    completed_at = Column(DateTime)
    records_fetched = Column(Integer, default=0)
    status = Column(Enum('RUNNING', 'SUCCESS', 'FAILED', name='sync_status_enum'), nullable=False)
    error_message = Column(Text)
