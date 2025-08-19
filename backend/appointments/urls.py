from django.urls import path
from .views import AppointmentListView, AppointmentDetailView, cancel_appointment, available_slots

urlpatterns = [
    path('appointments/', AppointmentListView.as_view(), name='appointment-list'),
    path('appointments/<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('appointments/<int:appointment_id>/cancel/', cancel_appointment, name='cancel-appointment'),
    path('doctors/<int:doctor_id>/available-slots/', available_slots, name='available-slots'),
]
