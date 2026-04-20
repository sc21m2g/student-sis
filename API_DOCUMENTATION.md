# API Documentation

## Student Information System

| Field | Value |
|-------|--------|
| **Module** | XJCO3011 Web Services and Web Data |
| **Project** | Student Information System |
| **Author** | Guo Mohan |
| **Student ID** | 2021110028 |
| **Version** | 1.0 |

---

## 1. API Overview

This project is a Django-based Student Information System with database integration. It supports student account registration, login and logout, linked student profiles, student record CRUD (web UI and JSON API), course browsing, course enrolment, personal timetable viewing, and course withdrawal.

The system combines page-based interaction with JSON API endpoints for student data management.

**Base URL (local development):**

```text
http://127.0.0.1:8000/
```

---

## 2. Authentication

The system uses **Django session-based authentication**.

### Authentication workflow

1. Users register at `/register/` (creates a `User` and a linked `Student` profile).
2. Users log in at `/login/` (session cookie is set).
3. Users log out at `/logout/` (session is cleared).
4. Protected pages and JSON API routes require an authenticated session (`@login_required`).

### Authentication details

| Item | Description |
|------|-------------|
| **Mechanism** | Session authentication (browser cookie) |
| **User model** | Django built-in `User` |
| **Profile link** | Each registered user has a one-to-one `Student` record (`Student.user`) |

### Protected routes (examples)

| Area | Example paths |
|------|----------------|
| Profile | `/profile/` |
| Courses | `/courses/`, `/courses/<course_id>/enroll/`, `/courses/<course_id>/drop/`, `/courses/create/` |
| Timetable | `/my-timetable/` |
| Student admin UI | `/students/`, `/students/create/`, `/students/<pk>/`, `/students/<pk>/edit/`, `/students/<pk>/delete/` |
| JSON API | `/api/students/`, `/api/students/<id>/` |

If a user is not authenticated, protected HTML views are typically **redirected to the login page** (HTTP **302**). JSON API endpoints use the same decorator; clients without a session should expect a **302** redirect to `/login/` rather than a JSON body unless you configure the client to follow redirects.

**Note:** API views are decorated with `@csrf_exempt` so JSON clients can call `POST`/`PUT`/`DELETE` without a CSRF token, but **login is still required** for the view to run.

---

## 3. Data Models

### 3.1 Student

Stores student profile and links to the authenticated user when created via registration.

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Primary key |
| `user` | OneToOne → User | Linked account (nullable in DB for legacy rows) |
| `student_id` | string | Unique student identifier |
| `full_name` | string | Full name |
| `email` | string | Unique email |
| `major` | string | Academic major |
| `year` | positive integer | Year of study (default `1`) |
| `enrolled_courses` | ManyToMany → Course | Enrolled courses |
| `created_at` | datetime | Auto-set on create |
| `updated_at` | datetime | Auto-updated on save |

### 3.2 Course

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Primary key |
| `code` | string | Unique course code |
| `name` | string | Course name |
| `lecturer` | string | Lecturer name |
| `credits` | integer | Credits (default `10`) |
| `weekday` | string | Teaching day |
| `start_time` | string | Class start time |
| `end_time` | string | Class end time |
| `classroom` | string | Room location |

### 3.3 Student–course relationship

Enrolment is a **many-to-many** relationship: one student can take many courses; one course can have many students (`Student.enrolled_courses`).

---

## 4. Web Routes

### 4.1 Home page

| Property | Value |
|----------|--------|
| **URL** | `/` |
| **Method** | `GET` |
| **Auth** | Not required |
| **Description** | System homepage. |

### 4.2 Register

| Property | Value |
|----------|--------|
| **URL** | `/register/` |
| **Method** | `GET`, `POST` |
| **Auth** | Not required for `GET`/`POST` |
| **Description** | Creates a `User`, a linked `Student`, and logs the user in on success. Redirects to **My Profile**. |

**Form fields:** `username`, `email`, `student_id`, `full_name`, `major`, `year`, `password1`, `password2`

### 4.3 Login

| Property | Value |
|----------|--------|
| **URL** | `/login/` |
| **Method** | `GET`, `POST` |
| **Auth** | Not required |
| **Description** | Authenticates the user and starts a session. |

### 4.4 Logout

| Property | Value |
|----------|--------|
| **URL** | `/logout/` |
| **Method** | `GET` (and other methods as allowed by Django’s `LogoutView`) |
| **Auth** | Typically used when logged in |
| **Description** | Ends the session. |

### 4.5 My profile

| Property | Value |
|----------|--------|
| **URL** | `/profile/` |
| **Method** | `GET`, `POST` |
| **Auth** | **Required** |
| **Description** | Shows the current user’s `Student` profile and allows updates via `StudentForm` fields. |

### 4.6 Student list (web CRUD)

