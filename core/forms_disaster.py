from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import DisasterReport
from .forms import DisasterReportFilterForm
from .decorators import role_required

from django import forms

class DisasterReportForm(forms.ModelForm):
    class Meta:
        model = DisasterReport
        fields = ['disaster_type', 'gps_lat', 'gps_long', 'severity', 'description']
        widgets = {
            'disaster_type': forms.Select(attrs={'class': 'form-select'}),
            'gps_lat': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'gps_long': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'severity': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
