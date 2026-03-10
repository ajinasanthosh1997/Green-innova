from rest_framework import serializers
from .models import ContactMessage,CalculatorLead,QuoteSelection



class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'phone', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']


class CalculatorLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalculatorLead
        fields = ['id', 'name', 'phone', 'email', 'location', 'type', 'subsidy', 'commercial_option', 'value']
        extra_kwargs = {
            'email': {'required': False, 'allow_blank': True},
            'name': {'required': False, 'allow_blank': True},
            'subsidy': {'required': False, 'allow_blank': True},
        }

class QuoteSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteSelection
        fields = ['id', 'lead', 'plan_name', 'system_size', 'price']   # ← added 'id'