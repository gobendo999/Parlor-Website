import uuid
import re
from django.db import models
from django.utils import timezone


class SalonProfile(models.Model):
    name = models.CharField(max_length=200, default="Nishi Makeup Artist & Beauty Parlour")
    tagline = models.CharField(max_length=255, default="Your Beauty, Our Priority")
    sub_tagline = models.CharField(max_length=255, default="Makeup + Hair + Beauty • Enhance Your Natural Beauty")
    phone = models.CharField(max_length=50, default="+880 1904-423317")
    phone_clean = models.CharField(max_length=50, default="+8801904423317")
    facebook_url = models.URLField(default="https://www.facebook.com/profile.php?id=61595083298208")
    whatsapp_number = models.CharField(max_length=50, default="8801904423317")
    address = models.CharField(max_length=300, default="Studio & Home/Venue Service, Dhaka, Bangladesh")
    business_hours = models.CharField(max_length=200, default="Every day: 10:00 AM - 08:30 PM (Appointment Based)")
    email = models.EmailField(blank=True, default="nishimakeupartist@gmail.com")
    about_story = models.TextField(
        default="Welcome to Nishi Makeup Artist & Beauty Parlour. Founded by passionate beauty creator Nishi, our studio is dedicated to celebrating the authentic radiance of every woman. With an eye for high-fashion aesthetics, delicate symmetry, and long-lasting luxury finishes, we craft unforgettable looks tailored exclusively to your personality. We believe that makeup is not just a cosmetic layer—it is an art of empowerment, confidence, and emotion."
    )
    philosophy = models.TextField(
        default="Because every bride deserves to feel beautiful. We pair world-class luxury international makeup cosmetics with state-of-the-art parlour treatments, unmatched hygiene standards, and bespoke consultations to make your special moments truly timeless."
    )

    class Meta:
        verbose_name = "Salon Profile & Settings"
        verbose_name_plural = "Salon Profile & Settings"

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=150, help_text="e.g. Lead Bridal Stylist & Creative Director")
    experience_years = models.PositiveIntegerField(default=5)
    specialties = models.CharField(max_length=255, help_text="Comma-separated e.g. Royal Bridal, 4K Airbrush, Bengali Traditional")
    bio = models.TextField()
    photo = models.CharField(max_length=500, help_text="URL or static path to artist image")
    portfolio_previews = models.TextField(
        blank=True, 
        help_text="Comma or newline separated image URLs for portfolio preview modal"
    )
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.9)
    completed_brides = models.PositiveIntegerField(default=350)
    is_featured = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} - {self.title}"

    @property
    def specialty_list(self):
        return [s.strip() for s in self.specialties.split(',') if s.strip()]

    @property
    def preview_images(self):
        if not self.portfolio_previews:
            return []
        return [img.strip() for img in self.portfolio_previews.replace('\n', ',').split(',') if img.strip()]


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True)
    icon = models.CharField(max_length=50, default="sparkles", help_text="Icon identifier e.g. sparkles, brush, hair, skin, nail")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Service Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    short_description = models.TextField(help_text="Short engaging summary of the service")
    full_description = models.TextField(blank=True, help_text="Detailed description of the procedure and benefits")
    starting_price = models.DecimalField(max_digits=10, decimal_places=0, help_text="Price in BDT (৳)")
    duration = models.CharField(max_length=100, help_text="e.g. 90 mins, 2-3 hours")
    image = models.CharField(max_length=500, help_text="URL or static path to service image")
    is_featured = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} (৳{self.starting_price})"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('parlor:service_detail', kwargs={'slug': self.slug})


