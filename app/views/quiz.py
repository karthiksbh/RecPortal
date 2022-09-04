from rest_framework.response import Response
from ..models import *
from ..serializers import *
from rest_framework.views import APIView
from ..helpers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import datetime
from django.db.models import Q
from datetime import datetime
from datetime import date


# To get days, hours and minutes
def days_hours_minutes(td):
    return td.days, td.seconds//3600, (td.seconds//60) % 60


# Start Quiz or Resume Quiz:
class QuizQues(APIView):
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
            now = datetime.now().time()
            current_time = now.strftime("%H:%M:%S")
            domain_id = Domain.objects.filter(id=domain_id).first()
            today = date.today()

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
                    my_date = date.today()
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

        except Exception as e:
            return Response({'error': 'Something Went Wrong'}, status=404)


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
                ans = "None answer"

            stu_result = Results.objects.filter(
                Q(student=user) & Q(domain=domain_id))

            stu_result = stu_result.earliest('id')

            stu_marks = Question.objects.get(
                Q(id=ques_id))

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
                        stu_result.Total = stu_result.MCQ_score + stu_result.Long_Ans_Score
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


# To submit the test
class TestSubmitted(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            user = request.user
            domain_id = data.get('domain')
            result_sub = Results.objects.filter(
                Q(student=user) & Q(domain=domain_id))
            result_sub = result_sub.earliest('id')
            result_sub.submitted = True
            result_sub.save()
            return Response({'message': 'Test Has Been Submitted'}, status=200)
        except Exception as e:
            return Response({'error': 'Something Went Wrong'}, status=404)
