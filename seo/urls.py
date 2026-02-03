from django.urls import path
from .views import (
    SEOSettingsListCreate,
    SEOSettingsRetrieveUpdateDestroy,
    BrokenLinkListCreate,
    BrokenLinkRetrieveUpdateDestroy,
    SEOImageListCreate,
    SEOImageRetrieveUpdateDestroy
)

urlpatterns = [
    # SEO Settings
    path('seo-settings/', SEOSettingsListCreate.as_view(), name='seo-settings-list'),
    path('seo-settings/<slug:slug>/', SEOSettingsRetrieveUpdateDestroy.as_view(), name='seo-settings-detail'),
    
    # Broken Links
    path('broken-links/', BrokenLinkListCreate.as_view(), name='broken-links-list'),
    path('broken-links/<int:pk>/', BrokenLinkRetrieveUpdateDestroy.as_view(), name='broken-links-detail'),
    
    # SEO Images
    path('seo-images/', SEOImageListCreate.as_view(), name='seo-images-list'),
    path('seo-images/<int:pk>/', SEOImageRetrieveUpdateDestroy.as_view(), name='seo-images-detail'),
]