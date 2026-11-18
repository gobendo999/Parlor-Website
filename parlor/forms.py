import re
from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from .models import (
    Appointment, ContactInquiry, Service, Package,
    SalonProfile, GalleryItem
)


class AppointmentBookingForm(forms.ModelForm):
    agree_terms = forms.BooleanField(
        required=True,
        error_messages={'required': 'You must agree to the appointment booking policy & studio guidelines.'},
        widget=forms.CheckboxInput(attrs={'class': 'custom-checkbox', 'id': 'agree_terms'})
    )

    class Meta:
        model = Appointment
        fields = [
            'customer_name',
            'phone_number',
            'customer_address',
            'service',
            'package',
            'appointment_date',
            'preferred_time',
            'event_type',
            'special_requests',
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '',
                'required': True,
                'autocomplete': 'name',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'tel',
                'placeholder': '',
                'required': True,
                'autocomplete': 'tel',
                'maxlength': '11',
                'minlength': '11',
                'pattern': '01[0-9]{9}',
                'inputmode': 'numeric',
                'title': 'ফোন নম্বরটি অবশ্যই ১১ ডিজিটের হতে হবে (যেমন: 01XXXXXXXXX)',
            }),
            'customer_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': '',
                'required': True,
            }),
            'service': forms.Select(attrs={
                'class': 'form-select',
                'id': 'service-select',
            }),
            'package': forms.Select(attrs={
                'class': 'form-select',
                'id': 'package-select',
            }),
            'appointment_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True,
                'id': 'appointment_date',
            }),
            'preferred_time': forms.Select(attrs={
                'class': 'form-select',
            }),
            'event_type': forms.Select(attrs={
                'class': 'form-select',
            }),
            'special_requests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Mention your skin type, desired look, dupatta setting, outfit color or any special requirements...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add friendly empty labels
        self.fields['service'].empty_label = "-- Select Specific Service (Optional) --"
        self.fields['package'].empty_label = "-- Select Luxury Package (Recommended) --"
        
        # Only show active services, packages
        self.fields['service'].queryset = Service.objects.filter(is_active=True)
        self.fields['package'].queryset = Package.objects.filter(is_active=True)

    def clean_phone_number(self):
        raw_phone = self.cleaned_data.get('phone_number', '').strip()
        digits = re.sub(r'\D', '', raw_phone)
        
        # If user included 880 at start (e.g. 88019...), normalize to 11 digits
        if digits.startswith('880') and len(digits) == 13:
            digits = '0' + digits[3:]
            
        if len(digits) != 11 or not digits.startswith('01'):
            raise ValidationError(
                'ফোন নম্বরটি অবশ্যই ১১ ডিজিটের হতে হবে (যেমন: 01XXXXXXXXX)।'
            )
        return digits

    def clean_appointment_date(self):
        appt_date = self.cleaned_data.get('appointment_date')
        if appt_date:
            today = date.today()
            if appt_date < today:
                raise ValidationError("Appointment date cannot be in the past. Please select today or a future date.")
        return appt_date

    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get('service')
        package = cleaned_data.get('package')
        if not service and not package:
            # We require at least a package or a service chosen
            pass
        return cleaned_data


class ContactInquiryForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ['name', 'phone', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number (e.g. +880 1904...)', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address (Optional)'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inquiry Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'How can we help make your event special?', 'required': True}),
        }


class BookingTrackForm(forms.Form):
    search_query = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control track-input',
            'placeholder': 'Enter Booking Reference (e.g. NB-2026-XXXX) or Phone Number',
        })
    )


class PortalLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'portal-input',
            'placeholder': 'Enter username (e.g. admin)',
            'autocomplete': 'username',
            'required': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'portal-input',
            'placeholder': 'Enter password',
            'autocomplete': 'current-password',
            'required': True,
        })
    )


class PortalServiceForm(forms.ModelForm):
    image = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'Or online image URL (https://...)'})
    )
    image_file = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'portal-input', 'accept': 'image/*'})
    )
    short_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'portal-input', 'rows': 2, 'placeholder': 'Brief description (optional)'})
    )

    class Meta:
        model = Service
        fields = [
            'category', 'name', 'starting_price', 'duration',
            'image', 'short_description', 'is_featured', 'is_active'
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'portal-input'}),
            'name': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'Service name (e.g. 24K Gold Facial)'}),
            'starting_price': forms.NumberInput(attrs={'class': 'portal-input', 'placeholder': 'Starting price in BDT (৳)'}),
            'duration': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'Duration (e.g. 60 Mins)'}),
            'short_description': forms.Textarea(attrs={'class': 'portal-input', 'rows': 2, 'placeholder': 'Brief summary of the service'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'portal-checkbox'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'portal-checkbox'}),
        }


class PortalPackageForm(forms.ModelForm):
    image = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'Or online image URL (https://...)'})
    )
    image_file = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'portal-input', 'accept': 'image/*'})
    )

    class Meta:
        model = Package
        fields = [
            'name', 'price', 'original_price', 'duration',
            'badge_text', 'is_popular', 'is_active', 'image',
            'short_description', 'included_features', 'bonus_perks'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'Package name (e.g. Royal Bridal Package)'}),
            'price': forms.NumberInput(attrs={'class': 'portal-input', 'placeholder': 'Package price in BDT (৳)'}),
            'original_price': forms.NumberInput(attrs={'class': 'portal-input', 'placeholder': 'Original / Regular price (optional)'}),
            'duration': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'Duration (e.g. 3-4 Hours)'}),
            'badge_text': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'Badge text (e.g. Most Popular)'}),
            'short_description': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'One-line engaging summary'}),
            'included_features': forms.Textarea(attrs={'class': 'portal-input', 'rows': 4, 'placeholder': 'Included features (one per line)'}),
            'bonus_perks': forms.Textarea(attrs={'class': 'portal-input', 'rows': 2, 'placeholder': 'Bonus perks / complimentary items (optional)'}),
            'is_popular': forms.CheckboxInput(attrs={'class': 'portal-checkbox'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'portal-checkbox'}),
        }


class PortalGalleryForm(forms.ModelForm):
    image = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'Or online image URL (https://...)'})
    )
    image_file = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'portal-input', 'accept': 'image/*'})
    )

    class Meta:
        model = GalleryItem
        fields = ['title', 'category', 'image', 'caption', 'artist_tag', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'Photo title (e.g. Royal Bridal HD Makeup)'}),
            'category': forms.Select(attrs={'class': 'portal-input'}),
            'caption': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'Short caption (optional)'}),
            'artist_tag': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'Artist name (e.g. Nishi Makeup Artist)'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'portal-checkbox'}),
        }


class PortalProfileForm(forms.ModelForm):
    facebook_url = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'https://facebook.com/...'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'portal-input', 'placeholder': 'e.g. nishimakeup@gmail.com'})
    )

    class Meta:
        model = SalonProfile
        fields = [
            'name', 'tagline', 'phone',
            'whatsapp_number', 'facebook_url', 'address',
            'business_hours', 'email', 'about_story'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'Studio name'}),
            'tagline': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'Studio tagline'}),
            'phone': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': '+880 1904-423317'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': '8801904423317'}),
            'address': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'Studio & venue service address'}),
            'business_hours': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'e.g. Every day: 10:00 AM - 08:30 PM'}),
            'about_story': forms.Textarea(attrs={'class': 'portal-input', 'rows': 3, 'placeholder': 'About your salon history, vision, and passion...'}),
        }

    def clean_facebook_url(self):
        url = self.cleaned_data.get('facebook_url', '').strip()
        if url and not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url