| Property | Value |
|----------|--------|
| **URL** | `/students/` |
| **Method** | `GET` |
| **Auth** | **Required** |
| **Description** | Lists all students (ordered by `student_id`). |

### 4.7 Create student (web)

| Property | Value |
|----------|--------|
| **URL** | `/students/create/` |
| **Method** | `GET`, `POST` |
| **Auth** | **Required** |
| **Description** | Create a new student via HTML form. |

### 4.8 Student detail (web)

| Property | Value |
|----------|--------|
| **URL** | `/students/<pk>/` |
| **Method** | `GET` |
| **Auth** | **Required** |
| **Path parameter** | `pk` — primary key of `Student` |

### 4.9 Edit student (web)

| Property | Value |
|----------|--------|
| **URL** | `/students/<pk>/edit/` |
| **Method** | `GET`, `POST` |
| **Auth** | **Required** |

### 4.10 Delete student (web)

| Property | Value |
|----------|--------|
| **URL** | `/students/<pk>/delete/` |
| **Method** | `GET`, `POST` |
| **Auth** | **Required** |
| **Description** | `POST` confirms deletion and redirects to the student list. |

### 4.11 Course list

| Property | Value |
|----------|--------|
| **URL** | `/courses/` |
| **Method** | `GET` |
| **Auth** | **Required** |
| **Description** | Lists all courses; enrolment uses `/courses/<course_id>/enroll/`. |

### 4.12 Create course (web)

| Property | Value |
|----------|--------|
| **URL** | `/courses/create/` |
| **Method** | `GET`, `POST` |
| **Auth** | **Required** |

### 4.13 Enrol in a course

| Property | Value |
|----------|--------|
| **URL** | `/courses/<course_id>/enroll/` |
| **Method** | `GET` |
| **Auth** | **Required** |
| **Path parameter** | `course_id` — primary key of `Course` |
| **Description** | Adds the course to the current user’s `enrolled_courses` if not already enrolled, then redirects to the course list. |

### 4.14 My timetable

| Property | Value |
|----------|--------|
| **URL** | `/my-timetable/` |
| **Method** | `GET` |
| **Auth** | **Required** |
| **Description** | Shows courses enrolled by the current student (ordered by `weekday`, `start_time`). |

### 4.15 Drop a course

| Property | Value |
|----------|--------|
| **URL** | `/courses/<course_id>/drop/` |
| **Method** | `GET` |
| **Auth** | **Required** |
| **Description** | Removes the course from enrolment if enrolled, then redirects to **My Timetable**. |

---

## 5. Student JSON API

All paths below require an **authenticated session** unless you have changed the project settings.

### 5.1 List all students

| Property | Value |
|----------|--------|
| **Endpoint** | `/api/students/` |
| **Method** | `GET` |
| **Authentication** | Session (required) |
| **Description** | Returns all student records as JSON. |

**Example request**

```http
GET /api/students/ HTTP/1.1
Host: 127.0.0.1:8000
Cookie: sessionid=... 
```

**Example response** (`200 OK`)

```json
{
  "students": [
    {
      "id": 1,
      "student_id": "2021110028",
      "full_name": "Guo Mohan",
      "email": "sc21m2g@leeds.ac.uk",
      "major": "Computer Science",
      "year": 3
    }
  ]
}
```

| Code | Meaning |
|------|---------|
| `200` | Success |
| `302` | Not logged in — redirect to login |
| `405` | Method not allowed (e.g. `PUT` on collection URL) |

---

### 5.2 Create a student

| Property | Value |
|----------|--------|
| **Endpoint** | `/api/students/` |
| **Method** | `POST` |
| **Authentication** | Session (required) |
| **Content-Type** | `application/json` |
| **Description** | Creates a new `Student` row (does not create a `User`; use `/register/` for full accounts). |

**Request body (required fields)**

| Field | Type | Required |
|-------|------|------------|
| `student_id` | string | Yes |
| `full_name` | string | Yes |
| `email` | string | Yes |
| `major` | string | Yes |
| `year` | integer | No (default `1`) |

**Example request**

```http
POST /api/students/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json
Cookie: sessionid=...

{
  "student_id": "2021110099",
  "full_name": "Test User",
  "email": "test@leeds.ac.uk",
  "major": "Software Engineering",
  "year": 2
}
```

**Example response** (`201 Created`)

```json
{
  "message": "Student created successfully",
  "student": {
    "id": 2,
    "student_id": "2021110099",
    "full_name": "Test User",
    "email": "test@leeds.ac.uk",
    "major": "Software Engineering",
    "year": 2
  }
}
```

| Code | Meaning |
|------|---------|
| `201` | Created |
| `400` | Missing field (`KeyError`) or other validation / DB error (returned as JSON `{"error": "..."}`) |
| `302` | Not logged in |
| `405` | Method not allowed |

