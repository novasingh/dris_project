# Name: AKASHDEEP SINGH
# Student ID: 24072095
from django.urls import path
from . import views
from .views import CustomLoginView, dashboard_router, profile, help_faq, add_shelter

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', dashboard_router, name='dashboard_router'),
    path('disasters/', views.disaster_report_list, name='disaster_report_list'),
    path('disasters/json/', views.disaster_report_list_json, name='disaster_report_list_json'),
    path('aid/request/', views.aid_request_create, name='aid_request_create'),
    path('volunteer/register/', views.volunteer_registration, name='volunteer_registration'),
    path('shelters/', views.shelter_directory, name='shelter_directory'),
    path('shelters/json/', views.shelter_directory_json, name='shelter_directory_json'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('volunteers/', views.volunteer_list, name='volunteer_list'),
    path('assign-volunteer/', views.assign_volunteer, name='assign_volunteer'),
    path('register/', views.register, name='register'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/profile/', profile, name='profile'),
    path('help/', help_faq, name='help_faq'),
    path('shelters/add/', add_shelter, name='add_shelter'),
]
