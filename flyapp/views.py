from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Course, Lesson, Enrollment, Quiz, Question, Choice
from .forms import CourseForm, LessonForm, QuizForm, QuestionForm, ChoiceForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import logout
from django.contrib.auth.models import User

def home(request):
    courses = Course.objects.all()
    return render(request, 'flyapp/home.html',locals())

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'flyapp/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_authenticated and user.is_superuser:
                   
                    return redirect('dashboard')
                else:
                    return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'flyapp/login.html', {'form': form})
def user_logout(request):
    logout(request)
    return redirect('home')


from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'flyapp/course_list.html', {'courses': courses})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'flyapp/course_detail.html', {'course': course})

def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'flyapp/course_form.html', {'form': form})

def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_detail', pk=pk)
    else:
        form = CourseForm(instance=course)
    return render(request, 'flyapp/course_form.html', {'form': form})

def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    return redirect('course_list')


# Lesson Views
def lesson_create(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect('course_detail', pk=course_pk)
    else:
        form = LessonForm(initial={'course': course})
    return render(request, 'flyapp/lesson_form.html', {'form': form, 'course': course})

def lesson_update(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('course_detail', pk=lesson.course.pk)
    else:
        form = LessonForm(instance=lesson)
    return render(request, 'flyapp/lesson_form.html', {'form': form})

def lesson_delete(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    course_pk = lesson.course.pk
   
    lesson.delete()
    return redirect('course_detail', pk=course_pk)
    

# Quiz Views
def quiz_create(request, lesson_pk):
    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.lesson = lesson
            quiz.save()
            return redirect('course_detail', pk=lesson.course.pk)
    else:
        form = QuizForm()
    return render(request, 'flyapp/quiz_form.html', {'form': form, 'lesson': lesson})

def quiz_update(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('course_detail', pk=quiz.lesson.course.pk)
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'flyapp/quiz_form.html', {'form': form})

def quiz_delete(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    course_pk = quiz.lesson.course.pk
    if request.method == 'POST':
        quiz.delete()
        return redirect('course_detail', pk=course_pk)
    return render(request, 'flyapp/quiz_confirm_delete.html', {'quiz': quiz})

# Question Views
def question_create(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('course_detail', pk=quiz.lesson.course.pk)
    else:
        form = QuestionForm()
    return render(request, 'flyapp/question_form.html', {'form': form, 'quiz': quiz})

def question_update(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('course_detail', pk=question.quiz.lesson.course.pk)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'flyapp/question_form.html', {'form': form})

def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    course_pk = question.quiz.lesson.course.pk
    if request.method == 'POST':
        question.delete()
        return redirect('course_detail', pk=course_pk)
    return render(request, 'flyapp/question_confirm_delete.html', {'question': question})

# Choice Views
def choice_create(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk)
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.question = question
            choice.save()
            return redirect('course_detail', pk=question.quiz.lesson.course.pk)
    else:
        form = ChoiceForm()
    return render(request, 'flyapp/choice_form.html', {'form': form, 'question': question})

def choice_update(request, pk):
    choice = get_object_or_404(Choice, pk=pk)
    if request.method == 'POST':
        form = ChoiceForm(request.POST, instance=choice)
        if form.is_valid():
            form.save()
            return redirect('course_detail', pk=choice.question.quiz.lesson.course.pk)
    else:
        form = ChoiceForm(instance=choice)
    return render(request, 'flyapp/choice_form.html', {'form': form})

def choice_delete(request, pk):
    choice = get_object_or_404(Choice, pk=pk)
    course_pk = choice.question.quiz.lesson.course.pk
    if request.method == 'POST':
        choice.delete()
        return redirect('course_detail', pk=course_pk)
    return render(request, 'flyapp/choice_confirm_delete.html', {'choice': choice})

@login_required(login_url='login')
def course_enroll(request, id):
    course = get_object_or_404(Course, pk=id)
    if request.method == 'POST':
        enrollment = Enrollment(user=request.user, course=course)
        enrollment.save()
        return redirect('course_detail', pk=id)
    return render(request, 'flyapp/payment.html', {'course': course})


def user_profile(request):
    user = request.user
    enrollments = Enrollment.objects.filter(user=user)
    return render(request, 'flyapp/user_profile.html', {'user': user, 'enrollments': enrollments})

def user_dashboard(request):
    courses_count = Course.objects.count()
    users_count = User.objects.count()
    enrollments_count = Enrollment.objects.count()
    recent_enrollments = Enrollment.objects.all()
    return render(request, 'flyapp/admin_dashboard.html',locals())