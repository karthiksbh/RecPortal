from xml.sax import xmlreader
from django.db import connection, connections
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
from datetime import date
import sqlite3
my_date = date(2021, 3, 2)


# User Registration
class RegisterView(APIView):
    def post(self, request):
        try:
            email = request.data['email']
            if(email.find('@vitstudent.ac.in') == -1):
                return Response({'message': 'Please Enter Your VIT Email ID'}, status=404)
            else:
                serializer = UserSerializer(data=request.data)
                if not serializer.is_valid():
                    return Response({'errors': 'Email or Registration Number Already Exists'}, status=403)
                serializer.save()

                return Response({'message': 'OTP sent to your mail'}, status=200)

        except Exception as e:
            print(e)
            return Response({'error': 'Something Went Wrong'}, status=404)


# Admin Registration
class AdminRegisterView(APIView):
    def post(self, request):
        try:
            email = request.data['email']
            if(email.find('@vitstudent.ac.in') == -1):
                return Response({'message': 'Please Enter Your VIT Email ID'}, status=404)
            else:
                serializer = AdminSerializer(data=request.data)
                if not serializer.is_valid():
                    return Response({'errors': serializer.errors}, status=403)
                serializer.save()
                return Response({'message': 'Admin Registered'}, status=200)

        except Exception as e:
            print(e)
            return Response({'error': 'Something Went Wrong'}, status=404)


# OTP Verification
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
            print(e)
        return Response({'error': 'Something Went Wrong'}, status=404)


# Generate OTP
class Generate_OTP(APIView):
    def get(self, request):
        try:
            user = request.user
            send_otp_to_email(user.email, user)

            return Response({'message': 'OTP Sent to the Mail'}, status=200)

        except Exception as e:
            print(e)
        return Response({'error': 'Something Went Wrong'}, status=404)


def tests_submitted(user):
    try:
        tests_done = []
        CSE_exists = False
        CSE_exists = Results.objects.filter(
            student=user, domain=1).exists()
        if(CSE_exists == True):
            tests_done.append("TECH CSE")

        MGT_exists = False
        MGT_exists = Results.objects.filter(
            student=user, domain=5).exists()
        if(MGT_exists == True):
            tests_done.append("Management")

        ECE_exists = False
        ECE_exists = Results.objects.filter(
            student=user, domain=2).exists()
        if(ECE_exists == True):
            tests_done.append("TECH ECE")

        Edit_exists = False
        Edit_exists = Results.objects.filter(
            student=user, domain=3).exists()
        if(Edit_exists == True):
            tests_done.append("Editorial")

        Design_exists = False
        Design_exists = Results.objects.filter(
            student=user, domain=4).exists()
        if(Design_exists == True):
            tests_done.append("Design")

        print(tests_done)

        return tests_done

    except Exception as e:
        print(e)


# User Login
class LoginView(APIView):
    def post(self, request):
        user_exists = False
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email, is_admin=False).first()

        if user is not None:
            print(user)
            done = tests_submitted(user)

        if user is None:
            raise AuthenticationFailed('User Not Found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Password is Incorrect!')

        refresh = RefreshToken.for_user(user)

        return Response({'jwt': str(refresh.access_token), 'submitted': done}, status=200)


# Admin Login
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

        return Response({'jwt': str(refresh.access_token)}, status=200)


# Log Out
class LogoutView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({'Message': 'Logged Out'}, status=200)


# Logged in User Details
class UserDetView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserDetSerializer(user)

        return Response(serializer.data, status=200)


def days_hours_minutes(td):
    return td.days, td.seconds//3600, (td.seconds//60) % 60


