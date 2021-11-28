from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import authentication, response
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
from datetime import datetime


class RegisterView(APIView):
    def post(self, request):
        try:
            # if('email' not in request.data.keys()):
            #     return Response({'status':404})
            email = request.data['email']
            if(email.find('@vitstudent.ac.in') == -1):
                return Response({'status': 404, 'message': 'Please Enter Your VIT Email ID'})
            else:
                serializer = UserSerializer(data=request.data)
                if not serializer.is_valid():
                    print(serializer.errors)
                    return Response({
                        'status': 403,
                        'errors': serializer.errors
                    })

                serializer.save()

                return Response({'status': 200, 'message': 'OTP sent to your mail'})

        except Exception as e:
            print(e)

            return Response({'status': 404, 'error': serializer.errors})


class AdminRegisterView(APIView):
    def post(self, request):
        try:
            email = request.data['email']
            if(email.find('@vitstudent.ac.in') == -1):
                return Response({'status': 404, 'message': 'Please Enter Your VIT Email ID'})
            else:
                serializer = AdminSerializer(data=request.data)
                if not serializer.is_valid():
                    print(serializer.errors)
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

        user = User.objects.filter(email=email, is_admin=False).first()

        if user is None:
            raise AuthenticationFailed('User Not Found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Password is Incorrect!')

        refresh = RefreshToken.for_user(user)

        return Response({'jwt': str(refresh.access_token)})


class AdminLoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email, is_admin=True).first()

        if user is None:
            raise AuthenticationFailed('Admin Not Found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Password is Incorrect!')

        refresh = RefreshToken.for_user(user)

        return Response({'jwt': str(refresh.access_token)})


class LogoutView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response()
        response.data = {
            'Message': 'Logged Out'
        }

        return response


