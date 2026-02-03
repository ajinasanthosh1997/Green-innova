from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.core.validators import RegexValidator
from django.utils.safestring import mark_safe

class SEOSettings(models.Model):
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE,
        null=True,  # Add this
        blank=True  # Add this
    )
    object_id = models.PositiveIntegerField(
        null=True,  # Add this
        blank=True  # Add this
    )
    content_object = GenericForeignKey('content_type', 'object_id')
    slug = models.SlugField(
        max_length=200,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[a-z0-9\-]+$',
            message='Slug must be lowercase with hyphens only',
            code='invalid_slug'
        )],
        help_text="URL-friendly version of the title"
    )

    focus_keyword = models.CharField(max_length=100, blank=True)
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    canonical_url = models.URLField(blank=True)

    ROBOTS_CHOICES = [
        ('index, follow', 'Index, Follow'),
        ('noindex, follow', 'Noindex, Follow'),
        ('index, nofollow', 'Index, Nofollow'),
        ('noindex, nofollow', 'Noindex, Nofollow'),
    ]
    robots_tag = models.CharField(
        max_length=50,
        choices=ROBOTS_CHOICES,
        default='index, follow'
    )

    og_title = models.CharField(max_length=100, blank=True)
    og_description = models.TextField(blank=True)
    og_image = models.URLField(blank=True)

    SCHEMA_TYPES = [
        ('Article', 'Article'),
        ('WebPage', 'Web Page'),
        ('Product', 'Product'),
        ('Event', 'Event'),
        ('LocalBusiness', 'Local Business'),
    ]
    schema_type = models.CharField(
        max_length=50,
        choices=SCHEMA_TYPES,
        blank=True
    )

    def __str__(self):
        return self.slug


class BrokenLink(models.Model):
    """
    Stores detected broken links
    """
    url = models.URLField(max_length=500)
    status_code = models.IntegerField()
    detected_on = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return self.url
    
 

class SEOImage(models.Model):
    """
    Optimized images for SEO with alt text
    """
    image = ProcessedImageField(
        upload_to='seo_images/%Y/%m',
        processors=[ResizeToFill(1200, 630)],
        format='JPEG',
        options={'quality': 80},
        help_text="Optimized for web (1200x630, 80% quality)"
    )
    alt_text = models.CharField(
        max_length=125,
        help_text="Description for accessibility and SEO"
    )
    
    def __str__(self):
        return self.alt_text

    @property
    def thumbnail(self):
  
        return mark_safe(f'<img src="{self.image.url}" width="100" />')
   