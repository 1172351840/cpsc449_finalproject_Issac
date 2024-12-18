Project Title: Cloud Service Access Management System
Name: Issac Zhou
CWID: 885251249
Class: CPSC 449
Project Description:
This project implements a backend system that manages access to various cloud services based on user subscriptions. Users (customers) subscribe to plans, each plan defines which APIs the user can access and how many requests they can make before hitting the limit. Administrators can manage subscription plans, permissions, and user subscriptions. Once a user reaches their allocated limit for a certain service, their access is restricted until the limit resets or their subscription changes.

Key Features Implemented:

Subscription Plan Management:

Create, modify, and delete subscription plans.
Each plan has permissions (API endpoints allowed) and usage limits.
Permission Management:

Add, modify, or delete permissions (essentially the allowed APIs).
User Subscription Handling:

Customers can subscribe to a plan, view their subscription details and usage.
Admins can assign or modify a user's subscription plan.
Access Control:

Before serving any request, the system checks if the user’s subscription plan includes the requested API and if the user is within their usage limits.
Usage Tracking and Limit Enforcement:

The system tracks API usage per user. Once the user reaches the limit for a particular API, access is denied for that API.
Endpoints Overview:

Subscription Plan Management

POST /plans (Create a new plan)
PUT /plans/{planId} (Modify an existing plan)
DELETE /plans/{planId} (Delete a plan)
Permission Management

POST /permissions (Add Permission)
PUT /permissions/{permissionId} (Modify Permission)
DELETE /permissions/{permissionId} (Delete Permission)
User Subscription Handling

POST /subscriptions (Subscribe a user to a plan)
GET /subscriptions/{userId} (View a user's subscription details)
GET /subscriptions/{userId}/usage (View usage statistics for a user)
PUT /subscriptions/{userId} (Assign/Modify a user's plan)
Access Control

GET /access/{userId}/{apiRequest} (Check if the user has access to a given API)
Usage Tracking and Limit Enforcement

POST /usage/{userId} (Record an API request made by a user)
GET /usage/{userId}/limit (Check the user's current usage against the limit)
How to Run (For the Instructor):

Install dependencies:

bash

pip install fastapi uvicorn sqlalchemy pydantic
Start the server:

bash

uvicorn main:app --reload
The API documentation and interactive UI is available at:
http://127.0.0.1:8000/docs

Database:

This implementation uses SQLite for simplicity.
All data files are automatically generated upon first run.
Error Handling & Async Programming:

The project uses FastAPI’s async capabilities (e.g., async def endpoints).
Proper HTTP status codes and JSON responses are returned on errors.
Code Organization:

A single main.py file containing all routes, models, and logic for simplicity.
Clear comments are provided in the code to explain functionalities.
