from rest_framework import serializers
from .models import AcademyEnrollment, ServiceEnquiry,AcademyCourse

class AcademyEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademyEnrollment
        fields = ['id', 'course', 'full_name', 'email', 'phone', 'background', 'created_at']
        read_only_fields = ['id', 'created_at']

class ServiceEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceEnquiry
        fields = ['id', 'name', 'email', 'phone', 'message', 'service', 'created_at']
        read_only_fields = ['id', 'created_at']