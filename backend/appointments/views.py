from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Appointment
from .serializers import AppointmentSerializer, AppointmentCreateSerializer, AppointmentUpdateSerializer
from datetime import date, timedelta, datetime
from doctors.models import Doctor

class AppointmentListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'doctor':
            return Appointment.objects.filter(doctor__user=user)
        elif user.user_type == 'admin':
            return Appointment.objects.all()
        else:
            return Appointment.objects.filter(patient=user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AppointmentCreateSerializer
        return AppointmentSerializer
    
    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'doctor':
            return Appointment.objects.filter(doctor__user=user)
        elif user.user_type == 'admin':
            return Appointment.objects.all()
        else:
            return Appointment.objects.filter(patient=user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check if user has permission to cancel this appointment
    user = request.user
    if user.user_type not in ['admin', 'doctor'] and appointment.patient != user:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    if appointment.status in ['cancelled', 'completed']:
        return Response({'error': 'Cannot cancel this appointment'}, status=status.HTTP_400_BAD_REQUEST)
    
    appointment.status = 'cancelled'
    appointment.save()
    
    return Response({'message': 'Appointment cancelled successfully'})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def available_slots(request, doctor_id):
    
    doctor = get_object_or_404(Doctor, id=doctor_id)
    requested_date = request.GET.get('date', date.today().isoformat())
    
    try:
        requested_date = date.fromisoformat(requested_date)
    except ValueError:
        return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Get doctor's availability for the requested day
    day_name = requested_date.strftime('%A').lower()
    try:
        availability = doctor.availabilities.get(day=day_name)
        if not availability.is_available:
            return Response({'available_slots': []})
    except:
        return Response({'available_slots': []})
    
    # Generate time slots
    start_time = availability.start_time
    end_time = availability.end_time
    
    # 30-minute slots
    slot_duration = timedelta(minutes=30)
    current_time = start_time
    
    available_slots = []
    while current_time < end_time:
        slot_time = current_time
        current_time = (datetime.combine(date.min, current_time) + slot_duration).time()
        
        # Check if slot is already booked
        if not Appointment.objects.filter(
            doctor=doctor,
            appointment_date=requested_date,
            appointment_time=slot_time,
            status__in=['pending', 'confirmed']
        ).exists():
            available_slots.append(slot_time.strftime('%H:%M'))
    
    return Response({'available_slots': available_slots})
