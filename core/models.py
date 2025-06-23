# Name: AKASHDEEP SINGH
# Student ID: 24072095
from django.db import models
from django.contrib.auth.models import AbstractUser
from .models_contact import ContactMessage

# User model with roles
class User(AbstractUser):
    ROLE_CHOICES = [
        ('citizen', 'Citizen'),
        ('volunteer', 'Volunteer'),
        ('authority', 'Authority'),
    ]
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    skills = models.CharField(max_length=255, blank=True, null=True)
    availability = models.CharField(max_length=255, blank=True, null=True)

class DisasterReport(models.Model):
    DISASTER_TYPE_CHOICES = [
        ('flood', 'Flood'),
        ('landslide', 'Landslide'),
        ('haze', 'Haze'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    disaster_type = models.CharField(max_length=20, choices=DISASTER_TYPE_CHOICES)
    gps_lat = models.DecimalField(max_digits=9, decimal_places=6)
    gps_long = models.DecimalField(max_digits=9, decimal_places=6)
    severity = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

class Shelter(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    available_capacity = models.PositiveIntegerField()
    description = models.TextField(blank=True)

class AidRequest(models.Model):
    AID_TYPE_CHOICES = [
        ('food', 'Food'),
        ('shelter', 'Shelter'),
        ('rescue', 'Rescue'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    disaster_report = models.ForeignKey(DisasterReport, on_delete=models.CASCADE)
    aid_type = models.CharField(max_length=20, choices=AID_TYPE_CHOICES)
    details = models.TextField()
    status = models.CharField(max_length=50, default='Pending')
    timestamp = models.DateTimeField(auto_now_add=True)

class VolunteerAssignment(models.Model):
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')
    aid_request = models.ForeignKey(AidRequest, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    status = models.CharField(max_length=50, default='Assigned')
    assigned_at = models.DateTimeField(auto_now_add=True)
