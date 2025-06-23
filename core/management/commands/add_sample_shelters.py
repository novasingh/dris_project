# Name: AKASHDEEP SINGH
# Student ID: 24072095
from django.core.management.base import BaseCommand
from core.models import Shelter

class Command(BaseCommand):
    help = 'Populates the database with initial shelter data for Malaysia'

    def handle(self, *args, **kwargs):
        shelters = [
            {
                'name': 'Kuala Lumpur Convention Centre Emergency Shelter',
                'location': 'Kuala Lumpur City Centre, 50088 Kuala Lumpur',
                'capacity': 500,
                'available_capacity': 500,
                'description': 'Large convention center converted to emergency shelter with medical facilities.'
            },
            {
                'name': 'Petaling Jaya Community Shelter',
                'location': 'Jalan Utara, 46200 Petaling Jaya, Selangor',
                'capacity': 300,
                'available_capacity': 300,
                'description': 'Community center equipped with beds, food storage, and basic medical supplies.'
            },
            {
                'name': 'Shah Alam Stadium Relief Center',
                'location': 'Jalan Persiaran Sukan, 40100 Shah Alam, Selangor',
                'capacity': 800,
                'available_capacity': 800,
                'description': 'Stadium facility with large capacity and medical wing.'
            },
            {
                'name': 'Penang International Sports Arena Shelter',
                'location': 'Jalan Tun Dr Awang, 11900 Bayan Lepas, Penang',
                'capacity': 600,
                'available_capacity': 600,
                'description': 'Indoor sports arena converted to disaster relief center.'
            },
            {
                'name': 'Johor Bahru Indoor Stadium Shelter',
                'location': 'Jalan Tebrau, 80200 Johor Bahru, Johor',
                'capacity': 450,
                'available_capacity': 450,
                'description': 'Climate-controlled facility with medical staff on standby.'
            },
            {
                'name': 'Melaka International Trade Centre Shelter',
                'location': 'Jalan MITC, 75450 Ayer Keroh, Melaka',
                'capacity': 400,
                'available_capacity': 400,
                'description': 'Large facility with separate family areas and childcare support.'
            },
            {
                'name': 'Ipoh City Council Hall Shelter',
                'location': 'Jalan Pandak Bandung, 30000 Ipoh, Perak',
                'capacity': 250,
                'available_capacity': 250,
                'description': 'Central location with easy access to medical facilities.'
            },
            {
                'name': 'Kuching Indoor Stadium Relief Center',
                'location': 'Jalan Stadium, 93100 Kuching, Sarawak',
                'capacity': 550,
                'available_capacity': 550,
                'description': 'Major relief center for Sarawak region with helicopter access.'
            },
            {
                'name': 'Kota Kinabalu Sports Complex Shelter',
                'location': 'Jalan UMS, 88400 Kota Kinabalu, Sabah',
                'capacity': 700,
                'available_capacity': 700,
                'description': 'Large facility serving Sabah region with full emergency services.'
            },
            {
                'name': 'Putrajaya Convention Centre Emergency Shelter',
                'location': 'Precinct 5, 62000 Putrajaya',
                'capacity': 1000,
                'available_capacity': 1000,
                'description': 'Primary government emergency shelter with advanced facilities.'
            }
        ]

        for shelter_data in shelters:
            Shelter.objects.get_or_create(
                name=shelter_data['name'],
                defaults={
                    'location': shelter_data['location'],
                    'capacity': shelter_data['capacity'],
                    'available_capacity': shelter_data['available_capacity'],
                    'description': shelter_data['description']
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully added sample shelter data'))
