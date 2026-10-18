from datetime import date, timedelta
from django.test import TestCase, Client
from django.urls import reverse
from parlor.models import (
    SalonProfile,
    Artist,
    ServiceCategory,
    Service,
    Package,
    Appointment,
    GalleryItem,
    Testimonial,
)
from parlor.forms import AppointmentBookingForm


class ParlorWebsiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile = SalonProfile.objects.create(
            name="Nishi Makeup Artist & Beauty Parlour",
            phone="+880 1904-423317",
            phone_clean="+8801904423317",
            facebook_url="https://www.facebook.com/profile.php?id=61595083298208",
        )
        self.artist = Artist.objects.create(
            name="Nishi Sultana",
            title="Lead Bridal Stylist",
            experience_years=8,
            specialties="Royal Bridal, 4K HD Airbrush",
            bio="Lead stylist test bio",
            photo="https://example.com/photo.jpg",
            rating=5.0,
            completed_brides=500,
        )
        self.category = ServiceCategory.objects.create(
            name="Bridal & Occasion",
            slug="bridal-occasion",
            icon="sparkles",
        )
        self.service = Service.objects.create(
            category=self.category,
            name="Bridal Makeup",
            slug="bridal-makeup",
            short_description="Signature royal bridal look",
            starting_price=10000,
            duration="3 Hours",
            image="https://example.com/bridal.jpg",
        )
        self.package = Package.objects.create(
            name="Luxury Bridal",
            slug="luxury-bridal",
            badge_text="Most Popular",
            is_popular=True,
            price=10000,
            short_description="All inclusive bridal",
            included_features="HD Base\nHairstyling\nSaree Draping",
        )

    def test_homepage_loads_successfully(self):
        response = self.client.get(reverse('parlor:home'))
        self.assertContains(response, "Your Beauty, Our Art")
        self.assertContains(response, "Your Special Moment")
        self.assertContains(response, "+880 1904-423317")
        self.assertContains(response, "https://www.facebook.com/profile.php?id=61595083298208")
        self.assertContains(response, "Nishi Sultana")
        self.assertContains(response, "Luxury Bridal")
        self.assertContains(response, "Book Your Appointment Now")

    def test_subpages_load_successfully(self):
        pages = ['about', 'artists', 'services', 'packages', 'gallery', 'book', 'track_booking', 'admin_dashboard']
        for page in pages:
            response = self.client.get(reverse(f'parlor:{page}'))
            self.assertEqual(response.status_code, 200, f"Page parlor:{page} failed to load.")

    def test_appointment_booking_submission(self):
        tomorrow = date.today() + timedelta(days=1)
        data = {
            'submit_booking': '1',
            'customer_name': 'Ayesha Siddiqua',
            'phone_number': '01904423317',
            'customer_address': 'Dhanmondi, Dhaka',
            'preferred_artist': self.artist.id,
            'package': self.package.id,
            'appointment_date': tomorrow.strftime('%Y-%m-%d'),
            'preferred_time': '03:30 PM',
            'event_type': 'Bridal',
            'special_requests': 'Red silk lehenga and heavy jewelry.',
            'agree_terms': 'on',
        }
        response = self.client.post(reverse('parlor:home'), data)
        # Should redirect to booking confirmation
        self.assertEqual(response.status_code, 302)
        
        # Verify saved in database
        appointment = Appointment.objects.filter(customer_name='Ayesha Siddiqua').first()
        self.assertIsNotNone(appointment)
        self.assertTrue(appointment.booking_reference.startswith('NB-'))
        self.assertEqual(appointment.status, 'pending')
        self.assertEqual(appointment.estimated_amount, 10000)

        # Test confirmation page
        conf_response = self.client.get(reverse('parlor:booking_confirmation', kwargs={'reference': appointment.booking_reference}))
        self.assertEqual(conf_response.status_code, 200)
        self.assertContains(conf_response, appointment.booking_reference)
        self.assertContains(conf_response, "Ayesha Siddiqua")

    def test_past_date_validation_fails(self):
        yesterday = date.today() - timedelta(days=1)
        form_data = {
            'customer_name': 'Test User',
            'phone_number': '01904423317',
            'customer_address': 'Dhaka',
            'appointment_date': yesterday.strftime('%Y-%m-%d'),
            'preferred_time': '03:30 PM',
            'event_type': 'Bridal',
            'agree_terms': True,
        }
        form = AppointmentBookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('appointment_date', form.errors)

    def test_track_booking_lookup(self):
        appt = Appointment.objects.create(
            customer_name="Taslima Nasrin",
            phone_number="01904423317",
            customer_address="Gulshan, Dhaka",
            appointment_date=date.today() + timedelta(days=3),
            preferred_time="05:30 PM",
            event_type="Reception",
            package=self.package,
        )
        response = self.client.get(reverse('parlor:track_booking') + f'?q={appt.booking_reference}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, appt.booking_reference)
        self.assertContains(response, "Taslima Nasrin")

    def test_status_update_on_dashboard(self):
        appt = Appointment.objects.create(
            customer_name="Sadia Islam",
            phone_number="01904423317",
            customer_address="Banani, Dhaka",
            appointment_date=date.today() + timedelta(days=5),
            preferred_time="01:30 PM",
            event_type="Bridal",
            package=self.package,
            status='pending',
        )
        response = self.client.post(reverse('parlor:update_status', kwargs={'pk': appt.id}), {
            'status': 'confirmed'
        })
        self.assertEqual(response.status_code, 302)
        appt.refresh_from_db()
        self.assertEqual(appt.status, 'confirmed')
