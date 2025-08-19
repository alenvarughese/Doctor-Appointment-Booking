from rest_framework import serializers
from .models import Doctor, Specialization, DoctorAvailability
from users.serializers import UserProfileSerializer

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'

class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    specialization = SpecializationSerializer(read_only=True)
    availabilities = DoctorAvailabilitySerializer(many=True, read_only=True)
    
    class Meta:
        model = Doctor
        fields = '__all__'

class DoctorListSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    specialization = SpecializationSerializer(read_only=True)
    
    class Meta:
        model = Doctor
        fields = ['id', 'user', 'specialization', 'experience_years', 'consultation_fee', 'is_available']
