from django.core.checks import messages
from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import login,logout,authenticate


from rest_framework.authentication import  BasicAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class UserdetailsAPI(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = User.objects.all()
        data = UserSerializer(user, many=True).data
        return Response({"data": data})

    def post(self, request, *args, **kwargs):
        if User.objects.filter(username=request.data.get('username')).exists():
            return Response({"msg": "This useername is alredy taken Choose other "})
        data = UserSerializer(data=request.data, many=True)
        username = request.data.get('username')
        password = request.data.get('password')
        User.objects.create(username=username, password=password)
        return Response({"msg": "User created Success "})

    def put(self, request, *args, **kwargs):
        # print(request.data)
        if User.objects.filter(username=request.data.get('username')).exists():
            user = User.objects.get(username=request.data.get('username'))
            # print(user)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"msg": "Details updated Successfully !"})
            return Response({"msg": "Invalid data"})
        return Response({"msg": "no user found on this username !"})

    def patch(self, request, *args, **kwargs):
        if User.objects.filter(username=request.data.get('username')).exists():
            user = User.objects.get(username=request.data.get('username'))
            data = UserSerializer(user, data=request.data)
            if data.is_valid():
                data.save()
                return Response({"msg": "Profile updated successful !"})
            return Response({"msg": "Invalid data !"})
        return Response({"msg": "NOo user found on this username !"})

    # def delete(self, request, *args, **kwargs):
    #     if User.objects.filter(username=request.data.get('username')).exists():
    #         user = User.objects.get(username=request.data.get('username'))
    #         user.delete()
    #         return Response({"msg": "User deleted Success !"})
    #     return Response({"msg": "No user found on this username !"})


class DeleteUserAPI(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request,*args,**kwargs):
        if User.objects.filter(username=request.data.get('username')).exists():
            user=User.objects.get(username=request.data.get('username'),password=request.data.get('password'))
            user.delete()
            return Response({"msg":"User deleted Success "})
        return Response({"msg":"No User found ! "})
    
            

class LoginAPI(APIView):
    def post(self,request,*args,**kwargs):
        username= request.data.get('username')
        password=request.data.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return Response({"msg":"logged in Success !"})
        return Response({"msg":"Invalid details"})


class LogoutAPI(APIView):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            logout(request)
        return Response({"msg":"logout Success !"})
