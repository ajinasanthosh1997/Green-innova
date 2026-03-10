from django.db import models
from django.utils.text import slugify
from django.db import models
from django.utils import timezone

class RenewableSubService(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    badge = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default="fa-solar-panel")
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    class Meta: ordering = ['display_order']

class EnergyEfficiencySubService(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    badge = models.CharField(max_length=100, help_text="e.g. 'ISO 50001 Aligned'")
    icon = models.CharField(
        max_length=50,
        default="fa-search-dollar",
        help_text="FontAwesome icon class (e.g., 'fa-search-dollar', 'fa-microchip')"
    )
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']
        verbose_name = "Energy Efficiency Sub-Service"
        verbose_name_plural = "Energy Efficiency Sub-Services"

    def __str__(self):
        return self.title

class AcademyCourse(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, default="fa-bolt")
    description = models.TextField()
    syllabus_file = models.FileField(upload_to='academy/syllabi/', blank=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class AcademyCourseFeature(models.Model):
    course = models.ForeignKey(
        AcademyCourse,
        on_delete=models.CASCADE,
        related_name='features'
    )
    text = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, default="fa-certificate")
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.text


class AcademyEnrollment(models.Model):
    # Link to the Course model you already have
    course = models.ForeignKey(
         AcademyCourse,                     # or the exact app_name.Course
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='enrollments'
    )
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    background = models.TextField(help_text="User's expertise / background")
    created_at = models.DateTimeField(default=timezone.now)
    # Optional: add a status field to track inquiry progress
    status = models.CharField(
        max_length=20,
        choices=[
            ('new', 'New'),
            ('contacted', 'Contacted'),
            ('enrolled', 'Enrolled'),
            ('lost', 'Lost'),
        ],
        default='new'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.course.title if self.course else 'No course'}"

class ServiceEnquiry(models.Model):
    SERVICE_CHOICES = [
        ('renewable', 'Renewable Energy'),
        ('efficiency', 'Energy Efficiency'),
        ('construction', 'Building & Construction'),
        ('industrial', 'Industrial Services'),
        ('academy', 'Academy'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    message = models.TextField()
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES, default='renewable')
    created_at = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    class Meta: ordering = ['-created_at']



class BuildingConstructionSubService(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    badge = models.CharField(max_length=100, help_text="e.g. 'High Thermal R-Value'")
    icon = models.CharField(
        max_length=50,
        default="fa-layer-group",
        help_text="FontAwesome icon class (e.g., 'fa-layer-group', 'fa-box-open')"
    )
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']
        verbose_name = "Building & Construction Sub-Service"
        verbose_name_plural = "Building & Construction Sub-Services"

    def __str__(self):
        return self.title

class IndustrialServiceSubService(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    badge = models.CharField(max_length=100, help_text="e.g. 'Thermal Max'")
    icon = models.CharField(
        max_length=50,
        default="fa-industry",
        help_text="FontAwesome icon class (e.g., 'fa-wind', 'fa-retweet')"
    )
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']
        verbose_name = "Industrial Service Sub‑Service"
        verbose_name_plural = "Industrial Service Sub‑Services"

    def __str__(self):
        return self.title


class EIFSTechnicalFeature(models.Model):
    icon = models.CharField(max_length=50, default="fa-shield-alt", help_text="FontAwesome icon class")
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']
        verbose_name = "EIFS Technical Feature"

    def __str__(self):
        return self.title


class EIFSProject(models.Model):
    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=300)
    image = models.ImageField(upload_to='eifs/projects/', blank=True, null=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']
        verbose_name = "EIFS Major Project"

    def __str__(self):
        return self.title


class EIFSReference(models.Model):
    project_name = models.CharField(max_length=200)
    area_sqm = models.CharField(max_length=50, help_text="e.g. '5,000 sqm'")
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']
        verbose_name = "EIFS Reference"

    def __str__(self):
        return self.project_name