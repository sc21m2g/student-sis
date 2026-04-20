# Student Information System

A Django-based student information system developed for the XJCO3011 coursework.  
This project evolved iteratively through multiple versions, starting from basic authentication and student CRUD, then extending to course selection and timetable viewing, and finally improving the design by linking authenticated users to their own student profiles.

## Features

### Version 1
- Homepage with system introduction
- Navigation bar
- User registration, login, and logout
- Student CRUD operations
- Basic JSON API endpoints for student data

### Version 2
- Course model added
- Course list page
- Course enrolment feature
- Timetable viewing
- Course withdrawal

### Version 3
- Authenticated users are linked to their own student profiles
- Automatic student profile creation during registration
- Personal profile page for each student
- Students can update their own profile information
- Self-service course enrolment
- Personal timetable page
- Self-service course withdrawal

## Technology Stack
- Python 3
- Django 4
- SQLite
- HTML / CSS

## Database Design
The main models in the project are:

- **User**: Django built-in authentication model
- **Student**: stores student profile information
- **Course**: stores course information
- **Student-Course relationship**: implemented through a many-to-many relationship for enrolment

## Main Functions

### Authentication
- Register
- Login
- Logout

### Student Profile
- View personal profile
- Edit personal information

### Course Management
- Browse all available courses
- Enrol in a course
- View personal timetable
- Drop a course

### Student Management
- View student list
- Add student
- Edit student
- Delete student

### API Endpoints
- `GET /api/students/`
- `POST /api/students/`
- `GET /api/students/<id>/`
- `PUT /api/students/<id>/`
- `DELETE /api/students/<id>/`

## Project Structure

```text
student_sis/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3
├── student_sis/
├── core/
└── templates/