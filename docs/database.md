# Database Architecture & Schema Specification

## Overview

The LeetCode Personal Analytics system uses a **single-user architecture** (no `User` table). The canonical source of raw attempt data is the **`Submission`** table. The **`UserProblem`** table is a derived summary table computed directly from `Submission` records.

---

## ER Diagram & Table Relationships

```
+---------------+        +------------------+        +---------------+
|    Problem    |------< |   ProblemTopic   | >------|     Topic     |
+---------------+        +------------------+        +---------------+
    |       |                                                |
    |       |                                                |
    |       +------------------------------------+           |
    v                                            v           v
+---------------+                        +----------------------+
|  Submission   | (Raw History)          |  TopicPrerequisite   |
+---------------+                        +----------------------+
    | (Derives)
    v
+---------------+
|  UserProblem  | (Summary View)
+---------------+

+---------------+        +----------------------+
|    Contest    |------< | ContestParticipation |
+---------------+        +----------------------+

+---------------+
|  SyncHistory  | (Audit Log)
+---------------+
```

---

## Core 10 Tables Summary

### 1. `Problem` (Global LeetCode Problems)
- **Primary Key**: `problem_id` (Integer)
- **Unique**: `frontend_id`, `title_slug`
- **Fields**: `title`, `difficulty`, `acceptance_rate`, `total_submissions`, `total_accepted`, `is_paid`, `problem_url`

### 2. `Topic` (Topic Categories)
- **Primary Key**: `topic_id` (Integer)
- **Unique**: `name`
- **Fields**: `description`

### 3. `ProblemTopic` (Problem-Topic Mapping)
- **Primary Key**: `(problem_id, topic_id)`
- **Foreign Keys**: `problem_id` -> `Problem.problem_id`, `topic_id` -> `Topic.topic_id`

### 4. `Submission` (Raw User Submissions - CANONICAL TRUTH)
- **Primary Key**: `submission_id` (BigInteger/Integer)
- **Foreign Key**: `problem_id` -> `Problem.problem_id`
- **Fields**: `submitted_at`, `result`, `language`, `runtime_ms`, `memory_kb`

### 5. `UserProblem` (Derived Summary State)
- **Primary Key**: `problem_id` (Integer)
- **Foreign Key**: `problem_id` -> `Problem.problem_id`
- **Fields**: `status`, `num_submissions`, `num_accepted`, `first_submitted_at`, `last_submitted_at`, `first_accepted_at`, `last_accepted_at`, `last_result`, `attempts_before_ac`
- **Derivation Rule**: Computed strictly from `Submission` rows grouped by `problem_id`.

### 6. `ProblemSimilarity` (Problem Relationships)
- **Primary Key**: `(problem_id, similar_problem_id)`
- **Check Constraint**: `problem_id <> similar_problem_id`

### 7. `TopicPrerequisite` (Learning Path Dependencies)
- **Primary Key**: `(topic_id, prerequisite_topic_id)`
- **Check Constraint**: `topic_id <> prerequisite_topic_id`

### 8. `Contest` (Global Contests)
- **Primary Key**: `contest_id` (Integer)
- **Unique**: `contest_slug`

### 9. `ContestParticipation` (User Contest History)
- **Primary Key**: `contest_id` (Integer)
- **Foreign Key**: `contest_id` -> `Contest.contest_id`

### 10. `SyncHistory` (System Audit Log)
- **Primary Key**: `sync_id` (Integer)
- **Fields**: `sync_type` (INITIAL, INCREMENTAL, RECONCILIATION), `started_at`, `completed_at`, `records_fetched`, `status`, `error_message`
