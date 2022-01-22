### Sberbank Project for short message analysis

 Project for text analysis and connection between client and database by using REST API 
 Right now it's in draft status, but some day it should be done.
 
#### Steps to deploy:
All commands are executed in root package
1. Get `configuration.py` file and place it in root package
2. Create python virtual env by `python -m venv venv`
3. Activate env by `venv\Scripts\activate.bat` on Windows or `source venv/bin/activate` on Unix or MacOS
4. Install all required packages by `python install -r requirements.txt`
5. Execute all migrations by `python manage.py migrate`
6. Run server by `python manage.py runserver`
7. PROFIT

#### Routes:
- `admin/` - admin routes
- `api/v1` - main api route
- `api/v1/messages` - api route for `Message` class
- `api/v1/cities` - api route for `City` class

#### Some tips:
- You can create admin user by `python manage.py createsuperuser` to use admin route
- You can handle all data in readonly mode without admin permission by message api route:
    - `GET api/v1/messages` for getting all messages
    - `GET api/v1/messages/:id` for getting message by id
    - `GET api/v1/cities` for getting all cities
    - `GET api/v1/cities/:id` for getting city by id
- If you have json-like file with message data, and you want to send it to server, try to use `fill_db.py` 
