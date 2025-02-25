from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'users', UserProfileViewSet, basename='user_profile'),
router.register(r'appointments', AppointmentViewSet, basename='appointment'),
router.register(r'medical_records', MedicalAdviceViewSet, basename='medical_record'),

urlpatterns = [
    path('', include(router.urls)),
    path('doctors/', DoctorListAPIView.as_view(), name='doctor-list'),
    path('doctors/<int:pk>/', DoctorDetailAPIView.as_view(), name='doctor-detail'),
    path('doctor-create/', DoctorCreateApiView.as_view(), name='doctor-create'),
    path('patients/', PatientListAPIView.as_view(), name='patient-list'),
    path('patient-create/', PatientCreateAPIView.as_view(), name='patient-create'),
    path('departments/', DepartmentListAPIView.as_view(), name='department-list'),
    path('department-create/', DepartmentCreateAPIView.as_view(), name='department-create'),
    path('departments/<int:pk>/', DepartmentDetailAPIView.as_view(), name='department-detail'),
    path('specialties/', SpecialtyListAPIView.as_view(), name='specialty-list'),
    path('specialty-create/', SpecialtyCreateAPIView.as_view(), name='specialty-create'),
    path('feedbacks/', FeedbackListAPIView.as_view(), name='feedback-list'),
    path('feedback-create/', FeedbackCreateAPIView.as_view(), name='feedback-create'),
    #
    path('doctor-register/', DoctorRegisterView.as_view(), name='register'),
    path('doctor-login/', DoctorCustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('patient-register/', PatientRegisterView.as_view(), name='register'),
    path('patient-login/', PatientCustomLoginView.as_view(), name='login'),
]