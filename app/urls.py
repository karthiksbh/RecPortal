from django.contrib import admin
from django.urls import path, include

from .views import AdminLoginView, CommentAdminView, Generate_OTP, IncDis, MarkLongAdmin, QuesAnsAdminView, LongResView, AdminRegisterView, AnswerSubmissionView, MarkLongAdmin, RegisterView, StudentCount, SubResView, TestSubmitted, VerifyOTP, LoginView, LogoutView, QuizQues, UserDetView, Student_check, AdminStudentCheck

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('verifyotp/', VerifyOTP.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('q/', QuizQues.as_view(), name='quizques'),
    path('a/<str:topic>/', SubResView.as_view(), name='subresult'),
    path('user/', UserDetView.as_view(), name='userdet'),
    path('sub/', AnswerSubmissionView.as_view(), name='answersub'),
    path('adminregister/', AdminRegisterView.as_view(), name='admin_register'),
    path('adminlogin/', AdminLoginView.as_view(), name='adminlogin'),
    path('a/<str:topic>/<str:student>/', LongResView.as_view(), name='longres'),
    path('adminmarklong/', MarkLongAdmin.as_view(), name='marklong'),
    path('testsubmit/', TestSubmitted.as_view(), name='testsubmit'),
    path('quesansadmin/<str:topic>/',
         QuesAnsAdminView.as_view(), name='quesansadmin'),
    path('addcommentsadmin/', CommentAdminView.as_view(), name='admincomment'),
    path('incdes/', IncDis.as_view(), name='incdes'),
    path('studentcheck/', Student_check.as_view(), name='checking'),
    path('generateotp/', Generate_OTP.as_view(), name='otpgen'),
    path('allanswerscheck/', AdminStudentCheck.as_view(), name='answerscheck'),
    # path('studentcount/', StudentCount.as_view(), name='studentcount'),
]