# Start Quiz or Resume Quiz
class QuizQues(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user
        domain_id = data.get('domain')
        temp_domain = domain_id
        print(domain_id)
        question = Question.objects.filter(
            domain=domain_id)
        user = User.objects.filter(id=user.id).first()

        now = datetime.now().time()

        current_time = now.strftime("%H:%M:%S")

        domain_id = Domain.objects.filter(id=domain_id).first()

        today = date.today()

        student_exists = False
        student_exists = Results.objects.filter(
            student=user, domain=domain_id).exists()

        domain_info = Domain.objects.get(Q(domain_name=domain_id))
        time = domain_info.quiz_time

        if(student_exists == False):
            sub_data = Results(student=user, domain=domain_id, MCQ_score=0, Long_Ans_Score=0, Total=0,
                               submitted=False, start_time=current_time, domain_temp=temp_domain, date_start=today)
            sub_data.save()
            serializer = QuizQuesSerializer(question, many=True)

            return Response({'data': serializer.data, 'starttime': current_time, 'totalduration': time}, status=200)

        else:

            student_exists = Results.objects.get(
                student=user, domain=domain_id)

            if(student_exists.submitted == True):
                return Response({'message': 'Test Submitted'}, status=200)
            else:
                starttime = student_exists.start_time
                serializer = QuizQuesSerializer(question, many=True)

                datetime1 = datetime.combine(my_date, starttime)
                datetime2 = datetime.combine(my_date, now)
                time_elapsed = datetime2 - datetime1
                rem_time = days_hours_minutes(time_elapsed)

                hours = rem_time[1]
                minutes = rem_time[2]

                if(hours >= 1 or minutes > time or today != student_exists.date_start):
                    student_exists.submitted = True
                    student_exists.save()
                    return Response({'message': 'Test Submitted'}, status=403)
                else:
                    return Response({'data': serializer.data, 'starttime': starttime, 'totalduration': time}, status=200)


# Discrepencies Increase and Decrease (maximum dis = 5)
class IncDis(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            user = request.user

            domain_id = data.get('domain')

            result_sub = Results.objects.get(
                Q(student=user) & Q(domain=domain_id))

            result_sub.discrepancies += 1
            result_sub.save()

            remaining = 5 - result_sub.discrepancies

            if(remaining == 0):
                result_sub.submitted = True
                result_sub.save()

                return Response({'message': 'Test Has Been Submitted'}, status=200)

            else:
                return Response({'Discrepancies Remaining': remaining}, status=200)

        except Exception as e:
            print(e)
            return Response({'error': 'Something Went Wrong'}, status=404)


# Submit Answer with Update
class AnswerSubmissionView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
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
                ans = "mnxjdiffjdkksasdada"

            stu_result = Results.objects.get(
                Q(student=user) & Q(domain=domain_id))

            stu_marks = Question.objects.get(
                Q(id=ques_id))

            student_submitted = False
            student_submitted = Submission.objects.filter(
                sub_student=user, domain=domain_id, question=ques_of).exists()

            if(student_submitted == False):

                if(str(ans_of) == str(ans)):
                    marks_each = stu_marks.mark_each
                    stu_result.MCQ_score += marks_each
                    stu_result.Total += marks_each
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

                return Response({'message': 'Answer Submitted'}, status=200)

            else:
                if(question_type == 0):
                    marks_before = Submission.objects.get(
                        sub_student=user, domain=domain_id, question=ques_of)
                    stu_result.MCQ_score = stu_result.MCQ_score - marks_before.mark_ques
                    stu_result.Total = stu_result.Total - marks_before.mark_ques
                    stu_result.save()

                    if(str(ans_of) == str(ans)):
                        marks_each = stu_marks.mark_each
                        stu_result.MCQ_score += stu_marks.mark_each
                        stu_result.Total += stu_result.MCQ_score
                        stu_result.save()
                    else:
                        marks_each = 0

                    marks_before.mark_ques = marks_each
                    marks_before.save()

                    student_ans = Submission.objects.get(
                        sub_student=user, domain=domain_id, question=ques_of)

                    student_ans.answer = ans_of
                    student_ans.save()

                else:
                    student_ans = Submission.objects.get(
                        sub_student=user, domain=domain_id, question=ques_of)

                    student_ans.answer = ans_of
                    student_ans.save()

                return Response({'message': 'Answer Submitted'}, status=200)

        except Exception as e:

            return Response({'error': 'Something Went Wrong'}, status=404)


# For submitting the test by the user
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

            return Response({'message': 'Test Has Been Submitted'}, status=200)

        except Exception as e:
            print(e)
            return Response({'error': 'Something Went Wrong'}, status=404)


# Displaying Answers to the Admin of the Student
class LongResView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        user = request.user
        if(user.is_admin == True):
            res = Submission.objects.filter(
                domain=kwargs['topic'], sub_student=kwargs['student'])
            serializer = LongAnsSerializer(res, many=True)

            return Response(serializer.data, status=200)

        else:
            return Response({'error': 'User Not Authorized'}, status=404)


# Results for a particular domain (Admin)
class SubResView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        res = Results.objects.filter(domain=kwargs['topic'])
        serializer = FinalResSerializer(res, many=True)

        return Response(serializer.data, status=200)


# Long Answer Marks Updation by Admin
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

            initial_mark = sub.mark_ques

            result_sub = Results.objects.get(
                Q(student=user) & Q(domain=domain_id))

            result_sub.Long_Ans_Score = result_sub.Long_Ans_Score - initial_mark
            result_sub.Total = result_sub.Total - initial_mark

            mark_ofques = data.get('marks')

            if(mark_ofques > ques_of.mark_each):
                return Response({'error': 'Cannot award more than the maximum marks'}, status=200)

            else:
                sub.mark_ques = mark_ofques
                sub.is_checked = True
                result_sub.Long_Ans_Score += mark_ofques
                result_sub.Total += mark_ofques
                sub.save()
                result_sub.save()

                return Response({'message': 'Long Answer Mark Updated'}, status=200)

        except Exception as e:
            print(e)
            return Response({'error': 'Something Went Wrong'}, status=404)


# Displaying Questions of one particular domain
class QuesAnsAdminView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        user = request.user
        if(user.is_admin == True):
            question = Question.objects.filter(
                domain=kwargs['topic'])

            serializer = QuizQuesSerializer(question, many=True)

            return Response({'data': serializer.data}, status=200)

        else:
            return Response({'error': 'User Not Authorized'}, status=404)


# Add comments to the student by the admin
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

                return Response({'message': 'Comments added'}, status=200)

            else:
                return Response({'error': 'User Not Authorized'}, status=404)
        except Exception as e:
            print(e)
            return Response({'error': 'Something Went Wrong'}, status=404)


# To make the result of student as checked (all answers checked)
class Student_check(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            data = request.data
            if(user.is_admin == True):
                user_id = data.get('user')
                domain_id = data.get('domain')

                result_of = Results.objects.get(
                    Q(student=user_id) & Q(domain=domain_id))

                result_of.save()

                return Response({'message': 'Student Checking Done'}, status=200)

            else:
                return Response({'error': 'User Not Authorized'}, status=404)
        except Exception as e:
            print(e)
            return Response({'error': 'Something Went Wrong'}, status=404)


# All the questions checked for the student
class AdminStudentCheck(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            data = request.data
            if(user.is_admin == True):
                user_id = data.get('user')
                domain_id = data.get('domain')

                result_sub = Results.objects.get(
                    Q(student=user_id) & Q(domain=domain_id))

                result_sub.result_checked = True
                result_sub.save()

                return Response({'message': 'Answers Checked for the Student'}, status=200)

            else:
                return Response({'error': 'User Not Authorized'}, status=404)
        except Exception as e:
            print(e)
            return Response({'error': 'Something Went Wrong'}, status=404)


# To count the students in each domain and send
class StudentCount(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            if(user.is_admin == True):
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT count(*) from app_results WHERE result_checked is True")
                row = cursor.fetchone()

                cursor.execute(
                    "SELECT count(*) from app_results WHERE result_checked is False")
                row_2 = cursor.fetchone()

                cursor.execute(
                    "SELECT count(*) from app_results WHERE domain_temp=1")
                CSE_students = cursor.fetchone()

                cursor.execute(
                    "SELECT count(*) from app_results WHERE domain_temp=2")
                ECE_students = cursor.fetchone()

                cursor.execute(
                    "SELECT count(*) from app_results WHERE domain_temp=3")
                EDITORIAL_students = cursor.fetchone()

                cursor.execute(
                    "SELECT count(*) from app_results WHERE domain_temp =4")
                DSN_students = cursor.fetchone()

                cursor.execute(
                    "SELECT count(*) from app_results WHERE domain_temp =5")
                MGT_students = cursor.fetchone()

                return Response({'CSE': CSE_students[0], 'ECE': ECE_students[0], 'Editorial': EDITORIAL_students[0], 'Design': DSN_students[0], 'Management': MGT_students[0], 'checked': row[0], 'not_checked': row_2[0]}, status=200)
            else:
                return Response({'error': 'User Not Authorized'}, status=404)

        except Exception as e:
            print(e)
            return Response({'error': 'Something Went Wrong'}, status=404)


class TestsSubmitted(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            done = tests_submitted(user)
            return Response({'submitted': done}, status=200)

        except Exception as e:
            print(e)
            return Response({'error': 'Something Went Wrong'}, status=404)
