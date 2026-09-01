# LeetCode Personal Analytics & Prediction System

A single-user system that collects LeetCode activity through a Chrome Extension (Manifest V3), stores data in MySQL, analyzes problem-solving behavior, visualizes performance via a React dashboard, and uses Machine Learning to predict solving probability and contest ratings.

## Tech Stack
- **Database**: MySQL, SQLAlchemy
- **Backend**: Python, FastAPI
- **Data Science & ML**: Pandas, NumPy, Scikit-Learn
- **Frontend**: React
- **Extension**: Chrome Extension (Manifest V3)

## Project Structure
```text
leetcode-analytics/
├── docs/             # Technical documentation & ER diagrams
├── database/         # SQL DDL schemas, views, indexes & queries
├── extension/        # Chrome Extension Manifest V3 source code
├── backend/          # FastAPI REST API services, schemas & routes
├── ml/               # Machine Learning features, models & notebooks
├── frontend/         # React visual dashboard
└── tests/            # Database, backend, extension & ML test suites
```

## Getting Started
1. Configure environment variables by copying `.env.example` to `.env`.
2. Initialize MySQL database using `database/schema.sql`.
3. Install backend dependencies and launch FastAPI dev server.
