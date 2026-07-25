from fastapi import FastAPI
from .routers import projects
from .database import Base, engine
from .auth import router as auth_router

from .routers import (
    projects,
    members,
    tasks,
    notification,
    activities,
    audit_logs
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Project Management API",
    description="Project Management API with RBAC, Notifications, Activity Logs and Audit Logs",
    version="4.0.0"
)

app.include_router(auth_router)
app.include_router(projects.router)
app.include_router(members.router)
app.include_router(tasks.router)
app.include_router(notification.router)
app.include_router(activities.router)
app.include_router(audit_logs.router)


@app.get("/")
def root():
    return {
        "message": "Project Management API is running successfully.",
        "version": "4.0.0",
        "documentation": "/docs"
    }