# Name: AKASHDEEP SINGH
# Student ID: 24072095
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import DisasterReport, AidRequest
from .forms import AidRequestForm, DisasterReportFilterForm, ContactForm
from .forms_volunteer import VolunteerRegistrationForm
from django.utils import timezone
from .decorators import role_required
from django.http import JsonResponse
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ShelterForm, ShelterFilterForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import User
from django.core.paginator import Paginator
from .forms_disaster import DisasterReportForm

def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent!')
            return redirect('home')
    else:
        form = ContactForm()
    return render(request, 'core/home.html', {'form': form})

@login_required
@role_required(['citizen', 'volunteer', 'authority'])
def disaster_report_list(request):
    form = DisasterReportFilterForm(request.GET or None)
    reports = DisasterReport.objects.all().select_related('user')
    if form.is_valid():
        if form.cleaned_data['disaster_type']:
            reports = reports.filter(disaster_type=form.cleaned_data['disaster_type'])
        if form.cleaned_data['severity']:
            reports = reports.filter(severity__icontains=form.cleaned_data['severity'])
        if form.cleaned_data['date']:
            date = form.cleaned_data['date']
            reports = reports.filter(timestamp__date=date)
    paginator = Paginator(reports.order_by('-timestamp'), 10)
    page_number = request.GET.get('page')
    reports_page = paginator.get_page(page_number)
    context = {
        'reports': reports_page,
        'form': form,
    }
    return render(request, 'core/disaster_report_list.html', context)

@login_required
@role_required(['citizen', 'authority'])
def disaster_report_create(request):
    if request.method == 'POST':
        form = DisasterReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.timestamp = timezone.now()
            report.save()
            return redirect('dashboard_router')
    else:
        form = DisasterReportForm()
    return render(request, 'core/disaster_report_form.html', {'form': form})

@login_required
@role_required(['citizen', 'authority'])
def aid_request_create(request):
    if request.method == 'POST':
        form = AidRequestForm(request.POST)
        if form.is_valid():
            aid_request = form.save(commit=False)
            aid_request.user = request.user
            aid_request.timestamp = timezone.now()
            aid_request.save()
            return redirect('dashboard_router')
    else:
        form = AidRequestForm()
    form.fields['disaster_report'].queryset = DisasterReport.objects.filter(user=request.user)
    context = {
        'form': form,
        'disaster_reports': DisasterReport.objects.filter(user=request.user),
    }
    return render(request, 'core/aid_request_form.html', context)

@login_required
@role_required(['volunteer', 'citizen'])
def volunteer_registration(request):
    if request.method == 'POST':
        form = VolunteerRegistrationForm(request.POST)
        if form.is_valid():
            request.user.skills = form.cleaned_data['skills']
            request.user.availability = form.cleaned_data['availability']
            request.user.save()
            return redirect('dashboard_router')
    else:
        form = VolunteerRegistrationForm()
    return render(request, 'core/volunteer_registration.html', {'form': form})

@login_required
@role_required(['citizen', 'volunteer', 'authority'])
def shelter_directory(request):
    from .models import Shelter
    shelters = Shelter.objects.all().order_by('name')
    form = ShelterFilterForm(request.GET)
    
    if form.is_valid():
        location = form.cleaned_data.get('location')
        availability = form.cleaned_data.get('availability')
        capacity_min = form.cleaned_data.get('capacity_min')
        capacity_max = form.cleaned_data.get('capacity_max')

        if location:
            shelters = shelters.filter(
                Q(name__icontains=location) | Q(location__icontains=location)
            )
        
        if availability:
            if availability == 'available':
                shelters = shelters.filter(available_capacity__gt=0)
            elif availability == 'limited':
                shelters = shelters.filter(
                    available_capacity__gt=0,
                    available_capacity__lt=0.2 * F('capacity')
                )
            elif availability == 'full':
                shelters = shelters.filter(available_capacity=0)

        if capacity_min is not None:
            shelters = shelters.filter(capacity__gte=capacity_min)
        if capacity_max is not None:
            shelters = shelters.filter(capacity__lte=capacity_max)

    return render(request, 'core/shelter_directory.html', {
        'shelters': shelters,
        'form': form
    })

@login_required
@role_required(['authority'])
def admin_dashboard(request):
    from .models import User, DisasterReport, AidRequest, Shelter, VolunteerAssignment
    user_count = User.objects.count()
    report_count = DisasterReport.objects.count()
    request_count = AidRequest.objects.count()
    assignment_count = VolunteerAssignment.objects.count()
    active_shelter_count = Shelter.objects.filter(available_capacity__gt=0).count()
    context = {
        'user_count': user_count,
        'report_count': report_count,
        'request_count': request_count,
        'assignment_count': assignment_count,
        'active_shelter_count': active_shelter_count,
    }
    return render(request, 'core/admin_dashboard.html', context)

@login_required
@role_required(['citizen', 'volunteer', 'authority'])
def shelter_directory_json(request):
    from .models import Shelter
    shelters = Shelter.objects.all().order_by('name')
    data = [
        {
            'name': s.name,
            'location': s.location,
            'capacity': s.capacity,
            'available_capacity': s.available_capacity,
            'description': s.description,
        } for s in shelters
    ]
    return JsonResponse({'shelters': data})

