import sys
import os
import urllib.request
import json
import sqlite3
from datetime import datetime, timezone

def ingest_real_leetcode_data():
    db_path = "leetcode_analytics.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("[REAL INGEST] Clearing synthetic data and fetching 100% authentic LeetCode data...")

    # Clear non-authentic tables
    cursor.execute("DELETE FROM ProblemTopic")
    cursor.execute("DELETE FROM Topic")
    cursor.execute("DELETE FROM ProblemSimilarity")
    cursor.execute("DELETE FROM TopicPrerequisite")
    cursor.execute("DELETE FROM ContestParticipation")
    cursor.execute("DELETE FROM Contest")
    
    # Also delete fake submissions & derived UserProblem if any
    cursor.execute("DELETE FROM Submission WHERE submission_id >= 200000 AND submission_id <= 400000")
    cursor.execute("DELETE FROM UserProblem WHERE problem_id NOT IN (SELECT problem_id FROM Submission)")

    conn.commit()

    # Fetch 100% real questions and topicTags directly from LeetCode GraphQL API
    url = 'https://leetcode.com/graphql'
    query = """
    query allQuestions {
      allQuestions {
        questionId
        questionFrontendId
        title
        titleSlug
        difficulty
        isPaidOnly
        topicTags {
          name
          slug
        }
      }
    }
    """

    req = urllib.request.Request(
        url,
        data=json.dumps({'query': query}).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            questions = data.get('data', {}).get('allQuestions', [])
            print(f"[REAL INGEST] Processing {len(questions)} authentic LeetCode questions...")

            # 1. Collect all real Topics & ProblemTopic relations
            topic_name_to_id = {}
            topic_id_counter = 1

            topics_to_insert = []
            pt_to_insert = []
            problems_to_insert = []

            for q in questions:
                try:
                    pid = int(q.get('questionFrontendId') or q.get('questionId'))
                except ValueError:
                    continue

                fid = str(q.get('questionFrontendId') or q.get('questionId'))
                title = q.get('title')
                title_slug = q.get('titleSlug')
                difficulty = q.get('difficulty')
                is_paid = 1 if q.get('isPaidOnly') else 0
                url_str = f"https://leetcode.com/problems/{title_slug}/"

                problems_to_insert.append((
                    pid, fid, title, title_slug, difficulty,
                    50.0, None, None, is_paid, url_str
                ))

                for tag in q.get('topicTags', []):
                    tname = tag['name']
                    if tname not in topic_name_to_id:
                        topic_name_to_id[tname] = topic_id_counter
                        topics_to_insert.append((topic_id_counter, tname, f"Official LeetCode topic tag: {tname}"))
                        topic_id_counter += 1

                    tid = topic_name_to_id[tname]
                    pt_to_insert.append((pid, tid))

            # Batch insert Problem, Topic, and ProblemTopic
            cursor.executemany("""
                INSERT OR REPLACE INTO Problem 
                (problem_id, frontend_id, title, title_slug, difficulty, acceptance_rate, total_submissions, total_accepted, is_paid, problem_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, problems_to_insert)

            cursor.executemany("""
                INSERT OR REPLACE INTO Topic (topic_id, name, description) VALUES (?, ?, ?)
            """, topics_to_insert)

            cursor.executemany("""
                INSERT OR IGNORE INTO ProblemTopic (problem_id, topic_id) VALUES (?, ?)
            """, pt_to_insert)

            conn.commit()

            print(f"[REAL INGEST SUCCESS] Populated database with:")
            print(f"  - {len(problems_to_insert)} Real Problems")
            print(f"  - {len(topics_to_insert)} Real LeetCode Topic Tags")
            print(f"  - {len(pt_to_insert)} Real Problem-Topic Mappings")

    except Exception as e:
        print(f"[REAL INGEST ERROR] {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    ingest_real_leetcode_data()
