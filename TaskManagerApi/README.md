# Project Management API with RBAC, Notifications & Audit Tracking

A RESTful **Project Management API** built using **FastAPI**, **SQLite**, **SQLAlchemy ORM**, **Pydantic**, and **JWT Authentication**.

This application provides project and task management with **Role-Based Access Control (RBAC)**. It also includes a complete **Notification System**, **Activity Tracking**, and **Audit Logging System** for monitoring user actions and system changes.

---

# Features

## Authentication & Authorization

- User Registration
- User Login
- JWT Authentication
- Password Hashing using bcrypt
- Protected API routes
- Current logged-in user endpoint
- Role-Based Access Control

Supported roles:

- Admin
- Manager
- Member

---

# Project Management

Users can manage projects with:

- Create projects
- View projects
- Update projects
- Delete projects
- Add project members
- View project members
- Remove project members

---

# Task Management

Task features:

- Create tasks
- View assigned tasks
- View single task details
- Update tasks
- Delete tasks

Each task contains:

- Title
- Description
- Status
- Priority
- Due Date
- Assigned User
- Project ID

Task Status:

- Pending
- In Progress
- Completed

Task Priority:

- Low
- Medium
- High

---

# Notification System

The system automatically creates notifications for important events.

Notifications are generated when:

- A task is assigned
- A task is reassigned
- A user is added to a project


Notification APIs:

- Get all notifications
- Get unread notifications
- Mark notification as read
- Mark all notifications as read
- Delete notification

---

# Activity Tracking System

The application records important user activities.

Tracked activities:

- Project Created
- Project Updated
- Project Deleted
- Task Created
- Task Updated
- Task Deleted
- Member Added
- Member Removed


Activity APIs:

- Get all activities
- Get activities by user
- Get activities by project
- Filter activities by action
- Filter activities by date

---

# Audit Logging System

Audit logs maintain a history of changes made in the application.

Tracked information:

- Entity Type
- Entity ID
- Field Name
- Old Value
- New Value
- Changed By User
- Changed Date


Examples:

- Task status change
- Task reassignment
- Project update
- Member changes

---

# Technology Stack

| Technology | Purpose |
|------------|---------|
| Python 3.12 | Programming Language |
| FastAPI | REST API Framework |
| SQLite | Database |
| SQLAlchemy | ORM |
| Pydantic | Data Validation |
| python-jose | JWT Authentication |
| Passlib | Password Hashing |
| bcrypt | Encryption |
| Uvicorn | ASGI Server |

---

`tasks.db` is created automatically when the application starts.

---

# Installation

## Clone Repository

```bash
cd Project-Management-API
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

---

## Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Application URL:

```
http://127.0.0.1:8000
```

---

# API Documentation

Swagger UI:

```
http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

---

# API Endpoints


## Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | /auth/signup | Register new user |
| POST | /auth/login | Login and generate JWT token |
| GET | /auth/me | Get current user |


---

## Projects

| Method | Endpoint | Description |
|---|---|---|
| POST | /projects | Create project |
| GET | /projects | Get projects |
| PUT | /projects/{id} | Update project |
| DELETE | /projects/{id} | Delete project |


---

## Project Members

| Method | Endpoint | Description |
|---|---|---|
| POST | /projects/{id}/members | Add member |
| GET | /projects/{id}/members | Get project members |
| DELETE | /projects/{id}/members/{user_id} | Remove member |


---

## Tasks

| Method | Endpoint | Description |
|---|---|---|
| POST | /tasks | Create task |
| GET | /tasks | Get tasks |
| GET | /tasks/{task_id} | Get task details |
| PUT | /tasks/{task_id} | Update task |
| DELETE | /tasks/{task_id} | Delete task |


---

## Notifications

| Method | Endpoint | Description |
|---|---|---|
| GET | /notifications | Get notifications |
| GET | /notifications/unread | Get unread notifications |
| PUT | /notifications/{id}/read | Mark notification read |
| PUT | /notifications/read-all | Mark all notifications read |
| DELETE | /notifications/{id} | Delete notification |


---

## Activities

| Method | Endpoint | Description |
|---|---|---|
| GET | /activities | Get all activities |
| GET | /activities/user/{id} | User activities |
| GET | /activities/project/{id} | Project activities |
| GET | /activities/action/{action} | Filter by action |
| GET | /activities/date | Filter by date |


---

## Audit Logs

| Method | Endpoint | Description |
|---|---|---|
| GET | /audit-logs | Get all audit logs |
| GET | /audit-logs/{entity_type}/{entity_id} | Get entity audit history |

---

# Security Implementation

Implemented security:

- JWT token authentication
- Secure password hashing
- Protected routes
- Role-based permissions
- User-specific task access
- Unauthorized access handling


---

# Role Permissions

| Feature | Admin | Manager | Member |
|-|-|-|-|
| Create Project | Yes | Yes | No |
| Manage Members | Yes | Yes | No |
| Create Task | Yes | Yes | No |
| Update Task | Yes | Yes | Limited |
| Delete Task | Yes | Yes | No |
| View Notifications | Yes | Yes | Yes |
| View Activities | Yes | Yes | Yes |
| View Audit Logs | Yes | Yes | Yes |

---

# Database Models

The application contains:

### User

Stores:

- Name
- Email
- Password
- Role


### Project

Stores:

- Project name
- Description
- Creator


### Project Member

Stores:

- Project ID
- User ID


### Task

Stores:

- Task details
- Status
- Priority
- Due date
- Assigned user


### Notification

Stores:

- Notification title
- Message
- Read status


### Activity Log

Stores:

- User actions
- Entity information
- Timestamp


### Audit Log

Stores:

- Previous values
- New values
- Changed user
- Timestamp

---

# Testing

APIs tested using:

- FastAPI Swagger UI
- JWT Authorization


Tested modules:

✅ User Signup  
✅ User Login  
✅ JWT Authentication  
✅ Project Management  
✅ Project Members  
✅ Task Management  
✅ Notifications  
✅ Activity Logs  
✅ Audit Logs  


---

# HTTP Status Codes

| Code | Meaning |
|-|-|
| 200 | Successful Request |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Server Error |

---

# Future Enhancements

- PostgreSQL support
- Docker deployment
- Background notification workers
- Email notifications
- Automated testing
- Pagination
- Advanced searching
- Frontend integration


---

# Author

**Developed by: Gayathri**

Backend Developer Evaluation Project

Built using:

**FastAPI + SQLAlchemy + JWT + RBAC + Notifications + Activity Tracking + Audit Logging**