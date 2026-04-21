# Student Information System

A Django-based Student Information System developed for the **XJCO3011 Web Services and Web Data** coursework.

This project was developed iteratively through multiple versions. It started from a basic Django authentication and student CRUD system, then expanded to include course selection and timetable viewing, and was later improved by linking authenticated users to their own student profiles. The final result is a database-backed web application that combines page-based workflows with JSON API endpoints.

---

## Project overview

The system supports the following core functions:

- User registration, login, and logout
- Automatic creation of a linked student profile during registration
- Personal profile viewing and updating
- Course browsing
- Course enrolment
- Personal timetable viewing
- Course withdrawal
- Student CRUD operations through both web pages and JSON API endpoints

This project demonstrates:

- Database integration
- Session-based authentication
- Web application workflows
- JSON API design
- Iterative software development using Git version control

**GitHub repository:** [https://github.com/sc21m2g/student-sis](https://github.com/sc21m2g/student-sis) (clone URL: `https://github.com/sc21m2g/student-sis.git`)

---

## Iterative development

### Version 1

- Homepage with system introduction
- Navigation bar
- User registration, login, and logout
- Student CRUD operations
- Basic student JSON API endpoints

### Version 2

- Added `Course` model
- Added course list page
- Added course enrolment feature
- Added timetable viewing
- Added course withdrawal

### Version 3

- Linked authenticated users to their own student profiles
- Automatically created student profiles during registration
- Added personal profile page
- Improved self-service course enrolment workflow
- Added automated tests for major workflows and API operations

---

## Technology stack

- **Python 3**
- **Django 4**
- **SQLite**
- **HTML / CSS**

### Why this stack was chosen

- **Python** supports rapid and clear development
- **Django** provides built-in authentication, ORM, routing, templates, and forms
- **SQLite** is lightweight and suitable for a coursework-scale project

---

## Database design

The main models in the system are:

- **User** — Django built-in authentication model
- **Student** — Student ID, full name, email, major, year; optional link to `User`; many-to-many enrolment on courses
- **Course** — Code, name, lecturer, credits, weekday, start/end time, classroom
- **Student–course relationship** — Many-to-many field on `Student` for enrolment

---

## Main features

### Authentication

- Register
- Login
- Logout

### Student profile

- View personal profile
- Edit personal information

### Course management

- Browse available courses
- Enrol in a course
- View personal timetable
- Drop a course

### Student management

- View student list
- Add student
- Edit student
- Delete student

---

## API endpoints

The project includes JSON API endpoints for student CRUD:

- `GET /api/students/`
- `POST /api/students/`
- `GET /api/students/<id>/`
- `PUT /api/students/<id>/`
- `DELETE /api/students/<id>/`

These endpoints use Django session-based authentication. Full parameters, examples, and status codes are in the API documentation (Markdown and PDF) linked below.

---

## Testing

Testing was performed using both manual workflow checks and automated Django tests.

### Manual testing included

- Register → automatic student profile creation
- Login and logout
- Profile update
- Course enrolment
- Timetable viewing
- Course withdrawal

### Automated testing included

- Registration creates a linked `User` and `Student`
- Protected routes redirect unauthenticated users
- Profile and course list access after login
- Enrolment and withdrawal
- Student JSON API list / create / get / update / delete
- Missing-field negative API test

Run tests with:

```bash
python manage.py test
```

Current automated result: **13 tests** passed successfully.

---

## Project structure

```text
student_sis/
├── manage.py
├── requirements.txt
├── readme.md
├── API_DOCUMENTATION.md
├── API_DOCUMENTATION.pdf
├── student_sis/
├── core/
└── templates/
```

---

## Setup instructions

### 1. Clone the repository

```bash
git clone https://github.com/sc21m2g/student-sis.git
cd student-sis
```

### 2. Create and activate a virtual environment

Example using conda:

```bash
conda create -n demo1 python=3.9
conda activate demo1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser (optional but recommended)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Then open: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Example workflow

1. Register a new student account  
2. Log in  
3. Open **My Profile**  
4. Browse available courses  
5. Enrol in courses  
6. View **My Timetable**  
7. Drop courses if needed  

---

## Documentation

### API documentation

- **PDF (GitHub, pinned commit):** [API_DOCUMENTATION.pdf on GitHub](https://github.com/sc21m2g/student-sis/blob/2122dc5169f12f9eadd08dba15cf7a50c28018c0/API_DOCUMENTATION.pdf)  

### Technical report

- **Technical report (in repository, pinned commit):** [technical report.pdf on GitHub]https://github.com/sc21m2g/student-sis/blob/9e8894cc46df37c255ccc0abef18a823a437ad38/technical%20report.pdf

### Presentation slides

- **PowerPoint (in repository, pinned commit):** [Student Information System.pptx](https://github.com/sc21m2g/student-sis/blob/2122dc5169f12f9eadd08dba15cf7a50c28018c0/Student%20Information%20System.pptx)

---

## Version control

This project was developed using Git and GitHub with visible commit history to demonstrate iterative improvement.

The commit history shows, among other steps:

- Initial Django project setup  
- Authentication and student CRUD  
- Course selection and timetable features  
- Profile linking improvements  
- Automated testing and documentation updates  

---

## Limitations

The current system is functional but still has some limitations:

- No role-based authorisation yet  
- Some management pages are accessible to any authenticated user  
- Some invalid resource requests still rely on Django’s default error handling  
- The project is currently demonstrated in local development mode  

---

## Future improvements

Possible future improvements include:

- Role-based access control for student and administrator users  
- More consistent JSON error handling  
- Deployment to an external platform such as PythonAnywhere  
- Search and filtering for courses  
- Timetable conflict checking  
- More advanced automated testing  

---

## Generative AI usage

This is a **Green Light** assessment, and generative AI was used as a support tool during development.

AI was used for:

- Planning and feature discussion  
- Debugging Django issues  
- Refining workflow design  
- Improving API documentation  
- Improving test coverage  
- Improving written documentation  

The final implementation, debugging decisions, and submission preparation were checked and controlled by the student.
