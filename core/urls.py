from django.urls import path
from .views import *

urlpatterns = [
    # Main pages
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    
    path("contact/", ContactView.as_view(), name="contact"),
    path('api/contact/', ContactMessageCreateAPIView.as_view(), name='contact_api'),

    path("projects/", ProjectsView.as_view(), name="projects"),
    path('projects/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),

    path('news/', NewsListView.as_view(), name='news'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news_detail'),

    path("safety/", SafetyView.as_view(), name="safety"),
    path("approvals/", ApprovalsView.as_view(), name="approvals"),
    path("downloads/", DownloadsView.as_view(), name="downloads"),
    path("calculator-results/", CalculatorResultsView.as_view(), name="calculator"),
    path('team/', TeamView.as_view(), name='team'),

    # Chat
    path('chat-api/', chat_api, name='chat_api'),
    path('chat-api/replies/', get_replies, name='chat_replies'),

    # Solar calculator
    path("solar-calculator/", solar_calculator, name="solar_calculator"),
    path('api/calculator-lead/', CalculatorLeadCreateAPIView.as_view(), name='calculator_lead_api'),

    path('api/quote-selection/', QuoteSelectionCreateAPIView.as_view(), name='quote_selection_api'),
]