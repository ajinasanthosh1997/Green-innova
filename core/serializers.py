from rest_framework import serializers
from .models import AcademyEnrollment, AcademyCourse,ServiceEnquiry,ContactMessage

class AcademyEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademyEnrollment
        fields = ['id', 'full_name', 'email', 'phone', 'course', 'background', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_course(self, value):
        if not value.is_active:
            raise serializers.ValidationError("Selected course is not available.")
        return value

class ServiceEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceEnquiry
        fields = ['id', 'name', 'email', 'phone', 'message', 'service', 'created_at']
        read_only_fields = ['id', 'created_at']

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'phone', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']