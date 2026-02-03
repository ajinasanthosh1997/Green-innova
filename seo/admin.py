from django.contrib import admin
from django.utils.html import format_html
from .models import SEOSettings, BrokenLink, SEOImage

@admin.register(SEOImage)
class SEOImageAdmin(admin.ModelAdmin):
    list_display = ('alt_text', 'thumbnail_preview')
    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        return format_html(
            '<img src="{}" width="100" style="border-radius:5px"/>',
            obj.image.url
        ) if obj.image else "No Image"
    thumbnail_preview.short_description = "Preview"

@admin.register(SEOSettings)
class SEOSettingsAdmin(admin.ModelAdmin):
    list_display = ('slug', 'focus_keyword', 'robots_tag')
    list_filter = ('robots_tag', 'schema_type')
    fieldsets = (
        ("Generic Relation (Optional)", {
            "fields": ("content_type", "object_id"),
            "classes": ("collapse",),
            "description": "Link to a specific content object if needed"
        }),
        ("Meta Settings", {
            "fields": ("slug", "focus_keyword", "canonical_url")
        }),
        ("Social/SEO", {
            "fields": ("meta_title", "meta_description", "og_title", "og_image")
        }),
        ("Advanced", {
            "fields": ("robots_tag", "schema_type"),
            "classes": ("collapse",)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Handle cases where generic relation fields are not provided"""
        if not obj.content_type_id or not obj.object_id:
            obj.content_type = None
            obj.object_id = None
        super().save_model(request, obj, form, change)
        
@admin.register(BrokenLink)
class BrokenLinkAdmin(admin.ModelAdmin):
    list_display = ('url', 'status_badge', 'detected_on', 'resolved')
    list_editable = ('resolved',)
    
    def status_badge(self, obj):
        color = "success" if obj.status_code == 200 else "danger"
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color, obj.status_code
        )
    status_badge.short_description = "Status"