class Package(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    badge_text = models.CharField(max_length=50, blank=True, help_text="e.g. 'Most Popular' or 'Best Seller' or 'Luxury Choice'")
    is_popular = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=0, help_text="Current price in BDT (৳)")
    original_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, help_text="Original crossed-out price for discount")
    short_description = models.CharField(max_length=255, help_text="One line value proposition")
    duration = models.CharField(max_length=100, default="2-3 Hours")
    included_features = models.TextField(help_text="One feature per line")
    bonus_perks = models.TextField(blank=True, help_text="Special bonus perks or touchup kits")
    image = models.CharField(max_length=500, blank=True, help_text="Hero image for this package")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'price']

    def __str__(self):
        return f"{self.name} - ৳{self.price}"

    @property
    def feature_list(self):
        return [f.strip() for f in self.included_features.split('\n') if f.strip()]

    @property
    def bonus_list(self):
        if not self.bonus_perks:
            return []
        return [b.strip() for b in self.bonus_perks.split('\n') if b.strip()]

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('parlor:package_detail', kwargs={'slug': self.slug})


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Request'),
        ('confirmed', 'Confirmed Appointment'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    EVENT_CHOICES = (
        ('Bridal', 'Wedding / Bridal Ceremony'),
        ('Reception', 'Wedding Reception (Bou-Bhat)'),
        ('Engagement', 'Engagement / Ring Ceremony'),
        ('Haldi_Mehendi', 'Gaye Holud & Mehendi Night'),
        ('Party', 'Party & Evening Glamour'),
        ('Birthday', 'Birthday / Anniversary Event'),
        ('Photoshoot', 'Model / Portfolio Photoshoot'),
        ('Parlour_Treatment', 'Parlour Skincare & Hair Spa Ritual'),
        ('Other', 'Other Special Occasion'),
    )

    TIME_CHOICES = (
        ('09:00 AM', '09:00 AM - Morning Slot'),
        ('11:00 AM', '11:00 AM - Mid-Day Slot'),
        ('01:30 PM', '01:30 PM - Early Afternoon Slot'),
        ('03:30 PM', '03:30 PM - Afternoon Slot'),
        ('05:30 PM', '05:30 PM - Evening Golden Hour Slot'),
        ('07:00 PM', '07:00 PM - Night Prime Slot'),
    )

    booking_reference = models.CharField(max_length=30, unique=True, editable=False)
    customer_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=30)
    customer_address = models.TextField(help_text="Home/Venue address or 'Studio Visit'")
    preferred_artist = models.ForeignKey(Artist, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    appointment_date = models.DateField()
    preferred_time = models.CharField(max_length=50, choices=TIME_CHOICES, default='03:30 PM')
    event_type = models.CharField(max_length=50, choices=EVENT_CHOICES, default='Bridal')
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    estimated_amount = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    admin_notes = models.TextField(blank=True, help_text="Internal notes by salon management")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            # Generate unique reference code like NB-2026-A1B2
            unique_part = uuid.uuid4().hex[:6].upper()
            year = timezone.now().year
            self.booking_reference = f"NB-{year}-{unique_part}"
        if not self.estimated_amount:
            if self.package:
                self.estimated_amount = self.package.price
            elif self.service:
                self.estimated_amount = self.service.starting_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_reference} - {self.customer_name} ({self.get_status_display()})"

    @property
    def clean_whatsapp_number(self):
        """Standardize phone number for WhatsApp international routing (880XXXXXXXXXX)."""
        raw = re.sub(r'\D', '', self.phone_number or '')
        if raw.startswith('880'):
            return raw
        elif raw.startswith('0'):
            return '88' + raw
        elif len(raw) == 10 and raw.startswith('1'):
            return '880' + raw
        return raw

    def get_whatsapp_confirmation_text(self, request=None):
        """Format the exact WhatsApp confirmation text with booking reference and status tracking URL."""
        if request:
            base_url = request.build_absolute_uri('/')[:-1]
        else:
            base_url = "https://parlor-website.onrender.com"
        track_url = f"{base_url}/track-booking/?q={self.booking_reference}"

        if self.package:
            item_name = f"প্যাকেজ: {self.package.name}"
        elif self.service:
            item_name = f"সার্ভিস: {self.service.name}"
        else:
            item_name = "কাস্টম পার্লার / মেকআপ সার্ভিস"

        msg = (
            f"🌸 *Nishi Makeup Artist & Beauty Parlour* 🌸\n\n"
            f"প্রিয় {self.customer_name},\n"
            f"আপনার পার্লার বুকিং রিকোয়েস্টটি সফলভাবে গ্রহণ করা হয়েছে! ✨\n\n"
            f"📋 *বুকিং বিবরণী:*\n"
            f"• বুকিং রেফারেন্স নম্বর: *{self.booking_reference}*\n"
            f"• সিলেক্টেড সার্ভিস/প্যাকেজ: {item_name}\n"
            f"• তারিখ: {self.appointment_date}\n"
            f"• সময় স্লট: {self.preferred_time}\n"
            f"• আনুমানিক বিল: ৳{int(self.estimated_amount)}\n"
            f"• বর্তমান স্ট্যাটাস: অপেক্ষমাণ ({self.get_status_display()})\n\n"
            f"🔍 *বুকিং স্ট্যাটাস চেক করতে:*\n"
            f"আপনার বুকিং সংক্রান্ত যেকোনো আপডেট বা স্ট্যাটাস চেক করার জন্য এই রেফারেন্স নম্বরটি (*{self.booking_reference}*) দিয়ে নিচের লিংকে ট্র্যাক করতে পারবেন:\n"
            f"👉 {track_url}\n\n"
            f"আমাদের স্টুডিও প্রতিনিধি খুব দ্রুত আপনার সাথে যোগাযোগ করে শিডিউল কনফার্ম করবেন।\n"
            f"📞 হটলাইন: +880 1904-423317\n"
            f"ধন্যবাদ! 💖"
        )
        return msg

    def get_whatsapp_url(self, request=None):
        from urllib.parse import quote
        phone = self.clean_whatsapp_number
        text = self.get_whatsapp_confirmation_text(request)
        return f"https://api.whatsapp.com/send?phone={phone}&text={quote(text)}"


class GalleryItem(models.Model):
    CATEGORY_CHOICES = (
        ('bridal', 'Bridal Transformations'),
        ('reception', 'Reception & Bou-Bhat'),
        ('engagement', 'Engagement & Ring Ceremony'),
        ('party', 'Party & Glamour Looks'),
        ('haldi', 'Haldi & Mehendi Vibes'),
        ('natural', 'Natural & Dewy HD Glass Skin'),
        ('hair', 'Hairstyling & Saree Draping'),
    )

    title = models.CharField(max_length=150)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='bridal')
    image = models.CharField(max_length=500, help_text="Image URL or static path")
    caption = models.CharField(max_length=255, blank=True)
    artist_tag = models.CharField(max_length=100, default="Nishi Makeup Artist")
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"


class Testimonial(models.Model):
    customer_name = models.CharField(max_length=150)
    customer_photo = models.CharField(max_length=500, blank=True)
    service_received = models.CharField(max_length=150, help_text="e.g. Royal Bridal HD Makeup")
    rating = models.PositiveSmallIntegerField(default=5)
    feedback = models.TextField()
    event_date = models.CharField(max_length=50, default="Recent Client")
    is_verified = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.customer_name} ({self.rating}★ - {self.service_received})"

    @property
    def stars(self):
        return range(self.rating)


class ContactInquiry(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    subject = models.CharField(max_length=200, default="Appointment & Service Inquiry")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Inquiry from {self.name} - {self.phone}"
