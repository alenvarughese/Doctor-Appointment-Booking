from rest_framework import serializers
from .models import Appointment
from users.serializers import UserProfileSerializer
from doctors.serializers import DoctorSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    patient = UserProfileSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['patient', 'created_at', 'updated_at']

class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'appointment_time', 'symptoms', 'notes']
    
    def validate(self, attrs):
        # Additional validation can be added here
        return attrs

class AppointmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['status', 'notes']
    
    def validate_status(self, value):
        # Only allow certain status transitions
        current_status = self.instance.status if self.instance else None
        if current_status == 'completed' and value != 'completed':
            raise serializers.ValidationError("Cannot change status of completed appointment")
        return value
