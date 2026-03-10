from django.urls import path
from .views import (
    RenewableEnergyView, EnergyEfficiencyView,
    BuildingConstructionView, IndustrialServicesView,
    ExteriorInsulationView, AcademyView,
    AcademyEnrollmentCreateView, ServiceEnquiryCreateAPIView
)

urlpatterns = [
    path('renewable-energy/', RenewableEnergyView.as_view(), name='renewable_energy'),
    path('energy-efficiency/', EnergyEfficiencyView.as_view(), name='energy_efficiency'),
    path('building-construction/', BuildingConstructionView.as_view(), name='building_construction'),
    path('industrial-services/', IndustrialServicesView.as_view(), name='industrial_services'),
    path('exterior-insulation/', ExteriorInsulationView.as_view(), name='exterior_insulation'),
    path('academy/', AcademyView.as_view(), name='academy'),
    # API endpoints
    path('api/enroll/',AcademyEnrollmentCreateView.as_view(), name='api-enroll'),
    path('api/service-enquiry/', ServiceEnquiryCreateAPIView.as_view(), name='service_enquiry_api'),
]