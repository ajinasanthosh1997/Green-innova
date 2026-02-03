from rest_framework import serializers
from .models import SEOSettings, BrokenLink, SEOImage

class SEOImageSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()
    
    class Meta:
        model = SEOImage
        fields = '__all__'
        read_only_fields = ('id',)
    
    def get_thumbnail(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

class SEOSettingsSerializer(serializers.ModelSerializer):
    content_object = serializers.SerializerMethodField()
    
    class Meta:
        model = SEOSettings
        fields = '__all__'
        read_only_fields = ('id',)
    
    def get_content_object(self, obj):
        if obj.content_object:
            return str(obj.content_object)
        return None

class BrokenLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrokenLink
        fields = '__all__'
        read_only_fields = ('id', 'detected_on')