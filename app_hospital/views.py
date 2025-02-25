from django.shortcuts import render
from rest_framework import viewsets, generics, permissions, status
from .serializers import *
from .models import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import UserProfilePagination
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListLSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)



class UserProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

from .filters import DoctorFilter
from .serializers import *
from rest_framework import viewsets, generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import CheckDoctor, CheckPatient
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

class DoctorRegisterView(generics.CreateAPIView):
    serializer_class = DoctorRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DoctorCustomLoginView(TokenObtainPairView):
    serializer_class = DoctorLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class PatientRegisterView(generics.CreateAPIView):
    serializer_class = PatientRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PatientCustomLoginView(TokenObtainPairView):
    serializer_class = PatientLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)



class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class DepartmentListAPIView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class DepartmentDetailAPIView(generics.RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentDetailSerializer
    permission_classes = [IsAuthenticated]

class DepartmentCreateAPIView(generics.CreateAPIView):
    serializer_class = DepartmentDetailSerializer
    permission_classes = [IsAdminUser]

class SpecialtyListAPIView(generics.ListAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtyListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class SpecialtyCreateAPIView(generics.CreateAPIView):
    serializer_class = SpecialtyDetailSerializer
    permission_classes = [IsAdminUser]

class DoctorListAPIView(generics.ListAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = DoctorFilter
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['experience']
    permission_classes = [IsAuthenticatedOrReadOnly]

class DoctorDetailAPIView(generics.RetrieveAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileDetailSerializer
    permission_classes = [IsAuthenticated]

class DoctorCreateApiView(generics.CreateAPIView):
    serializer_class = DoctorProfileDetailSerializer
    permission_classes = [IsAdminUser]

class PatientListAPIView(generics.ListAPIView):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [CheckDoctor]

class PatientCreateAPIView(generics.CreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [CheckDoctor]

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [CheckDoctor]

class MedicalAdviceViewSet(viewsets.ModelViewSet):
    queryset = MedicalAdvice.objects.all()
    serializer_class = MedicalAdviceSerializer
    permission_classes = [CheckDoctor, CheckPatient]

class FeedbackListAPIView(generics.ListAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackListSerializer
    permission_classes = [CheckPatient]

class FeedbackCreateAPIView(generics.CreateAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [CheckPatient]




