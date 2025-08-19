from django.db import models
from users.models import CustomUser
from doctors.models import Doctor
from django.core.exceptions import ValidationError
from django.utils import timezone

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('no_show', 'No Show'),
    ]
    
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    symptoms = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.patient.get_full_name()} - Dr. {self.doctor.user.get_full_name()} - {self.appointment_date} {self.appointment_time}"
    
    def clean(self):
        # Check if appointment is in the past
        if self.appointment_date < timezone.now().date():
            raise ValidationError("Appointment date cannot be in the past")
        
        # Check if appointment time is available
        if self.appointment_time:
            # Check if doctor is available at this time
            day_name = self.appointment_date.strftime('%A').lower()
            try:
                availability = self.doctor.availabilities.get(day=day_name)
                if not availability.is_available:
                    raise ValidationError("Doctor is not available on this day")
                if self.appointment_time < availability.start_time or self.appointment_time > availability.end_time:
                    raise ValidationError("Appointment time is outside doctor's available hours")
            except:
                raise ValidationError("Doctor is not available on this day")
            
            # Check for conflicting appointments
            conflicting_appointments = Appointment.objects.filter(
                doctor=self.doctor,
                appointment_date=self.appointment_date,
                appointment_time=self.appointment_time,
                status__in=['pending', 'confirmed']
            ).exclude(id=self.id)
            
            if conflicting_appointments.exists():
                raise ValidationError("This time slot is already booked")
    
    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        unique_together = ['doctor', 'appointment_date', 'appointment_time']
        ordering = ['appointment_date', 'appointment_time']
