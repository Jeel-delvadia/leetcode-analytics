from sqlalchemy.orm import Session
from sqlalchemy import func, text
from app.database.models import (
    Problem, Topic, ProblemTopic, Submission, UserProblem, 
    ProblemSimilarity, TopicPrerequisite, Contest, ContestParticipation, SyncHistory
)
from datetime import datetime, timezone

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_overall_progress(self):
        total_problems = self.db.query(Problem).count()
        solved_count = self.db.query(UserProblem).filter(UserProblem.status == "Solved").count()
        attempted_count = self.db.query(UserProblem).filter(UserProblem.status == "Attempted").count()
        total_submissions = self.db.query(Submission).count()
        ac_submissions = self.db.query(Submission).filter(Submission.result == "Accepted").count()

        easy_solved = self.db.query(UserProblem).join(Problem).filter(
            UserProblem.status == "Solved", Problem.difficulty == "Easy"
        ).count()
        medium_solved = self.db.query(UserProblem).join(Problem).filter(
            UserProblem.status == "Solved", Problem.difficulty == "Medium"
        ).count()
        hard_solved = self.db.query(UserProblem).join(Problem).filter(
            UserProblem.status == "Solved", Problem.difficulty == "Hard"
        ).count()

        ac_rate = round((ac_submissions / total_submissions * 100), 2) if total_submissions > 0 else 0.0

        return {
            "total_problems": total_problems,
            "solved_count": solved_count,
            "attempted_count": attempted_count,
            "total_submissions": total_submissions,
            "overall_ac_rate": ac_rate,
            "difficulty_breakdown": {
                "easy": easy_solved,
                "medium": medium_solved,
                "hard": hard_solved
            }
        }

    def get_problem_analytics(self, problem_id: int):
        user_prob = self.db.query(UserProblem).filter(UserProblem.problem_id == problem_id).first()
        prob = self.db.query(Problem).filter(Problem.problem_id == problem_id).first()

        if not prob:
            return None

        submissions = self.db.query(Submission).filter(Submission.problem_id == problem_id).all()
        wa_count = sum(1 for s in submissions if s.result == "Wrong Answer")
        tle_count = sum(1 for s in submissions if s.result == "Time Limit Exceeded")
        mle_count = sum(1 for s in submissions if s.result == "Memory Limit Exceeded")

        first_ac = user_prob.first_accepted_at if user_prob else None
        first_sub = user_prob.first_submitted_at if user_prob else None
        time_to_ac_minutes = None

        if first_sub and first_ac:
            delta = first_ac - first_sub
            time_to_ac_minutes = round(delta.total_seconds() / 60, 2)

        return {
            "problem_id": prob.problem_id,
            "title": prob.title,
            "difficulty": prob.difficulty,
            "status": user_prob.status if user_prob else "Unsolved",
            "attempts": user_prob.num_submissions if user_prob else 0,
            "ac_count": user_prob.num_accepted if user_prob else 0,
            "wa_count": wa_count,
            "tle_count": tle_count,
            "mle_count": mle_count,
            "attempts_before_ac": user_prob.attempts_before_ac if user_prob else None,
            "first_attempt_ac": (user_prob.attempts_before_ac == 0) if (user_prob and user_prob.status == "Solved") else False,
            "time_to_ac_minutes": time_to_ac_minutes,
            "last_result": user_prob.last_result if user_prob else None
        }

    def get_topic_analytics(self):
        topics = self.db.query(Topic).all()
        results = []

        for topic in topics:
            problem_ids = [pt.problem_id for pt in self.db.query(ProblemTopic).filter(ProblemTopic.topic_id == topic.topic_id).all()]
            total_topic_problems = len(problem_ids)

            if total_topic_problems == 0:
                continue

            solved_count = self.db.query(UserProblem).filter(
                UserProblem.problem_id.in_(problem_ids),
                UserProblem.status == "Solved"
            ).count()

            attempted_count = self.db.query(UserProblem).filter(
                UserProblem.problem_id.in_(problem_ids),
                UserProblem.status == "Attempted"
            ).count()

            topic_submissions = self.db.query(Submission).filter(Submission.problem_id.in_(problem_ids)).all()
            total_subs = len(topic_submissions)
            wa_subs = sum(1 for s in topic_submissions if s.result == "Wrong Answer")
            tle_subs = sum(1 for s in topic_submissions if s.result == "Time Limit Exceeded")

            ac_rate = round((sum(1 for s in topic_submissions if s.result == "Accepted") / total_subs * 100), 2) if total_subs > 0 else 0.0
            solving_percentage = round((solved_count / total_topic_problems * 100), 2) if total_topic_problems > 0 else 0.0
            mastery_score = round(solving_percentage * 0.7 + ac_rate * 0.3, 2)

            results.append({
                "topic_id": topic.topic_id,
                "topic_name": topic.name,
                "total_problems": total_topic_problems,
                "solved_count": solved_count,
                "attempted_count": attempted_count,
                "solving_percentage": solving_percentage,
                "ac_rate": ac_rate,
                "wa_rate": round((wa_subs / total_subs * 100), 2) if total_subs > 0 else 0.0,
                "tle_rate": round((tle_subs / total_subs * 100), 2) if total_subs > 0 else 0.0,
                "mastery_score": mastery_score
            })

        return results

    def get_difficulty_analytics(self):
        difficulties = ["Easy", "Medium", "Hard"]
        stats = {}

        for diff in difficulties:
            problems = self.db.query(Problem).filter(Problem.difficulty == diff).all()
            prob_ids = [p.problem_id for p in problems]
            total = len(prob_ids)

            if total == 0:
                stats[diff.lower()] = {
                    "total": 0, "solved": 0, "success_rate": 0.0, "avg_attempts": 0.0
                }
                continue

            solved = self.db.query(UserProblem).filter(
                UserProblem.problem_id.in_(prob_ids),
                UserProblem.status == "Solved"
            ).count()

            user_probs = self.db.query(UserProblem).filter(UserProblem.problem_id.in_(prob_ids)).all()
            total_attempts = sum(up.num_submissions for up in user_probs)
            avg_attempts = round(total_attempts / len(user_probs), 2) if user_probs else 0.0
            success_rate = round((solved / total * 100), 2) if total > 0 else 0.0

            stats[diff.lower()] = {
                "total": total,
                "solved": solved,
                "success_rate": success_rate,
                "avg_attempts": avg_attempts
            }

        return stats

    def get_all_tables_summary(self):
        tables = [
            ("Problem", self.db.query(Problem).count()),
            ("Topic", self.db.query(Topic).count()),
            ("ProblemTopic", self.db.query(ProblemTopic).count()),
            ("Submission", self.db.query(Submission).count()),
            ("UserProblem", self.db.query(UserProblem).count()),
            ("ProblemSimilarity", self.db.query(ProblemSimilarity).count()),
            ("TopicPrerequisite", self.db.query(TopicPrerequisite).count()),
            ("Contest", self.db.query(Contest).count()),
            ("ContestParticipation", self.db.query(ContestParticipation).count()),
            ("SyncHistory", self.db.query(SyncHistory).count())
        ]
        return [{"table_name": t[0], "row_count": t[1]} for t in tables]

    def get_table_records(self, table_name: str, limit: int = 50):
        model_map = {
            "Problem": Problem,
            "Topic": Topic,
            "ProblemTopic": ProblemTopic,
            "Submission": Submission,
            "UserProblem": UserProblem,
            "ProblemSimilarity": ProblemSimilarity,
            "TopicPrerequisite": TopicPrerequisite,
            "Contest": Contest,
            "ContestParticipation": ContestParticipation,
            "SyncHistory": SyncHistory
        }

        model = model_map.get(table_name)
        if not model:
            return None

        # Order by primary key desc for Submission, SyncHistory, etc.
        query = self.db.query(model)
        if table_name == "Submission":
            query = query.order_by(Submission.submission_id.desc())
        elif table_name == "SyncHistory":
            query = query.order_by(SyncHistory.sync_id.desc())

        rows = query.limit(limit).all()
        result = []
        for r in rows:
            dict_row = {}
            for col in r.__table__.columns:
                val = getattr(r, col.name)
                if isinstance(val, datetime):
                    val = val.isoformat()
                dict_row[col.name] = val
            result.append(dict_row)
        return result
