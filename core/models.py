from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from django.core.validators import FileExtensionValidator
from django.conf import settings

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
    main_image = models.ImageField(upload_to='projects/main/')
    capacity = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=200)
    date_completed = models.DateField()
    duration = models.CharField(max_length=100, blank=True)
    layout = models.CharField(max_length=20, choices=LAYOUT_CHOICES, default='medium')
    featured = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    energy_savings = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage of energy savings"
    )
    panels_installed = models.IntegerField(default=0, blank=True, null=True)
    homes_powered = models.IntegerField(default=0, blank=True, null=True)
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
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    image_caption = models.CharField(max_length=200, blank=True)
    is_featured = models.BooleanField(default=False, help_text="Show as the main featured story")
    published_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    read_time = models.IntegerField(default=5, help_text="Estimated reading time in minutes")
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
            size = self.file.size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    self.file_size = f"{size:.1f} {unit}"
                    break
                size /= 1024.0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ChatMessage(models.Model):
    user_message = models.TextField()
    admin_reply = models.TextField(blank=True, null=True)
    replied_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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
    phone = models.CharField(max_length=30, default="+1 (234) 567 890")
    email = models.EmailField(default="info@green-innova.com")
    address = models.TextField(max_length=500, default="123 Green Street, Eco Heights, EH 456")
    linkedin = models.URLField(blank=True, default="https://linkedin.com/company/green-innova")
    instagram = models.URLField(blank=True, default="https://instagram.com/greeninnova")
    facebook = models.URLField(blank=True, default="https://facebook.com/greeninnova")
    youtube = models.URLField(blank=True, default="https://youtube.com/c/greeninnova")
    map_embed_url = models.URLField(
        blank=True,
        help_text="Paste the full Google Maps embed URL (src) here. Example: https://www.google.com/maps/embed?pb=..."
    )
    is_main = models.BooleanField(default=True, editable=False, unique=True)

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def save(self, *args, **kwargs):
        self.is_main = True
        super().save(*args, **kwargs)
        SiteConfiguration.objects.exclude(id=self.id).delete()

    def __str__(self):
        return "Global Contact, Social & Map Settings"


class Client(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(blank=True, help_text="Optional link to client's website")
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.name


class Partner(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(
        upload_to='partners/',
        blank=True,
        null=True,
        help_text="Optional logo image (will be displayed instead of name if provided)"
    )
    url = models.URLField(blank=True, help_text="Optional link to partner's website")
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "Partner"
        verbose_name_plural = "Partners"

    def __str__(self):
        return self.name


class JourneyMilestone(models.Model):
    ACCENT_COLORS = [
        ('primary', 'Primary (Green)'),
        ('blue', 'Blue'),
        ('amber', 'Amber'),
    ]

    year = models.IntegerField(help_text="Year of the milestone (e.g., 2015)")
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=400)
    image = models.ImageField(
        upload_to='about/journey/',
        blank=True,
        null=True,
        help_text="Optional image for this milestone. If not provided, a default Unsplash image will be used."
    )
    accent_color = models.CharField(max_length=20, choices=ACCENT_COLORS, default='primary')
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['year', 'display_order']
        verbose_name = "Journey Milestone"
        verbose_name_plural = "Journey Milestones"

    def __str__(self):
        return f"{self.year} – {self.title}"


class Certificate(models.Model):
    title = models.CharField(max_length=200, help_text="e.g., ISO 9001:2015")
    description = models.TextField(max_length=400, help_text="Short description of the certificate")
    icon = models.CharField(
        max_length=50,
        default="fa-certificate",
        help_text="FontAwesome icon class (e.g., 'fa-certificate', 'fa-leaf')"
    )
    status_label = models.CharField(max_length=100, blank=True, help_text="Left label, e.g., 'Status'")
    status_value = models.CharField(max_length=100, blank=True, help_text="Value, e.g., 'Verified'")
    badge_icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Optional icon to show after status, e.g., 'fa-check-circle'"
    )
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']
        verbose_name = "Certificate"
        verbose_name_plural = "Certificates"

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    CATEGORY_CHOICES = [
        ('founder', 'Founder'),
        ('team', 'Team'),
    ]
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='team')
    quote = models.TextField(help_text="Inspirational quote from the member")
    bio = models.TextField(blank=True, help_text="Detailed bio (for founders)")
    image = models.ImageField(upload_to='team/', blank=True, null=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['category', 'display_order', 'name']

    def __str__(self):
        return self.name


class SolarLead(models.Model):
    phone = models.CharField(max_length=20)
    monthly_units = models.IntegerField()
    system_size = models.FloatField()
    cost = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class CalculatorLead(models.Model):
    TYPE_CHOICES = [
        ('Residential', 'Residential'),
        ('Commercial', 'Commercial'),
    ]
    SUBSIDY_CHOICES = [
        ('Subsidized', 'Subsidized'),
        ('Non-Subsidized', 'Non-Subsidized'),
    ]
    OPTION_CHOICES = [
        ('Bill', 'Bill'),
        ('Unit', 'Unit'),
    ]

    name = models.CharField(max_length=100, blank=True, null=True)   # optional
    email = models.EmailField(blank=True, null=True)          # optional
    phone = models.CharField(max_length=30)
    location = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    subsidy = models.CharField(max_length=20, choices=SUBSIDY_CHOICES, blank=True, null=True) 
    commercial_option = models.CharField(max_length=10, choices=OPTION_CHOICES)
    value = models.FloatField(help_text="Monthly bill or units")
    created_at = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name or 'Anonymous'} - {self.location} - {self.created_at.date()}"
    
class QuoteSelection(models.Model):
    lead = models.ForeignKey(CalculatorLead, on_delete=models.CASCADE, related_name='quotes')
    plan_name = models.CharField(max_length=50)  # e.g., 'Capex', '6-month', 'Bank', 'PPA'
    system_size = models.FloatField(help_text="System size in kW")
    price = models.FloatField(help_text="Calculated price in BHD")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.plan_name} for lead {self.lead.id}"