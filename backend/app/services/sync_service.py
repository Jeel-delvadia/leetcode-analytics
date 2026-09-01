from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.models import (
    Problem, Topic, ProblemTopic, Submission, UserProblem, 
    Contest, ContestParticipation, SyncHistory, SyncTypeEnum, SyncStatusEnum
)
from app.schemas.sync import (
    InitialSyncPayloadSchema, IncrementalSubmissionPayloadSchema, ProblemSyncItemSchema
)
from datetime import datetime

class SyncService:
    def __init__(self, db: Session):
        self.db = db

    def process_initial_sync(self, payload: InitialSyncPayloadSchema) -> SyncHistory:
        sync_record = SyncHistory(
            sync_type=SyncTypeEnum.INITIAL,
            started_at=datetime.utcnow(),
            status=SyncStatusEnum.RUNNING
        )
        self.db.add(sync_record)
        self.db.commit()
        self.db.refresh(sync_record)

        total_records = 0
        try:
            # 1. Process Problems & Topics
            for prob_data in payload.problems:
                self._upsert_problem_and_topics(prob_data)
                total_records += 1

            # 2. Process Submissions
            for sub_data in payload.submissions:
                self._upsert_submission(sub_data)
                total_records += 1

            # 3. Process Contests
            for contest_data in payload.contests:
                self._upsert_contest_and_participation(contest_data)
                total_records += 1

            sync_record.records_fetched = total_records
            sync_record.completed_at = datetime.utcnow()
            sync_record.status = SyncStatusEnum.SUCCESS
            self.db.commit()
            return sync_record
        except Exception as e:
            self.db.rollback()
            sync_record.status = SyncStatusEnum.FAILED
            sync_record.error_message = str(e)
            sync_record.completed_at = datetime.utcnow()
            self.db.commit()
            raise e

    def process_incremental_submission(self, payload: IncrementalSubmissionPayloadSchema) -> Submission:
        # 1. Insert or ignore submission
        existing_sub = self.db.query(Submission).filter(
            Submission.submission_id == payload.submission_id
        ).first()

        if existing_sub:
            return existing_sub

        new_sub = Submission(
            submission_id=payload.submission_id,
            problem_id=payload.problem_id,
            submitted_at=payload.submitted_at,
            result=payload.result,
            language=payload.language,
            runtime_ms=payload.runtime_ms,
            memory_kb=payload.memory_kb
        )
        self.db.add(new_sub)

        # 2. Update UserProblem state
        user_prob = self.db.query(UserProblem).filter(
            UserProblem.problem_id == payload.problem_id
        ).first()

        is_ac = (payload.result.lower() == "accepted")

        if not user_prob:
            user_prob = UserProblem(
                problem_id=payload.problem_id,
                status="Solved" if is_ac else "Attempted",
                num_submissions=1,
                num_accepted=1 if is_ac else 0,
                first_submitted_at=payload.submitted_at,
                last_submitted_at=payload.submitted_at,
                first_accepted_at=payload.submitted_at if is_ac else None,
                last_accepted_at=payload.submitted_at if is_ac else None,
                last_result=payload.result,
                attempts_before_ac=0 if is_ac else None
            )
            self.db.add(user_prob)
        else:
            user_prob.num_submissions += 1
            user_prob.last_submitted_at = payload.submitted_at
            user_prob.last_result = payload.result

            if is_ac:
                if user_prob.status != "Solved":
                    user_prob.attempts_before_ac = user_prob.num_submissions - 1
                    user_prob.first_accepted_at = payload.submitted_at
                    user_prob.status = "Solved"
                user_prob.num_accepted += 1
                user_prob.last_accepted_at = payload.submitted_at

        # Log Sync History
        sync_log = SyncHistory(
            sync_type=SyncTypeEnum.INCREMENTAL,
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow(),
            records_fetched=1,
            status=SyncStatusEnum.SUCCESS
        )
        self.db.add(sync_log)
        self.db.commit()
        return new_sub

    def _upsert_problem_and_topics(self, data: ProblemSyncItemSchema):
        prob = self.db.query(Problem).filter(Problem.problem_id == data.problem_id).first()
        if not prob:
            prob = Problem(
                problem_id=data.problem_id,
                frontend_id=data.frontend_id,
                title=data.title,
                title_slug=data.title_slug,
                difficulty=data.difficulty,
                acceptance_rate=data.acceptance_rate,
                total_submissions=data.total_submissions,
                total_accepted=data.total_accepted,
                is_paid=data.is_paid,
                problem_url=data.problem_url or f"https://leetcode.com/problems/{data.title_slug}/"
            )
            self.db.add(prob)
        else:
            prob.acceptance_rate = data.acceptance_rate
            prob.total_submissions = data.total_submissions
            prob.total_accepted = data.total_accepted

        # Upsert Topics
        for topic_name in data.topics:
            topic = self.db.query(Topic).filter(Topic.name == topic_name).first()
            if not topic:
                topic = Topic(name=topic_name)
                self.db.add(topic)
                self.db.flush()

            # ProblemTopic relation
            pt = self.db.query(ProblemTopic).filter(
                ProblemTopic.problem_id == data.problem_id,
                ProblemTopic.topic_id == topic.topic_id
            ).first()
            if not pt:
                pt = ProblemTopic(problem_id=data.problem_id, topic_id=topic.topic_id)
                self.db.add(pt)

    def _upsert_submission(self, data):
        sub = self.db.query(Submission).filter(Submission.submission_id == data.submission_id).first()
        if not sub:
            sub = Submission(
                submission_id=data.submission_id,
                problem_id=data.problem_id,
                submitted_at=data.submitted_at,
                result=data.result,
                language=data.language,
                runtime_ms=data.runtime_ms,
                memory_kb=data.memory_kb
            )
            self.db.add(sub)

    def _upsert_contest_and_participation(self, data):
        contest = self.db.query(Contest).filter(Contest.contest_id == data.contest_id).first()
        if not contest:
            contest = Contest(
                contest_id=data.contest_id,
                contest_name=data.contest_name,
                contest_slug=data.contest_slug,
                contest_date=data.contest_date,
                contest_type=data.contest_type
            )
            self.db.add(contest)
            self.db.flush()

        part = self.db.query(ContestParticipation).filter(ContestParticipation.contest_id == data.contest_id).first()
        if not part:
            part = ContestParticipation(
                contest_id=data.contest_id,
                attended=data.attended,
                rank=data.rank,
                score=data.score,
                rating_before=data.rating_before,
                rating_after=data.rating_after,
                rating_change=data.rating_change,
                problems_attempted=data.problems_attempted,
                problems_solved=data.problems_solved
            )
            self.db.add(part)
