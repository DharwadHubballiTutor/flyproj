from django.urls import path
from django.contrib import admin
from django.urls import path, include
from flyapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('',views.home, name='home'),
    path('course/list/', views.course_list, name='course_list'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('course/new/', views.course_create, name='course_create'),
    path('course/<int:pk>/edit/', views.course_update, name='course_update'),
    path('course/<int:pk>/delete/', views.course_delete, name='course_delete'),
    path('course/<int:course_pk>/lesson/new/', views.lesson_create, name='lesson_create'),
    path('lesson/<int:pk>/edit/', views.lesson_update, name='lesson_update'),
    path('lesson/<int:pk>/delete/', views.lesson_delete, name='lesson_delete'),
    path('lesson/<int:lesson_pk>/quiz/new/', views.quiz_create, name='quiz_create'),
    path('quiz/<int:pk>/edit/', views.quiz_update, name='quiz_update'),
    path('quiz/<int:pk>/delete/', views.quiz_delete, name='quiz_delete'),
    path('quiz/<int:quiz_pk>/question/new/', views.question_create, name='question_create'),
    path('question/<int:pk>/edit/', views.question_update, name='question_update'),
    path('question/<int:pk>/delete/', views.question_delete, name='question_delete'),
    path('question/<int:question_pk>/choice/new/', views.choice_create, name='choice_create'),
    path('choice/<int:pk>/edit/', views.choice_update, name='choice_update'),
    path('choice/<int:pk>/delete/', views.choice_delete, name='choice_delete'),
    path('course/<int:id>/enroll/', views.course_enroll, name='enroll'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('myprofile/', views.user_profile, name='user_profile'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)