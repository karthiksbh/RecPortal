from django.db import connection
from rest_framework.response import Response
from ..models import *
from ..serializers import *
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


# Displaying Answers to the Admin of the Student
class LongResView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        try:
            user = request.user
            if(user.is_admin == True):
                res = Submission.objects.filter(
                    domain=kwargs['topic'], sub_student=kwargs['student'])
                serializer = LongAnsSerializer(res, many=True)
                return Response(serializer.data, status=200)
            else:
                return Response({'error': 'User Not Authorized'}, status=404)
        except Exception as e:
            return Response({'error': 'Something Went Wrong'}, status=404)


# Results for a particular domain (Admin)
class SubResView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        try:
            res = Results.objects.filter(domain=kwargs['topic'])
            serializer = FinalResSerializer(res, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({'error': 'Something Went Wrong'}, status=404)


# Long Answer Marks Updation by Admin: Admin checks the Long Answer and gives the marks
class MarkLongAdmin(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            user = data.get('user')
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
            return Response({'error': 'Something Went Wrong'}, status=404)


class getTime(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            user = request.user
            domain_id = data.get('domain')
            temp_domain = domain_id
            question = Question.objects.filter(
                domain=domain_id)
            user = User.objects.filter(id=user.id).first()

            domain_id = Domain.objects.filter(id=domain_id).first()

            student_exists = False
            student_exists = Results.objects.filter(
                student=user, domain=domain_id).exists()

            domain_info = Domain.objects.get(Q(domain_name=domain_id))
            time = domain_info.quiz_time

            if(student_exists == False):
                serializer = QuizQuesSerializer(question, many=True)

                return Response({'data': serializer.data, 'totalduration': time}, status=200)

            else:
                student_exists = Results.objects.get(
                    student=user, domain=domain_id)

                if(student_exists.submitted == True):
                    return Response({'message': 'Test Submitted'}, status=200)
                else:
                    serializer = QuizQuesSerializer(question, many=True)
                    return Response({'data': serializer.data, 'totalduration': time}, status=200)

        except Exception as e:
            return Response({'data': e}, status=404)