@login_required
@role_required(['citizen', 'volunteer', 'authority'])
def disaster_report_list_json(request):
    reports = DisasterReport.objects.all().select_related('user').order_by('-timestamp')
    data = [
        {
            'type': r.get_disaster_type_display(),
            'severity': r.severity,
            'gps_lat': str(r.gps_lat),
            'gps_long': str(r.gps_long),
            'user': r.user.full_name,
            'timestamp': r.timestamp.strftime('%Y-%m-%d %H:%M'),
            'description': r.description,
        } for r in reports
    ]
    return JsonResponse({'reports': data})

@login_required
@role_required(['authority'])
def volunteer_list(request):
    from .models import User
    volunteers = User.objects.filter(role='volunteer').order_by('full_name')
    q = request.GET.get('q', '')
    if q:
        volunteers = volunteers.filter(
            Q(full_name__icontains=q) | Q(email__icontains=q) | Q(skills__icontains=q)
        )
    paginator = Paginator(volunteers, 10)
    page_number = request.GET.get('page')
    volunteers_page = paginator.get_page(page_number)
    return render(request, 'core/volunteer_list.html', {'volunteers': volunteers_page})

@login_required
@role_required(['authority'])
def assign_volunteer(request):
    from .models import AidRequest, User, VolunteerAssignment
    aid_requests = AidRequest.objects.filter(status='Pending').order_by('-timestamp')
    volunteers = User.objects.filter(role='volunteer')
    if request.method == 'POST':
        aid_request_id = request.POST.get('aid_request')
        volunteer_id = request.POST.get('volunteer')
        if aid_request_id and volunteer_id:
            aid_request = AidRequest.objects.get(id=aid_request_id)
            volunteer = User.objects.get(id=volunteer_id)
            VolunteerAssignment.objects.create(
                volunteer=volunteer,
                aid_request=aid_request,
                assigned_by=request.user,
                status='Assigned'
            )
            aid_request.status = 'Assigned'
            aid_request.save()
            return redirect('assign_volunteer')
    return render(request, 'core/assign_volunteer.html', {
        'aid_requests': aid_requests,
        'volunteers': volunteers,
    })

def register(request):
    from .forms import UserRegistrationForm
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def dashboard_router(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_superuser:
        return render(request, 'core/dashboard_superuser.html')
    if hasattr(request.user, 'role') and request.user.role == 'authority':
        return render(request, 'core/dashboard_authority.html')
    elif hasattr(request.user, 'role'):
        if request.user.role == 'citizen':
            return render(request, 'core/dashboard_citizen.html')
        elif request.user.role == 'volunteer':
            return render(request, 'core/dashboard_volunteer.html')
    # fallback
    logout(request)
    return redirect('login')

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        next_url = request.GET.get('next', '')
        if next_url == '/volunteer/register/':
            return redirect(reverse_lazy('register'))
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('dashboard_router')

@login_required
def profile(request):
    return render(request, 'core/profile.html')

def help_faq(request):
    return render(request, 'core/help_faq.html')

def is_admin_or_authority(user):
    return user.is_superuser or user.role == 'authority'

@login_required
@user_passes_test(is_admin_or_authority)
def add_shelter(request):
    if request.method == 'POST':
        form = ShelterForm(request.POST)
        if form.is_valid():
            shelter = form.save(commit=False)
            shelter.added_by = request.user
            shelter.save()
            messages.success(request, 'Shelter added successfully!')
            return redirect('shelter_directory')
    else:
        form = ShelterForm()
    return render(request, 'core/add_shelter.html', {'form': form})

@login_required
@role_required(['authority', 'superuser'])
def user_list(request):
    users = User.objects.all().order_by('full_name')
    q = request.GET.get('q', '')
    role = request.GET.get('role', '')
    if q:
        users = users.filter(
            Q(full_name__icontains=q) | Q(username__icontains=q) | Q(email__icontains=q)
        )
    if role:
        users = users.filter(role=role)
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    users_page = paginator.get_page(page_number)
    return render(request, 'core/user_list.html', {'users': users_page})

@login_required
@role_required(['authority', 'superuser'])
def aid_request_list(request):
    aid_requests = AidRequest.objects.all().select_related('user', 'disaster_report').order_by('-timestamp')
    q = request.GET.get('q', '')
    status = request.GET.get('status', '')
    if q:
        aid_requests = aid_requests.filter(
            Q(user__full_name__icontains=q) | Q(details__icontains=q) | Q(status__icontains=q)
        )
    if status:
        aid_requests = aid_requests.filter(status=status)
    paginator = Paginator(aid_requests, 10)
    page_number = request.GET.get('page')
    aid_requests_page = paginator.get_page(page_number)
    return render(request, 'core/aid_request_list.html', {'aid_requests': aid_requests_page})

@login_required
@role_required(['citizen'])
def my_aid_requests(request):
    aid_requests = AidRequest.objects.filter(user=request.user).order_by('-timestamp')
    paginator = Paginator(aid_requests, 10)
    page_number = request.GET.get('page')
    aid_requests_page = paginator.get_page(page_number)
    return render(request, 'core/my_aid_requests.html', {'aid_requests': aid_requests_page})

def permission_denied_view(request, exception=None):
    return render(request, 'registration/permission_denied.html', status=403)
