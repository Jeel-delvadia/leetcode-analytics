-- Mock Seed Data for Testing and Verification

-- 1. Seed Topics
INSERT INTO Topic (topic_id, name, description) VALUES
(1, 'Array', 'Array data structure and algorithms'),
(2, 'String', 'String manipulation and algorithms'),
(3, 'Hash Table', 'Hash maps and hash sets'),
(4, 'Dynamic Programming', 'Dynamic programming and memoization'),
(5, 'Two Pointers', 'Two pointer technique'),
(6, 'Binary Search', 'Binary search technique'),
(7, 'Depth-First Search', 'DFS graph/tree traversal'),
(8, 'Breadth-First Search', 'BFS graph/tree traversal'),
(9, 'Shortest Path', 'Graph shortest path algorithms'),
(10, 'Dijkstra', 'Dijkstra shortest path algorithm')
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- 2. Seed Problems
INSERT INTO Problem (problem_id, frontend_id, title, title_slug, difficulty, acceptance_rate, total_submissions, total_accepted, is_paid, problem_url) VALUES
(1, '1', 'Two Sum', 'two-sum', 'Easy', 50.100, 20000000, 10020000, FALSE, 'https://leetcode.com/problems/two-sum/'),
(15, '15', '3Sum', '3sum', 'Medium', 33.500, 8000000, 2680000, FALSE, 'https://leetcode.com/problems/3sum/'),
(200, '200', 'Number of Islands', 'number-of-islands', 'Medium', 57.800, 4000000, 2312000, FALSE, 'https://leetcode.com/problems/number-of-islands/'),
(743, '743', 'Network Delay Time', 'network-delay-time', 'Medium', 52.400, 800000, 419200, FALSE, 'https://leetcode.com/problems/network-delay-time/'),
(210, '210', 'Course Schedule II', 'course-schedule-ii', 'Medium', 49.200, 1200000, 590400, FALSE, 'https://leetcode.com/problems/course-schedule-ii/')
ON DUPLICATE KEY UPDATE title=VALUES(title);

-- 3. Seed ProblemTopic
INSERT INTO ProblemTopic (problem_id, topic_id) VALUES
(1, 1), (1, 3),        -- Two Sum: Array, Hash Table
(15, 1), (15, 5),      -- 3Sum: Array, Two Pointers
(200, 7), (200, 8),    -- Number of Islands: DFS, BFS
(743, 9), (743, 10),   -- Network Delay Time: Shortest Path, Dijkstra
(210, 7), (210, 8)     -- Course Schedule II: DFS, BFS
ON DUPLICATE KEY UPDATE problem_id=VALUES(problem_id);

-- 4. Seed Submissions
INSERT INTO Submission (submission_id, problem_id, submitted_at, result, language, runtime_ms, memory_kb) VALUES
(1001, 1, '2026-01-10 10:15:00', 'Wrong Answer', 'cpp', 0, 0),
(1002, 1, '2026-01-10 10:20:00', 'Accepted', 'cpp', 4, 10400),
(1003, 15, '2026-01-15 14:00:00', 'Time Limit Exceeded', 'python3', 0, 0),
(1004, 15, '2026-01-15 14:30:00', 'Accepted', 'python3', 450, 18200),
(1005, 200, '2026-02-01 09:00:00', 'Accepted', 'python3', 280, 19500),
(1006, 743, '2026-02-10 18:00:00', 'Wrong Answer', 'cpp', 45, 12100)
ON DUPLICATE KEY UPDATE result=VALUES(result);

-- 5. Seed UserProblem
INSERT INTO UserProblem (problem_id, status, num_submissions, num_accepted, first_submitted_at, last_submitted_at, first_accepted_at, last_accepted_at, last_result, attempts_before_ac) VALUES
(1, 'Solved', 2, 1, '2026-01-10 10:15:00', '2026-01-10 10:20:00', '2026-01-10 10:20:00', '2026-01-10 10:20:00', 'Accepted', 1),
(15, 'Solved', 2, 1, '2026-01-15 14:00:00', '2026-01-15 14:30:00', '2026-01-15 14:30:00', '2026-01-15 14:30:00', 'Accepted', 1),
(200, 'Solved', 1, 1, '2026-02-01 09:00:00', '2026-02-01 09:00:00', '2026-02-01 09:00:00', '2026-02-01 09:00:00', 'Accepted', 0),
(743, 'Attempted', 1, 0, '2026-02-10 18:00:00', '2026-02-10 18:00:00', NULL, NULL, 'Wrong Answer', NULL)
ON DUPLICATE KEY UPDATE status=VALUES(status);

-- 6. Seed ProblemSimilarity
INSERT INTO ProblemSimilarity (problem_id, similar_problem_id, similarity_score, source) VALUES
(1, 15, 0.85000, 'LeetCode'),
(200, 210, 0.75000, 'LeetCode')
ON DUPLICATE KEY UPDATE similarity_score=VALUES(similarity_score);

-- 7. Seed TopicPrerequisite
INSERT INTO TopicPrerequisite (topic_id, prerequisite_topic_id, prerequisite_strength) VALUES
(9, 7, 0.90),    -- Shortest Path requires DFS
(9, 8, 0.90),    -- Shortest Path requires BFS
(10, 9, 0.95)    -- Dijkstra requires Shortest Path
ON DUPLICATE KEY UPDATE prerequisite_strength=VALUES(prerequisite_strength);

-- 8. Seed Contests
INSERT INTO Contest (contest_id, contest_name, contest_slug, contest_date, contest_type) VALUES
(380, 'Weekly Contest 380', 'weekly-contest-380', '2026-01-14 02:30:00', 'Weekly'),
(381, 'Weekly Contest 381', 'weekly-contest-381', '2026-01-21 02:30:00', 'Weekly')
ON DUPLICATE KEY UPDATE contest_name=VALUES(contest_name);

-- 9. Seed ContestParticipation
INSERT INTO ContestParticipation (contest_id, attended, rank, score, rating_before, rating_after, rating_change, problems_attempted, problems_solved) VALUES
(380, TRUE, 2450, 12.00, 1500.00, 1532.00, 32.00, 3, 3),
(381, TRUE, 1820, 18.00, 1532.00, 1585.00, 53.00, 4, 4)
ON DUPLICATE KEY UPDATE rank=VALUES(rank);

-- 10. Seed SyncHistory
INSERT INTO SyncHistory (sync_id, sync_type, started_at, completed_at, records_fetched, status, error_message) VALUES
(1, 'INITIAL', '2026-02-15 10:00:00', '2026-02-15 10:05:00', 450, 'SUCCESS', NULL)
ON DUPLICATE KEY UPDATE status=VALUES(status);
