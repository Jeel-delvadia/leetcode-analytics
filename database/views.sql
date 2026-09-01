-- Analytical Views

-- 1. View for Problem Topic Aggregations
CREATE OR REPLACE VIEW vw_problem_details AS
SELECT 
    p.problem_id,
    p.frontend_id,
    p.title,
    p.difficulty,
    p.acceptance_rate,
    GROUP_CONCAT(t.name ORDER BY t.name SEPARATOR ', ') AS topics
FROM Problem p
LEFT JOIN ProblemTopic pt ON p.problem_id = pt.problem_id
LEFT JOIN Topic t ON pt.topic_id = t.topic_id
GROUP BY p.problem_id, p.frontend_id, p.title, p.difficulty, p.acceptance_rate;

-- 2. View for User Difficulty Summary
CREATE OR REPLACE VIEW vw_user_difficulty_stats AS
SELECT 
    p.difficulty,
    COUNT(up.problem_id) AS attempted_count,
    SUM(CASE WHEN up.status = 'Solved' THEN 1 ELSE 0 END) AS solved_count,
    AVG(up.num_submissions) AS avg_attempts
FROM Problem p
JOIN UserProblem up ON p.problem_id = up.problem_id
GROUP BY p.difficulty;

-- 3. View for User Topic Performance
CREATE OR REPLACE VIEW vw_user_topic_stats AS
SELECT 
    t.topic_id,
    t.name AS topic_name,
    COUNT(DISTINCT pt.problem_id) AS total_problems,
    COUNT(DISTINCT CASE WHEN up.status = 'Solved' THEN up.problem_id END) AS solved_problems,
    COUNT(DISTINCT CASE WHEN up.status = 'Attempted' THEN up.problem_id END) AS attempted_problems
FROM Topic t
JOIN ProblemTopic pt ON t.topic_id = pt.topic_id
LEFT JOIN UserProblem up ON pt.problem_id = up.problem_id
GROUP BY t.topic_id, t.name;
