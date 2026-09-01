# LeetCode Personal Analytics & Prediction System

## Project Goal

Build a single-user system that collects LeetCode data through a Chrome
extension, stores it in MySQL, analyzes the user's problem-solving behavior,
visualizes progress, and uses ML to predict solving ability and future progress.

---

# PHASE 1 — PROJECT SETUP

## Project Structure

- [x] Create GitHub repository (Git repo initialized)
- [x] Create project folder structure
- [x] Create README.md
- [x] Create PROJECT_STATUS.md
- [x] Create TODO.md
- [x] Create CHANGELOG.md
- [x] Create docs/
- [x] Create database/
- [x] Create extension/
- [x] Create backend/
- [x] Create ml/
- [x] Create frontend/
- [x] Create tests/
- [x] Create .gitignore
- [x] Create .env.example
- [x] Make first Git commit

## Technologies

- [x] Setup MySQL (DDL Schema & Connection configured)
- [x] Setup Python virtual environment (venv initialized)
- [x] Setup FastAPI (FastAPI app configured in main.py)
- [x] Setup SQLAlchemy (Connection engine & SessionLocal configured)
- [x] Setup MySQL Python driver (PyMySQL installed & configured)
- [x] Setup Pandas (Dependencies installed)
- [x] Setup NumPy (Dependencies installed)
- [x] Setup Scikit-learn (Dependencies installed)
- [x] Setup Matplotlib (Dependencies installed)
- [x] Setup Chrome Extension Manifest V3 (manifest.json & popup.html configured)
- [x] Setup React (frontend package.json & Vite setup)
- [x] Setup chart library (Recharts dependency configured)

---

# PHASE 2 — DATABASE DESIGN

## Problem Data

### Problem table

- [x] Create Problem table
- [x] Store LeetCode problem ID
- [x] Store frontend ID
- [x] Store title
- [x] Store title slug
- [x] Store difficulty
- [x] Store acceptance rate
- [x] Store total submissions
- [x] Store total accepted
- [x] Store paid/free status
- [x] Store problem URL

### Topic table

- [x] Create Topic table
- [x] Store topic ID
- [x] Store topic name
- [x] Store topic description

### ProblemTopic table

- [x] Create ProblemTopic table
- [x] Connect problems with topics
- [x] Support multiple topics per problem

### ProblemSimilarity table

- [x] Create ProblemSimilarity table
- [x] Store problem → similar problem relationship
- [x] Store similarity score
- [x] Store source of similarity

### TopicPrerequisite table

- [x] Create TopicPrerequisite table
- [x] Store topic → prerequisite topic
- [x] Store prerequisite strength

---

## User Problem Data

### UserProblem table

- [x] Create UserProblem table
- [x] Store problem ID
- [x] Store solved/attempted status
- [x] Store number of submissions
- [x] Store number of accepted submissions
- [x] Store first submission time
- [x] Store last submission time
- [x] Store first accepted time
- [x] Store last result
- [x] Store attempts before AC

### Submission table

- [x] Create Submission table
- [x] Store submission ID
- [x] Store problem ID
- [x] Store submission time
- [x] Store result
- [x] Store language
- [x] Store runtime
- [x] Store memory

---

## Contest Data

### Contest table

- [x] Create Contest table
- [x] Store contest ID
- [x] Store contest name
- [x] Store contest slug
- [x] Store contest date
- [x] Store contest type

### ContestParticipation table

- [x] Create ContestParticipation table
- [x] Store contest ID
- [x] Store attended status
- [x] Store rank
- [x] Store score
- [x] Store rating before contest
- [x] Store rating after contest
- [x] Store rating change
- [x] Store problems attempted
- [x] Store problems solved

---

## Synchronization

### SyncHistory table

- [x] Create SyncHistory table
- [x] Store sync type
- [x] Store start time
- [x] Store completion time
- [x] Store records fetched
- [x] Store sync status

---

# PHASE 3 — DATABASE VALIDATION

## Relationships

- [x] Problem → UserProblem
- [x] Problem → Submission
- [x] Problem → ProblemTopic
- [x] Topic → ProblemTopic
- [x] Problem → ProblemSimilarity
- [x] Topic → TopicPrerequisite
- [x] Contest → ContestParticipation

## Constraints

- [x] Add primary keys
- [x] Add foreign keys
- [x] Add unique constraints
- [x] Add required NOT NULL constraints
- [x] Add difficulty validation
- [x] Add result validation
- [x] Add useful indexes (database/indexes.sql)
- [x] Test duplicate submissions (tests/database/test_schema.py)
- [x] Test duplicate problems (database/seed.sql)
- [x] Test foreign key errors (PRAGMA foreign_keys validation)

