from django.views.generic import TemplateView,DetailView
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import (Project, ProjectImage, ProjectStat,NewsArticle,
                     DownloadCategory,DownloadItem,ChatMessage,ServiceEnquiry,ContactMessage)
from django.views.generic import ListView, DetailView
from django.db import models
from rest_framework import generics, status
from rest_framework.response import Response

from .models import AcademyCourse, AcademyEnrollment,AcademyCourseFeature
from .serializers import AcademyEnrollmentSerializer,ServiceEnquirySerializer,ContactMessageSerializer
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json



# Main pages
class HomeView(TemplateView):
    template_name = "core/index.html"

class AboutView(TemplateView):
    template_name = "core/about.html"

class ContactView(TemplateView):
    template_name = "core/contact.html"

class ContactMessageCreateAPIView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "success": True,
                "message": "Thank you for contacting us! We’ll get back to you within 24 hours.",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class ProjectsView(TemplateView):
    template_name = "core/projects.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all active projects
        projects_list = Project.objects.filter(is_active=True).order_by('display_order', '-date_completed')
        
        # Prefetch related images to avoid N+1 queries
        projects_list = projects_list.prefetch_related('project_images')
        
        # Pagination (optional, show 6 per page)
        paginator = Paginator(projects_list, 6)
        page = self.request.GET.get('page')
        projects = paginator.get_page(page)
        
        # Get active project statistics
        project_stats = ProjectStat.objects.filter(is_active=True).order_by('display_order')
        
        context['projects'] = projects
        context['project_stats'] = project_stats
        return context
    
class ProjectDetailView(DetailView):
    model = Project
    template_name = 'core/project_detail.html'   
    context_object_name = 'project'

class NewsListView(ListView):
    model = NewsArticle
    template_name = 'core/news.html'
    context_object_name = 'articles'
    paginate_by = 6  # 3 columns, 2 rows per page

    def get_queryset(self):
        return NewsArticle.objects.filter(is_active=True).select_related()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Separate featured article from the rest
        featured = NewsArticle.objects.filter(is_active=True, is_featured=True).first()
        if featured:
            context['featured_article'] = featured
            # Exclude featured from the main list
            context['article_list'] = self.get_queryset().exclude(id=featured.id)
        else:
            context['featured_article'] = None
            context['article_list'] = self.get_queryset()
        return context


class NewsDetailView(DetailView):
    model = NewsArticle
    template_name = 'core/news_detail.html'
    context_object_name = 'article'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return NewsArticle.objects.filter(is_active=True)

class SafetyView(TemplateView):
    template_name = "core/safety.html"

class ApprovalsView(TemplateView):
    template_name = "core/approvals.html"

class DownloadsView(ListView):
    model = DownloadCategory
    template_name = 'core/downloads.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return DownloadCategory.objects.filter(
            is_active=True
        ).prefetch_related(
            models.Prefetch(
                'items',
                queryset=DownloadItem.objects.filter(is_active=True).order_by('display_order'),
                to_attr='active_items'
            )
        ).order_by('display_order')

class CalculatorResultsView(TemplateView):
    template_name = "core/calculator-results.html"

# Services pages
class AcademyView(TemplateView):
    template_name = 'core/services/academy.html'

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

class AcademyEnrollmentAPIView(generics.CreateAPIView):
    queryset = AcademyEnrollment.objects.all()
    serializer_class = AcademyEnrollmentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "success": True,
                "message": "Enrollment submitted successfully. Our advisor will contact you soon.",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class BuildingConstructionView(TemplateView):
    template_name = "core/services/building-construction.html"

class EnergyEfficiencyView(TemplateView):
    template_name = "core/services/energy-efficiency.html"

class IndustrialServicesView(TemplateView):
    template_name = "core/services/industrial-services.html"

class RenewableEnergyView(TemplateView):
    template_name = "core/services/renewable-energy.html"

class SolarCalculatorView(TemplateView):
    template_name = "core/services/solar-calculator.html"

class ServiceEnquiryCreateAPIView(generics.CreateAPIView):
    queryset = ServiceEnquiry.objects.all()
    serializer_class = ServiceEnquirySerializer

    def create(self, request, *args, **kwargs):
        # You can pre‑set the service if you prefer:
        # data = request.data.copy()
        # data['service'] = 'renewable'
        # serializer = self.get_serializer(data=data)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "success": True,
                "message": "Your enquiry has been sent. Our team will contact you within 24 hours.",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )

@csrf_exempt
def chat_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        user_msg = data.get('message', '').strip()
    except:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if not user_msg:
        return JsonResponse({'reply': 'Please type a message.'})

    # --- SAVE USER MESSAGE TO DATABASE ---
    chat = ChatMessage.objects.create(user_message=user_msg)

    # --- (OPTIONAL) TRY TO ANSWER AUTOMATICALLY ---
    # Your existing keyword matching logic here
    # If you have a match, set chat.admin_reply and chat.replied_by = 'AI'
    # For now, we just save the message and return a fallback

    return JsonResponse({
        'reply': 'Thank you for your message. Our expert will get back to you within 2 hours.',
        'message_id': chat.id  # useful for tracking
    })


@csrf_exempt
def get_replies(request):
    """Return any new admin reply for messages with ID >= last_id."""
    last_id = request.GET.get('last_id')
    if not last_id:
        return JsonResponse({'reply': None})

    try:
        last_id = int(last_id)

        # 1️⃣ Check if the message with ID = last_id now has a reply
        current = ChatMessage.objects.filter(
            id=last_id,
            admin_reply__isnull=False
        ).first()
        if current:
            return JsonResponse({
                'reply': current.admin_reply,
                'message_id': current.id
            })

        # 2️⃣ Check newer messages that have replies
        newer = ChatMessage.objects.filter(
            id__gt=last_id,
            admin_reply__isnull=False
        ).order_by('id').first()
        if newer:
            return JsonResponse({
                'reply': newer.admin_reply,
                'message_id': newer.id
            })

    except (ValueError, TypeError):
        pass

    return JsonResponse({'reply': None})