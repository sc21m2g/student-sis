from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Student, Course
import json


class StudentSystemTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username='testuser',
            email='test@leeds.ac.uk',
            password='Testpass123'
        )

        self.student = Student.objects.create(
            user=self.user,
            student_id='2021110001',
            full_name='Test Student',
            email='test@leeds.ac.uk',
            major='Computer Science',
            year=3
        )

        self.course = Course.objects.create(
            code='CS101',
            name='Introduction to Programming',
            lecturer='Dr Smith',
            credits=10,
            weekday='Monday',
            start_time='09:00',
            end_time='11:00',
            classroom='A101'
        )

    def login(self):
        self.client.login(username='testuser', password='Testpass123')

    def test_register_creates_linked_student_profile(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@leeds.ac.uk',
            'student_id': '2021110099',
            'full_name': 'New User',
            'major': 'Software Engineering',
            'year': 2,
            'password1': 'Strongpass123',
            'password2': 'Strongpass123'
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('my_profile'))

        user = User.objects.get(username='newuser')
        student = Student.objects.get(user=user)

        self.assertEqual(student.student_id, '2021110099')
        self.assertEqual(student.full_name, 'New User')
        self.assertEqual(student.major, 'Software Engineering')

    def test_profile_requires_login(self):
        response = self.client.get(reverse('my_profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_profile_page_loads_after_login(self):
        self.login()
        response = self.client.get(reverse('my_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Student')

    def test_course_list_loads_after_login(self):
        self.login()
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'CS101')

    def test_enroll_course(self):
        self.login()
        response = self.client.get(reverse('enroll_course', args=[self.course.id]))
        self.assertEqual(response.status_code, 302)

        self.student.refresh_from_db()
        self.assertIn(self.course, self.student.enrolled_courses.all())

    def test_drop_course(self):
        self.student.enrolled_courses.add(self.course)
        self.login()

        response = self.client.get(reverse('drop_course', args=[self.course.id]))
        self.assertEqual(response.status_code, 302)

        self.student.refresh_from_db()
        self.assertNotIn(self.course, self.student.enrolled_courses.all())

    def test_api_list_students_requires_login(self):
        response = self.client.get(reverse('api_students'))
        self.assertEqual(response.status_code, 302)

    def test_api_list_students_after_login(self):
        self.login()
        response = self.client.get(reverse('api_students'))
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn('students', data)
        self.assertEqual(data['students'][0]['student_id'], '2021110001')

    def test_api_create_student(self):
        self.login()
        response = self.client.post(
            reverse('api_students'),
            data=json.dumps({
                'student_id': '2021110022',
                'full_name': 'API Student',
                'email': 'api@leeds.ac.uk',
                'major': 'Data Science',
                'year': 2
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Student.objects.filter(student_id='2021110022').exists())

    def test_api_get_single_student(self):
        self.login()
        response = self.client.get(reverse('api_student_detail', args=[self.student.id]))
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['student_id'], '2021110001')

    def test_api_update_student(self):
        self.login()
        response = self.client.put(
            reverse('api_student_detail', args=[self.student.id]),
            data=json.dumps({
                'full_name': 'Updated Student',
                'major': 'Software Engineering',
                'year': 4
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.student.refresh_from_db()
        self.assertEqual(self.student.full_name, 'Updated Student')
        self.assertEqual(self.student.major, 'Software Engineering')
        self.assertEqual(self.student.year, 4)

    def test_api_delete_student(self):
        self.login()
        response = self.client.delete(reverse('api_student_detail', args=[self.student.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Student.objects.filter(id=self.student.id).exists())

    def test_api_create_student_missing_field(self):
        self.login()
        response = self.client.post(
            reverse('api_students'),
            data=json.dumps({
                'student_id': '2021110033',
                'full_name': 'Incomplete Student',
                'email': 'incomplete@leeds.ac.uk'
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)