class QuizQues(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user
        print(user.id)
        domain_id = data.get('domain')
        question = Question.objects.filter(
            domain=domain_id)
        user = User.objects.filter(id=user.id).first()

        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")

        domain_id = Domain.objects.filter(id=domain_id).first()

        student_exists = False
        student_exists = Results.objects.filter(
            student=user, domain=domain_id).exists()

        domain_info = Domain.objects.get(Q(domain_name=domain_id))
        time = domain_info.quiz_time

        if(student_exists == False):
            sub_data = Results(student=user, domain=domain_id, MCQ_score=0, Long_Ans_Score=0, Total=0,
                               submitted=False, start_time=current_time)
            sub_data.save()
            serializer = QuizQuesSerializer(question, many=True)

            return Response({'status': 200, 'data': serializer.data, 'Start Time': current_time, 'Total Duration': time})

        else:
            student_exists = Results.objects.get(
                student=user, domain=domain_id)
            starttime = student_exists.start_time
            serializer = QuizQuesSerializer(question, many=True)

            return Response({'status': 200, 'data': serializer.data, 'Start Time': starttime, 'Total Duration': time})


class UserDetView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        print(user)

        serializer = UserDetSerializer(user)

        return Response(serializer.data)


class SubResView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        res = Results.objects.filter(domain=kwargs['topic'])
        serializer = FinalResSerializer(res, many=True)

        return Response(serializer.data)


class AnswerSubmissionView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            print(user.id)
            data = request.data
            user = User.objects.filter(id=user.id).first()

            ques_id = data.get('question')
            ques_of = Question.objects.filter(id=ques_id).first()
            ans_of = data.get('option')

            now = datetime.now()

            current_time = now.strftime("%H:%M:%S")
            question_type = data.get('ques_type')

            domain_id = data.get('domain')
            domain_id = Domain.objects.filter(id=domain_id).first()

            ans = Answer.objects.filter(
                question=ques_id, is_right=True).first()

            if(ans == None):
                ans = "mnxjdiffjdkks"

            stu_result = Results.objects.get(
                Q(student=user) & Q(domain=domain_id))

            stu_marks = Question.objects.get(
                Q(id=ques_id))

            if(str(ans_of) == str(ans)):
                marks_each = stu_marks.mark_each
                stu_result.MCQ_score += stu_marks.mark_each
                stu_result.Total += stu_result.MCQ_score
                stu_result.save()
            else:
                marks_each = 0

            if(question_type == 0):
                sub_data = Submission(sub_student=user, question=ques_of, answer=ans_of,
                                      correct_option=ans, submitted_time=current_time, ques_type=question_type, domain=domain_id, is_checked=True, mark_ques=marks_each)
                sub_data.save()

            else:
                sub_data = Submission(sub_student=user, question=ques_of, answer=ans_of,
                                      correct_option=ans, submitted_time=current_time, ques_type=question_type, domain=domain_id, is_checked=False, mark_ques=0)
                sub_data.save()

            return Response({'status': 200, 'message': 'Answer Submitted'})

        except Exception as e:
            print(e)

            return Response({'status': 404, 'error': 'Error'})


class LongResView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        user = request.user
        if(user.is_admin == True):
            res = Submission.objects.filter(
                domain=kwargs['topic'], sub_student=kwargs['student'])
            print(res)
            serializer = LongAnsSerializer(res, many=True)

            return Response(serializer.data)

        else:
            return Response({'status': 404, 'error': 'User Not Authorized'})


class MarkLongAdmin(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            user = data.get('user')
            print(user)
            user_id = User.objects.filter(id=user).first()

            ques_id = data.get('question')
            ques_of = Question.objects.filter(id=ques_id).first()

            domain_id = data.get('domain')
            domain_id = Domain.objects.filter(id=domain_id).first()

            sub = Submission.objects.get(
                Q(question=ques_id) & Q(sub_student=user_id) & Q(domain=domain_id) & Q(ques_type=1))

            print(sub)

            initial_mark = sub.mark_ques

            result_sub = Results.objects.get(
                Q(student=user) & Q(domain=domain_id))
            print(result_sub)

            result_sub.Long_Ans_Score = result_sub.Long_Ans_Score - initial_mark
            result_sub.Total = result_sub.Total - initial_mark

            mark_each = data.get('marks')

            sub.mark_ques = mark_each
            sub.is_checked = True
            result_sub.Long_Ans_Score += mark_each
            result_sub.Total += mark_each
            sub.save()
            result_sub.save()

            return Response({'status': 200, 'message': 'Long Answer Mark Updated'})

        except Exception as e:
            print(e)
            return Response({'status': 404, 'error': 'Error'})


class QuestionAddView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = QuestionAddSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'status': 403,
                    'errors': serializer.errors
                })

            serializer.save()

            return Response({'status': 200, 'data': serializer.data})

        except Exception as e:
            print(e)
            return Response({'status': 404, 'error': 'Error'})


class TestSubmitted(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            user = request.user

            domain_id = data.get('domain')

            result_sub = Results.objects.get(
                Q(student=user) & Q(domain=domain_id))

            result_sub.submitted = True

            result_sub.save()

            return Response({'status': 200, 'message': 'Test Has Been Submitted'})

        except Exception as e:
            print(e)
            return Response({'status': 404, 'error': 'Error'})


class QuesAnsAdminView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        user = request.user
        if(user.is_admin == True):
            question = Question.objects.filter(
                domain=kwargs['topic'])

            serializer = QuizQuesSerializer(question, many=True)

            return Response({'status': 200, 'data': serializer.data})

        else:
            return Response({'status': 404, 'error': 'User Not Authorized'})


class CommentAdminView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            data = request.data
            if(user.is_admin == True):
                user_id = data.get('user')
                domain_id = data.get('domain')
                comment = data.get('comments')

                result_sub = Results.objects.get(
                    Q(student=user_id) & Q(domain=domain_id))

                result_sub.comments = comment

                result_sub.save()

                return Response({'status': 200, 'message': 'Comments added'})

            else:
                return Response({'status': 404, 'error': 'User Not Authorized'})
        except Exception as e:
            print(e)
            return Response({'status': 404, 'error': 'Error'})
