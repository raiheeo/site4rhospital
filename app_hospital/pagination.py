from rest_framework.pagination import PageNumberPagination

class DoctorProfilePagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 30

class PatientProfilePagination(PageNumberPagination):
    page_size = 10


class SpecialtyPagination(PageNumberPagination):
    page_size = 10


class DepartmentPagination(PageNumberPagination):
    page_size = 15