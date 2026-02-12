# models.py
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from django.core.validators import FileExtensionValidator
from django.conf import settings
from django.core.validators import URLValidator

class Project(models.Model):
    CATEGORY_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
    ]
    
    LAYOUT_CHOICES = [
        ('large_wide', 'Large Wide - 8 columns'),
        ('tall', 'Tall - 4 columns'),
        ('square', 'Square - 5 columns'),
        ('wide', 'Wide - 7 columns'),
        ('medium', 'Medium - 6 columns'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    short_description = models.CharField(max_length=300)
    full_description = CKEditor5Field(blank=False)
    
    # Main image (kept separate for easy access)
    main_image = models.ImageField(upload_to='projects/main/')
    
    # Technical details
    capacity = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=200)
    date_completed = models.DateField()
    duration = models.CharField(max_length=100, blank=True)
    
    # Layout control
    layout = models.CharField(max_length=20, choices=LAYOUT_CHOICES, default='medium')
    featured = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    
    # Stats
    energy_savings = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage of energy savings"
    )
    panels_installed = models.IntegerField(default=0, blank=True, null=True)
    homes_powered = models.IntegerField(default=0, blank=True, null=True)
    
    # Meta
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def additional_images(self):
        """Get all additional images for this project"""
        return self.project_images.all().order_by('display_order')
    
    class Meta:
        ordering = ['display_order', '-date_completed']
        verbose_name = "Project"
        verbose_name_plural = "Projects"


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='project_images'
    )
    image = models.ImageField(upload_to='projects/extra/')
    caption = models.CharField(max_length=200, blank=True)
    alt_text = models.CharField(max_length=200, blank=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.project.title} ({self.display_order})"
    
    class Meta:
        ordering = ['display_order']
        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"


class ProjectStat(models.Model):
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class")
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['display_order']
        verbose_name = "Project Statistic"
        verbose_name_plural = "Project Statistics"

