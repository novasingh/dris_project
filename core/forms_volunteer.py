# Name: AKASHDEEP SINGH
# Student ID: 24072095
from django import forms

class VolunteerRegistrationForm(forms.Form):
    skills = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. First Aid, Search & Rescue'})
    )
    availability = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Weekends, Evenings'})
    )
