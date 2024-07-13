
# Amity Event Venue Booking Portal

This project aims to streamline the process of booking Venue halls with Admin/Chairman. Any Faculty can login with their university email and easily book a venue, this system provides a user-friendly interface to facilitate the appointment booking process efficiently.

## _Email verified Appointment Service_

A Simple yet effective venue appointment system that can run on remote server/local machine and it sends Email to given admin everytime for booking confirmation.

## Features
- Lightweight & Easy to deploy and integrate.
- Secured with additional hashing for passwords and sensitive information. 
- Uses a offline sql lite database server to run every child process in single server.
- Email verification.

## Tech

- [Flask & WSGI] - Hosting Server
- [Jinja2] - Render Frontend
- [SQLite3] - Lite Database server
- [HTML/CSS/JS] - Frontend
- [Python] - Backend 

And of course it is open source with a [public repository](https://github.com/nexiouscaliver/amity-booking-portal/) on GitHub.

## System Requirments :

- Min. 1GB RAM
- Min. 2GB Free space
- Win/Linux/Unix Operating System (tested on Windows11/Linux/Rpi4)
- [Python](https://www.python.org/)(v3.11+)

## Download

Clone the repository from github :
```sh
git clone https://github.com/nexiouscaliver/amity-booking-portal.git
```

## Installation
It requires [Python](https://www.python.org/) v3.11+ to work perfectly.

Change directory:
```sh
cd amity-booking-portal/
```
Create virtual environment :
```sh
python -m venv .venv
```
Activate virtual environment(linux) :
```sh
source .venv/Scripts/activate
```
Activate virtual environment(windows) :
```sh
.\.venv\Scripts\activate
```
Install the dependencies :
```sh
pip install -r requirements.txt
```
## Change Variables

Change the following variables in *app.py* brfore deployment:
```sh
app.py
  |-- secret_key (line no. 18 & 19)
  |-- sender email and password (line no. 23,24,25)
  |-- admin_email (line no. 26)
  |-- it_email (line no. 27)
  |-- server_link (line no. 29)
```
Description for purpose is mentioned commented alongside variables.

## Deployment

*run the following steps in above created virtual environment*

Run init script to initialize the database:
```sh
python3 initapp.py
```

Start the server on  127.0.0.1:8000 (change address and port as needed) :
*(WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.)*
```sh
flask run -p 8000 -h 127.0.0.1
```

Verify the deployment by navigating to your server address(localhost) in
your preferred browser.

```sh
http://127.0.0.1:8000
```
For production deployment kindly use production WSGI server instead or any other compatible server.
[Production Deployment](https://flask.palletsprojects.com/en/3.0.x/tutorial/deploy/)

## License

MIT ;)

**Free Software, Hell Yeah!**