---

### 5.3 Get one student

| Property | Value |
|----------|--------|
| **Endpoint** | `/api/students/<id>/` |
| **Method** | `GET` |
| **Authentication** | Session (required) |
| **Path parameter** | `id` — integer primary key of `Student` |

**Example request**

```http
GET /api/students/1/ HTTP/1.1
Host: 127.0.0.1:8000
Cookie: sessionid=...
```

**Example response** (`200 OK`)

```json
{
  "id": 1,
  "student_id": "2021110028",
  "full_name": "Guo Mohan",
  "email": "sc21m2g@leeds.ac.uk",
  "major": "Computer Science",
  "year": 3
}
```

| Code | Meaning |
|------|---------|
| `200` | Success |
| `404` | No student with that `id` (Django **HTML** error page by default for this view) |
| `302` | Not logged in |

---

### 5.4 Update a student

| Property | Value |
|----------|--------|
| **Endpoint** | `/api/students/<id>/` |
| **Method** | `PUT` |
| **Authentication** | Session (required) |
| **Content-Type** | `application/json` |
| **Description** | Partial update: any omitted JSON keys keep their existing values (`data.get(..., current)`). |

**Example request body**

```json
{
  "full_name": "Updated Name",
  "major": "Data Science",
  "year": 4
}
```

**Example request**

```http
PUT /api/students/1/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json
Cookie: sessionid=...
```

**Example response** (`200 OK`)

```json
{
  "message": "Student updated successfully"
}
```

| Code | Meaning |
|------|---------|
| `200` | Updated |
| `400` | JSON or validation error (`{"error": "..."}`) |
| `404` | Student not found |
| `302` | Not logged in |
| `405` | Unsupported method |

---

### 5.5 Delete a student

| Property | Value |
|----------|--------|
| **Endpoint** | `/api/students/<id>/` |
| **Method** | `DELETE` |
| **Authentication** | Session (required) |

**Example request**

```http
DELETE /api/students/1/ HTTP/1.1
Host: 127.0.0.1:8000
Cookie: sessionid=...
```

**Example response** (`200 OK`)

```json
{
  "message": "Student deleted successfully"
}
```

| Code | Meaning |
|------|---------|
| `200` | Deleted |
| `404` | Student not found |
| `302` | Not logged in |
| `405` | Unsupported method |

---

## 6. HTTP status and error codes

Standard HTTP semantics apply.

| Code | When it applies |
|------|-----------------|
| `200 OK` | Successful `GET`, `PUT`, `DELETE` (API) |
| `201 Created` | Successful `POST` create student |
| `302 Found` | Redirect (typical unauthenticated access to `@login_required` views) |
| `400 Bad Request` | API: invalid JSON, missing keys, or DB constraint messages in JSON `error` |
| `404 Not Found` | Invalid `id` / `pk` for detail views |
| `405 Method Not Allowed` | Wrong HTTP method on `/api/students/` or `/api/students/<id>/` |
| `500 Internal Server Error` | Unexpected server error |

---

## 7. Example error responses

**Missing required field** (`POST /api/students/`, `400`)

```json
{
  "error": "Missing field: 'major'"
}
```

**Invalid or duplicate data** (`400`, message from server)

```json
{
  "error": "UNIQUE constraint failed: core_student.email"
}
```

**Not found** (detail URL with invalid id — format depends on `DEBUG` and client; API views use `get_object_or_404`)

```json
{
  "detail": "Not found."
}
```

*(Browsers may receive an HTML 404 page for the same URL.)*

---

## 8. Testing notes

Testing was performed using both manual browser-based checks and automated Django tests.

### Manual testing
The following user flows were tested manually in the browser:
- Register → automatic Student profile creation → redirect to My Profile
- Login and logout
- Profile viewing and profile update
- Course browsing
- Course enrolment
- Timetable viewing
- Course withdrawal

### Automated testing
Automated tests were implemented in `core/tests.py` using Django’s `TestCase` and test client.

The automated test suite covers:
- Registration creates a linked `User` and `Student`
- Protected routes redirect unauthenticated users to login
- Authenticated users can view profile and course list
- Course enrolment and withdrawal
- Student JSON API list/create/get/update/delete
- Negative API case for missing required fields

### Example command
```bash
python manage.py test

---

## 9. Summary

This system provides:

- **JSON student CRUD** at `/api/students/` and `/api/students/<id>/`.
- **Session authentication** integrated with Django’s `User` and linked `Student` profiles.
- **Web workflows** for profile editing, course listing, enrolment, personal timetable, and withdrawal, plus optional staff-style student/course management pages under `/students/` and `/courses/create/`.

The project demonstrates database-backed web services, authentication, and data-driven student workflows in a single Django application.
