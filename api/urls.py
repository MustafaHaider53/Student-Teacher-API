from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from api.views import UserRegister , UserLogin , AssingmentView , SubmissionView ,  ProfileView  ,GradeView , ListGradesView , ListAssingmentView , ListSubmissionView ,TeacherReportViewSet, StudentReportViewSet

 
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
    # path('teacher-report/', TeacherReportViewSet.as_view(), name='teacher-report'),  
    # path('student-report/', StudentReportViewSet.as_view(), name='student-report'),  
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
