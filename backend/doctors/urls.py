from django.urls import path
from .views import (
    DoctorListView, DoctorDetailView, SpecializationListView, doctors_by_specialization,
    AdminDoctorCreateView, AdminDoctorListView, AdminDoctorDetailView
)

urlpatterns = [
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('specializations/', SpecializationListView.as_view(), name='specialization-list'),
    path('doctors/specialization/<int:specialization_id>/', doctors_by_specialization, name='doctors-by-specialization'),
    
    # Admin URLs
    path('admin/doctors/', AdminDoctorCreateView.as_view(), name='admin-doctor-create'),
    path('admin/doctors/list/', AdminDoctorListView.as_view(), name='admin-doctor-list'),
    path('admin/doctors/<int:pk>/', AdminDoctorDetailView.as_view(), name='admin-doctor-detail'),
]
