# Flask API Template

The following is a project template for a Flask backend for a tech stack that uses JavaScript Framework for the front end to handle routing. The worst part of developing a full stack web application is the initial setup, especially if you want the project to scale well during the development life cycle. As such, I created this as a skeleton for a backend API that uses Flask that works right out of the box. 

## Notes 
* The template is a "to do" app and after initial setup supports basic features such as User Authentication and and passing JSON data from API routes to the frontend. 
* The directory structure is designed to be modular but can be changed as needed
* The template is designed to work in conjunction with a JavaScript framework and does not handle routing to templates or any frontend components

## Setup
> Change directories to "backend" and create & activate a virtual environment 
```bash
cd backend
```
* Unix Based
```bash
python3 -m venv .venv
source venv/bin/activate
```
* Windows
```ps1
python -m venv .venv
.\venv\Scripts\activate
```
>  Install requirements.txt
```bash
pip install -r requirements.txt
```
> Run the application
```bash
python run.py
```


