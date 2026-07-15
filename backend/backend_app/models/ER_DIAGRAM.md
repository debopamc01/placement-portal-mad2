# Database ER Diagram

This diagram is based on the SQLAlchemy models in `backend_app/models`.
Table names use Flask-SQLAlchemy's default naming convention from the model class names.

```mermaid
erDiagram
    USER {
        int id PK
        string email UK
        string password_hash
        enum role
    }

    STUDENT {
        int id PK
        int user_id FK, UK
        string name
        string resume_filename
        string description
        boolean blacklisted
        string registered_at
    }

    COMPANY {
        int id PK
        int user_id FK, UK
        string name
        string hr_contact
        string website
        enum approval_status
        string registered_at
    }

    PLACEMENT_DRIVE {
        int id PK
        int company_id FK
        enum status
        string job_title
        string job_description
        string eligibility_criteria
        string application_deadline
        string created_at
    }

    JOB_APPLICATION {
        int id PK
        int student_id FK
        int placement_drive_id FK
        string application_date
        enum status
    }

    USER ||--o| STUDENT : "has profile"
    USER ||--o| COMPANY : "has profile"
    COMPANY ||--o{ PLACEMENT_DRIVE : "creates"
    STUDENT ||--o{ JOB_APPLICATION : "submits"
    PLACEMENT_DRIVE ||--o{ JOB_APPLICATION : "receives"
```

## Enum Values

- `USER.role`: `admin`, `company`, `student`
- `COMPANY.approval_status`: `pending`, `approved`, `rejected`, `blacklisted`
- `PLACEMENT_DRIVE.status`: `pending`, `active`, `declined`, `closed`
- `JOB_APPLICATION.status`: `applied`, `shortlisted`, `selected`, `rejected`

## Relationship Notes

- `student.user_id` is unique, so each student profile belongs to exactly one user.
- `company.user_id` is unique, so each company profile belongs to exactly one user.
- Deleting a user cascades to the linked student or company profile.
- Deleting a company cascades to its placement drives.
- Deleting a placement drive cascades to its job applications.
