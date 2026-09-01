-- Indexes for Optimizing Analytical Queries

-- Problem Indexes
CREATE INDEX idx_problem_difficulty ON Problem(difficulty);
CREATE INDEX idx_problem_title_slug ON Problem(title_slug);
CREATE INDEX idx_problem_frontend_id ON Problem(frontend_id);

-- Topic Indexes
CREATE INDEX idx_topic_name ON Topic(name);

-- Submission Indexes
CREATE INDEX idx_submission_submitted_at ON Submission(submitted_at);
CREATE INDEX idx_submission_problem_id ON Submission(problem_id);
CREATE INDEX idx_submission_result ON Submission(result);
CREATE INDEX idx_submission_problem_result ON Submission(problem_id, result);

-- UserProblem Indexes
CREATE INDEX idx_userproblem_status ON UserProblem(status);

-- Contest Indexes
CREATE INDEX idx_contest_date ON Contest(contest_date);
CREATE INDEX idx_contest_slug ON Contest(contest_slug);

-- Sync History Index
CREATE INDEX idx_synchistory_started_at ON SyncHistory(started_at);
CREATE INDEX idx_synchistory_status ON SyncHistory(status);
