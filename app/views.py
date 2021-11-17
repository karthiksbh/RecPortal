from rest_framework import response
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from .models import *
from .serializers import *
from rest_framework.views import APIView
from .helpers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime
from django.db.models import Q


class RegisterView(APIView):
    def post(self, request):
        try:
            email = request.data['email']
            if(email.find('@vitstudent.ac.in') == -1):
                return Response({'status': 404, 'message': 'Please Enter Your VIT Email ID'})
            else:
                serializer = UserSerializer(data=request.data)
                if not serializer.is_valid():
                    return Response({
                        'status': 403,
                        'errors': serializer.errors
                    })

                serializer.save()

                return Response({'status': 200, 'message': 'OTP sent to your mail'})

        except Exception as e:

            return Response({'status': 404, 'error': 'Error'})


class AdminRegisterView(APIView):
    def post(self, request):
        try:
            email = request.data['email']
            if(email.find('@vitstudent.ac.in') == -1):
                return Response({'status': 404, 'message': 'Please Enter Your VIT Email ID'})
            else:
                serializer = AdminSerializer(data=request.data)
                if not serializer.is_valid():
                    return Response({
                        'status': 403,
                        'errors': serializer.errors
                    })

                serializer.save()

                return Response({'status': 200, 'message': 'Admin Registered'})

        except Exception as e:
            print(e)

            return Response({'status': 404, 'error': 'Error'})


class VerifyOTP(APIView):
    def post(self, request):
        try:
            data = request.data
            user_obj = User.objects.get(email=data.get('email'))
            otp = data.get('otp')

            if user_obj.otp == otp:
                user_obj.is_email_verified = True
                user_obj.save()
                return Response({'status': 200, 'message': 'Email verified'})

            return Response({'status': 403, 'message': 'OTP wrong'})

        except Exception as e:
            print(e)
        return Response({'status': 404, 'error': 'something went wrong'})

    def patch(self, request):
        try:
            data = request.data
            user_obj = User.objects.filter(email=data.get('email'))
            if not user_obj.exists():
                return Response({'status': 200, 'message': 'No User Found'})

            status, time = send_otp_to_email(data.get('email'), user_obj[0])
            if status:
                return Response({'status': 200, 'message': 'OTP Sent Again'})

            return Response({'status': 404, 'error': f'try after {time} seconds'})

        except Exception as e:
            print(e)

        return Response({'status': 404, 'error': f'try after {time} seconds'})


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User Not Found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Password is Incorrect!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        jwt_token = jwt.encode(payload, 'Kihtrak',
                               algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=jwt_token, httponly=True)

        response.data = {
            'jwt': jwt_token
        }

        return response


class AdminLoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email, is_admin=True).first()

        if user is None:
            raise AuthenticationFailed('Admin Not Found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Password is Incorrect!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        jwt_token = jwt.encode(payload, 'Kihtrak',
                               algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=jwt_token, httponly=True)

        response.data = {
            'jwt': jwt_token,
            'message': "Admin Logged In",
        }

        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'Message': 'Logged Out'
        }

        return response


class QuizQues(APIView):
    def post(self, request):
        data = request.data
        domain_id = data.get('domain')
        question = Question.objects.filter(
            domain=domain_id)
        user_id = data.get('student')
        user = User.objects.filter(id=user_id).first()
        starttime = data.get('start_time')
        domain_id = Domain.objects.filter(id=domain_id).first()
        sub_data = Results(student=user, domain=domain_id, MCQ_score=0, Long_Ans_Score=0, Total=0,
                           submitted=False, start_time=starttime)
        sub_data.save()
        serializer = QuizQuesSerializer(question, many=True)

        return Response(serializer.data)


class UserDetView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('User Not Authenticated!')

        try:
            payload = jwt.decode(token, 'Kihtrak', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('User Not Authenticated!')

        user = User.objects.filter(id=payload['id']).first()

        serializer = UserDetSerializer(user)

        return Response(serializer.data)


class SubResView(APIView):
    def get(self, request, **kwargs):
        res = Results.objects.filter(domain=kwargs['topic'])
        serializer = FinalResSerializer(res, many=True)

        return Response(serializer.data)


class AnswerSubmissionView(APIView):
    def post(self, request):
        try:
            data = request.data
            user_id = data.get('user')
            user = User.objects.filter(id=user_id).first()

            ques_id = data.get('question')
            ques_of = Question.objects.filter(id=ques_id).first()
            ans_of = data.get('answer')
            sub_time = data.get('submitted_time')

            domain_id = data.get('domain')
            domain_id = Domain.objects.filter(id=domain_id).first()

            ans = Answer.objects.filter(
                question=ques_id, is_right=True).first()

            if(ans == None):
                ans = "123456789abcdef"

            print("The answer submitted is: " + str(ans_of))
            print("The correct answer is: " + str(ans))

            stu_result = Results.objects.get(
                Q(student=user) & Q(domain=domain_id))

            print(ques_of)

            stu_marks = Question.objects.get(
                Q(id=ques_id))

            if(str(ans_of) == str(ans)):
                stu_result.MCQ_score += stu_marks.mark_each
                stu_result.save()
            else:
                print("NOOO")

            stu_result.Total += stu_result.MCQ_score
            stu_result.save()

            sub_data = Submission(user=user, question=ques_of, answer=ans_of,
                                  correct_option=ans, submitted_time=sub_time)
            sub_data.save()

        #     serializer = AnsSubSerializer(data=request.data)
        #     if not serializer.is_valid():
        #         return Response({
        #             'status': 403,
        #             'errors': serializer.errors
        #         })

        #     serializer.save()

            return Response({'status': 200, 'message': 'Answer Submitted'})

        except Exception as e:
            print(e)

            return Response({'status': 404, 'error': 'Error'})


# class AddQuestionView(APIView):
#     def post(self, request, **kwargs):
#         question = Question.objects.filter(
#             domain=kwargs['topic'])
#         serializer = QuizQuesSerializer(question, many=True)

#         return Response(serializer.data)
