from django.urls import path
from .views.users import RegisterView, VerifyOTP, LoginView, LogoutView, UserDetView, AdminRegisterView, AdminLoginView, TestsSubmitted, Generate_OTP
from .views.quiz import QuizQues, AnswerSubmissionView, TestSubmitted, IncDis
from .views.adminpanel import MarkLongAdmin, SubResView, LongResView, QuesAnsAdminView, CommentAdminView, Student_check, AdminStudentCheck, StudentCount, getTime

# URLs for the User
urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('verifyotp/', VerifyOTP.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('user/', UserDetView.as_view(), name='userdet'),
    path('adminregister/', AdminRegisterView.as_view(), name='admin_register'),
    path('adminlogin/', AdminLoginView.as_view(), name='adminlogin'),
    path('testdone/', TestsSubmitted.as_view(), name='testsdone'),
    path('generateotp/', Generate_OTP.as_view(), name='otpgen')
]

# URLs for the Quiz Panel
urlpatterns += [
    path('q/', QuizQues.as_view(), name='quizques'),
    path('sub/', AnswerSubmissionView.as_view(), name='answersub'),
    path('testsubmit/', TestSubmitted.as_view(), name='testsubmit'),
    path('incdes/', IncDis.as_view(), name='incdes')
]

# URLs for the Admin Panel
urlpatterns += [
    path('adminmarklong/', MarkLongAdmin.as_view(), name='marklong'),
    path('a/<str:topic>/', SubResView.as_view(), name='subresult'),
    path('a/<str:topic>/<str:student>/', LongResView.as_view(), name='longres'),
    path('quesansadmin/<str:topic>/',
         QuesAnsAdminView.as_view(), name='quesansadmin'),
    path('addcommentsadmin/', CommentAdminView.as_view(), name='admincomment'),
    path('studentcheck/', Student_check.as_view(), name='checking'),
    path('allanswerscheck/', AdminStudentCheck.as_view(), name='answerscheck'),
    path('studentcount/', StudentCount.as_view(), name='studentcount'),
    path('time/', getTime.as_view(), name='time'),
]
