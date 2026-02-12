from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.core.cache import cache
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import (
    Project, ProjectImage, ProjectStat, NewsArticle,
    DownloadCategory, DownloadItem,
    AcademyCourse, AcademyCourseFeature, AcademyEnrollment,
    ChatMessage, ServiceEnquiry, ContactMessage, SiteConfiguration
)


# ---------- PROJECTS ----------
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 0
    fields = ('image', 'caption', 'alt_text', 'display_order', 'is_active')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'date_completed', 'featured', 'is_active', 'display_order')
    list_filter = ('category', 'featured', 'is_active', 'date_completed')
    search_fields = ('title', 'location', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
    
    # ✅ NO fieldsets – simple field list
    fields = (
        'title', 'slug', 'category', 'short_description', 'full_description',
        'main_image',
        'capacity', 'location', 'date_completed', 'duration',
        'layout', 'display_order', 'featured',
        'energy_savings', 'panels_installed', 'homes_powered',
        'is_active',
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('display_order', '-date_completed')


@admin.register(ProjectStat)
class ProjectStatAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'description', 'display_order', 'is_active')
    list_editable = ('value', 'display_order', 'is_active')
    fields = ('title', 'value', 'description', 'icon', 'display_order', 'is_active')


# ---------- NEWS ----------
@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_date', 'is_featured', 'is_active')
    list_filter = ('category', 'is_featured', 'is_active')
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}
    
    fields = (
        'title', 'slug', 'category', 'summary', 'content',
        'image', 'image_caption',
        'is_featured', 'published_date', 'is_active', 'read_time',
    )


# ---------- DOWNLOADS ----------
@admin.register(DownloadCategory)
class DownloadCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'layout', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    fields = ('name', 'slug', 'icon', 'layout', 'display_order', 'is_active')


@admin.register(DownloadItem)
class DownloadItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'version', 'file_size', 'download_count', 'is_active')
    list_filter = ('category', 'is_active')
    list_editable = ('is_active',)
    list_select_related = ('category',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')
    readonly_fields = ('download_count', 'file_size')
    
    fields = (
        'category', 'title', 'slug', 'description', 'version',
        'file', 'file_size',
        'display_order', 'is_secure', 'is_active', 'download_count',
    )


# ---------- ACADEMY ----------
class AcademyCourseFeatureInline(admin.TabularInline):
    model = AcademyCourseFeature
    extra = 0
    fields = ('text', 'icon', 'display_order')


@admin.register(AcademyCourse)
class AcademyCourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [AcademyCourseFeatureInline]
    search_fields = ('title', 'description')
    list_filter = ('is_active',)
    
    fields = (
        'title', 'slug', 'icon', 'description', 'syllabus_file',
        'display_order', 'is_active',
    )


@admin.register(AcademyEnrollment)
class AcademyEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'course', 'created_at', 'is_contacted')
    list_filter = ('course', 'is_contacted', 'created_at')
    list_editable = ('is_contacted',)
    list_select_related = ('course',)
    search_fields = ('full_name', 'email', 'phone')
    readonly_fields = ('created_at',)
    
    fields = (
        'full_name', 'email', 'phone', 'course', 'background',
        'is_contacted', 'notes', 'created_at',
    )


# ---------- SERVICE ENQUIRY ----------
@admin.register(ServiceEnquiry)
class ServiceEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'service', 'created_at', 'is_contacted')
    list_filter = ('service', 'is_contacted', 'created_at')
    search_fields = ('name', 'email', 'message')
    actions = ['mark_as_contacted']
    
    fields = (
        'name', 'email', 'phone', 'message', 'service',
        'created_at', 'is_contacted', 'notes',
    )
    readonly_fields = ('created_at',)
    
    def mark_as_contacted(self, request, queryset):
        queryset.update(is_contacted=True)
    mark_as_contacted.short_description = "Mark selected as contacted"


# ---------- CHAT ----------


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    # ... your existing fields, list_display, etc.

    def save_model(self, request, obj, form, change):
        # Set replied_by and replied_at if a reply is added
        if obj.admin_reply and not obj.replied_by:
            obj.replied_by = request.user
            obj.replied_at = timezone.now()

        super().save_model(request, obj, form, change)

        # --- Send WebSocket notification ---
        if obj.admin_reply:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'chat_{obj.id}',           # room name = chat_<message_id>
                {
                    'type': 'chat_reply',   # must match consumer method name
                    'reply': obj.admin_reply,
                    'message_id': obj.id
                }
            )
# ---------- CONTACT ----------
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at', 'is_contacted')
    list_filter = ('is_contacted', 'created_at')
    search_fields = ('name', 'email', 'message')
    actions = ['mark_as_contacted']
    
    fields = (
        'name', 'email', 'phone', 'message',
        'created_at', 'is_contacted', 'notes',
    )
    readonly_fields = ('created_at',)

    def mark_as_contacted(self, request, queryset):
        queryset.update(is_contacted=True)
    mark_as_contacted.short_description = "Mark selected as contacted"


# ---------- SITE CONFIGURATION (SINGLETON) ----------
@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    # ✅ NO fieldsets – just a clean list of all editable fields
    fields = (
        'phone', 'email', 'address',
        'linkedin', 'instagram', 'facebook', 'youtube',
        'map_embed_url',
    )

    def has_add_permission(self, request):
        # Cache the existence check – speeds up admin
        if not hasattr(self, '_has_add_permission'):
            exists = cache.get('siteconfig_exists')
            if exists is None:
                exists = SiteConfiguration.objects.exists()
                cache.set('siteconfig_exists', exists, 300)
            self._has_add_permission = not exists
        return self._has_add_permission

    def has_delete_permission(self, request, obj=None):
        return False