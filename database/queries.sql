-- Verification & Analytical Queries for Database Validation

-- Query 1: Count solved problems overall and by difficulty
SELECT 
    p.difficulty,
    COUNT(up.problem_id) AS total_attempted,
    SUM(CASE WHEN up.status = 'Solved' THEN 1 ELSE 0 END) AS total_solved
FROM Problem p
JOIN UserProblem up ON p.problem_id = up.problem_id
GROUP BY p.difficulty;

-- Query 2: Calculate overall submission statistics (AC, WA, TLE counts and rates)
SELECT 
    result,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Submission), 2) AS percentage
FROM Submission
GROUP BY result;

-- Query 3: Find attempted but unsolved problems
SELECT 
    p.problem_id,
    p.frontend_id,
    p.title,
    p.difficulty,
    up.num_submissions,
    up.last_result,
    up.last_submitted_at
FROM Problem p
JOIN UserProblem up ON p.problem_id = up.problem_id
WHERE up.status = 'Attempted';

-- Query 4: Calculate average attempts before achieving AC
SELECT 
    ROUND(AVG(attempts_before_ac + 1), 2) AS avg_attempts_to_solve
FROM UserProblem
WHERE status = 'Solved';

-- Query 5: Find solved problems by topic
SELECT 
    t.name AS topic_name,
    COUNT(DISTINCT pt.problem_id) AS total_problems,
    COUNT(DISTINCT CASE WHEN up.status = 'Solved' THEN up.problem_id END) AS solved_count
FROM Topic t
JOIN ProblemTopic pt ON t.topic_id = pt.topic_id
LEFT JOIN UserProblem up ON pt.problem_id = up.problem_id
GROUP BY t.topic_id, t.name;

-- Query 6: Find similar problems for candidate recommendation
SELECT 
    p1.title AS problem,
    p2.title AS similar_problem,
    ps.similarity_score,
    COALESCE(up.status, 'Unsolved') AS user_status_on_similar
FROM ProblemSimilarity ps
JOIN Problem p1 ON ps.problem_id = p1.problem_id
JOIN Problem p2 ON ps.similar_problem_id = p2.problem_id
LEFT JOIN UserProblem up ON ps.similar_problem_id = up.problem_id;

-- Query 7: Contest rating and rank history
SELECT 
    c.contest_name,
    c.contest_date,
    cp.rank,
    cp.score,
    cp.rating_before,
    cp.rating_after,
    cp.rating_change
FROM Contest c
JOIN ContestParticipation cp ON c.contest_id = cp.contest_id
ORDER BY c.contest_date ASC;
