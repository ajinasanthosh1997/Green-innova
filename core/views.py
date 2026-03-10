from django.views.generic import TemplateView, DetailView, ListView
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db import models
from rest_framework import generics, status
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import (
    Project, ProjectStat, NewsArticle,
    DownloadCategory, DownloadItem, ChatMessage,
    ContactMessage, Client, Partner, JourneyMilestone,QuoteSelection,
    Certificate, TeamMember
)
from .serializers import ContactMessageSerializer,QuoteSelectionSerializer


from .serializers import CalculatorLeadSerializer
from .models import CalculatorLead


def solar_calculator(request):
    result = None
    if request.method == "POST":
        category = request.POST.get("category")
        subsidy = request.POST.get("subsidy")
        input_type = request.POST.get("input_type")
        value = request.POST.get("value")
        engine = SolarCalculator(category, subsidy, input_type, value)
        result = engine.calculate()
    return render(request, "calculator/calculator.html", {"result": result})


# Main pages
class HomeView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients'] = Client.objects.filter(is_active=True)
        context['partners'] = Partner.objects.filter(is_active=True)
        return context


class AboutView(TemplateView):
    template_name = "core/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['journey_milestones'] = JourneyMilestone.objects.filter(is_active=True).order_by('year', 'display_order')
        return context


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
        projects_list = Project.objects.filter(is_active=True).order_by('display_order', '-date_completed')
        projects_list = projects_list.prefetch_related('project_images')
        paginator = Paginator(projects_list, 6)
        page = self.request.GET.get('page')
        projects = paginator.get_page(page)
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
    paginate_by = 6

    def get_queryset(self):
        return NewsArticle.objects.filter(is_active=True).select_related()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        featured = NewsArticle.objects.filter(is_active=True, is_featured=True).first()
        if featured:
            context['featured_article'] = featured
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['certificates'] = Certificate.objects.filter(is_active=True).order_by('display_order')
        return context


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


class TeamView(TemplateView):
    template_name = "core/team.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['founders'] = TeamMember.objects.filter(category='founder', is_active=True).order_by('display_order')
        context['team_members'] = TeamMember.objects.filter(category='team', is_active=True).order_by('display_order')
        return context


# Chat API
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
    chat = ChatMessage.objects.create(user_message=user_msg)
    return JsonResponse({
        'reply': 'Thank you for your message. Our expert will get back to you within 2 hours.',
        'message_id': chat.id
    })


@csrf_exempt
def get_replies(request):
    last_id = request.GET.get('last_id')
    if not last_id:
        return JsonResponse({'reply': None})
    try:
        last_id = int(last_id)
        current = ChatMessage.objects.filter(id=last_id, admin_reply__isnull=False).first()
        if current:
            return JsonResponse({'reply': current.admin_reply, 'message_id': current.id})
        newer = ChatMessage.objects.filter(id__gt=last_id, admin_reply__isnull=False).order_by('id').first()
        if newer:
            return JsonResponse({'reply': newer.admin_reply, 'message_id': newer.id})
    except (ValueError, TypeError):
        pass
    return JsonResponse({'reply': None})

class CalculatorLeadCreateAPIView(generics.CreateAPIView):
    queryset = CalculatorLead.objects.all()
    serializer_class = CalculatorLeadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lead = serializer.save()
        return Response(
            {
                "success": True,
                "message": "Lead saved successfully.",
                "lead_id": lead.id
            },
            status=status.HTTP_201_CREATED
        )

class QuoteSelectionCreateAPIView(generics.CreateAPIView):
    queryset = QuoteSelection.objects.all()
    serializer_class = QuoteSelectionSerializer