from api.models import User , Assingment , Submission , Grade 
from api.serializers import RegistrationSerializer , LoginSerializer , AssingmentSerializer , SubmissionSerializer ,GradeSerializer , UserSerializer
from rest_framework.generics import CreateAPIView , ListAPIView , RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from api.permissions import IsTeacher , IsStudent
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle


# Create your views here.

class UserRegister(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = self.get_queryset().get(id=response.data['id'])  # get the created user
        refresh = RefreshToken.for_user(user)
        response.data['access'] = str(refresh.access_token)
        response.data['refresh'] = str(refresh)
        return response
    

class UserLogin(APIView):
    def post(self , request , format=None):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(username = email , password = password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                            } , status=status.HTTP_201_CREATED)
            else:
                return Response({'msg':'Email or Password is incorrect'} , status=status.HTTP_404_NOT_FOUND)
            
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        

class AssingmentView(ModelViewSet):
    queryset = Assingment
    serializer_class = AssingmentSerializer
    permission_classes = [IsTeacher]

    throttle_classes = [UserRateThrottle]
    
    def perform_create(self, serializer):
        serializer.save(created_by = self.request.user)


class ListAssingmentView(ListAPIView):
    serializer_class = AssingmentSerializer
    permission_classes = [IsStudent]

    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        return Assingment.objects.filter(assigned_to = self.request.user)


class SubmissionView(ModelViewSet):
    queryset = Submission
    serializer_class = SubmissionSerializer
    permission_classes = [IsStudent]
    
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        serializer.save(submit_by = self.request.user)

class ListSubmissionView(ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsTeacher]

    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        return Submission.objects.filter(assingment__created_by = self.request.user)


class GradeView(ModelViewSet):
    queryset = Grade
    serializer_class  = GradeSerializer
    permission_classes = [IsTeacher]

    throttle_classes = [UserRateThrottle]
    
    def perform_create(self, serializer):
        serializer.save(graded_by = self.request.user)

class ListGradesView(ListAPIView):
    serializer_class = GradeSerializer
    permission_classes = [IsStudent]

    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        return Grade.objects.filter(graded_to = self.request.user)
    
    
class ProfileView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    throttle_classes = [UserRateThrottle]
    
    def get_object(self):
        return self.request.user


    
    


