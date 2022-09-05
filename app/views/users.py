from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from ..models import *
from ..serializers import *
from rest_framework.views import APIView
from ..helpers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed


# User Registration: To Register a New User
class RegisterView(APIView):
    def post(self, request):
        try:
            email = request.data['email']
            reg_no = request.data['reg_no']
            if (email.find('@vitstudent.ac.in') == -1):
                return Response({'message': 'Please Enter Your VIT Email ID'}, status=404)
            else:
                user_exists = User.objects.filter(email=email).exists()
                if (user_exists == True):
                    return Response({'message': 'User with the given Email ID already exists'}, status=404)
                regNo_exists = User.objects.filter(reg_no=reg_no).exists()
                if (regNo_exists == True):
                    return Response({'message': 'User with the given Registration Number exists already exists'}, status=404)
                serializer = UserSerializer(data=request.data)
                if not serializer.is_valid():
                    return Response({'errors': 'Email or Registration Number Already Exists'}, status=404)
                serializer.save()
                return Response({'message': 'OTP sent to your mail'}, status=200)
        except Exception as e:
            return Response({'error': 'Something Went Wrong'}, status=404)


# Admin Registration: To register an Admin
class AdminRegisterView(APIView):
    def post(self, request):
        try:
            serializer = AdminSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({'errors': serializer.errors}, status=404)
            serializer.save()
            return Response({'message': 'Admin Registered'}, status=200)
        except Exception as e:
            return Response({'error': 'Something Went Wrong'}, status=404)


# OTP Verification: To verify the user by sending OTP to their mail
class VerifyOTP(APIView):
    def post(self, request):
        try:
            data = request.data
            user_obj = User.objects.get(email=data.get('email'))
            otp = data.get('otp')

            if user_obj.otp == otp:
                user_obj.is_email_verified = True
                user_obj.save()
                return Response({'message': 'Email verified'}, status=200)
            return Response({'message': 'Incorrect OTP'}, status=403)
        except Exception as e:
            return Response({'error': 'Something Went Wrong'}, status=404)


# Generate OTP: Generate an OTP
class Generate_OTP(APIView):
    def get(self, request):
        try:
            user = request.user
            Util.send_otp_to_email(user.email, user)
            return Response({'message': 'OTP Sent to the Mail'}, status=200)

        except Exception as e:
            return Response({'error': 'Something Went Wrong'}, status=404)


# User Login: Login a regular User
class LoginView(APIView):
    def post(self, request):
        try:
            email = request.data['email']
            password = request.data['password']
            user = User.objects.filter(email=email, is_admin=False).first()

            if user is None:
                raise AuthenticationFailed('User Not Found!')

            if not user.check_password(password):
                raise AuthenticationFailed('Password is Incorrect!')

            refresh = RefreshToken.for_user(user)
            return Response({'jwt': str(refresh.access_token), 'refresh_token': str(refresh)}, status=200)
        except Exception as e:
            return Response({'error': 'Something Went Wrong'}, status=404)


# Admin Login: Login an Admin User
class AdminLoginView(APIView):
    def post(self, request):
        try:
            email = request.data['email']
            password = request.data['password']
            user = User.objects.filter(email=email, is_admin=True).first()

            if user is None:
                raise AuthenticationFailed('Admin Not Found!')
            if not user.check_password(password):
                raise AuthenticationFailed('Password is Incorrect!')

            refresh = RefreshToken.for_user(user)
            return Response({'jwt': str(refresh.access_token), 'refresh_token': str(refresh)}, status=200)

        except Exception as e:
            return Response({'error': 'Something Went Wrong'}, status=404)


# Log Out
class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.auth.delete()
            return Response({'Message': 'Logged Out'}, status=200)
        except Exception as e:
            return Response({'error': 'Something Went Wrong'}, status=404)


# To know all the tests submitted by the user
def tests_submitted(user):
    try:
        tests_done = []

        CSE_exists = Results.objects.filter(
            student=user, domain=1, submitted=True).exists()
        if (CSE_exists == True):
            tests_done.append("Tech CSE")

        MGT_exists = Results.objects.filter(
            student=user, domain=5, submitted=True).exists()
        if (MGT_exists == True):
            tests_done.append("Management")

        ECE_exists = Results.objects.filter(
            student=user, domain=2, submitted=True).exists()
        if (ECE_exists == True):
            tests_done.append("Tech ECE")

        Edit_exists = Results.objects.filter(
            student=user, domain=3, submitted=True).exists()
        if (Edit_exists == True):
            tests_done.append("Editorial")

        Design_exists = Results.objects.filter(
            student=user, domain=4, submitted=True).exists()
        if (Design_exists == True):
            tests_done.append("Design")

        return tests_done

    except Exception as e:
        return Response({'error': 'Something Went Wrong'}, status=404)


# Class which calls the tests submitted function
class TestsSubmitted(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            done = tests_submitted(user)
            return Response({'submitted': done}, status=200)
        except Exception as e:
            return Response({'error': 'Something Went Wrong'}, status=404)


# Logged in User Details: To get the details of the logged in User
class UserDetView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            serializer = UserDetSerializer(user)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({'error': 'Something Went Wrong'}, status=404)
