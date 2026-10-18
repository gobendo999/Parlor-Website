import re
from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from .models import (
    Appointment, ContactInquiry, Artist, Service, Package,
    SalonProfile, GalleryItem, ServiceCategory
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
                'placeholder': 'Enter your full name (e.g. Nusrat Jahan)',
                'required': True,
                'autocomplete': 'name',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 01904423317 or +880 1904-423317',
                'required': True,
                'autocomplete': 'tel',
            }),
            'customer_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Enter your address or write "Studio Visit" (Dhanmondi, Dhaka)',
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
        # Remove common separators like spaces, hyphens, brackets
        cleaned_digits = re.sub(r'[\s\-\(\)\.]', '', raw_phone)
        
        # Check standard BD formats: 01XXXXXXXXX (11 digits) or +8801XXXXXXXXX (14 digits) or 8801XXXXXXXXX (13 digits)
        bd_match = re.search(r'^(?:\+?880|0)?1[3-9]\d{8}$', cleaned_digits)
        if not bd_match and len(re.sub(r'\D', '', cleaned_digits)) < 10:
            raise ValidationError(
                'Please enter a valid phone number (e.g., 01904-423317 or +8801904423317).'
            )
        return raw_phone

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
            'placeholder': 'ইউজারনেম লিখুন (e.g. admin)',
            'autocomplete': 'username',
            'required': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'portal-input',
            'placeholder': 'পাসওয়ার্ড লিখুন',
            'autocomplete': 'current-password',
            'required': True,
        })
    )


class PortalServiceForm(forms.ModelForm):
    image = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'অথবা ছবির অনলাইন লিঙ্ক (Image URL)'})
    )
    image_file = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'portal-input', 'accept': 'image/*'})
    )
    short_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'portal-input', 'rows': 2, 'placeholder': 'সংক্ষিপ্ত বিবরণ (ঐচ্ছিক)'})
    )

    class Meta:
        model = Service
        fields = [
            'category', 'name', 'starting_price', 'duration',
            'image', 'short_description', 'is_featured', 'is_active'
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'portal-input'}),
            'name': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'সার্ভিসের নাম'}),
            'starting_price': forms.NumberInput(attrs={'class': 'portal-input', 'placeholder': 'মূল্য (টাকা)'}),
            'duration': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'সময় (e.g. 45 Mins)'}),
            'short_description': forms.Textarea(attrs={'class': 'portal-input', 'rows': 2, 'placeholder': 'সংক্ষিপ্ত বিবরণ'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'portal-checkbox'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'portal-checkbox'}),
        }


class PortalPackageForm(forms.ModelForm):
    image = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'অথবা ছবির অনলাইন লিঙ্ক (Image URL)'})
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
            'name': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'প্যাকেজের নাম'}),
            'price': forms.NumberInput(attrs={'class': 'portal-input', 'placeholder': 'বর্তমান মূল্য (টাকা)'}),
            'original_price': forms.NumberInput(attrs={'class': 'portal-input', 'placeholder': 'আগের মূল্য (ঐচ্ছিক)'}),
            'duration': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'সময় (e.g. 3-4 Hours)'}),
            'badge_text': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'ব্যাজ (e.g. Most Popular)'}),
            'short_description': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'এক লাইনে বিবরণ'}),
            'included_features': forms.Textarea(attrs={'class': 'portal-input', 'rows': 4, 'placeholder': 'প্রতি লাইনে একটি করে সুবিধা লিখুন'}),
            'bonus_perks': forms.Textarea(attrs={'class': 'portal-input', 'rows': 2, 'placeholder': 'বোনাস সুবিধা (ঐচ্ছিক)'}),
            'is_popular': forms.CheckboxInput(attrs={'class': 'portal-checkbox'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'portal-checkbox'}),
        }


class PortalGalleryForm(forms.ModelForm):
    image = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'অথবা ছবির অনলাইন লিঙ্ক (Image URL)'})
    )
    image_file = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'portal-input', 'accept': 'image/*'})
    )

    class Meta:
        model = GalleryItem
        fields = ['title', 'category', 'image', 'caption', 'artist_tag', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'ছবির শিরোনাম'}),
            'category': forms.Select(attrs={'class': 'portal-input'}),
            'caption': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'ক্যাপশন'}),
            'artist_tag': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': 'আর্টিস্ট নাম'}),
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
            'name': forms.TextInput(attrs={'class': 'portal-input'}),
            'tagline': forms.TextInput(attrs={'class': 'portal-input'}),
            'phone': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': '+880 1904-423317'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'portal-input', 'placeholder': '8801904423317'}),
            'address': forms.TextInput(attrs={'class': 'portal-input'}),
            'business_hours': forms.TextInput(attrs={'class': 'portal-input'}),
            'about_story': forms.Textarea(attrs={'class': 'portal-input', 'rows': 3}),
        }

    def clean_facebook_url(self):
        url = self.cleaned_data.get('facebook_url', '').strip()
        if url and not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url

