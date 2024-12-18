# cpsc449_finalproject_Issac
# Cloud Service Access Management System

## Project Information
**Student Name**: Issac Zhou  
**CWID**: 885251249  
**Team Members**: This project was completed individually by Issac Zhou.

## Project Description
This backend system dynamically manages access to cloud services based on user subscriptions. The project is implemented using FastAPI and provides CRUD operations for managing permissions, subscription plans, user subscriptions, and API usage tracking. Access control is enforced based on defined permissions and usage limits.

## System Features
### 1. **Subscription Plan Management**
- Create, modify, and delete subscription plans.
- Each plan contains permissions (API access) and usage limits.

### 2. **Permission Management**
- Add, modify, and delete permissions that control API access.

### 3. **User Subscription Handling**
- Users can subscribe to a plan, view their subscription details, and track usage statistics.

### 4. **Access Control**
- Checks user access to APIs based on their subscription plan permissions and enforces limits.

### 5. **Usage Tracking**
- Tracks API requests made by users and temporarily restricts access when usage limits are reached.

## Technology Stack
- **Backend Framework**: FastAPI
- **Database**: SQLite (SQLAlchemy ORM)
- **Programming Language**: Python

## Setup and Installation
1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   uvicorn main:app --reload
   ```

4. **Access API Documentation**:
   Navigate to `http://127.0.0.1:8000/docs` in your browser to view the automatically generated API documentation by FastAPI.

## API Overview
### Permission Management
- `POST /permissions`: Create a new permission.
- `PUT /permissions/{permission_id}`: Update an existing permission.
- `DELETE /permissions/{permission_id}`: Delete a permission.

### Subscription Plan Management
- `POST /plans`: Create a new subscription plan.
- `PUT /plans/{plan_id}`: Update an existing plan.
- `DELETE /plans/{plan_id}`: Delete a plan.

### User Subscription Handling
- `POST /subscriptions`: Subscribe a user to a plan.
- `GET /subscriptions/{user_id}`: View user subscription details.
- `GET /subscriptions/{user_id}/usage`: View API usage statistics for a user.

### Access Control
- `GET /access/{user_id}/{api_name}`: Check if a user has access to an API.

### Usage Tracking
- `POST /usage/{user_id}`: Simulate an API request and track usage.
- `GET /usage/{user_id}/limit`: View usage limits for a user.

## Example Usage
- **Create a Permission**:
   ```bash
   curl -X POST "http://127.0.0.1:8000/permissions" -H "Content-Type: application/json" -d '{
       "name": "service1",
       "endpoint": "/service1",
       "description": "Access to service1"
   }'
   ```

- **Create a Plan**:
   ```bash
   curl -X POST "http://127.0.0.1:8000/plans" -H "Content-Type: application/json" -d '{
       "name": "Basic Plan",
       "description": "Basic subscription plan",
       "permissions": ["service1"],
       "limits": {"service1": 10}
   }'
   ```

- **Subscribe a User**:
   ```bash
   curl -X POST "http://127.0.0.1:8000/subscriptions" -H "Content-Type: application/json" -d '{
       "user_id": 1,
       "plan_id": 1
   }'
   ```

## Testing
- The application has been tested using Postman to validate all endpoints.
- Unit tests have been included in `main.py` for key functionalities.

## Video Demonstration
A video demonstration showcasing the design choices, functionality, and API usage has been prepared and submitted alongside this project.

## Repository
The full project, including the source code, is hosted on GitHub:
[GitHub Repository Link](<repository_url>)

