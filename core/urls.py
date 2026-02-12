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

    path('news/',NewsListView.as_view(), name='news'),
    path('news/<slug:slug>/',NewsDetailView.as_view(), name='news_detail'),

    path("safety/", SafetyView.as_view(), name="safety"),
    path("approvals/", ApprovalsView.as_view(), name="approvals"),
    path("downloads/", DownloadsView.as_view(), name="downloads"),
    path("calculator-results/", CalculatorResultsView.as_view(), name="calculator"),

    # Services
    path("services/academy/", AcademyView.as_view(), name="academy"),
    path('api/academy/enroll/', AcademyEnrollmentAPIView.as_view(), name='academy_enroll_api'),

    path("services/building-construction/", BuildingConstructionView.as_view(), name="building_construction"),
    path("services/energy-efficiency/", EnergyEfficiencyView.as_view(), name="energy_efficiency"),
    path("services/industrial-services/", IndustrialServicesView.as_view(), name="industrial_services"),

    path("services/renewable-energy/", RenewableEnergyView.as_view(), name="renewable_energy"),
    path('api/service-enquiry/', ServiceEnquiryCreateAPIView.as_view(), name='service_enquiry_api'),

    path('chat-api/',chat_api, name='chat_api'),
    path('chat-api/replies/',get_replies, name='chat_replies'),
]

