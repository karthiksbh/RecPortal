from .models import Answer, Domain, Question, QuestionsTags, User, Submission, Results
from rest_framework import serializers
from app.helpers import send_otp_to_email
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'reg_no', 'email', 'password', 'phone']
        abstract = True

    def create(self, validated_data):
        user = User.objects.create(name=validated_data['name'], reg_no=validated_data['reg_no'],
                                   email=validated_data['email'], phone=validated_data['phone'])
        user.set_password(validated_data['password'])
        user.save()
        send_otp_to_email(user.email, user)
        return user


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'reg_no', 'email', 'password', 'phone']
        abstract = True

    def create(self, validated_data):
        user = User.objects.create(name=validated_data['name'], reg_no=validated_data['reg_no'],
                                   email=validated_data['email'], phone=validated_data['phone'], is_admin=True)
        user.set_password(validated_data['password'])
        user.save()
        return user


class QuizSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Domain
        fields = [
            'id',
            'domain_name',
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionsTags
        fields = ['tags']


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = [
            'answer_text',
        ]


class QuizQuesSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(many=True, read_only=True)
    quiz = QuizSerializer(read_only=True)

    class Meta:
        model = Question
        fields = [
            'id',
            'quiz',
            'ques_main',
            'ques_type',
            'answer',
        ]


class UserDetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'reg_no',
                  'email', 'phone', 'is_email_verified', 'is_admin']


class FinalResSerializer(serializers.ModelSerializer):
    student = UserDetSerializer(read_only=True)

    class Meta:
        model = Results
        fields = ['student', 'Total', 'comments', 'submitted']


class AnsSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['user', 'question', 'answer', 'submitted_time']


# class AnswerInsert(serializers.ModelSerializer):
#     class Meta:
#         model = Answer
#         fields = ['answer_text', 'is_right']


# class QuesSubSerializer(serializers.ModelSerializer):
#     answer = AnswerInsert(many=True)

#     class Meta:
#         model = Question
#         fields = ['domain', 'ques_type',
#                   'mark_each', 'ques_main', 'answer']