class NewsArticle(models.Model):
    CATEGORY_CHOICES = [
        ('innovation', 'Innovation'),
        ('infrastructure', 'Infrastructure'),
        ('academy', 'Academy'),
        ('awards', 'Awards'),
        ('industry', 'Industry'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='industry')
    summary = models.CharField(max_length=300, help_text="Short description for cards and meta")
    content = CKEditor5Field(help_text="Full article content")
    
    # Media
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    image_caption = models.CharField(max_length=200, blank=True)
    
    # Metadata
    is_featured = models.BooleanField(default=False, help_text="Show as the main featured story")
    published_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    read_time = models.IntegerField(default=5, help_text="Estimated reading time in minutes")
    
    # Technical identifiers (matching your existing style)
    transaction_id = models.CharField(max_length=20, blank=True, editable=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-published_date']
        verbose_name = "News Article"
        verbose_name_plural = "News Articles"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.transaction_id:
            # Generate a unique ID like "TRANS_ID: #4012"
            last_id = NewsArticle.objects.aggregate(models.Max('id'))['id__max'] or 0
            self.transaction_id = f"TRANS_ID: #{last_id + 4012}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class DownloadCategory(models.Model):
    LAYOUT_CHOICES = [
        ('grid_3_cols', '3‑Column Grid (Brochures)'),
        ('grid_2_cols_large', '2‑Column Large Cards (Technical Specs)'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    icon = models.CharField(
        max_length=50,
        help_text="FontAwesome icon class (e.g., 'fas fa-file-pdf')",
        blank=True
    )
    layout = models.CharField(max_length=20, choices=LAYOUT_CHOICES, default='grid_3_cols')
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "Download Category"
        verbose_name_plural = "Download Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class DownloadItem(models.Model):
    category = models.ForeignKey(
        DownloadCategory,
        on_delete=models.CASCADE,
        related_name='items'
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    file = models.FileField(
        upload_to='downloads/',
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip']
        )],
        help_text="Allowed: PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX, ZIP"
    )
    file_size = models.CharField(
        max_length=20,
        blank=True,
        help_text="e.g. '4.2 MB' – auto‑filled on save"
    )
    version = models.CharField(max_length=50, blank=True, help_text="e.g. 'Rev 2.1'")
    is_secure = models.BooleanField(
        default=False,
        help_text="Require login to download? (future feature)"
    )
    download_count = models.PositiveIntegerField(default=0, editable=False)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = "Download Item"
        verbose_name_plural = "Download Items"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.file and not self.file_size:
            # Compute file size in human‑readable format
            size = self.file.size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    self.file_size = f"{size:.1f} {unit}"
                    break
                size /= 1024.0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class AcademyCourse(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    icon = models.CharField(
        max_length=50,
        help_text="FontAwesome icon class (e.g., 'fa-bolt', 'fa-sun')",
        default="fa-bolt"
    )
    description = models.TextField()
    syllabus_file = models.FileField(
        upload_to='academy/syllabi/',
        blank=True,
        null=True,
        help_text="PDF syllabus (optional)"
    )
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']
        verbose_name = "Academy Course"
        verbose_name_plural = "Academy Courses"

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
    icon = models.CharField(
        max_length=50,
        default="fa-certificate",
        help_text="FontAwesome icon class"
    )
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order']
        verbose_name = "Course Feature"
        verbose_name_plural = "Course Features"

    def __str__(self):
        return f"{self.course.title}: {self.text}"


class AcademyEnrollment(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    course = models.ForeignKey(
        AcademyCourse,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Course Interest"
    )
    background = models.TextField(verbose_name="Your Expertise / Background")
    created_at = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Academy Enrollment"
        verbose_name_plural = "Academy Enrollments"

    def __str__(self):
        return f"{self.full_name} – {self.course.title if self.course else 'Unknown'}"


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

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Service Enquiry"
        verbose_name_plural = "Service Enquiries"

    def __str__(self):
        return f"{self.name} – {self.get_service_display()} ({self.created_at.date()})"

class ChatMessage(models.Model):
    user_message = models.TextField()
    admin_reply = models.TextField(blank=True, null=True)
    replied_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,           # ✅ use AUTH_USER_MODEL
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='chat_replies'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    replied_at = models.DateTimeField(blank=True, null=True)
    is_archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True, help_text="Optional")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} – {self.created_at.date()}"


class SiteConfiguration(models.Model):
    """
    Singleton – stores global settings (contact, social, map).
    Only ONE record ever exists.
    """

    # ---------- CONTACT INFO ----------
    phone = models.CharField(max_length=30, default="+1 (234) 567 890")
    email = models.EmailField(default="info@green-innova.com")
    address = models.TextField(max_length=500, default="123 Green Street, Eco Heights, EH 456")

    # ---------- SOCIAL LINKS ----------
    linkedin = models.URLField(blank=True, default="https://linkedin.com/company/green-innova")
    instagram = models.URLField(blank=True, default="https://instagram.com/greeninnova")
    facebook = models.URLField(blank=True, default="https://facebook.com/greeninnova")
    youtube = models.URLField(blank=True, default="https://youtube.com/c/greeninnova")

    # ---------- 🗺️ MAP – DIRECT IFRAME URL ----------
    map_embed_url = models.URLField(
        blank=True,
        help_text="Paste the full Google Maps embed URL (src) here. Example: https://www.google.com/maps/embed?pb=..."
    )

    # ---------- SINGLETON ENFORCEMENT ----------
    is_main = models.BooleanField(default=True, editable=False, unique=True)

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def save(self, *args, **kwargs):
        self.is_main = True
        super().save(*args, **kwargs)
        # Delete any other records – keeps it singleton
        SiteConfiguration.objects.exclude(id=self.id).delete()

    def __str__(self):
        return "Global Contact, Social & Map Settings"