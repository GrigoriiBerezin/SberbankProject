### Sberbank Project for short message analysis

 Project for text analysis and connection between client and database by using REST API 
 Right now it's in draft status, but some day it should be done.
 
#### Steps to deploy:
All commands are executed in root package
1. Get `configuration.py` file and place it in root package
2. Create python virtual env by `python -m venv venv`
3. Activate env by `venv\Scripts\activate.bat` on Windows or `source venv/bin/activate` on Unix or MacOS
4. Install all required packages by `python install -r requirements.txt`
5. Run server by `python manage.py runserver`
6. PROFIT

#### Routes:
- `admin/` - admin routes
- `api/v1` - main api route
- `api/v1/messages` - api route for `Message` class

#### Some tips:
- You can create admin user by `python manage.py createsuperuser` to use admin route
- You can handle all data without admin permission by message api route:
    - `POST api/v1/messages` for creating the message
    - `PUT api/v1/messages/:id` for updating the message by id
    - `DELETE api/v1/messages/:id` for deleting the message by id
    - `GET api/v1/messages` for getting all the messages
    - `GET api/v1/messages/:id` for getting the message with id
- If you have json-like file with message data, and you want to send it to server, try to use `fill_db.py` 