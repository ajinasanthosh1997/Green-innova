from django.contrib import admin
from .models import (
    RenewableSubService, EnergyEfficiencySubService,
    AcademyCourse, AcademyCourseFeature, AcademyEnrollment, ServiceEnquiry,
    BuildingConstructionSubService,IndustrialServiceSubService,EIFSTechnicalFeature, EIFSProject, EIFSReference
)

class AcademyCourseFeatureInline(admin.TabularInline):
    model = AcademyCourseFeature
    extra = 0

@admin.register(RenewableSubService)
class RenewableSubServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'badge', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')


@admin.register(EnergyEfficiencySubService)
class EnergyEfficiencySubServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'badge', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    fields = ('title', 'description', 'badge', 'icon', 'display_order', 'is_active')

@admin.register(AcademyCourse)
class AcademyCourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [AcademyCourseFeatureInline]

@admin.register(AcademyEnrollment)
class AcademyEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'course', 'created_at', 'status')
    list_filter = ('status', 'course', 'created_at')
    search_fields = ('full_name', 'email')
    readonly_fields = ('created_at',)

@admin.register(ServiceEnquiry)
class ServiceEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'service', 'created_at', 'is_contacted')
    list_filter = ('service', 'is_contacted')



@admin.register(BuildingConstructionSubService)
class BuildingConstructionSubServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'badge', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    fields = ('title', 'description', 'badge', 'icon', 'display_order', 'is_active')



@admin.register(IndustrialServiceSubService)
class IndustrialServiceSubServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'badge', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    fields = ('title', 'description', 'badge', 'icon', 'display_order', 'is_active')


@admin.register(EIFSTechnicalFeature)
class EIFSTechnicalFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    fields = ('icon', 'title', 'description', 'display_order', 'is_active')

@admin.register(EIFSProject)
class EIFSProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    fields = ('title', 'short_description', 'image', 'display_order', 'is_active')

@admin.register(EIFSReference)
class EIFSReferenceAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'area_sqm', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    fields = ('project_name', 'area_sqm', 'display_order', 'is_active')



