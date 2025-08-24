# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the Amity Event Venue Booking Portal - a Flask-based web application for booking university event halls. The system allows faculty to book venues via email-verified appointments with admin approval workflow.

## Tech Stack

- **Backend**: Python Flask with WSGI
- **Database**: MySQL (primary) with SQLite3 fallback option
- **Frontend**: HTML/CSS/JS with Jinja2 templating
- **Email**: Flask-Mail with SMTP
- **Authentication**: Custom login system with password hashing

## Key Development Commands

### Setup and Initialization
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment (Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python3 initapp.py
```

### Running the Application
```bash
# Development server (default)
flask run -p 8000 -h 127.0.0.1

# Production deployment
# Use production WSGI server as per Flask documentation
```

### Database Operations
```bash
# Backup MySQL database
mysqldump -u dead -p amievent > amievent_backup.sql

# Connect to MySQL
mysql -u dead -p amievent
```

## Core Architecture

### Database Layer (`dbscript.py` / `dbscriptlite.py`)
- **Connection Management**: MySQL connector with fallback database creation
- **Core Tables**: `booking`, `halls`, `login` (admin/user separation)
- **Key Functions**:
  - `init()`: Initialize database and halls table
  - `calendermain()`: Process and format booking data for calendar display
  - `request_hall()`: Create new booking requests
  - `verify()`: Admin booking approval/rejection

### Authentication Layer (`loginscript.py` / `loginscriptlite.py`)
- **User Management**: Separate admin and user accounts
- **Security**: SHA256 password hashing with salt
- **Session Management**: Flask session-based authentication

### Application Layer (`app.py`)
- **Configuration**: Email settings, database credentials, admin contacts
- **Core Functions**:
  - `hallname(hallid)` / `hallid(hallname)`: Hall ID/name mapping
  - `send_mail()`: Email notification system
- **Routes**: Form handling, calendar views, admin operations

### Frontend Structure
- **Templates**: Located in `web/templates/`
  - `index.html`: Main hall selection page
  - `[hall].html`: Individual hall booking forms (e.g., `room105.html`, `crc.html`)
  - `admin2.html`: Admin dashboard
  - `calenderuser.html`: Calendar view for users
- **Static Assets**: `web/static/` contains CSS, JS, and images

## Hall Management System

The application uses a numeric hall ID system:
1. Auditorium Hall
2. Seminar Hall  
3. Room No. 105, A2 Building
4. CRC Conference Room

### Adding New Halls
When adding a new hall, update these components:
1. **Database**: Modify `init()` function in `dbscript.py`
2. **Mapping Functions**: Update `hallname()` and `hallid()` in `app.py`
3. **Calendar System**: Extend `calendermain()` processing logic
4. **Templates**: Create new hall-specific form template
5. **Routes**: Add route handler for new hall
6. **Frontend**: Update index page and calendar displays

## Important Configuration Variables (app.py)

Before deployment, update these variables:
- Lines 26-27: `app.secret_key` and `app.config['SECRET_KEY']`
- Lines 31-32: Email credentials (`MAIL_USERNAME`, `MAIL_PASSWORD`)
- Line 35: `admin_email`
- Line 39: `server_link` (production URL)

## Email System

The application sends notifications to multiple stakeholder groups:
- **Admin emails**: For booking requests and confirmations
- **User notifications**: Booking status updates
- **VC/Director emails**: For specific booking types

## Security Considerations

- Database credentials are hardcoded (hostname='127.0.0.1', username='dead', passwd='1234')
- Secret keys should be changed from defaults before production
- Email passwords are stored in plain text in configuration