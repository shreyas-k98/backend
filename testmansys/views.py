from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .serializers import UserSerializer

class Student(APIView):
    def get(self, request):
        user = User.objects.filter(is_staff = False)
        serializer = UserSerializer(user, many = True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = User.objects.create_user(username = data['username'], password = data['password'])
            user.email = data['email']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.is_staff = False
            user.save()
            return Response({
                "status": "success",
                "info": "Student created successfully"
            })
            
class Staff(APIView):
    def get(self, request):
        staff = User.objects.filter(is_staff = True)
        serializer = UserSerializer(staff, many = True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = User.objects.create_user(username = data['username'], password = data['password'], email = data['email'])
            user.is_staff = True
            user.save()
            return Response({
                "status": "success",
                "info": "Staff created successfully"
            })

@method_decorator(csrf_exempt, name="dispatch")
class UserLogin(APIView):
    @csrf_exempt
    def post(self, request): # login user by username and password
        data = request.data
        user = authenticate(username = data['username'], password = data['password'])
        if user is not None:
            login(request, user)
            return Response({
                "status": "success",
                "current_user": data['username']
            })
        else:
            return Response({
                "status": "failure",
                "info": "Invalid Login Credentials or User Done Not Exists"
            })

    
    def get(self, request): # get details of the current user
        user = request.user
        if user is not None:
            return Response({
                "current_user": user.username
            })
        else:
            return Response({
                "info": "no user logged in"
            })
    
    def delete(self, request): # logout current user
        logout(request)
        return Response({
            "info": "Successfully logged out"
        })

@api_view(['GET'])
def get_curr_user_details(request): 
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)