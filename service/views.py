from django.views.generic import TemplateView
from rest_framework import generics, status
from rest_framework.response import Response
from .models import (
    RenewableSubService,
    EnergyEfficiencySubService,
    AcademyCourse,
    AcademyEnrollment,
    ServiceEnquiry,BuildingConstructionSubService,IndustrialServiceSubService,AcademyCourseFeature,EIFSTechnicalFeature, EIFSProject, EIFSReference
)
from .serializers import AcademyEnrollmentSerializer, ServiceEnquirySerializer
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db import models
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# ---------- Template Views ----------
class RenewableEnergyView(TemplateView):
    template_name = "services/renewable-energy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_services'] = RenewableSubService.objects.filter(
            is_active=True
        ).order_by('display_order')
        return context


class EnergyEfficiencyView(TemplateView):
    template_name = "services/energy-efficiency.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_services'] = EnergyEfficiencySubService.objects.filter(
            is_active=True
        ).order_by('display_order')
        return context


class BuildingConstructionView(TemplateView):
    template_name = "services/building-construction.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_services'] = BuildingConstructionSubService.objects.filter(
            is_active=True
        ).order_by('display_order')
        return context


class IndustrialServicesView(TemplateView):
    template_name = "services/industrial-services.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_services'] = IndustrialServiceSubService.objects.filter(
            is_active=True
        ).order_by('display_order')
        return context


class ExteriorInsulationView(TemplateView):
    template_name = "services/exterior-insulation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['eifs_features'] = EIFSTechnicalFeature.objects.filter(is_active=True).order_by('display_order')
        context['eifs_projects'] = EIFSProject.objects.filter(is_active=True).order_by('display_order')
        context['eifs_references'] = EIFSReference.objects.filter(is_active=True).order_by('display_order')
        return context


class AcademyView(TemplateView):
    template_name = 'services/academy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all active courses, ordered by display_order, prefetch features
        context['courses'] = AcademyCourse.objects.filter(
            is_active=True
        ).prefetch_related(
            models.Prefetch('features', queryset=AcademyCourseFeature.objects.order_by('display_order'))
        ).order_by('display_order')
        return context

    def post(self, request, *args, **kwargs):
        """Handle traditional form submission (non-AJAX)."""
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        course_id = request.POST.get('course')
        background = request.POST.get('background')

        if full_name and email and phone and course_id and background:
            try:
                course = AcademyCourse.objects.get(id=course_id, is_active=True)
                AcademyEnrollment.objects.create(
                    full_name=full_name,
                    email=email,
                    phone=phone,
                    course=course,
                    background=background
                )
                messages.success(request, 'Thank you! Our academic advisor will contact you within 24 hours.')
            except AcademyCourse.DoesNotExist:
                messages.error(request, 'Invalid course selection.')
        else:
            messages.error(request, 'Please fill in all fields.')

        return redirect('academy')

@method_decorator(csrf_exempt, name='dispatch')
class AcademyEnrollmentCreateView(CreateAPIView):
    queryset = AcademyEnrollment.objects.all()
    serializer_class = AcademyEnrollmentSerializer
    permission_classes = [AllowAny]  # Allow anyone to submit the form

class ServiceEnquiryCreateAPIView(generics.CreateAPIView):
    queryset = ServiceEnquiry.objects.all()
    serializer_class = ServiceEnquirySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "success": True,
                "message": "Your enquiry has been sent. Our team will contact you within 24 hours.",
            },
            status=status.HTTP_201_CREATED,
        )