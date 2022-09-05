# IETE-ISF Recruitment Portal (Backend)

## 💻 Short Description

Includes a quiz application built on the Django Rest Framework that enables users to test their knowledge in the area of their interest. 

## 👉 Index

- [Features](#features)
- [Structure](#structure)
- [Installation](#installation)
- [Documentation](#documentation)
- [Bug Reporting](#bug)
- [Feature Request](#feature-request)
- [License](#license)

<a id="features"></a>

## 💡Features
1) The portal is highly responsive and includes various security features like detecting Tab switch, JWT authentication for every API request , Auto submission on    test timeout etc.
2) The system automatically verifies the responses and assigns the final quiz score.
3) The portal was used by more than 300 students to give test.
 
 <a id="structure"></a>
 
 ## 🏗️ Structure
 
 ### Project Folder(recportal): 
 
 Contains configuration files of the project.
 
* manage.py
*  __init.py_
*  settings.py
*  urls.py
*  wsgi.py
*  asgi.py

### Application Folder(app): 
 
 Contains configuration files of the particular app in this project.
 
*  __init.py_
*  admin.py
*  apps.py
*  models.py
*  views
  - adminpanel.py
  - quiz.py
  - users.py
*  urls.py
*  tests.py

<a id="installation"></a>

## ⚙️ Installation

- Bring Up local setup
- Clone the repo
- Execute the following commands:  
    `cd ..`  
    `python -m venv venv`  
    `venv\Scripts\activate`    
    `pip install -r requirements.txt`  
    `cd recportal`   
    `python manage.py migrate`   
    `python manage.py collectstatic`  
    `python manage.py runserver`  

<a id="documentation"></a>

## 📄 Documentation
- API Documentation listed to Postman link :- https://documenter.getpostman.com/view/18159368/UVC8CRdf
- Database Diagram listed to DBDiagram link :- https://dbdiagram.io/d/6314ee740911f91ba5319c36

<a id="bug"></a>

## 🐛 Bug Reporting

Feel free to [open an issue](https://github.com/karthiksbh/RecPortal/issues) on GitHub if you find any bug.

<a id="feature-request"></a>

## ⭐ Feature Request

- Feel free to [Open an issue](https://github.com/karthiksbh/RecPortal/issues) on GitHub to request any additional features you might need for your use case.
- Connect with me on [LinkedIn](https://www.linkedin.com/in/karthik-srinivas-bhallamudi-b5b535203/). Would love to know about your opinion. ❤️

<a id="license"></a>

## 📜 License

This software is open source, licensed under the [MIT License](https://github.com/karthiksbh/RecPortal/LICENSE).


