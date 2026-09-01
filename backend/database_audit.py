import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import sqlite3

def run_audit():
    db_path = "leetcode_analytics.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("==========================================")
    print("      LEETCODE DATABASE INTEGRITY AUDIT    ")
    print("==========================================")

    tables = [
        "Problem", "Topic", "ProblemTopic", "Submission", "UserProblem",
        "ProblemSimilarity", "TopicPrerequisite", "Contest", "ContestParticipation", "SyncHistory"
    ]

    counts = {}
    for t in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {t}")
        counts[t] = cursor.fetchone()[0]
        print(f"Table '{t}': {counts[t]} records")

    # 1. Orphan Submissions
    cursor.execute("SELECT COUNT(*) FROM Submission s LEFT JOIN Problem p ON s.problem_id = p.problem_id WHERE p.problem_id IS NULL")
    orphan_subs = cursor.fetchone()[0]

    # 2. Orphan UserProblem
    cursor.execute("SELECT COUNT(*) FROM UserProblem up LEFT JOIN Problem p ON up.problem_id = p.problem_id WHERE p.problem_id IS NULL")
    orphan_up = cursor.fetchone()[0]

    # 3. Duplicate Submissions
    cursor.execute("SELECT COUNT(*) FROM (SELECT submission_id FROM Submission GROUP BY submission_id HAVING COUNT(*) > 1)")
    dup_subs = cursor.fetchone()[0]

    # 4. Duplicate ProblemTopic
    cursor.execute("SELECT COUNT(*) FROM (SELECT problem_id, topic_id FROM ProblemTopic GROUP BY problem_id, topic_id HAVING COUNT(*) > 1)")
    dup_pt = cursor.fetchone()[0]

    # 5. Invalid Self-Similarities
    cursor.execute("SELECT COUNT(*) FROM ProblemSimilarity WHERE problem_id = similar_problem_id")
    self_sim = cursor.fetchone()[0]

    # 6. UserProblem Derivation Mismatches
    cursor.execute("SELECT DISTINCT problem_id FROM Submission UNION SELECT problem_id FROM UserProblem")
    all_pids = [r[0] for r in cursor.fetchall()]
    mismatches = 0

    for pid in all_pids:
        cursor.execute("SELECT result, submitted_at FROM Submission WHERE problem_id = ? ORDER BY submitted_at ASC, submission_id ASC", (pid,))
        subs = cursor.fetchall()
        cursor.execute("SELECT status, num_submissions, num_accepted, attempts_before_ac FROM UserProblem WHERE problem_id = ?", (pid,))
        up = cursor.fetchone()

        calc_num_submissions = len(subs)
        calc_num_accepted = sum(1 for s in subs if s[0] == 'Accepted')
        calc_status = "Solved" if calc_num_accepted > 0 else ("Attempted" if calc_num_submissions > 0 else "Unsolved")

        calc_attempts_before_ac = None
        if calc_num_accepted > 0:
            count = 0
            for s in subs:
                count += 1
                if s[0] == 'Accepted':
                    break
            calc_attempts_before_ac = count

        if up is None:
            mismatches += 1
        else:
            up_status, up_num_sub, up_num_ac, up_attempts_before_ac = up
            if (up_num_sub != calc_num_submissions or up_num_ac != calc_num_accepted or 
                up_status != calc_status or up_attempts_before_ac != calc_attempts_before_ac):
                mismatches += 1

    print("\n--- Integrity Audit Summary ---")
    print(f"Orphan Submissions: {orphan_subs}")
    print(f"Orphan UserProblem: {orphan_up}")
    print(f"Duplicate Submissions: {dup_subs}")
    print(f"Duplicate ProblemTopic: {dup_pt}")
    print(f"Self Similarity References: {self_sim}")
    print(f"UserProblem Derivation Mismatches: {mismatches}")

    conn.close()

    if orphan_subs == 0 and orphan_up == 0 and dup_subs == 0 and dup_pt == 0 and self_sim == 0 and mismatches == 0:
        print("\nSTATUS: PASS")
        return 0
    else:
        print("\nSTATUS: FAIL")
        return 1

if __name__ == "__main__":
    sys.exit(run_audit())
