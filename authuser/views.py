from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http import JsonResponse
from rest_framework import generics
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericAPIView
from .serializers import *
from .emails import *


class RegisterAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                send_otp_via_email(serializer.data["useremail"])
                return Response(
                    {
                        "status": 200,
                        "message": "registration is successfull check email",
                        "data": serializer.data,
                    }
                )
            return Response(
                {
                    "status": 400,
                    "message": "something went wrong",
                    "data": serializer.errors,
                }
            )
        except Exception as e:
            print(e)


@api_view(["POST"])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({"message": "Logged in successfully."})
    else:
        return Response(
            {"message": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED
        )


class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class VerifyOTP(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyAccountSerializer(data=data)

            if serializer.is_valid():
                email = serializer.data["email"]
                otp = serializer.data["otp"]
                user = User.objects.filter(email=email)
                if not user.exists():
                    return Response(
                        {
                            "status": 400,
                            "message": "something went wrong",
                            "data": "invalid email",
                        }
                    )

                if user[0].otp != otp:
                    return Response(
                        {
                            "status": 400,
                            "message": "something went wrong",
                            "data": "wrong otp",
                        }
                    )
                user = user.first()
                user.is_verified = True
                user.save()

                return Response(
                    {
                        "status": 200,
                        "message": "account verified",
                        "data": serializer.data,
                    }
                )
            return Response(
                {
                    "status": 400,
                    "message": "something went wrong",
                    "data": serializer.errors,
                }
            )

        except Exception as e:
            print(e)