---

# PHASE 4 — LEETCODE NETWORK DATA

## Understand Requests

- [x] Understand Fetch/XHR requests
- [x] Understand HTTP POST
- [x] Understand GraphQL
- [x] Understand operationName
- [x] Understand query
- [x] Understand variables
- [x] Understand payload
- [x] Understand response
- [x] Understand authentication/session
- [x] Understand cookies
- [x] Understand pagination
- [x] Understand skip
- [x] Understand limit

## Find Required LeetCode Data

- [x] Find problem information request (`problemsetQuestionList`)
- [x] Find user progress request (`userProfileUserQuestionProgressV2`)
- [x] Find submission history request (`submissionList`)
- [x] Find contest history request (`userContestRankingInfo`)
- [x] Find problem topics (`topicTags`)
- [x] Find similar questions (`similarQuestions`)
- [x] Find acceptance rate (`acRate`)
- [x] Find submission result (`statusDisplay`)
- [x] Find submission time (`timestamp`)
- [x] Find runtime (`runtime`)
- [x] Find memory (`memory`)
- [x] Find contest rating (`rating`)
- [x] Find contest rank (`ranking`)

## Document Requests

- [x] Document request URL (docs/data-sources.md)
- [x] Document request method (POST / GraphQL)
- [x] Document operationName
- [x] Document required variables
- [x] Document useful response fields
- [x] Document pagination
- [x] Document authentication requirements
- [x] Map every response field to database column (docs/data-sources.md)

---

# PHASE 5 — INITIAL DATA COLLECTION

## Initial Synchronization

- [ ] Create extension
- [ ] Create Manifest V3
- [ ] Create background service worker
- [ ] Create LeetCode data collector
- [ ] Fetch problem list
- [ ] Fetch user progress
- [ ] Handle skip/limit pagination
- [ ] Fetch all pages
- [ ] Fetch submission history
- [ ] Fetch contest history
- [ ] Fetch problem topics
- [ ] Fetch similar problems

## Store Data

- [ ] Send problem data to FastAPI
- [ ] Insert/update Problem
- [ ] Insert/update Topic
- [ ] Insert ProblemTopic
- [ ] Insert Submission
- [ ] Insert/update UserProblem
- [ ] Insert ProblemSimilarity
- [ ] Insert Contest
- [ ] Insert ContestParticipation
- [ ] Record SyncHistory

## Validate

- [ ] Compare fetched problem count with LeetCode
- [ ] Compare solved count
- [ ] Compare submission count
- [ ] Compare contest count
- [ ] Check missing problems
- [ ] Check duplicate records
- [ ] Check incorrect relationships

---

# PHASE 6 — CONTINUOUS DATA UPDATE

## New Submission

When the user submits a new solution:

- [ ] Detect new submission
- [ ] Obtain submission details
- [ ] Check whether submission already exists
- [ ] Insert new Submission
- [ ] Update UserProblem
- [ ] Update number of attempts
- [ ] Update last result
- [ ] Update solved status
- [ ] Update first AC if applicable
- [ ] Update last submission time

## Periodic Synchronization

- [ ] Store last synchronization time
- [ ] Fetch only required new data
- [ ] Detect activity outside extension
- [ ] Reconcile missed submissions
- [ ] Prevent duplicate records
- [ ] Update SyncHistory

---

# PHASE 7 — USER PROBLEM ANALYSIS

For every problem the user attempted, calculate:

- [ ] Number of attempts
- [ ] Number of AC
- [ ] Number of WA
- [ ] Number of TLE
- [ ] Number of MLE
- [ ] First-attempt AC
- [ ] Attempts before AC
- [ ] Time between first attempt and AC
- [ ] Last result
- [ ] Solved status
- [ ] Number of failed attempts before solving

Example output:

```text
Problem: Binary Search

- Attempts: 4
- Solved: Yes
- First AC: Attempt 4
- WA: 2
- TLE: 1
- Acceptance rate: 46%
- Difficulty: Medium
```

---

# PHASE 8 — TOPIC ANALYSIS

For every topic:

- [ ] Count total problems
- [ ] Count solved problems
- [ ] Count attempted problems
- [ ] Count unsolved problems
- [ ] Calculate solving percentage
- [ ] Calculate average attempts
- [ ] Calculate AC rate
- [ ] Calculate WA rate
- [ ] Calculate TLE rate
- [ ] Calculate Easy solved
- [ ] Calculate Medium solved
- [ ] Calculate Hard solved
- [ ] Find last practice date
- [ ] Calculate days since last practice
- [ ] Calculate topic mastery score

