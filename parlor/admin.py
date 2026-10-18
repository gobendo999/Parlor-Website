from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SalonProfile,
    Artist,
    ServiceCategory,
    Service,
    Package,
    Appointment,
    GalleryItem,
    Testimonial,
    ContactInquiry,
)


@admin.register(SalonProfile)
class SalonProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'business_hours', 'address')
    fieldsets = (
        ('Branding & Titles', {
            'fields': ('name', 'tagline', 'sub_tagline')
        }),
        ('Contact Coordinates', {
            'fields': ('phone', 'phone_clean', 'whatsapp_number', 'facebook_url', 'email', 'address', 'business_hours')
        }),
        ('Brand Narrative', {
            'fields': ('about_story', 'philosophy')
        }),
    )

    def has_add_permission(self, request):
        # Only allow 1 salon profile instance
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'experience_years', 'rating', 'completed_brides', 'is_available', 'is_featured', 'order')
    list_editable = ('is_available', 'is_featured', 'order')
    list_filter = ('is_available', 'is_featured')
    search_fields = ('name', 'title', 'specialties', 'bio')


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'starting_price', 'duration', 'is_active', 'is_featured', 'order')
    list_editable = ('starting_price', 'is_active', 'is_featured', 'order')
    list_filter = ('category', 'is_active', 'is_featured')
    search_fields = ('name', 'short_description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'original_price', 'duration', 'badge_text', 'is_popular', 'is_active', 'order')
    list_editable = ('price', 'badge_text', 'is_popular', 'is_active', 'order')
    list_filter = ('is_popular', 'is_active')
    search_fields = ('name', 'short_description', 'included_features')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'booking_reference',
        'customer_name',
        'phone_number',
        'event_type',
        'appointment_date',
        'preferred_time',
        'package',
        'service',
        'preferred_artist',
        'status_badge',
        'estimated_amount',
        'created_at',
    )
    list_filter = ('status', 'event_type', 'appointment_date', 'preferred_artist')
    search_fields = ('booking_reference', 'customer_name', 'phone_number', 'customer_address')
    readonly_fields = ('booking_reference', 'created_at', 'updated_at')
    list_per_page = 25
    actions = ['mark_as_confirmed', 'mark_as_completed', 'mark_as_cancelled']

    def status_badge(self, obj):
        colors = {
            'pending': '#d97706',    # Warm Amber
            'confirmed': '#059669',  # Emerald Green
            'completed': '#2563eb',  # Royal Blue
            'cancelled': '#dc2626',  # Crimson Red
        }
        color = colors.get(obj.status, '#4b5563')
        return format_html(
            '<span style="background-color: {}; color: #fff; padding: 4px 10px; border-radius: 9999px; font-weight: 600; font-size: 0.78rem;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = "Status"

    @admin.action(description="Mark selected appointments as Confirmed")
    def mark_as_confirmed(self, request, queryset):
        count = queryset.update(status='confirmed')
        self.message_user(request, f"{count} appointment(s) successfully marked as Confirmed.")

    @admin.action(description="Mark selected appointments as Completed")
    def mark_as_completed(self, request, queryset):
        count = queryset.update(status='completed')
        self.message_user(request, f"{count} appointment(s) marked as Completed.")

    @admin.action(description="Mark selected appointments as Cancelled")
    def mark_as_cancelled(self, request, queryset):
        count = queryset.update(status='cancelled')
        self.message_user(request, f"{count} appointment(s) marked as Cancelled.")


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'artist_tag', 'is_featured', 'created_at')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'caption')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'service_received', 'rating', 'event_date', 'is_verified', 'is_featured')
    list_filter = ('rating', 'is_verified', 'is_featured')
    search_fields = ('customer_name', 'service_received', 'feedback')


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'subject', 'created_at', 'is_resolved')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('name', 'phone', 'message')
    list_editable = ('is_resolved',)
