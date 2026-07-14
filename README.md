# Placement Portal

A full-stack Placement Portal developed using **Flask**, **Vue.js**, **SQLite**, **Redis**, and **Celery**. The application provides role-based access for **Administrators**, **Companies**, and **Students** to manage campus placement activities through a modern web interface.

---

## Features

### Administrator

- Manage companies, students, placement drives, and applications
- Approve, reject, and blacklist company registrations
- View placement statistics
- Receive automated monthly placement reports via email

### Company

- Register and maintain company profile
- Create, edit, approve, close, and reopen placement drives
- Review applicants
- Update application status

### Student

- Register and maintain student profile
- Browse placement drives
- Apply for placement drives
- Track application status
- Export placement application history as CSV

---

# Technology Stack

## Frontend

- Vue.js 3
- Vue Router
- Pinia
- Bootstrap 5
- Vite

## Backend

- Flask
- SQLAlchemy ORM
- Flask-Login
- Flask-Mail
- SQLite

## Background Processing

- Celery
- Celery Beat
- Redis

## Testing

- Pytest

---

# Project Structure

```
placement-portal/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── router/
│   │   ├── stores/
│   │   └── common/
│   └── ...
│
├── backend/
│   ├── backend_app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── tasks/
│   │   ├── templates/
│   │   └── utils/
│   │
│   ├── celery_utils/
│   │   ├── celery_app.py
│   │   └── celery_main.py
│   │
│   ├── test/
│   ├── config.py
│   ├── main.py
│   └── pyproject.toml
│
├── LICENSE
└── README.md
```

---

# Architecture

The application follows a layered architecture.

```
Vue Frontend
        │
 REST API (Flask)
        │
Business Services
        │
SQLAlchemy Models
        │
SQLite Database
```

Background jobs are handled independently using Celery.

```
User Request / Celery Beat
            │
            ▼
       Celery Task
            │
            ▼
     Business Service
            │
            ▼
Database / Email / CSV
```

---

# Authentication

Authentication is implemented using **Flask-Login** with session-based authentication.

The application supports three roles:

- Administrator
- Company
- Student

Authorization is enforced on all protected API endpoints.

---

# Background Jobs

The project implements three asynchronous jobs using **Celery** and **Redis**.

### Daily Deadline Reminder

Runs once every day.

- Finds placement drives approaching their application deadline.
- Sends reminder emails to students who have not yet applied.

### Monthly Placement Report

Runs on the first day of every month.

Generates an HTML report containing:

- Placement drives created during the previous month
- Number of applications received
- Number of selected applications

The report is emailed to the administrator.

### Export Application History

Triggered by a student from the dashboard.

The request immediately returns while a Celery worker:

- Generates a CSV containing the student's application history.
- Emails the CSV as an attachment.

---

# Email Support

Emails are sent using **Flask-Mail** with Gmail SMTP.

The project currently sends:

- Daily reminder emails
- Monthly administrator reports
- Student application history exports

Email templates are implemented using **Jinja2**.

---

# Environment Variables

Create a `.env` file inside the `backend` directory.

```env
MAIL_ADDRESS=your_email@gmail.com
MAIL_PASSWORD=your_gmail_app_password

ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=your_admin_password
```

> **Note:** For Gmail, `MAIL_PASSWORD` should be an App Password generated after enabling Two-Factor Authentication.

---

# Running the Project

## Backend

```bash
cd backend

uv sync

uv run main.py
```

## Frontend

```bash
cd frontend

npm install

npm run dev
```

## Redis

```bash
cd backend

./launch_redis_server.sh
```

## Celery Worker

```bash
cd backend

./launch_celery_worker.sh
```

## Celery Beat

```bash
cd backend

./launch_celery_beat.sh
```

---

# Running Tests

```bash
cd backend

uv run pytest
```

---