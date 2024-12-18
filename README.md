Cloud Service Access Management System

Author: Issac Zhou  
CWID: 885251249  

Project Description:  
This project implements a backend system for managing access to cloud services based on user subscriptions. The system dynamically manages API permissions, tracks usage, and restricts access when usage limits are exceeded. It features:  
- 6 Cloud Service APIs (simulated).  
- Subscription Plan Management (create, modify, delete plans).  
- Permission Management (add, modify, delete permissions).  
- User Subscription Handling (subscribe to plans, view usage statistics).  
- Access Control (validate API requests based on user permissions and limits).  
- Usage Tracking and Enforcement (track requests, restrict access beyond limits).  

Prerequisites:  
Software Requirements:  
1. Python 3.9+  
2. pip (Python package manager)  
3. Virtual Environment Tool:  
   - For Mac/Linux: venv  
   - For Windows: virtualenv (optional).  
4. FastAPI and Uvicorn for the backend.  
5. Postman (optional, for testing APIs).  

Installation Instructions:  
Step 1: Clone the Repository  
Open your terminal (Mac/Linux) or command prompt (Windows) and run:  
git clone <your-github-repository-link>  
cd <repository-folder>  

Step 2: Setup Virtual Environment  
For Mac/Linux:  
1. Create a virtual environment:  
   python3 -m venv venv  
2. Activate the virtual environment:  
   source venv/bin/activate  

For Windows:  
1. Create a virtual environment:  
   python -m venv venv  
2. Activate the virtual environment:  
   venv\Scripts\activate  

Step 3: Install Dependencies  
After activating the virtual environment, install all required Python packages:  
pip install fastapi uvicorn  

Running the Project:  
1. Start the FastAPI server:  
   uvicorn main:app --reload  
2. Open your browser and go to Swagger UI for testing:  
   http://127.0.0.1:8000/docs  

Testing the APIs:  
Use Swagger UI or Postman to test the endpoints. Below is an overview of available routes:  

1. Cloud Service APIs (6 Random APIs):  
- GET /service1  
- GET /service2  
- GET /service3  
- GET /service4  
- GET /service5  
- GET /service6  

2. Subscription Plan Management:  
- POST /plans - Create a subscription plan.  
- PUT /plans/{plan_name} - Modify a subscription plan.  
- DELETE /plans/{plan_name} - Delete a subscription plan.  

3. Permission Management:  
- POST /permissions - Add permissions.  
- PUT /permissions/{permission_name} - Modify permissions.  
- DELETE /permissions/{permission_name} - Delete permissions.  

4. User Subscription Handling:  
- POST /subscriptions - Subscribe a user to a plan.  
- GET /subscriptions/{user_id} - View subscription details.  

5. Access Control:  
- GET /access/{user_id}/{api_name} - Check API access.  

6. Usage Tracking:  
- POST /usage/{user_id}/track - Track API usage.  
- GET /usage/{user_id} - Get usage statistics.  

Deployment:  
If you want to deploy the project to production, use the following command without --reload:  
uvicorn main:app --host 0.0.0.0 --port 8000  

Demo Video:  
For a demonstration of the project and its functionality, please check the following video:  
Google Drive Link: https://drive.google.com/file/d/1ya_WVoZtp1HYkudRmEbp9vWszrtajgOT/view?usp=sharing  

Contribution:  
This project was completed individually by Issac Zhou (CWID: 885251249).  

License:  
This project is licensed under the MIT License.
