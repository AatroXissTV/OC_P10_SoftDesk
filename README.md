# Soft Desk

SoftDesk is an RESTful API made with Django REST Framework. It'an issue tracking system API and is intended to be used by developers from different platforms (web, mobile, desktop, etc.).

The API allows users to create projects, add other users to the project, create issues within projects, and add comments to issues.

## Download & create a virtual environment

For this software you will need to have Python 3 installed on your machine (more specifically, Python 3.9 or higher). You will also need to have pip installed.

Then open a terminal and navigate to the directory where you want to install SoftDesk. Then run the following command:

1. From repository download files and clone the folder.

    $ git clone https://github.com/AatroXissTV/SoftDesk.git SoftDesk
    $ cd SoftDesk

2. Create a Python virtual environment.

    $ python -m venv env

3. Activate the virtual environment.

    $ source env/bin/activate  #MacOS & Linux
    $ source env/Scripts/activate  #Windows

4. Install the requirements.

    $ pip install -r requirements.txt

## How to run the API

First you will need to run the API. You can do this by running the following command:

    $ python manage.py runserver

To request data from the API you will first need to create a user. You can do this by running the following command:

    $ python manage.py createsuperuser

or alternatively you can run the server and go to the following URL:

    http://localhost:8000/api/register/

or AND I HIGHLY SUGGEST you read the documentation for the API that can be found at this [link](https://documenter.getpostman.com/view/17750814/UVXgKcDJ)

## Updates

This project is still in development. If you have any suggestions or comments, please feel free to contact me at [AatroXissTV](https://twitter.com/AatroXissTV).

## Author

This software was made by Antoine "AatroXiss" Beaudesson with ❤️ and ☕

## Support

Contributions, issues and features requests are welcome ! Feel free to give a ⭐️ if you liked this project.