---

# PHASE 9 — DIFFICULTY ANALYSIS

- [ ] Count Easy solved
- [ ] Count Medium solved
- [ ] Count Hard solved
- [ ] Calculate Easy success rate
- [ ] Calculate Medium success rate
- [ ] Calculate Hard success rate
- [ ] Calculate average attempts by difficulty
- [ ] Calculate first-attempt AC rate by difficulty
- [ ] Track difficulty progression over time
- [ ] Identify difficulty level where performance decreases

---

# PHASE 10 — TOPIC PROGRESSION

Use TopicPrerequisite to analyze learning progression.

Example:

```text
DFS
↓
BFS
↓
Topological Sort
↓
Shortest Path
↓
Dijkstra
```

Implement:

- [ ] Find solved topics
- [ ] Find unsolved prerequisite topics
- [ ] Check prerequisite completion
- [ ] Find topics whose prerequisites are satisfied
- [ ] Identify possible next topics
- [ ] Rank possible next topics
- [ ] Generate next-topic candidates

Example:

```text
Solved:
DFS
BFS
Topological Sort

Possible next:
Shortest Path
Dijkstra
```

---

# PHASE 11 — SIMILAR PROBLEM ANALYSIS

For every candidate problem:

- [ ] Get similar problems
- [ ] Check which similar problems user solved
- [ ] Count solved similar problems
- [ ] Count unsolved similar problems
- [ ] Calculate percentage of similar problems solved
- [ ] Check difficulty of similar solved problems
- [ ] Check topics of similar solved problems
- [ ] Calculate similarity-based readiness

Example:

```text
Candidate:
Course Schedule II

Similar:
Course Schedule       ✓
Parallel Courses      ✓
Alien Dictionary      ✗
Another Problem       ✓

Similar problems solved = 3/4
```

---

# PHASE 12 — PERSONALIZED PROBLEM DIFFICULTY

Calculate how difficult a problem appears for THIS user.

Use:

- [ ] Problem difficulty
- [ ] Acceptance rate
- [ ] User performance on same topic
- [ ] User performance on similar problems
- [ ] User's previous performance at same difficulty
- [ ] Average attempts
- [ ] Recent performance
- [ ] Similar-problem success
- [ ] Topic mastery

Create:

- [ ] Personalized difficulty score
- [ ] Easy-for-user classification
- [ ] Appropriate-for-user classification
- [ ] Challenging-for-user classification
- [ ] Very-difficult-for-user classification

---

# PHASE 13 — SOLVE PROBABILITY ML

## Define Target

- [ ] Define what "solve" means
- [ ] Define prediction point
- [ ] Prevent future information leakage
- [ ] Create historical training examples

## Features

- [ ] Problem difficulty
- [ ] Problem acceptance rate
- [ ] Problem topics
- [ ] User total solved
- [ ] User solved count for topic
- [ ] User topic success rate
- [ ] User average attempts
- [ ] User difficulty success rate
- [ ] User recent success rate
- [ ] User WA rate
- [ ] User TLE rate
- [ ] Similar problems solved
- [ ] Time since topic practice
- [ ] Recent solving velocity
- [ ] Number of previous attempts on related problems

## Models

- [ ] Create baseline model
- [ ] Train Logistic Regression
- [ ] Train Random Forest
- [ ] Train Gradient Boosting
- [ ] Compare models

## Evaluation

- [ ] Accuracy
- [ ] Precision
- [ ] Recall
- [ ] F1 score
- [ ] ROC-AUC
- [ ] Probability calibration
- [ ] Compare model against baseline

## Output

For a candidate:

```text
Problem: Dijkstra

Probability of solving:
74%
```

- [ ] Generate solve probability
- [ ] Generate confidence/range
- [ ] Test predictions on unseen problems

---

# PHASE 14 — PROBLEM SELECTION

Use all available information to select suitable problems.

For each unsolved problem calculate:

- [ ] Topic match
- [ ] Difficulty suitability
- [ ] Acceptance rate
- [ ] User topic performance
- [ ] Similar problems solved
- [ ] Personalized difficulty
- [ ] Solve probability
- [ ] Recent topic activity
- [ ] Prerequisite completion

Then:

- [ ] Generate candidate problems
- [ ] Remove solved problems
- [ ] Rank candidates
- [ ] Select suitable problems

