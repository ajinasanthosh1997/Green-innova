from rest_framework import serializers
from .models import *
from django.utils import translation

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'code', 'is_default']

class ContactMessageSerializer(serializers.ModelSerializer):
    type_of_request_display = serializers.CharField(
        source='get_type_of_request_display', 
        read_only=True
    )
    
    class Meta:
        model = ContactMessage
        fields = '__all__'
        read_only_fields = ('submitted_at',)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class GalleryItemSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    country = CountrySerializer(read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(),
        source='country',
        write_only=True,
        required=False
    )
    
    class Meta:
        model = GalleryItem
        fields = '__all__'
        read_only_fields = ('created_at',)
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

class AuthorSerializer(serializers.ModelSerializer):
    profile_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = '__all__'
    
    def get_profile_image_url(self, obj):
        request = self.context.get('request')
        if obj.profile_image:
            return request.build_absolute_uri(obj.profile_image.url)
        return None

class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = '__all__'




class BlogPostSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    author = AuthorSerializer(read_only=True)
    category = BlogCategorySerializer(read_only=True)

    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source='author',
        write_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=BlogCategory.objects.all(),
        source='category',
        write_only=True
    )

    country = CountrySerializer(read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(),
        source='country',
        write_only=True,
        required=False
    )

    class Meta:
        model = BlogPost
        fields = '__all__'
        read_only_fields = ('created_at', 'slug', 'image_url')

    def get_title(self, obj):
        lang = translation.get_language() or 'en'
        return getattr(obj, f"title_{lang}", obj.title)

    def get_description(self, obj):
        lang = translation.get_language() or 'en'
        return getattr(obj, f"description_{lang}", obj.description)

    def get_content(self, obj):
        lang = translation.get_language() or 'en'
        return getattr(obj, f"content_{lang}", obj.content)

    def get_image_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url) if obj.image else None
