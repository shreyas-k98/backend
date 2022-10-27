from rest_framework.views import APIView
from rest_framework.response import Response
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

    