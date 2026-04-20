import json
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from .forms import RegisterForm, StudentForm, CourseForm
from .models import Student, Course


def home(request):
    return render(request, 'home.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            Student.objects.create(
                user=user,
                student_id=form.cleaned_data['student_id'],
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                major=form.cleaned_data['major'],
                year=form.cleaned_data['year'],
            )

            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('my_profile')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def student_list(request):
    students = Student.objects.all().order_by('student_id')
    return render(request, 'students/student_list.html', {'students': students})


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/student_detail.html', {'student': student})


@login_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student created successfully.')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Add Student'})


@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Edit Student'})


@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully.')
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})

@login_required
@csrf_exempt
def api_students(request):
    if request.method == 'GET':
        students = list(Student.objects.values('id', 'student_id', 'full_name', 'email', 'major', 'year'))
        return JsonResponse({'students': students}, status=200)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student = Student.objects.create(
                student_id=data['student_id'],
                full_name=data['full_name'],
                email=data['email'],
                major=data['major'],
                year=data.get('year', 1),
            )
            return JsonResponse({
                'message': 'Student created successfully',
                'student': {
                    'id': student.id,
                    'student_id': student.student_id,
                    'full_name': student.full_name,
                    'email': student.email,
                    'major': student.major,
                    'year': student.year,
                }
            }, status=201)
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return HttpResponseNotAllowed(['GET', 'POST'])


@login_required
@csrf_exempt
def api_student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'GET':
        return JsonResponse({
            'id': student.id,
            'student_id': student.student_id,
            'full_name': student.full_name,
            'email': student.email,
            'major': student.major,
            'year': student.year,
        }, status=200)

    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            student.student_id = data.get('student_id', student.student_id)
            student.full_name = data.get('full_name', student.full_name)
            student.email = data.get('email', student.email)
            student.major = data.get('major', student.major)
            student.year = data.get('year', student.year)
            student.save()
            return JsonResponse({'message': 'Student updated successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    if request.method == 'DELETE':
        student.delete()
        return JsonResponse({'message': 'Student deleted successfully'}, status=200)

    return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])


@login_required
def course_list(request):
    courses = Course.objects.all().order_by('code')
    student = get_object_or_404(Student, user = request.user)
    enrolled_course_ids = []

    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'student': student,
        'enrolled_course_ids': enrolled_course_ids,
    })


@login_required
def enroll_course(request, course_id):
    student = get_object_or_404(Student, user = request.user)
    course = get_object_or_404(Course, pk=course_id)

    if course in student.enrolled_courses.all():
        messages.warning(request, f'You have already enrolled in {course.name}.')
    else:
        student.enrolled_courses.add(course)
        messages.success(request, f'You successfully enrolled in {course.name}.')

    return redirect('course_list')


@login_required
def my_timetable(request):
    student = get_object_or_404(Student, user=request.user)
    courses = student.enrolled_courses.all().order_by('weekday', 'start_time')

    return render(request, 'courses/my_timetable.html', {
        'student': student,
        'courses': courses,
    })


@login_required
def drop_course(request, course_id):
    student = get_object_or_404(Student, user = request.user)
    course = get_object_or_404(Course, pk=course_id)

    if course in student.enrolled_courses.all():
        student.enrolled_courses.remove(course)
        messages.success(request, f'You dropped {course.name}.')
    else:
        messages.warning(request, f'You are not enrolled in this course.')

    return redirect('my_timetable')


@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course created successfully.')
            return redirect('course_list')
    else:
        form = CourseForm()

    return render(request, 'courses/course_form.html', {
        'form': form,
        'title': 'Add Course'
    })


@login_required
def my_profile(request):
    student = get_object_or_404(Student, user=request.user)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            updated_student = form.save(commit=False)
            updated_student.user = request.user
            updated_student.save()

            if request.user.email != updated_student.email:
                request.user.email = updated_student.email
                request.user.username = updated_student.student_id
                request.user.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('my_profile')
    else:
        form = StudentForm(instance=student)

    return render(request, 'students/my_profile.html', {
        'student': student,
        'form': form
    })
