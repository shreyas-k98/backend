from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CourseAPI.as_view()),
    path('test/', views.TetsAPI.as_view()),
    path('test/question/', views.QuestionAPI.as_view()),
    path('test/question/answer/', views.student_answering_question),
    path('enroll/', views.student_enrolles_in_course),
    path('appear/', views.student_appears_for_test),
    path('enrolled/', views.get_enrolled_courses)
]