Example:

```text
Dijkstra
Medium
Similar solved: 4/5
Topic mastery: High
Solve probability: 74%

→ Suitable candidate
```

---

# PHASE 15 — CONTEST ANALYSIS

- [ ] Store contest history
- [ ] Plot rating history
- [ ] Calculate average rank
- [ ] Calculate average score
- [ ] Calculate average problems solved
- [ ] Calculate rating change
- [ ] Analyze rating trend
- [ ] Analyze contest solving performance
- [ ] Analyze performance by contest

---

# PHASE 16 — CONTEST RATING PREDICTION

## Features

- [ ] Current rating
- [ ] Previous rating
- [ ] Rating trend
- [ ] Previous contest rank
- [ ] Previous contest score
- [ ] Problems solved in previous contests
- [ ] Recent LeetCode solving performance
- [ ] Difficulty performance

## Model

- [ ] Define target rating
- [ ] Create historical training data
- [ ] Train regression model
- [ ] Compare prediction models
- [ ] Evaluate prediction error
- [ ] Generate expected next rating
- [ ] Generate expected rating range

Example:

```text
Current rating: 1256

Expected next rating:
1280–1330
```

---

# PHASE 17 — PROGRESS FORECASTING

- [ ] Calculate problems solved per week
- [ ] Calculate problems solved per month
- [ ] Calculate recent solving velocity
- [ ] Calculate target remaining problems
- [ ] Estimate expected date to reach target
- [ ] Estimate topic completion date
- [ ] Compare expected vs actual progress

Example:

```text
Current: 232 solved
Target: 300 solved

Expected completion:
~8 weeks
```

---

# PHASE 18 — VISUALIZATION

## Overall Progress

- [ ] Total solved
- [ ] Easy/Medium/Hard distribution
- [ ] Problems solved over time
- [ ] Problems attempted over time
- [ ] Solving velocity

## Submission Analysis

- [ ] AC/WA/TLE distribution
- [ ] Attempts per problem
- [ ] Attempts by difficulty
- [ ] Average attempts over time

## Topic Analysis

- [ ] Problems solved per topic
- [ ] Topic mastery
- [ ] Topic success rate
- [ ] Weak topics
- [ ] Topic practice timeline

## Contest Analysis

- [ ] Rating history
- [ ] Rating change
- [ ] Rank history
- [ ] Problems solved per contest

## Prediction

- [ ] Solve probability
- [ ] Personalized difficulty
- [ ] Expected rating
- [ ] Expected completion date

---

# PHASE 19 — DASHBOARD

- [ ] Create React dashboard
- [ ] Connect React to FastAPI
- [ ] Display total progress
- [ ] Display topic performance
- [ ] Display difficulty performance
- [ ] Display submission statistics
- [ ] Display contest statistics
- [ ] Display weak topics
- [ ] Display next topic candidates
- [ ] Display candidate problems
- [ ] Display similar solved problems
- [ ] Display solve probability
- [ ] Display predicted rating
- [ ] Display expected progress date

---

# PHASE 20 — TESTING

## Database

- [ ] Test every table
- [ ] Test foreign keys
- [ ] Test duplicate prevention
- [ ] Test analytical queries
- [ ] Test indexes

## Data Collection

- [ ] Test initial synchronization
- [ ] Test pagination
- [ ] Test incomplete responses
- [ ] Test duplicate data
- [ ] Test new submissions
- [ ] Test missed submissions

## ML

- [ ] Test missing values
- [ ] Test prediction inputs
- [ ] Test unseen problems
- [ ] Test data leakage
- [ ] Test probability output
- [ ] Test model performance

## Dashboard

- [ ] Test API failures
- [ ] Test empty data
- [ ] Test charts
- [ ] Test recommendations/predictions
- [ ] Test different screen sizes

---

# PHASE 21 — FINAL PROJECT

- [ ] Complete ER diagram
- [ ] Complete relational schema
- [ ] Complete normalization explanation
- [ ] Complete architecture diagram
- [ ] Document LeetCode data collection
- [ ] Document database
- [ ] Document analytics
- [ ] Document ML features
- [ ] Document ML models
- [ ] Document prediction results
- [ ] Document recommendation logic
- [ ] Add screenshots
- [ ] Clean GitHub repository
- [ ] Remove secrets
- [ ] Complete README
- [ ] Prepare project presentation
- [ ] Prepare DBMS viva questions
- [ ] Prepare ML viva questions
- [ ] Prepare final demo
