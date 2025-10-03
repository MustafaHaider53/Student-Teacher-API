from django.contrib import admin
from django.urls import path , include
from api.views import UserRegister , UserLogin , AssingmentView , SubmissionView ,  ProfileView  ,GradeView , ListGradesView , ListAssingmentView , ListSubmissionView ,TeacherReportViewSet, StudentReportViewSet , chat , room

 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('assingmentapi' , AssingmentView , basename='assingmentapi' )
router.register('submissionapi' , SubmissionView , basename='submissionapi' )
router.register('gradeapi' , GradeView , basename='grade' )
router.register('teacher-report', TeacherReportViewSet, basename='teacher-report')
router.register('student-report', StudentReportViewSet, basename='student-report')

urlpatterns = [
    path('register/',UserRegister.as_view() , name='register'),
    path('login/',UserLogin.as_view() , name='login'),
    path('view-grade/',ListGradesView.as_view() , name='view-grade'),
    path('profile/',ProfileView.as_view() , name='profile'),
    path('list-assingment/' , ListAssingmentView.as_view() , name = 'list-assingment' ),
    path('list-submission/' , ListSubmissionView.as_view() , name = 'list-submission' ),
    path('', include(router.urls)),
]
