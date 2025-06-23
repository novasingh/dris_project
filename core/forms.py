# Name: AKASHDEEP SINGH
# Student ID: 24072095
from django import forms
from .models import AidRequest, DisasterReport, User, Shelter
from .models_contact import ContactMessage

class AidRequestForm(forms.ModelForm):
    class Meta:
        model = AidRequest
        fields = ['aid_type', 'disaster_report', 'details']
        widgets = {
            'aid_type': forms.Select(attrs={'class': 'form-select'}),
            'disaster_report': forms.Select(attrs={'class': 'form-select'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class DisasterReportFilterForm(forms.Form):
    disaster_type = forms.ChoiceField(
        choices=[('', 'All Types'), ('flood', 'Flood'), ('landslide', 'Landslide'), ('haze', 'Haze')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    severity = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Severity'}))
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Password',
        min_length=8,
        help_text='Password must be at least 8 characters long.'
    )
    role = forms.ChoiceField(
        choices=[('citizen', 'Citizen'), ('volunteer', 'Volunteer')],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Role'
    )
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        return password
    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'role', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 4}),
        }

class ShelterForm(forms.ModelForm):
    class Meta:
        model = Shelter
        fields = ['name', 'location', 'capacity', 'available_capacity', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shelter Name'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Address'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total Capacity'}),
            'available_capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Available Spaces'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional Details'}),
        }

class ShelterFilterForm(forms.Form):
    location = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by location'
        })
    )
    availability = forms.ChoiceField(
        choices=[
            ('', 'All'),
            ('available', 'Available'),
            ('limited', 'Limited'),
            ('full', 'Full')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    capacity_min = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min capacity'
        })
    )
    capacity_max = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max capacity'
        })
    )
