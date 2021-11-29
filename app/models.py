from django.utils.translation import gettext_lazy as _
from django.db.models.fields import related
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager


class User(AbstractUser):
    username = None
    reg_no = models.CharField(
        max_length=100, unique=True)
    is_admin = models.BooleanField(default=False)
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=12)
    is_email_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.id)


class Domain(models.Model):
    domain_name = models.CharField(max_length=255, unique=True)
    quiz_time = models.IntegerField()

    def __str__(self):
        return str(self.domain_name)


QUESTION_TYPE = (
    (0, _('MCQ')),
    (1, _('LONG')),
)


class Question(models.Model):

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ['id']

    domain = models.ForeignKey(
        Domain, related_name='domain', on_delete=models.CASCADE)
    ques_type = models.IntegerField(
        choices=QUESTION_TYPE, default=0, verbose_name=_("Question Type"))
    mark_each = models.IntegerField(
        default=0, verbose_name=_("Mark for the Question"))
    ques_main = models.CharField(max_length=255, verbose_name=_("Question"))

    def __str__(self):
        return str(self.id)


class Answer(models.Model):

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
        ordering = ['id']

    question = models.ForeignKey(
        Question, related_name='options', on_delete=models.CASCADE)
    option = models.CharField(max_length=255, verbose_name=_("Answer"))
    is_right = models.BooleanField(default=False)

    def __str__(self):
        return str(self.option)


QUESTION_TAGS = (
    (_('Microcontroller and Microprocessors'),
     _('Microcontroller and Microprocessors')),
    (_('Digital logic design'), _('Digital logic design')),
    (_('Sensors'), _('Sensors')),
    (_('Basic electronics'), _('Basic electronics')),
    (_('IoT'), _('IoT')),
    (_('Python'), _('Python')),
    (_('DSA - Trees mostly'), _('DSA - Trees mostly')),
    (_('Competitive Coding'), _('Competitive Coding')),
    (_('CAO - basic computer knowledge stuff'),
     _('CAO - basic computer knowledge stuff')),
    (_('Logical reasoning '), _('Logical reasoning')),
    (_('Exposure triangle'), _('Composition')),
    (_('Framing'), _('Framing')),
    (_('Editing'), _('Editing')),
    (_('Software'), _('Software')),
    (_('Hardware'), _('Hardware')),
    (_('UI/UX'), _('UI/UX')),
    (_('Vectors'), _('Vectors')),
    (_('Colour Palette'), _('Colour Palette')),
    (_('Figma'), _('Figma')),
    (_('Typography'), _('Typography')),
    (_('Teamwork'), _('Teamwork')),
    (_('Radical thinking'), _('Radical thinking')),
    (_('Convincing skills'), _('Convincing skills')),
    (_('Assertiveness'), _('Assertiveness')),
    (_('Communication skills'), _('Communication skills')),
    (_('Decisiveness'), _('Decisiveness')),
    (_('Empathy'), _('Empathy')),
    (_('Honesty/Trust'), _('Honesty/Trust')),
    (_('Vision and Communicating'), _('Vision and Communicating')),
    (_('Autonomous and Responsible'), _('Autonomous and Responsible')),
    (_('How to Be in Command'), _('How to Be in Command')),
)


class QuestionsTags(models.Model):

    class Meta:
        verbose_name = _("Tags")
        verbose_name_plural = _("Tags")
        ordering = ['id']

    question = models.ForeignKey(
        Question, related_name='tag', on_delete=models.CASCADE)
    tags = models.CharField(choices=QUESTION_TAGS,
                            verbose_name=_("Tags"), max_length=100)

    def __str__(self):
        return str(self.question)


class Submission(models.Model):
    class Meta:
        verbose_name = _("Submission")
        verbose_name_plural = _("Submissions")
        ordering = ['id']

    sub_student = models.ForeignKey(
        User, related_name='sub_student', on_delete=models.CASCADE)
    ques_type = models.IntegerField(
        choices=QUESTION_TYPE, default=0, verbose_name=_("Question Type"))
    domain = models.ForeignKey(
        Domain, related_name='sub_domain', on_delete=models.CASCADE)
    question = models.ForeignKey(
        Question, related_name='question', on_delete=models.CASCADE)
    answer = models.CharField(max_length=1000)
    correct_option = models.CharField(max_length=1000)
    submitted_time = models.TimeField()
    is_checked = models.BooleanField(default=False)
    mark_ques = models.IntegerField()

    def __str__(self):
        return str(self.sub_student)


class Results(models.Model):
    class Meta:
        verbose_name = _("Result")
        verbose_name_plural = _("Results")

    student = models.ForeignKey(
        User, related_name='student', on_delete=models.CASCADE)
    domain = models.ForeignKey(
        Domain, related_name='maindomain', on_delete=models.CASCADE)
    MCQ_score = models.IntegerField()
    Long_Ans_Score = models.IntegerField()
    Total = models.IntegerField()
    comments = models.TextField(max_length=1000)
    submitted = models.BooleanField(default=False)
    start_time = models.TimeField()

    def __str__(self):
        return str(self.student)
