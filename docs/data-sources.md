# Data Sources & GraphQL Mapping Specification

## Data Flow Architecture

All external problem and user attempt data originates from **LeetCode GraphQL API (`https://leetcode.com/graphql`)** and is ingested by the Chrome Extension background service worker into the FastAPI backend.

---

## Field-to-Source Mapping Table

| DB Table | Field | Source System | Endpoint / GraphQL Query | Operation / Transformation |
|---|---|---|---|---|
| `Problem` | `problem_id` | LeetCode | `query allQuestions` | `parseInt(questionFrontendId)` |
| `Problem` | `title` | LeetCode | `query allQuestions` | `q.title` |
| `Problem` | `title_slug` | LeetCode | `query allQuestions` | `q.titleSlug` |
| `Problem` | `difficulty` | LeetCode | `query allQuestions` | `q.difficulty` ("Easy", "Medium", "Hard") |
| `Topic` | `name` | LeetCode | `query allQuestions` | `topicTags.name` |
| `Submission` | `submission_id` | LeetCode | `query submissionList` | `parseInt(s.id)` |
| `Submission` | `submitted_at` | LeetCode | `query submissionList` | `new Date(timestamp * 1000).toISOString()` |
| `Submission` | `result` | LeetCode | `query submissionList` | `s.statusDisplay` ("Accepted", "Wrong Answer", etc.) |
| `Submission` | `language` | LeetCode | `query submissionList` | `s.lang` |
| `UserProblem` | `status` | **Derived** | Local `Submission` Table | `"Solved"` if `num_accepted > 0` else `"Attempted"` |
| `UserProblem` | `num_submissions` | **Derived** | Local `Submission` Table | `COUNT(Submission)` for `problem_id` |
| `UserProblem` | `num_accepted` | **Derived** | Local `Submission` Table | `COUNT(Submission WHERE result='Accepted')` |
| `UserProblem` | `attempts_before_ac` | **Derived** | Local `Submission` Table | 1-indexed count of submissions up to first Accepted |
