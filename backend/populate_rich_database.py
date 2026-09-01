import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import sqlite3
import random
from datetime import datetime, timedelta

def populate_rich_database():
    db_path = "leetcode_analytics.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("[RICH POPULATE] Expanding relational dataset across all 10 Database Design Tables...")

    # 1. Topic Table (50 Topics)
    topic_names = [
        "Array", "String", "Hash Table", "Dynamic Programming", "Math",
        "Sorting", "Greedy", "Depth-First Search", "Binary Search", "Database",
        "Breadth-First Search", "Tree", "Matrix", "Two Pointers", "Bit Manipulation",
        "Binary Tree", "Heap (Priority Queue)", "Stack", "Prefix Sum", "Graph",
        "Simulation", "Design", "Counting", "Backtracking", "Sliding Window",
        "Union Find", "Linked List", "Monotonic Stack", "Ordered Set", "Recursion",
        "Trie", "Divide and Conquer", "Bitmask", "Queue", "Memoization",
        "Geometry", "Segment Tree", "Topological Sort", "Hash Function", "Game Theory",
        "Shortest Path", "Combinatorics", "Interactive", "String Matching", "Data Stream",
        "Rolling Hash", "Brainteaser", "Randomized", "Monotonic Queue", "Merge Sort"
    ]

    topics = [(i + 1, name, f"{name} algorithms and problem patterns") for i, name in enumerate(topic_names)]
    cursor.executemany('INSERT OR REPLACE INTO Topic (topic_id, name, description) VALUES (?, ?, ?)', topics)

    # 2. ProblemTopic Table (Connect 500 Problems to Topics)
    problem_topics = []
    for pid in range(1, 501):
        # Assign 1 to 3 random topics to each problem
        t_ids = random.sample(range(1, 51), random.randint(1, 3))
        for tid in t_ids:
            problem_topics.append((pid, tid))
    cursor.executemany('INSERT OR IGNORE INTO ProblemTopic (problem_id, topic_id) VALUES (?, ?)', problem_topics)

    # 3. TopicPrerequisite Table (25 Prerequisite Relationships)
    prereqs = [
        (8, 9, 0.85),    # DFS -> BFS
        (9, 10, 0.90),   # BFS -> Graph
        (10, 17, 0.75),  # Graph -> Heap
        (1, 14, 0.80),   # Array -> Two Pointers
        (14, 25, 0.70),  # Two Pointers -> Sliding Window
        (4, 35, 0.95),   # DP -> Memoization
        (10, 38, 0.88),  # Graph -> Topological Sort
        (10, 41, 0.92),  # Graph -> Shortest Path
        (12, 50, 0.80),  # Sorting -> Merge Sort
        (7, 16, 0.95),   # Tree -> Binary Tree
        (18, 28, 0.85),  # Stack -> Monotonic Stack
        (34, 49, 0.80),  # Queue -> Monotonic Queue
        (3, 39, 0.75),   # Hash Table -> Hash Function
        (3, 46, 0.70),   # Hash Table -> Rolling Hash
        (31, 2, 0.80),   # Trie -> String
        (26, 10, 0.85),  # Union Find -> Graph
        (6, 1, 0.75),    # Binary Search -> Array
        (19, 1, 0.70),   # Prefix Sum -> Array
        (4, 33, 0.80),   # DP -> Bitmask
        (37, 7, 0.85)    # Segment Tree -> Tree
    ]
    cursor.executemany('INSERT OR REPLACE INTO TopicPrerequisite (topic_id, prerequisite_topic_id, prerequisite_strength) VALUES (?, ?, ?)', prereqs)

    # 4. ProblemSimilarity Table (40 Problem Similarities)
    similarities = []
    for pid in range(1, 41):
        sim_id = pid + 5
        score = round(random.uniform(0.70, 0.98), 2)
        similarities.append((pid, sim_id, score, 'LeetCode Tags'))
    cursor.executemany('INSERT OR REPLACE INTO ProblemSimilarity (problem_id, similar_problem_id, similarity_score, source) VALUES (?, ?, ?, ?)', similarities)

    # 5. UserProblem & Submission Tables (120 User Problems & 400 Submissions across ALL statuses)
    now = datetime.utcnow()
    statuses = ['Accepted', 'Wrong Answer', 'Time Limit Exceeded', 'Memory Limit Exceeded', 'Compile Error', 'Runtime Error']
    languages = ['cpp', 'python3', 'java', 'javascript']

    submissions = []
    user_problems = []
    sub_id = 300000

    for pid in range(1, 121):
        num_subs = random.randint(1, 5)
        is_solved = random.choice([True, True, False])
        user_status = "Solved" if is_solved else "Attempted"
        
        first_sub_time = now - timedelta(days=random.randint(1, 60), hours=random.randint(1, 12))
        last_sub_time = first_sub_time + timedelta(hours=random.randint(1, 48))
        first_ac_time = last_sub_time if is_solved else None

        num_ac = 0
        attempts_before_ac = None

        for s_idx in range(num_subs):
            sub_id += 1
            s_time = first_sub_time + timedelta(minutes=s_idx * 30)
            
            if is_solved and s_idx == num_subs - 1:
                res = "Accepted"
                num_ac += 1
                if attempts_before_ac is None:
                    attempts_before_ac = s_idx
            else:
                res = random.choice(statuses[1:])  # WA, TLE, MLE, CE, RE

            runtime = random.randint(0, 500) if res == "Accepted" else random.randint(0, 3000)
            memory = random.randint(10000, 25000)

            submissions.append((
                sub_id, pid, s_time.strftime('%Y-%m-%d %H:%M:%S'),
                res, random.choice(languages), runtime, memory
            ))

        last_res = submissions[-1][3]
        user_problems.append((
            pid, user_status, num_subs, num_ac,
            first_sub_time.strftime('%Y-%m-%d %H:%M:%S'),
            first_ac_time.strftime('%Y-%m-%d %H:%M:%S') if first_ac_time else None,
            last_res, attempts_before_ac
        ))

    cursor.executemany('INSERT OR REPLACE INTO Submission (submission_id, problem_id, submitted_at, result, language, runtime_ms, memory_kb) VALUES (?, ?, ?, ?, ?, ?, ?)', submissions)
    cursor.executemany('INSERT OR REPLACE INTO UserProblem (problem_id, status, num_submissions, num_accepted, first_submitted_at, first_accepted_at, last_result, attempts_before_ac) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', user_problems)

    # 6. Contest Table (15 Contests)
    contests = []
    for c_id in range(1, 16):
        c_date = now - timedelta(days=c_id * 7)
        c_type = 'Weekly' if c_id % 2 == 1 else 'Biweekly'
        c_name = f"{c_type} Contest {380 - c_id}"
        c_slug = f"{c_type.lower()}-contest-{380 - c_id}"
        contests.append((c_id, c_name, c_slug, c_date.strftime('%Y-%m-%d %H:%M:%S'), c_type))

    cursor.executemany('INSERT OR REPLACE INTO Contest (contest_id, contest_name, contest_slug, contest_date, contest_type) VALUES (?, ?, ?, ?, ?)', contests)

    # 7. ContestParticipation Table (15 Contest Participations)
    participations = []
    rating = 1500
    for c_id in range(1, 16):
        rank = random.randint(400, 2500)
        solved = random.randint(1, 4)
        score = solved * 5.0
        rating_before = rating
        rating += random.randint(-20, 45)
        participations.append((c_id, 1, rank, score, rating_before, rating, solved))

    cursor.executemany('INSERT OR REPLACE INTO ContestParticipation (contest_id, attended, rank, score, rating_before, rating_after, problems_solved) VALUES (?, ?, ?, ?, ?, ?, ?)', participations)

    # 8. SyncHistory Table (20 Sync Logs)
    sync_logs = []
    types = ['INITIAL', 'INCREMENTAL', 'RECONCILIATION']
    for s_id in range(10, 30):
        s_time = now - timedelta(days=30 - s_id)
        c_time = s_time + timedelta(seconds=random.randint(1, 15))
        stype = random.choice(types)
        rfetched = 4041 if stype == 'INITIAL' else random.randint(1, 15)
        sync_logs.append((s_id, stype, s_time.strftime('%Y-%m-%d %H:%M:%S'), c_time.strftime('%Y-%m-%d %H:%M:%S'), rfetched, 'SUCCESS', None))

    cursor.executemany('INSERT OR REPLACE INTO SyncHistory (sync_id, sync_type, started_at, completed_at, records_fetched, status, error_message) VALUES (?, ?, ?, ?, ?, ?, ?)', sync_logs)

    conn.commit()
    conn.close()
    print("[RICH POPULATE SUCCESS] All 10 Database Design Tables populated with extensive relational data!")

if __name__ == "__main__":
    populate_rich_database()
