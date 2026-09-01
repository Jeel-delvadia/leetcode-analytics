# Database Design Document

## 1. Entity-Relationship Diagram

```text
                         ┌──────────────┐
                         │    Topic     │
                         │──────────────│
                         │ topic_id PK  │
                         │ name         │
                         └──────┬───────┘
                                │
                         ProblemTopic
                                │
                                ▼
┌──────────────┐        ┌──────────────┐
│   Problem    │        │              │
│──────────────│        │              │
│ problem_id PK│◄───────│ UserProblem  │
│ title        │        │──────────────│
│ difficulty   │        │ status       │
│ acceptance   │        │ attempts     │
│ submissions  │        │ first_AC     │
│ accepted     │        └──────┬───────┘
└──────┬───────┘               │
       │                       │
       │                       ▼
       │                ┌──────────────┐
       │                │ Submission   │
       │                │──────────────│
       │                │ submission_id│
       │                │ result       │
       │                │ language     │
       │                │ runtime      │
       │                │ memory       │
       │                │ submitted_at │
       │                └──────────────┘
       │
       ├──────────────► ProblemSimilarity ◄──────────────┐
       │                                                  │
       ▼                                                  ▼
┌──────────────┐                                  ┌──────────────┐
│   Contest    │                                  │    Problem   │
│──────────────│                                  │              │
│ contest_id PK│                                  │              │
│ name         │                                  │              │
│ date         │                                  │              │
└──────┬───────┘                                  └──────────────┘
       │
       ▼
┌──────────────────────┐
│ ContestParticipation │
│──────────────────────│
│ contest_id FK        │
│ rank                 │
│ score                │
│ rating_before        │
│ rating_after         │
│ rating_change        │
│ solved               │
└──────────────────────┘

Topic ──────► TopicPrerequisite ◄────── Topic

SyncHistory
```

---

## 2. Table Specifications

### 2.1. Problem
Stores global information about every LeetCode problem.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `problem_id` | INT | PRIMARY KEY | LeetCode integer ID |
| `frontend_id` | VARCHAR(20) | UNIQUE, NOT NULL | Display problem number |
| `title` | VARCHAR(255) | NOT NULL | Problem title |
| `title_slug` | VARCHAR(255) | UNIQUE, NOT NULL | URL slug |
| `difficulty` | ENUM | NOT NULL | 'Easy', 'Medium', 'Hard' |
| `acceptance_rate` | DECIMAL(6,3) | | Global acceptance rate percentage |
| `total_submissions` | BIGINT | | Total global submissions |
| `total_accepted` | BIGINT | | Total global accepted submissions |
| `is_paid` | BOOLEAN | DEFAULT FALSE | Premium status |
| `problem_url` | VARCHAR(500) | | LeetCode problem URL |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record insertion time |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record update time |

### 2.2. Topic
Stores LeetCode topics and categories.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `topic_id` | INT | AUTO_INCREMENT, PRIMARY KEY | Internal topic ID |
| `name` | VARCHAR(100) | UNIQUE, NOT NULL | Topic name |
| `description` | TEXT | | Topic description |

### 2.3. ProblemTopic
Junction table for many-to-many problem and topic relationship.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `problem_id` | INT | FK -> Problem(problem_id) | Foreign key to Problem |
| `topic_id` | INT | FK -> Topic(topic_id) | Foreign key to Topic |

### 2.4. Submission
Stores individual submission records.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `submission_id` | BIGINT | PRIMARY KEY | Submission ID |
| `problem_id` | INT | FK -> Problem(problem_id) | Foreign key to Problem |
| `submitted_at` | DATETIME | NOT NULL | Timestamp of submission |
| `result` | VARCHAR(50) | NOT NULL | Result status (Accepted, Wrong Answer, TLE, etc.) |
| `language` | VARCHAR(50) | | Programming language used |
| `runtime_ms` | INT | | Execution runtime in ms |
| `memory_kb` | INT | | Memory usage in KB |

### 2.5. UserProblem
Single-user aggregate relationship state per problem.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `problem_id` | INT | PRIMARY KEY, FK -> Problem | Foreign key to Problem |
| `status` | ENUM | NOT NULL | 'Attempted', 'Solved' |
| `num_submissions` | INT | DEFAULT 0 | Total user attempts |
| `num_accepted` | INT | DEFAULT 0 | Total AC submissions |
| `first_submitted_at` | DATETIME | | First attempt date |
| `last_submitted_at` | DATETIME | | Latest attempt date |
| `first_accepted_at` | DATETIME | | First AC date |
| `last_accepted_at` | DATETIME | | Latest AC date |
| `last_result` | VARCHAR(50) | | Latest submission result |
| `attempts_before_ac` | INT | | Failed attempts prior to first AC |

### 2.6. ProblemSimilarity
Stores similarity relationships between problems for recommendation models.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `problem_id` | INT | FK -> Problem(problem_id) | Base problem ID |
| `similar_problem_id` | INT | FK -> Problem(problem_id) | Related problem ID |
| `similarity_score` | DECIMAL(6,5) | | Calculated or source similarity score |
| `source` | VARCHAR(50) | | Source of similarity data |

### 2.7. TopicPrerequisite
Represents prerequisite graphs between topics for learning flow prediction.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `topic_id` | INT | FK -> Topic(topic_id) | Target topic |
| `prerequisite_topic_id` | INT | FK -> Topic(topic_id) | Prerequisite topic |
| `prerequisite_strength` | DECIMAL(5,2) | | Strength weight of prerequisite |

### 2.8. Contest
Stores global contest information.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `contest_id` | INT | PRIMARY KEY | Contest ID |
| `contest_name` | VARCHAR(255) | NOT NULL | Name of contest |
| `contest_slug` | VARCHAR(255) | UNIQUE | URL slug |
| `contest_date` | DATETIME | | Contest start time |
| `contest_type` | VARCHAR(50) | | Weekly/Biweekly type |

### 2.9. ContestParticipation
User performance per contest.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `contest_id` | INT | PRIMARY KEY, FK -> Contest | Foreign key to Contest |
| `attended` | BOOLEAN | DEFAULT TRUE | Attendance indicator |
| `rank` | INT | | Final rank achieved |
| `score` | DECIMAL(8,2) | | Total contest score |
| `rating_before` | DECIMAL(8,2) | | Rating before contest |
| `rating_after` | DECIMAL(8,2) | | Rating after contest |
| `rating_change` | DECIMAL(8,2) | | Delta rating change |
| `problems_attempted` | INT | | Count of attempted problems |
| `problems_solved` | INT | | Count of solved problems |

### 2.10. SyncHistory
Tracks Chrome extension sync executions and health.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `sync_id` | BIGINT | AUTO_INCREMENT, PRIMARY KEY | Sync operation ID |
| `sync_type` | ENUM | NOT NULL | 'INITIAL', 'INCREMENTAL', 'RECONCILIATION' |
| `started_at` | DATETIME | NOT NULL | Sync start timestamp |
| `completed_at` | DATETIME | | Sync end timestamp |
| `records_fetched` | INT | DEFAULT 0 | Number of records pulled |
| `status` | ENUM | NOT NULL | 'RUNNING', 'SUCCESS', 'FAILED' |
| `error_message` | TEXT | | Failure traceback or message |
