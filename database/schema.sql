-- LeetCode Personal Analytics & Prediction System - Database Schema

CREATE TABLE IF NOT EXISTS Problem (
    problem_id INT PRIMARY KEY,
    frontend_id VARCHAR(20) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    title_slug VARCHAR(255) UNIQUE NOT NULL,

    difficulty ENUM('Easy', 'Medium', 'Hard') NOT NULL,

    acceptance_rate DECIMAL(6,3),
    total_submissions BIGINT,
    total_accepted BIGINT,

    is_paid BOOLEAN DEFAULT FALSE,

    problem_url VARCHAR(500),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Topic (
    topic_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS ProblemTopic (
    problem_id INT NOT NULL,
    topic_id INT NOT NULL,

    PRIMARY KEY (problem_id, topic_id),

    FOREIGN KEY (problem_id)
        REFERENCES Problem(problem_id)
        ON DELETE CASCADE,

    FOREIGN KEY (topic_id)
        REFERENCES Topic(topic_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Submission (
    submission_id BIGINT PRIMARY KEY,

    problem_id INT NOT NULL,

    submitted_at DATETIME NOT NULL,

    result VARCHAR(50) NOT NULL,

    language VARCHAR(50),

    runtime_ms INT,
    memory_kb INT,

    FOREIGN KEY (problem_id)
        REFERENCES Problem(problem_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS UserProblem (
    problem_id INT PRIMARY KEY,

    status ENUM('Attempted', 'Solved') NOT NULL,

    num_submissions INT DEFAULT 0,
    num_accepted INT DEFAULT 0,

    first_submitted_at DATETIME,
    last_submitted_at DATETIME,

    first_accepted_at DATETIME,
    last_accepted_at DATETIME,

    last_result VARCHAR(50),

    attempts_before_ac INT,

    FOREIGN KEY (problem_id)
        REFERENCES Problem(problem_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ProblemSimilarity (
    problem_id INT NOT NULL,
    similar_problem_id INT NOT NULL,

    similarity_score DECIMAL(6,5),

    source VARCHAR(50),

    PRIMARY KEY (problem_id, similar_problem_id),

    FOREIGN KEY (problem_id)
        REFERENCES Problem(problem_id)
        ON DELETE CASCADE,

    FOREIGN KEY (similar_problem_id)
        REFERENCES Problem(problem_id)
        ON DELETE CASCADE,

    CHECK (problem_id <> similar_problem_id)
);

CREATE TABLE IF NOT EXISTS TopicPrerequisite (
    topic_id INT NOT NULL,
    prerequisite_topic_id INT NOT NULL,

    prerequisite_strength DECIMAL(5,2),

    PRIMARY KEY (topic_id, prerequisite_topic_id),

    FOREIGN KEY (topic_id)
        REFERENCES Topic(topic_id)
        ON DELETE CASCADE,

    FOREIGN KEY (prerequisite_topic_id)
        REFERENCES Topic(topic_id)
        ON DELETE CASCADE,

    CHECK (topic_id <> prerequisite_topic_id)
);

CREATE TABLE IF NOT EXISTS Contest (
    contest_id INT PRIMARY KEY,

    contest_name VARCHAR(255) NOT NULL,
    contest_slug VARCHAR(255) UNIQUE,

    contest_date DATETIME,

    contest_type VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS ContestParticipation (
    contest_id INT PRIMARY KEY,

    attended BOOLEAN DEFAULT TRUE,

    rank INT,
    score DECIMAL(8,2),

    rating_before DECIMAL(8,2),
    rating_after DECIMAL(8,2),
    rating_change DECIMAL(8,2),

    problems_attempted INT,
    problems_solved INT,

    FOREIGN KEY (contest_id)
        REFERENCES Contest(contest_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS SyncHistory (
    sync_id BIGINT AUTO_INCREMENT PRIMARY KEY,

    sync_type ENUM(
        'INITIAL',
        'INCREMENTAL',
        'RECONCILIATION'
    ) NOT NULL,

    started_at DATETIME NOT NULL,
    completed_at DATETIME,

    records_fetched INT DEFAULT 0,

    status ENUM(
        'RUNNING',
        'SUCCESS',
        'FAILED'
    ) NOT NULL,

    error_message TEXT
);
