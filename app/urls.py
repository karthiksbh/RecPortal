from django.contrib import admin
from django.urls import path, include

from .views import AdminLoginView, AdminRegisterView, AnswerSubmissionView, RegisterView, SubResView, VerifyOTP, LoginView, LogoutView, QuizQues, UserDetView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('verifyotp/', VerifyOTP.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('q/', QuizQues.as_view(), name='quizques'),
    path('a/<str:topic>/', SubResView.as_view(), name='subresult'),
    path('user/', UserDetView.as_view(), name='userdet'),
    path('sub/', AnswerSubmissionView.as_view(), name='answersub'),
    # path('quesadd/', AddQuestionView.as_view(), name='questionadd'),
    path('adminregister/', AdminRegisterView.as_view(), name='admin_register'),
    path('adminlogin/', AdminLoginView.as_view(), name='adminlogin'),
]
