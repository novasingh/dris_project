# Name: AKASHDEEP SINGH
# Student ID: 24072095
from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from .models import User, DisasterReport, AidRequest, Shelter, VolunteerAssignment
from .models_contact import ContactMessage
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import ValidationError

class CustomAdminSite(admin.AdminSite):
    site_header = 'DRIS Admin'
    site_title = 'DRIS Admin Portal'
    index_title = 'Welcome to DRIS Admin Portal'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dris-dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        # You can add context data here as needed
        context = dict(
            self.each_context(request),
            title='Admin Dashboard',
        )
        return TemplateResponse(request, 'core/admin_dashboard.html', context)

admin_site = CustomAdminSite()

# Register models with the custom admin site
admin_site.register(User)
admin_site.register(DisasterReport)
admin_site.register(AidRequest)
admin_site.register(Shelter)
admin_site.register(VolunteerAssignment)
admin_site.register(ContactMessage)

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        return password

class UserAdmin(BaseUserAdmin):
    form = UserAdminForm
    add_form = UserAdminForm

admin_site.unregister(User)
admin_site.register(User, UserAdmin)
