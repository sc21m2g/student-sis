from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),

    path('courses/', views.course_list, name='course_list'),
    path('courses/create/', views.course_create, name='course_create'),
    path('students/<int:student_id>/enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('my-timetable/', views.my_timetable, name='my_timetable'),
    path('students/<int:student_id>/drop/<int:course_id>/', views.drop_course, name='drop_course'),

    path('api/students/', views.api_students, name='api_students'),
    path('api/students/<int:pk>/', views.api_student_detail, name='api_student_detail'),
]