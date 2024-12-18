# ===========================================================
# Cloud Service Access Management System
# ===========================================================
# This script implements the backend system for managing cloud
# service access based on user subscriptions. It includes CRUD
# operations for permissions, plans, and user subscriptions,
# along with access control and usage tracking.

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import json

# ===========================================================
# DATABASE SETUP
# ===========================================================
DATABASE_URL = "sqlite:///./test.db"

# Database connection and session setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# ===========================================================
# MODELS
# ===========================================================
class Permission(Base):
    """Represents a permission granting access to a specific API endpoint."""
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    endpoint = Column(String)
    description = Column(Text)

class Plan(Base):
    """Represents a subscription plan with associated permissions and limits."""
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(Text)
    permissions_json = Column(Text)  # Stores permissions as JSON string
    limits_json = Column(Text)  # Stores limits as JSON string

    def get_permissions(self):
        return json.loads(self.permissions_json) if self.permissions_json else []

    def get_limits(self):
        return json.loads(self.limits_json) if self.limits_json else {}

class Subscription(Base):
    """Associates a user with a subscription plan."""
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, index=True)
    plan_id = Column(Integer, ForeignKey("plans.id"))
    plan = relationship("Plan", backref="subscriptions")

class Usage(Base):
    """Tracks the number of times a user has called a specific API."""
    __tablename__ = "usage"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    api_name = Column(String)
    count = Column(Integer, default=0)

# Create all tables
Base.metadata.create_all(bind=engine)

# ===========================================================
# SCHEMAS
# ===========================================================
class PermissionCreate(BaseModel):
    name: str
    endpoint: str
    description: Optional[str] = None

class PlanCreate(BaseModel):
    name: str
    description: str
    permissions: List[str] = Field(default_factory=list)
    limits: Dict[str, int] = Field(default_factory=dict)

class SubscriptionCreate(BaseModel):
    user_id: int
    plan_id: int

class UsageStats(BaseModel):
    api_name: str
    used: int
    limit: Optional[int]

# ===========================================================
# DEPENDENCIES
# ===========================================================
def get_db():
    """Provides a database session to API endpoints."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ===========================================================
# APPLICATION SETUP
# ===========================================================
app = FastAPI(title="Cloud Service Access Management System")

# ===========================================================
# API ENDPOINTS
# ===========================================================

# Permissions Management
@app.post("/permissions", response_model=dict)
def create_permission(perm: PermissionCreate, db=Depends(get_db)):
    """Creates a new permission."""
    if db.query(Permission).filter(Permission.name == perm.name).first():
        raise HTTPException(status_code=400, detail="Permission already exists.")
    new_perm = Permission(name=perm.name, endpoint=perm.endpoint, description=perm.description)
    db.add(new_perm)
    db.commit()
    db.refresh(new_perm)
    return {"status": "success", "permission_id": new_perm.id}

# Subscription Plan Management
@app.post("/plans", response_model=dict)
def create_plan(plan: PlanCreate, db=Depends(get_db)):
    """Creates a new subscription plan."""
    if db.query(Plan).filter(Plan.name == plan.name).first():
        raise HTTPException(status_code=400, detail="Plan already exists.")
    new_plan = Plan(
        name=plan.name,
        description=plan.description,
        permissions_json=json.dumps(plan.permissions),
        limits_json=json.dumps(plan.limits)
    )
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return {"status": "success", "plan_id": new_plan.id}

# User Subscription Handling
@app.post("/subscriptions", response_model=dict)
def subscribe_user(sub: SubscriptionCreate, db=Depends(get_db)):
    """Subscribes a user to a plan."""
    existing_sub = db.query(Subscription).filter(Subscription.user_id == sub.user_id).first()
    if existing_sub:
        raise HTTPException(status_code=400, detail="User already subscribed. Update plan instead.")
    plan = db.query(Plan).filter(Plan.id == sub.plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found.")
    new_sub = Subscription(user_id=sub.user_id, plan_id=sub.plan_id)
    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)
    return {"status": "success", "subscription_id": new_sub.id}

# Access Control
@app.get("/access/{user_id}/{api_name}", response_model=dict)
def check_access(user_id: int, api_name: str, db=Depends(get_db)):
    """Checks if a user has access to an API and enforces limits."""
    sub = db.query(Subscription).filter(Subscription.user_id == user_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found.")
    if api_name not in sub.plan.get_permissions():
        return {"access": False, "reason": "Permission not granted."}
    usage = db.query(Usage).filter(Usage.user_id == user_id, Usage.api_name == api_name).first()
    used = usage.count if usage else 0
    limit = sub.plan.get_limits().get(api_name)
    if limit is not None and used >= limit:
        return {"access": False, "reason": "Usage limit reached."}
    return {"access": True}

# Usage Tracking
@app.post("/usage/{user_id}", response_model=dict)
def track_usage(user_id: int, api_name: str, db=Depends(get_db)):
    """Tracks usage of an API by a user."""
    sub = db.query(Subscription).filter(Subscription.user_id == user_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found.")
    if api_name not in sub.plan.get_permissions():
        raise HTTPException(status_code=403, detail="No permission for this API.")
    usage = db.query(Usage).filter(Usage.user_id == user_id, Usage.api_name == api_name).first()
    if not usage:
        usage = Usage(user_id=user_id, api_name=api_name, count=1)
        db.add(usage)
    else:
        usage.count += 1
    db.commit()
    return {"status": "success", "new_count": usage.count}
