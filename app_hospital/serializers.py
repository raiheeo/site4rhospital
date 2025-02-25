from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class DoctorRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'phone_number', 'department', 'specialty', 'working_days',
                  'experience', 'gender', 'shift_start', 'shift_end', 'appointment_price')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = DoctorProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Data")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileListLSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name']


class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'profile_picture', 'phone_number']


class DoctorProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ['first_name', 'last_name']


class DoctorProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ['first_name', 'last_name', 'working_days', 'price', 'experience', 'doctor_bio']

class DepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_name']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class DepartmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_name',]

class SpecialtyListSerializer(serializers.ModelSerializer):
    department = DepartmentDetailSerializer()

    class Meta:
        model = Specialty
        fields = ['id', 'specialty_name', 'department']

class SpecialtyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['specialty_name']

class PatientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ['user', ]

class PatientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ['user', 'emergency_contact', 'blood_type']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = '__all__'

class  MedicalAdviceSerializer(serializers.ModelSerializer):
    class Meta:
        model =  MedicalAdvice
        fields = '__all__'

class  MedicalAdviceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model =  MedicalAdvice
        fields = ['patient', 'doctor', 'diagnosis', 'treatment', 'medication', 'created_at']


class  MedicalAdviceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalAdvice
        fields = ['id', 'diagnosis', 'treatment', 'medication']

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

class FeedbackListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['doctor', 'rating']

class FeedbackDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['patient', 'doctor', 'rating', 'comment', 'created_at']


class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientListSerializer()
    doctor = DoctorProfileListSerializer()
    date_time = serializers.DateTimeField(format('%Y-%B-%d  %H:%M'))

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'status', 'date_time']

