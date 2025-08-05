from rest_framework import serializers
from api.models import User , Assingment , Submission , Grade





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ['id' , 'name' , 'email' ,'password' , 'role']

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id' , 'name' , 'email' ,'password' , 'role']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = User
        fields = ['email' ,'password']


class AssingmentSerializer(serializers.ModelSerializer):
    # created_by = serializers.StringRelatedField()  # Shows teacher's username
    # assigned_to = serializers.StringRelatedField()  # Shows student's username

    class Meta:
        model = Assingment
        fields = ['id', 'title', 'illustration', 'assigned_to']

class SubmissionSerializer(serializers.ModelSerializer):
    # assingment =serializers.StringRelatedField()
    class Meta:
        model = Submission
        fields = ['assingment' , 'solution' ]


class GradeSerializer(serializers.ModelSerializer):
    # graded_to = serializers.StringRelatedField()
    # assingment = serializers.StringRelatedField()
    class Meta:
        model = Grade
        fields = ['assingment' , 'graded_to' , 'grades']  