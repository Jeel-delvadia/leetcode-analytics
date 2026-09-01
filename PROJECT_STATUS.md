# LeetCode Personal Analytics & Prediction System — Project Status

## Project Overview
**Goal**: Build a single-user system that collects LeetCode data via a Chrome Extension (Manifest V3), stores it in a MySQL database, analyzes problem-solving performance, visualizes statistics via a React dashboard, and uses Machine Learning to predict solving probabilities and contest ratings.

- **GitHub Repository**: [https://github.com/Jeel-delvadia/leetcode-analytics](https://github.com/Jeel-delvadia/leetcode-analytics)
- **Primary Branch**: `main`

---

## How to Run the Application

### 1. FastAPI Backend Server
Run from the root repository directory (`D:\lc\leetcode-analytics`):

```cmd
# Terminal 1 - Backend Server
cd D:\lc\leetcode-analytics
venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000 --app-dir backend
```
*API Base URL*: `http://localhost:8000`  
*Swagger Documentation*: `http://localhost:8000/docs`

---

### 2. React Frontend Dashboard
Run from the `frontend` directory (`D:\lc\leetcode-analytics\frontend`):

```cmd
# Terminal 2 - Frontend App
cd D:\lc\leetcode-analytics\frontend
npm install
npm run dev
```
*Dashboard Web URL*: `http://localhost:5173`

---

### 3. Chrome Extension (Manifest V3)
1. Open Google Chrome and navigate to: `chrome://extensions/`
2. Enable **Developer mode** toggle in the top-right corner.
3. Click **Load unpacked** in the top-left menu.
4. Select the **`extension`** folder: `D:\lc\leetcode-analytics\extension`
5. Open `https://leetcode.com`, click the extension icon, and press **Trigger Full Sync**.

---

### 4. Running Test Suites
Run unit tests from the root directory:

```cmd
# Schema & Database Verification Test
venv\Scripts\python.exe tests/database/test_schema.py

# FastAPI Sync API Test
venv\Scripts\python.exe -c "import sys; sys.path.insert(0, 'backend'); from tests.backend.test_sync_api import test_root_endpoint, test_sync_status_endpoint; test_root_endpoint(); test_sync_status_endpoint(); print('API PASSED')"

# Phase 6 Continuous Data Update Test
venv\Scripts\python.exe tests/backend/test_phase6_verification.py
```

---

## Current Status Summary
- **Current Phase**: Phase 7 (User Problem Analytics)
- **Phase 1 Progress**: 100% Repository Setup & Tech Stack Configured
- **Phase 2 Progress**: 100% Database Schema & SQLAlchemy ORM Models Completed
- **Phase 3 Progress**: 100% Database Indexes, Seed Data & Validation Passing
- **Phase 4 Progress**: 100% LeetCode GraphQL Endpoints & Field Mapping Documented
- **Phase 5 Progress**: 100% Chrome Extension Initial Sync & Backend Endpoint Completed
- **Phase 6 Progress**: 100% Real-time Incremental Submission Capture & Reconciler Completed
- **Overall Progress**: ~30%

---

## Completed Milestones & Prompt History

### Prompt 1: Initial Folder Structure Creation
- Created full workspace directory tree under `leetcode-analytics/`:
  - `docs/`, `database/`, `extension/`, `backend/`, `ml/`, `frontend/`, `tests/`
  - Core root files: `README.md`, `PROJECT_STATUS.md`, `TODO.md`, `CHANGELOG.md`, `.gitignore`, `.env.example`

### Prompt 2, 3 & 4: Master 21-Phase Project Plan
- Created comprehensive `TODO.md` roadmap covering setup, DB design, sync engine, analytics, ML models, dashboard, and testing.

### Prompt 5: Database Design & Schema Implementation
- Created ASCII ER Diagram in `docs/database.md`.
- Created `database/schema.sql` DDL for all 10 core tables (`Problem`, `Topic`, `ProblemTopic`, `Submission`, `UserProblem`, `ProblemSimilarity`, `TopicPrerequisite`, `Contest`, `ContestParticipation`, `SyncHistory`).
- Implemented SQLAlchemy ORM classes in `backend/app/database/models.py`.

### Prompt 6 & 7: GitHub Remote Setup & Initial Push
- Configured Git remote `origin` to `https://github.com/Jeel-delvadia/leetcode-analytics.git`.
- Pushed initial codebase to `main` branch.

### Prompt 8: Data Sources & Network Protocol
- Documented LeetCode GraphQL endpoints, queries, variables, and response mapping in `docs/data-sources.md`.

### Prompt 9: Data Collection & Incremental Sync Engine
- Built Chrome extension Manifest V3 background service worker, pagination collectors, and DOM content scripts.
- Built FastAPI sync API routes (`POST /api/v1/sync/initial`, `POST /api/v1/sync/submission`, `GET /api/v1/sync/status`).
- Implemented `SyncService` for upserting problems, submissions, user-problem state, and sync logging.
- Created empirical test suite (`tests/backend/test_phase6_verification.py`).

---

## Workspace Map

| File / Folder | Status | Description |
|---|---|---|
| [TODO.md](file:///d:/lc/leetcode-analytics/TODO.md) | Active | Master 21-phase task list |
| [PROJECT_STATUS.md](file:///d:/lc/leetcode-analytics/PROJECT_STATUS.md) | Updated | Current project status, execution guide & GitHub log |
| [database/schema.sql](file:///d:/lc/leetcode-analytics/database/schema.sql) | Completed | MySQL DDL table definitions |
| [docs/database.md](file:///d:/lc/leetcode-analytics/docs/database.md) | Completed | ER Diagram & Table Specifications |
| [docs/data-sources.md](file:///d:/lc/leetcode-analytics/docs/data-sources.md) | Completed | LeetCode GraphQL endpoints & field mapping |
| [docs/extension-guide.md](file:///d:/lc/leetcode-analytics/docs/extension-guide.md) | Completed | Chrome extension development & store publishing guide |
| [backend/app/main.py](file:///d:/lc/leetcode-analytics/backend/app/main.py) | Completed | FastAPI app entrypoint & middleware |
| [backend/app/database/models.py](file:///d:/lc/leetcode-analytics/backend/app/database/models.py) | Completed | SQLAlchemy ORM models |
| [backend/app/services/sync_service.py](file:///d:/lc/leetcode-analytics/backend/app/services/sync_service.py) | Completed | Initial & incremental data sync logic |
| [extension/manifest.json](file:///d:/lc/leetcode-analytics/extension/manifest.json) | Completed | Chrome Extension Manifest V3 configuration |
| [extension/src/background/service-worker.js](file:///d:/lc/leetcode-analytics/extension/src/background/service-worker.js) | Completed | Extension background worker |
| [extension/src/content/leetcode-page.js](file:///d:/lc/leetcode-analytics/extension/src/content/leetcode-page.js) | Completed | Page DOM submission listener script |
| [frontend/package.json](file:///d:/lc/leetcode-analytics/frontend/package.json) | Completed | React + Vite dashboard configuration |
