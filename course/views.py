from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
from .serializers import *
# from rest_framework import authentication, permissions
# from django.contrib.auth.models import User


class CourseAPI(APIView):
    def get(self, request):
        course = Course.objects.all()
        serializer = CourseSerializer(course, many = True)
        for i in serializer.data:
            course = Course.objects.filter(id = i['id'])
            i['creator_name'] = course[0].creator_name.username
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        user = request.user

        if user is not None and user.is_staff == True:
            data['creator_name'] = user.id
            serializer = CourseSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "info": "Course created successfully"
                })
        else:
            return Response({
                "status": "failure",
                "info": "either no user logged in or logged in with student account"
            })

class TetsAPI(APIView):
    def get(self, request):
        test = Test.objects.all()
        serializer = TestSerializer(test, many = True)
        for i in serializer.data:
            test = Test.objects.filter(id = i['id'])
            i['course_related'] = test[0].course_related.course_name
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        user = request.user
        print(data)
        if user is not None and user.is_staff == True:
            # course = Course.objects.filter(course_name = data['course_related'])
            # data['course_related'] = course[0].id
            serializer = TestSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "info": "test posted succcessfully"
                })
            else:
                return Response({
                    "info": "serialzer invalid"
                })
        return Response({
                "status": "failure",
                "info": "either no user logged in or logged in with student account"
            })

class QuestionAPI(APIView):
    def get(self, request):
        question = Question.objects.all()
        serializer = QuestionSerializer(question, many = True)
        for i in serializer.data:
            test = Test.objects.filter(id = i['test_related'])
            i['test_related'] = test[0].test_name
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        user = request.user
        print(data)
        if user is not None and user.is_staff == True:
            # test = Test.objects.filter(test_name = data['test_related'])
            # data['test_related'] = test[0].id
            serializer = QuestionSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "info": "question added successfully"
                })
        else:
            return Response({
                "status": "failure",
                "info": "either no user logged in or logged in with student account"
            })

@api_view(['POST'])
def student_answering_question(request):
    data = request.data
    user = request.user

    if user is not None and user.is_staff == False:
        data['given_by_student'] = user.id
        question = Question.objects.filter(question = data['question_related'])
        test = Test.objects.filter(test_name = question[0].test_related)
        data['test_related'] = test[0].id
        data['question_related'] = question[0].id
        serializer = SelectedAnswerSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "info": "student answerd the question"
            })
        else:
            return Response({
                "info": "serializer not valid"
            })
    else:
        return Response({
            "status": "failure",
            "info": "no user logged in"
        })

@api_view(['POST'])
def student_enrolles_in_course(request):
    data = request.data
    user = request.user
    
    if user.id is not None and user.is_staff == False:
        print(user.username)
        data['student'] = user.id
        course = Course.objects.filter(course_name = data['course_enrolled'])
        data['course_enrolled'] = course[0].id
        print(data['student'], data['course_enrolled'])
        serializer = StudentCourseSerilizer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "info": "student enrolled for course"
            })
        else:
            return Response({
                "info": "serializer not valid"
            })
    else:
        return Response({
            "status": "failure",
            "info": "User not logged in or not a student"
        })

@api_view(['POST'])
def student_appears_for_test(request):
        data = request.data
        user = request.user

        if user.id is not None and user.is_staff == False:
            data['given_by_student'] = user.id
            data['start_time'] = datetime.datetime.now()
            test = Test.objects.filter(test_name = data['test_related'])
            data['test_related'] = test[0].id
            data['end_time'] = datetime.datetime.now() + test[0].duration
            serializer = TestAppearedSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "info": "student appeared for test"
                })
            else:
                return Response({
                    "status": "failure",
                    "info": "invalid serializer"
                })


@api_view(['GET'])
def get_enrolled_courses(request):
    user = request.user
    if user is not None and user.is_staff == False:
        courses = StudentCourse.objects.filter(student = user.id)
        serializer = StudentCourseSerilizer(courses, many=True)
        for i in serializer.data:
            course = Course.objects.get(id = i.get('course_enrolled'))
            i['course_name'] = course.course_name
        return Response(serializer.data)