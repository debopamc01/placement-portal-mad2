from enum import StrEnum

class UserRole(StrEnum):
    ADMIN = 'admin'
    COMPANY = 'company'
    STUDENT = 'student'

class CompanyApprovalStatus(StrEnum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    BLACKLISTED = 'blacklisted'

class PlacementDriveStatus(StrEnum):
    PENDING = 'pending'
    ACTIVE = 'active'
    DECLINED = 'declined'
    CLOSED = 'closed'

class JobApplicationStatus(StrEnum):
    APPLIED = 'applied'
    SHORTLISTED = 'shortlisted'
    SELECTED = 'selected'
    REJECTED = 'rejected'
    CLOSED = 'closed'