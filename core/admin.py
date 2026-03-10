from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.core.cache import cache
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import (
    Project, ProjectImage, ProjectStat, NewsArticle,
    DownloadCategory, DownloadItem,
    ChatMessage, ContactMessage, SiteConfiguration, Client, Partner,
    JourneyMilestone, Certificate, TeamMember, SolarLead,CalculatorLead,QuoteSelection
)


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


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_message', 'admin_reply', 'created_at', 'replied_at', 'is_archived')
    list_filter = ('is_archived', 'created_at')
    search_fields = ('user_message', 'admin_reply')
    readonly_fields = ('created_at', 'replied_at', 'replied_by')
    
    def save_model(self, request, obj, form, change):
        if obj.admin_reply and not obj.replied_by:
            obj.replied_by = request.user
            obj.replied_at = timezone.now()
        super().save_model(request, obj, form, change)
        if obj.admin_reply:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'chat_{obj.id}',
                {
                    'type': 'chat_reply',
                    'reply': obj.admin_reply,
                    'message_id': obj.id
                }
            )


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


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    fields = (
        'phone', 'email', 'address',
        'linkedin', 'instagram', 'facebook', 'youtube',
        'map_embed_url',
    )

    def has_add_permission(self, request):
        if not hasattr(self, '_has_add_permission'):
            exists = cache.get('siteconfig_exists')
            if exists is None:
                exists = SiteConfiguration.objects.exists()
                cache.set('siteconfig_exists', exists, 300)
            self._has_add_permission = not exists
        return self._has_add_permission

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    search_fields = ('name',)


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    search_fields = ('name',)
    fields = ('name', 'logo', 'url', 'display_order', 'is_active')


@admin.register(JourneyMilestone)
class JourneyMilestoneAdmin(admin.ModelAdmin):
    list_display = ('year', 'title', 'accent_color', 'display_order', 'is_active')
    list_editable = ('accent_color', 'display_order', 'is_active')
    list_filter = ('year', 'accent_color', 'is_active')
    search_fields = ('title', 'description')
    fields = ('year', 'title', 'description', 'image', 'accent_color', 'display_order', 'is_active')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('title', 'status_value', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    fields = ('title', 'description', 'icon', 'status_label', 'status_value', 'badge_icon', 'display_order', 'is_active')


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'category', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'role')
    fields = ('name', 'role', 'category', 'quote', 'bio', 'image',
              'linkedin_url', 'twitter_url', 'instagram_url', 'facebook_url',
              'display_order', 'is_active')


@admin.register(SolarLead)
class SolarLeadAdmin(admin.ModelAdmin):
    list_display = ('phone', 'monthly_units', 'system_size', 'cost', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(CalculatorLead)
class CalculatorLeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'location', 'type', 'commercial_option', 'value', 'created_at', 'is_contacted')
    list_filter = ('type', 'subsidy', 'commercial_option', 'is_contacted', 'created_at')
    search_fields = ('name', 'email', 'phone', 'location')
    list_editable = ('is_contacted',)
    readonly_fields = ('created_at',)
    


@admin.register(QuoteSelection)
class QuoteSelectionAdmin(admin.ModelAdmin):
    list_display = ('lead', 'plan_name', 'system_size', 'price', 'created_at')
    list_filter = ('plan_name', 'created_at')
    search_fields = ('lead__name', 'lead__email')