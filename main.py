from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from asyncio import sleep

app = FastAPI()

# Mock Databases
plans_db: Dict[str, dict] = {}
permissions_db: Dict[str, dict] = {}
subscriptions_db: Dict[str, dict] = {}
usage_db: Dict[str, int] = {}

# Models
class Plan(BaseModel):
    name: str
    description: str
    permissions: List[str]
    usage_limit: int

class Permission(BaseModel):
    name: str
    api_endpoint: str
    description: str

class Subscription(BaseModel):
    user_id: str
    plan_name: str

# Root Endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Cloud Service Access Management System"}

# Cloud Service APIs (6 Random APIs)
@app.get("/service1")
async def service1():
    await sleep(0.1)
    return {"message": "Service 1 response"}

@app.get("/service2")
async def service2():
    await sleep(0.1)
    return {"message": "Service 2 response"}

@app.get("/service3")
async def service3():
    await sleep(0.1)
    return {"message": "Service 3 response"}

@app.get("/service4")
async def service4():
    await sleep(0.1)
    return {"message": "Service 4 response"}

@app.get("/service5")
async def service5():
    await sleep(0.1)
    return {"message": "Service 5 response"}

@app.get("/service6")
async def service6():
    await sleep(0.1)
    return {"message": "Service 6 response"}

# Subscription Plan Management
@app.post("/plans")
async def create_plan(plan: Plan):
    if plan.name in plans_db:
        raise HTTPException(status_code=400, detail="Plan already exists.")
    plans_db[plan.name] = plan.dict()
    return {"message": f"Plan '{plan.name}' created successfully"}

@app.put("/plans/{plan_name}")
async def modify_plan(plan_name: str, plan: Plan):
    if plan_name not in plans_db:
        raise HTTPException(status_code=404, detail="Plan not found.")
    plans_db[plan_name] = plan.dict()
    return {"message": f"Plan '{plan_name}' modified successfully"}

@app.delete("/plans/{plan_name}")
async def delete_plan(plan_name: str):
    if plan_name not in plans_db:
        raise HTTPException(status_code=404, detail="Plan not found.")
    del plans_db[plan_name]
    return {"message": f"Plan '{plan_name}' deleted successfully"}

# Permission Management
@app.post("/permissions")
async def add_permission(permission: Permission):
    if permission.name in permissions_db:
        raise HTTPException(status_code=400, detail="Permission already exists.")
    permissions_db[permission.name] = permission.dict()
    return {"message": f"Permission '{permission.name}' added successfully"}

@app.put("/permissions/{permission_name}")
async def modify_permission(permission_name: str, permission: Permission):
    if permission_name not in permissions_db:
        raise HTTPException(status_code=404, detail="Permission not found.")
    permissions_db[permission_name] = permission.dict()
    return {"message": f"Permission '{permission_name}' modified successfully"}

@app.delete("/permissions/{permission_name}")
async def delete_permission(permission_name: str):
    if permission_name not in permissions_db:
        raise HTTPException(status_code=404, detail="Permission not found.")
    del permissions_db[permission_name]
    return {"message": f"Permission '{permission_name}' deleted successfully"}

# User Subscription Handling
@app.post("/subscriptions")
async def subscribe_to_plan(subscription: Subscription):
    if subscription.user_id in subscriptions_db:
        raise HTTPException(status_code=400, detail="User already subscribed.")
    if subscription.plan_name not in plans_db:
        raise HTTPException(status_code=404, detail="Plan not found.")
    subscriptions_db[subscription.user_id] = {"plan_name": subscription.plan_name, "usage_count": 0}
    return {"message": f"User '{subscription.user_id}' subscribed to plan '{subscription.plan_name}'"}

@app.get("/subscriptions/{user_id}")
async def get_subscription_details(user_id: str):
    if user_id not in subscriptions_db:
        raise HTTPException(status_code=404, detail="Subscription not found.")
    return subscriptions_db[user_id]

# Access Control
@app.get("/access/{user_id}/{api_name}")
async def check_access(user_id: str, api_name: str):
    subscription = subscriptions_db.get(user_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found.")
    plan = plans_db.get(subscription["plan_name"])
    if api_name not in plan["permissions"]:
        return {"access": "denied", "reason": "API not included in the plan permissions."}
    if subscription["usage_count"] >= plan["usage_limit"]:
        return {"access": "denied", "reason": "Usage limit reached."}
    subscriptions_db[user_id]["usage_count"] += 1
    return {"access": "granted"}

# Usage Tracking
@app.get("/usage/{user_id}")
async def get_usage(user_id: str):
    if user_id not in subscriptions_db:
        raise HTTPException(status_code=404, detail="Subscription not found.")
    return {"user_id": user_id, "usage_count": subscriptions_db[user_id]["usage_count"]}

@app.post("/usage/{user_id}/track")
async def track_usage(user_id: str):
    if user_id not in subscriptions_db:
        raise HTTPException(status_code=404, detail="Subscription not found.")
    subscriptions_db[user_id]["usage_count"] += 1
    return {"message": "Usage tracked successfully"}
