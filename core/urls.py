from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),

    path('api/students/', views.api_students, name='api_students'),
    path('api/students/<int:pk>/', views.api_student_detail, name='api_student_detail'),
]