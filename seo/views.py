from rest_framework import generics
from .models import SEOSettings, BrokenLink, SEOImage
from .serializers import (
    SEOSettingsSerializer,
    BrokenLinkSerializer,
    SEOImageSerializer
)

class SEOSettingsListCreate(generics.ListCreateAPIView):
    queryset = SEOSettings.objects.all()
    serializer_class = SEOSettingsSerializer
    filterset_fields = ['slug', 'robots_tag', 'schema_type']
    search_fields = ['slug', 'focus_keyword', 'meta_title']

class SEOSettingsRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = SEOSettings.objects.all()
    serializer_class = SEOSettingsSerializer
    lookup_field = 'slug'

class BrokenLinkListCreate(generics.ListCreateAPIView):
    queryset = BrokenLink.objects.all()
    serializer_class = BrokenLinkSerializer
    filterset_fields = ['status_code', 'resolved']
    search_fields = ['url']

class BrokenLinkRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = BrokenLink.objects.all()
    serializer_class = BrokenLinkSerializer

class SEOImageListCreate(generics.ListCreateAPIView):
    queryset = SEOImage.objects.all()
    serializer_class = SEOImageSerializer
    search_fields = ['alt_text']

class SEOImageRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = SEOImage.objects.all()
    serializer_class = SEOImageSerializer