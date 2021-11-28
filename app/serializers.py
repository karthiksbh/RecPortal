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
            'option',
        ]


class QuizQuesSerializer(serializers.ModelSerializer):
    options = AnswerSerializer(many=True, read_only=True)
    quiz = QuizSerializer(read_only=True)

    class Meta:
        model = Question
        fields = [
            'quiz',
            'ques_main',
            'ques_type',
            'options',
        ]


class QuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'ques_main',
            'ques_type',
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
        fields = ['student', 'MCQ_score', 'Long_Ans_Score',
                  'Total', 'comments', 'submitted', 'domain']


class AnsSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['sub_student', 'question', 'answer', 'submitted_time']


class LongAnsSerializer(serializers.ModelSerializer):
    sub_student = UserDetSerializer(read_only=True)
    question = QuesSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = ['sub_student', 'id',
                  'question', 'answer', 'submitted_time', 'is_checked']


class AnswerAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = [
            'id',
            'option',
            'is_right',
        ]


class QuestionAddSerializer(serializers.ModelSerializer):
    options = AnswerAddSerializer(many=True)
    tag = TagSerializer(many=True)

    class Meta:
        model = Question
        fields = [
            'id',
            'domain',
            'ques_type',
            'mark_each',
            'ques_main',
            'options',
            'tag'
        ]

    def create(self, validated_data):
        answers = validated_data.pop('options')
        new_tag = validated_data.pop('tag')
        question = Question.objects.create(**validated_data)
        for answer in answers:
            Answer.objects.create(**answer, question=question)
        for temp in new_tag:
            QuestionsTags.objects.create(**temp, question=question)

        return question
