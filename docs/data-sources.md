# LeetCode API & Network Data Documentation

This document outlines the GraphQL and REST network requests utilized by LeetCode, detailing request payloads, response structures, authentication requirements, and field mapping to our MySQL database schema.

---

## 1. Network Protocol Overview

- **Protocol**: HTTP/2 over HTTPS
- **Primary Endpoint**: `https://leetcode.com/graphql`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Authentication**: Cookie-based authentication (`LEETCODE_SESSION` & `csrftoken`).
- **CSRF Protection**: Header `x-csrftoken` matching the `csrftoken` cookie value.

---

## 2. LeetCode GraphQL Operations

### 2.1. Problem List & Global Metadata (`problemsetQuestionList`)

- **URL**: `https://leetcode.com/graphql`
- **Operation Name**: `problemsetQuestionList`
- **Method**: `POST`
- **Pagination**: `skip` and `limit` parameters in variables.

#### Request Payload:
```json
{
  "operationName": "problemsetQuestionList",
  "query": "query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) { problemsetQuestionList: questionList(categorySlug: $categorySlug, limit: $limit, skip: $skip, filters: $filters) { total: totalNum questions: questions { acRate difficulty freqBar frontendQuestionId: questionFrontendId isFavor isPaidOnly status title titleSlug topicTags { name id slug } hasSolution hasVideoSolution } } }",
  "variables": {
    "categorySlug": "",
    "skip": 0,
    "limit": 100,
    "filters": {}
  }
}
```

#### Response Field Mapping:

| Response JSON Path | Target DB Table | Target Column | Data Type Transformation |
|---|---|---|---|
| `questions[].frontendQuestionId` | `Problem` | `frontend_id` | String |
| `questions[].title` | `Problem` | `title` | String |
| `questions[].titleSlug` | `Problem` | `title_slug` | String |
| `questions[].difficulty` | `Problem` | `difficulty` | ENUM ('Easy', 'Medium', 'Hard') |
| `questions[].acRate` | `Problem` | `acceptance_rate` | DECIMAL(6,3) |
| `questions[].isPaidOnly` | `Problem` | `is_paid` | Boolean |
| `questions[].topicTags[].id` | `Topic` | `topic_id` | Integer |
| `questions[].topicTags[].name` | `Topic` | `name` | String |

---

### 2.2. Problem Detail & Similar Questions (`questionData`)

- **URL**: `https://leetcode.com/graphql`
- **Operation Name**: `questionData`
- **Method**: `POST`

#### Request Payload:
```json
{
  "operationName": "questionData",
  "query": "query questionData($titleSlug: String!) { question(titleSlug: $titleSlug) { questionId questionFrontendId title titleSlug content difficulty stats topicTags { name slug } similarQuestions stats totalSubmit totalAccepted } }",
  "variables": {
    "titleSlug": "two-sum"
  }
}
```

#### Response Field Mapping:

| Response JSON Path | Target DB Table | Target Column | Description |
|---|---|---|---|
| `question.questionId` | `Problem` | `problem_id` | Primary Key |
| `question.similarQuestions` | `ProblemSimilarity` | `similar_problem_id` | Parsed JSON array of similar problems |
| `stats.totalSubmit` | `Problem` | `total_submissions` | BigInt total attempts |
| `stats.totalAccepted` | `Problem` | `total_accepted` | BigInt total accepted |

---

### 2.3. User Submission History (`submissionList`)

- **URL**: `https://leetcode.com/graphql`
- **Operation Name**: `submissionList`
- **Method**: `POST`
- **Pagination**: `offset` and `limit`.

#### Request Payload:
```json
{
  "operationName": "submissionList",
  "query": "query submissionList($offset: Int!, $limit: Int!, $lastIndexOf: String, $questionSlug: String!) { questionSubmissionList(offset: $offset, limit: $limit, lastIndexOf: $lastIndexOf, questionSlug: $questionSlug) { lastKey hasNext submissions { id statusDisplay lang timestamp runtime memory url } } }",
  "variables": {
    "offset": 0,
    "limit": 20,
    "questionSlug": "two-sum"
  }
}
```

#### Response Field Mapping:

| Response JSON Path | Target DB Table | Target Column | Transformation |
|---|---|---|---|
| `submissions[].id` | `Submission` | `submission_id` | BigInt PK |
| `submissions[].timestamp` | `Submission` | `submitted_at` | Epoch timestamp -> DATETIME |
| `submissions[].statusDisplay` | `Submission` | `result` | Accepted, Wrong Answer, TLE, etc. |
| `submissions[].lang` | `Submission` | `language` | String (cpp, python3, java, etc.) |
| `submissions[].runtime` | `Submission` | `runtime_ms` | Stripped 'ms' -> Integer |
| `submissions[].memory` | `Submission` | `memory_kb` | Stripped 'MB/KB' -> Integer KB |

---

### 2.4. User Contest Ranking History (`userContestRankingInfo`)

- **URL**: `https://leetcode.com/graphql`
- **Operation Name**: `userContestRankingInfo`
- **Method**: `POST`

#### Request Payload:
```json
{
  "operationName": "userContestRankingInfo",
  "query": "query userContestRankingInfo($username: String!) { userContestRanking(username: $username) { attendedContestsCount rating globalRanking totalParticipants } userContestRankingHistory(username: $username) { attended trendDirection problemsSolved totalProblems finishTimeInSeconds rating ranking contest { title startTime } } }",
  "variables": {
    "username": "user123"
  }
}
```

#### Response Field Mapping:

| Response JSON Path | Target DB Table | Target Column | Transformation |
|---|---|---|---|
| `userContestRankingHistory[].contest.title` | `Contest` | `contest_name` | String |
| `userContestRankingHistory[].contest.startTime` | `Contest` | `contest_date` | Epoch -> DATETIME |
| `userContestRankingHistory[].attended` | `ContestParticipation` | `attended` | Boolean |
| `userContestRankingHistory[].ranking` | `ContestParticipation` | `rank` | Integer |
| `userContestRankingHistory[].rating` | `ContestParticipation` | `rating_after` | Decimal rating after contest |
| `userContestRankingHistory[].problemsSolved` | `ContestParticipation` | `problems_solved` | Count of solved problems |

---

## 3. Data Synchronization Strategy

1. **Initial Full Sync (`SyncHistory.sync_type = 'INITIAL'`)**:
   - Extension queries `problemsetQuestionList` with `limit = 100` iteratively until `questions.length < 100`.
   - Fetches user contest history `userContestRankingInfo`.
   - Posts data array to `/api/v1/sync/problems`, `/api/v1/sync/submissions`, `/api/v1/sync/contests`.

2. **Incremental Sync (`SyncHistory.sync_type = 'INCREMENTAL'`)**:
   - Extension monitors active tab network events for submission POSTs to `https://leetcode.com/problems/*/submit/`.
   - On submission result, queries latest submission for slug and updates `Submission` and `UserProblem` state.
