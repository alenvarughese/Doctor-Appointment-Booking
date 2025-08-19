from django.contrib import admin
from .models import Doctor, Specialization, DoctorAvailability

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialization', 'license_number', 'experience_years', 'consultation_fee', 'is_available']
    list_filter = ['specialization', 'is_available', 'experience_years']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'license_number']

@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'day', 'start_time', 'end_time', 'is_available']
    list_filter = ['day', 'is_available']
    search_fields = ['doctor__user__username']
