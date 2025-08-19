from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Doctor, Specialization
from .serializers import DoctorSerializer, DoctorListSerializer, SpecializationSerializer
from users.models import CustomUser

class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.filter(is_available=True)
    serializer_class = DoctorListSerializer
    permission_classes = [permissions.AllowAny]

class DoctorDetailView(generics.RetrieveAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.AllowAny]

class SpecializationListView(generics.ListAPIView):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = [permissions.AllowAny]

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def doctors_by_specialization(request, specialization_id):
    try:
        doctors = Doctor.objects.filter(specialization_id=specialization_id, is_available=True)
        serializer = DoctorListSerializer(doctors, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

# Admin views for doctor management
class AdminDoctorCreateView(generics.CreateAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        # Check if user is admin
        if request.user.user_type != 'admin':
            return Response({'error': 'Only admins can create doctors'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            # Get the user by ID
            user_id = request.data.get('user_id')
            user = CustomUser.objects.get(id=user_id)
            
            # Create doctor profile
            doctor_data = {
                'user': user,
                'specialization_id': request.data.get('specialization_id'),
                'license_number': request.data.get('license_number'),
                'experience_years': request.data.get('experience_years'),
                'consultation_fee': request.data.get('consultation_fee'),
                'bio': request.data.get('bio', '')
            }
            
            doctor = Doctor.objects.create(**doctor_data)
            serializer = self.get_serializer(doctor)
            
            return Response({
                'message': 'Doctor profile created successfully',
                'doctor': serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AdminDoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type != 'admin':
            return Doctor.objects.none()
        return Doctor.objects.all()

class AdminDoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type != 'admin':
            return Doctor.objects.none()
        return Doctor.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        if request.user.user_type != 'admin':
            return Response({'error': 'Only admins can delete doctors'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            doctor = self.get_object()
            # Set doctor as unavailable instead of deleting
            doctor.is_available = False
            doctor.save()
            return Response({'message': 'Doctor removed successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
