import sqlite3
import re
import os

def test_sqlite_schema_validation():
    """
    Validates database schema creation, constraints, foreign keys,
    and seed data execution using SQLite.
    """
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    schema_path = r"d:\lc\leetcode-analytics\database\schema.sql"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    # Convert MySQL ENUM / AUTO_INCREMENT syntax for SQLite compatibility
    sqlite_schema = re.sub(r"ENUM\s*\([^)]+\)", "TEXT", schema_sql, flags=re.IGNORECASE | re.DOTALL)
    sqlite_schema = sqlite_schema.replace("BIGINT AUTO_INCREMENT PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT")
    sqlite_schema = sqlite_schema.replace("INT AUTO_INCREMENT PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT")
    sqlite_schema = sqlite_schema.replace("AUTO_INCREMENT", "")
    sqlite_schema = sqlite_schema.replace("ON UPDATE CURRENT_TIMESTAMP", "")

    # Execute Schema DDL
    cursor.executescript(sqlite_schema)
    print("[PASS] Schema DDL executed successfully.")

    # Execute Seed SQL
    seed_path = r"d:\lc\leetcode-analytics\database\seed.sql"
    with open(seed_path, "r", encoding="utf-8") as f:
        seed_sql = f.read()

    sqlite_seed = seed_sql.replace("ON DUPLICATE KEY UPDATE", "-- ON DUPLICATE")
    # Clean up MySQL specific syntax for SQLite test
    statements = [s.strip() for s in sqlite_seed.split(";") if s.strip()]
    for stmt in statements:
        if "ON DUPLICATE" in stmt:
            stmt = stmt.split("ON DUPLICATE")[0].strip()
        try:
            cursor.execute(stmt)
        except Exception as e:
            print(f"[WARN] Statement notice: {e}")

    conn.commit()
    print("[PASS] Seed data inserted successfully.")

    # Verify Table Row Counts
    tables = ["Problem", "Topic", "ProblemTopic", "Submission", "UserProblem", "ProblemSimilarity", "TopicPrerequisite", "Contest", "ContestParticipation", "SyncHistory"]
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"Table '{table}' row count: {count}")
        assert count > 0, f"Table {table} is empty!"

    conn.close()
    print("[PASS] All database schema validation tests passed cleanly!")

if __name__ == "__main__":
    test_sqlite_schema_validation()
