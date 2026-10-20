import os
import re
import json
import uuid
from urllib.parse import urlparse, parse_qs, unquote
from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Sum
from django.utils import timezone
from django.utils.text import slugify
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
from .notifications import send_whatsapp_notification
from .forms import (
    AppointmentBookingForm,
    ContactInquiryForm,
    BookingTrackForm,
    PortalLoginForm,
    PortalServiceForm,
    PortalPackageForm,
    PortalGalleryForm,
    PortalProfileForm,
)


def index(request):
    """Main luxurious homepage with all interconnected sections."""
    profile = SalonProfile.objects.first()
    artists = Artist.objects.filter(is_available=True)
    categories = ServiceCategory.objects.prefetch_related('services').all()
    services = Service.objects.filter(is_active=True)
    packages = Package.objects.filter(is_active=True)
    gallery_items = GalleryItem.objects.all()
    testimonials = Testimonial.objects.filter(is_featured=True)

    # Initial prefilled values from query params (e.g. ?service=1&package=2)
    initial_data = {}
    if request.GET.get('service'):
        initial_data['service'] = request.GET.get('service')
    if request.GET.get('package'):
        initial_data['package'] = request.GET.get('package')

    booking_form = AppointmentBookingForm(initial=initial_data)
    contact_form = ContactInquiryForm()

    if request.method == 'POST' and 'submit_booking' in request.POST:
        booking_form = AppointmentBookingForm(request.POST)
        if booking_form.is_valid():
            appointment = booking_form.save()
            try:
                send_whatsapp_notification(appointment, request)
            except Exception:
                pass
            messages.success(
                request,
                f"Your appointment request has been submitted successfully! Your booking reference is {appointment.booking_reference}."
            )
            return redirect('parlor:booking_confirmation', reference=appointment.booking_reference)
        else:
            messages.error(request, "Please correct the highlighted errors in the booking form.")

    context = {
        'profile': profile,
        'artists': artists,
        'categories': categories,
        'services': services,
        'packages': packages,
        'gallery_items': gallery_items,
        'testimonials': testimonials,
        'booking_form': booking_form,
        'contact_form': contact_form,
        'active_page': 'home',
    }
    return render(request, 'parlor/index.html', context)


def about_view(request):
    """Dedicated About Us page."""
    profile = SalonProfile.objects.first()
    testimonials = Testimonial.objects.all()[:4]
    return render(request, 'parlor/about.html', {
        'profile': profile,
        'testimonials': testimonials,
        'active_page': 'about',
    })


def artists_view(request):
    """Redirect to about page as no extra artists are showcased."""
    return redirect('parlor:about')


def services_view(request):
    """Dedicated Services & Parlour Rituals page."""
    categories = ServiceCategory.objects.prefetch_related('services').all()
    services = Service.objects.filter(is_active=True)
    return render(request, 'parlor/services.html', {
        'categories': categories,
        'services': services,
        'active_page': 'services',
    })


def service_detail(request, slug):
    """Dedicated luxury showcase page for an individual parlour service."""
    service = get_object_or_404(Service, slug=slug, is_active=True)
    related_services = Service.objects.filter(
        category=service.category,
        is_active=True
    ).exclude(id=service.id)[:4]

    if related_services.count() < 3:
        extra = Service.objects.filter(is_active=True).exclude(id=service.id).exclude(id__in=[s.id for s in related_services])[:4 - related_services.count()]
        related_services = list(related_services) + list(extra)

    return render(request, 'parlor/service_detail.html', {
        'service': service,
        'related_services': related_services,
        'active_page': 'services',
    })


def packages_view(request):
    """Dedicated Packages & Pricing page."""
    packages = Package.objects.filter(is_active=True)
    return render(request, 'parlor/packages.html', {
        'packages': packages,
        'active_page': 'packages',
    })


def package_detail(request, slug):
    """Dedicated luxury showcase page for a makeup package."""
    package = get_object_or_404(Package, slug=slug, is_active=True)
    other_packages = Package.objects.filter(is_active=True).exclude(id=package.id)[:3]

    return render(request, 'parlor/package_detail.html', {
        'package': package,
        'other_packages': other_packages,
        'active_page': 'packages',
    })


def gallery_view(request):
    """Dedicated Transformation & Portfolio Gallery page."""
    gallery_items = GalleryItem.objects.all()
    categories = [
        ('all', 'All Looks'),
        ('bridal', 'Bridal Transformations'),
        ('reception', 'Reception & Bou-Bhat'),
        ('engagement', 'Engagement'),
        ('party', 'Party & Glamour'),
        ('haldi', 'Haldi & Mehendi'),
        ('natural', 'Natural & Glass Skin'),
        ('hair', 'Hair & Saree Draping'),
    ]
    return render(request, 'parlor/gallery.html', {
        'gallery_items': gallery_items,
        'categories': categories,
        'active_page': 'gallery',
    })


def book_appointment(request):
    """Dedicated Booking page with interactive calculations."""
    initial_data = {}
    preselected_item = None
    item_type = None

    if request.GET.get('service'):
        srv_id = request.GET.get('service')
        initial_data['service'] = srv_id
        try:
            preselected_item = Service.objects.get(id=srv_id, is_active=True)
            item_type = 'service'
        except (Service.DoesNotExist, ValueError):
            pass

    if request.GET.get('package'):
        pkg_id = request.GET.get('package')
        initial_data['package'] = pkg_id
        try:
            preselected_item = Package.objects.get(id=pkg_id, is_active=True)
            item_type = 'package'
        except (Package.DoesNotExist, ValueError):
            pass

    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            try:
                send_whatsapp_notification(appointment, request)
            except Exception:
                pass
            messages.success(
                request,
                f"Booking submitted successfully! Reference: {appointment.booking_reference}"
            )
            return redirect('parlor:booking_confirmation', reference=appointment.booking_reference)
        else:
            messages.error(request, "Please resolve the form errors below.")
    else:
        form = AppointmentBookingForm(initial=initial_data)

    artists = Artist.objects.filter(is_available=True)
    packages = Package.objects.filter(is_active=True)
    services = Service.objects.filter(is_active=True)

    # Package details map for JS live preview
    packages_json = {
        p.id: {
            'name': p.name,
            'price': int(p.price),
            'features': p.feature_list,
            'duration': p.duration,
            'badge': p.badge_text,
        }
        for p in packages
    }

    services_json = {
        s.id: {
            'name': s.name,
            'price': int(s.starting_price),
            'duration': s.duration,
        }
        for s in services
    }

    return render(request, 'parlor/booking.html', {
        'form': form,
        'artists': artists,
        'packages': packages,
        'services': services,
        'preselected_item': preselected_item,
        'item_type': item_type,
        'packages_json': json.dumps(packages_json),
        'services_json': json.dumps(services_json),
        'active_page': 'booking',
    })


def booking_confirmation(request, reference):
    """Confirmation page with complete booking breakdown, reference code, and status."""
    appointment = get_object_or_404(Appointment, booking_reference=reference)
    track_url = request.build_absolute_uri(f"/track-booking/?q={appointment.booking_reference}")
    whatsapp_url = appointment.get_whatsapp_url(request)
    whatsapp_text = appointment.get_whatsapp_confirmation_text(request)

    return render(request, 'parlor/booking_confirmation.html', {
        'appointment': appointment,
        'track_url': track_url,
        'whatsapp_url': whatsapp_url,
        'whatsapp_text': whatsapp_text,
        'active_page': 'booking',
    })


def track_booking(request):
    """Customer self-service tracker by Reference Code or Phone Number."""
    query = request.GET.get('q', '').strip()
    results = None
    searched = False

    if query:
        searched = True
        # Match either exact reference or phone number containing query
        results = Appointment.objects.filter(
            Q(booking_reference__iexact=query) |
            Q(phone_number__icontains=query)
        )

    form = BookingTrackForm(initial={'search_query': query})
    return render(request, 'parlor/track_booking.html', {
        'form': form,
        'query': query,
        'results': results,
        'searched': searched,
        'active_page': 'track',
    })


@require_POST
def contact_submit(request):
    """Handle contact us form submissions."""
    form = ContactInquiryForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Thank you! Your message has been received. Our team will get in touch shortly.")
    else:
        messages.error(request, "Please enter valid contact details.")
    
    # Redirect back to where the user came from
    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)


def admin_dashboard(request):
    """Redirect legacy admin_dashboard to the new custom portal."""
    return redirect('parlor:portal_dashboard')


@require_POST
def update_appointment_status(request, pk):
    """Legacy redirect."""
    return redirect('parlor:portal_dashboard')


def staff_required_portal(view_func):
    """Decorator to restrict access only to staff / superusers and redirect to custom login."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('parlor:portal_login')
        if not request.user.is_staff:
            messages.error(request, "আপনার এই পোর্টালে প্রবেশের অনুমতি নেই।")
            return redirect('parlor:portal_login')
        return view_func(request, *args, **kwargs)
    return wrapper


def portal_login(request):
    """Feminine luxury login screen for the salon owner."""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('parlor:portal_dashboard')

    if request.method == 'POST':
        form = PortalLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                name_display = user.first_name if user.first_name else "নিশি আপু"
                messages.success(request, f"🌸 স্বাগতম, {name_display}! আপনার বিউটি পার্লার কন্ট্রোল প্যানেলে স্বাগতম।")
                return redirect('parlor:portal_dashboard')
            else:
                messages.error(request, "ভুল ইউজারনেম অথবা পাসওয়ার্ড। অনুগ্রহ করে সঠিক তথ্য দিন।")
    else:
        form = PortalLoginForm()

    profile = SalonProfile.objects.first()
    return render(request, 'parlor/portal_login.html', {
        'form': form,
        'profile': profile,
    })


def portal_logout(request):
    """Logout action redirecting to portal login."""
    logout(request)
    messages.info(request, "🌸 আপনি সফলভাবে লগআউট হয়েছেন। ভালো থাকবেন!")
    return redirect('parlor:portal_login')


@staff_required_portal
def portal_dashboard(request):
    """
    Ultra-aesthetic, feminine custom CMS dashboard for salon owner.
    Features:
    - Overview KPIs & Quick Actions
    - Appointments Management with WhatsApp/Call integration
    - Service price & active status editor
    - Package price & details editor
    - Gallery photo manager
    - Salon contact & information settings
    """
    today = timezone.localdate()
    status_filter = request.GET.get('status', 'all')
    active_tab = request.GET.get('tab', 'overview')
    search_q = request.GET.get('q', '').strip()

    # Base query
    appointments = Appointment.objects.all().select_related('service', 'package')
    if status_filter != 'all':
        appointments = appointments.filter(status=status_filter)
    if search_q:
        appointments = appointments.filter(
            Q(booking_reference__icontains=search_q) |
            Q(customer_name__icontains=search_q) |
            Q(phone_number__icontains=search_q)
        )

    # Key Performance Indicators
    total_count = Appointment.objects.count()
    pending_count = Appointment.objects.filter(status='pending').count()
    confirmed_count = Appointment.objects.filter(status='confirmed').count()
    completed_count = Appointment.objects.filter(status='completed').count()
    cancelled_count = Appointment.objects.filter(status='cancelled').count()
    today_count = Appointment.objects.filter(appointment_date=today).count()
    
    total_revenue = Appointment.objects.filter(
        status__in=['confirmed', 'completed']
    ).aggregate(total=Sum('estimated_amount'))['total'] or 0

    # Content Collections
    categories = ServiceCategory.objects.prefetch_related('services').all()
    services = Service.objects.select_related('category').order_by('category__order', 'order', 'name')
    packages = Package.objects.all().order_by('order', 'price')
    gallery_items = GalleryItem.objects.all().order_by('-id')
    recent_inquiries = ContactInquiry.objects.order_by('-created_at')[:10]
    profile = SalonProfile.objects.first()

    # Forms for adding/editing
    service_form = PortalServiceForm()
    package_form = PortalPackageForm()
    gallery_form = PortalGalleryForm()
    profile_form = PortalProfileForm(instance=profile)

    context = {
        'today': today,
        'active_tab': active_tab,
        'status_filter': status_filter,
        'search_q': search_q,
        'appointments': appointments,
        'total_count': total_count,
        'pending_count': pending_count,
        'confirmed_count': confirmed_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
        'today_count': today_count,
        'total_revenue': total_revenue,
        'categories': categories,
        'services': services,
        'packages': packages,
        'gallery_items': gallery_items,
        'recent_inquiries': recent_inquiries,
        'profile': profile,
        'service_form': service_form,
        'package_form': package_form,
        'gallery_form': gallery_form,
        'profile_form': profile_form,
    }
    return render(request, 'parlor/portal_dashboard.html', context)


@require_POST
@staff_required_portal
def portal_appointment_status(request, pk):
    """Change status and save admin notes for an appointment."""
    appointment = get_object_or_404(Appointment, pk=pk)
    new_status = request.POST.get('status')
    if new_status in ['pending', 'confirmed', 'completed', 'cancelled']:
        appointment.status = new_status
        admin_notes = request.POST.get('admin_notes', '').strip()
        if admin_notes:
            appointment.admin_notes = admin_notes
        appointment.save()
        status_bn = {
            'pending': 'অপেক্ষমাণ (Pending)',
            'confirmed': 'নিশ্চিত (Confirmed)',
            'completed': 'সম্পন্ন (Completed)',
            'cancelled': 'বাতিল (Cancelled)',
        }.get(new_status, new_status)
        messages.success(request, f"বুকিং #{appointment.booking_reference} স্ট্যাটাস '{status_bn}' হিসেবে সংরক্ষিত হয়েছে।")
    return redirect('/nishi-portal/?tab=appointments')


@require_POST
def process_image_upload(request, existing_image=None):
    """
    Intelligently handles image inputs:
    1. If user uploaded a file from PC/phone, save it safely to MEDIA_ROOT/uploads/ and return /media/uploads/...
    2. If user pasted a Google Images redirect URL, extract the direct target image URL.
    3. If user pasted a direct URL, trim and return it.
    4. If none provided, keep existing image or provide high-res fallback.
    """
    if 'image_file' in request.FILES and request.FILES['image_file']:
        uploaded = request.FILES['image_file']
        ext = os.path.splitext(uploaded.name)[1].lower() or '.jpg'
        safe_name = f"uploads/{uuid.uuid4().hex[:12]}{ext}"
        saved_path = default_storage.save(safe_name, uploaded)
        return settings.MEDIA_URL + saved_path

    raw_url = request.POST.get('image', '').strip()
    if raw_url:
        # Resolve Google Images redirect URL if user pasted from Google Search
        if 'google.' in raw_url and 'imgurl=' in raw_url:
            parsed = urlparse(raw_url)
            qs = parse_qs(parsed.query)
            if 'imgurl' in qs:
                return qs['imgurl'][0]
        return raw_url

    return existing_image or '/static/images/hero-bride.jpg'


@require_POST
@staff_required_portal
def portal_service_save(request):
    """Add or update a service with file upload or URL."""
    service_id = request.POST.get('service_id')
    existing_img = None
    if service_id:
        service = get_object_or_404(Service, pk=service_id)
        existing_img = service.image
        form = PortalServiceForm(request.POST, request.FILES, instance=service)
        action_msg = "আপডেট"
    else:
        form = PortalServiceForm(request.POST, request.FILES)
        action_msg = "যোগ"

    if form.is_valid():
        service = form.save(commit=False)
        resolved_img = process_image_upload(request, existing_img)
        if resolved_img:
            service.image = resolved_img
        if not service.slug:
            base_slug = slugify(service.name) or "service"
            service.slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
        service.save()
        messages.success(request, f"সার্ভিস '{service.name}' সফলভাবে {action_msg} করা হয়েছে! 💖")
    else:
        messages.error(request, "সার্ভিস তথ্যে সমস্যা রয়েছে। অনুগ্রহ করে সঠিক ইনপুট দিন।")
    
    return redirect('/nishi-portal/?tab=services')


@require_POST
@staff_required_portal
def portal_service_toggle(request, pk):
    """1-click toggle for service availability (is_active)."""
    service = get_object_or_404(Service, pk=pk)
    service.is_active = not service.is_active
    service.save()
    state = "সক্রিয় (Active)" if service.is_active else "লুকানো/নিষ্ক্রিয় (Inactive)"
    messages.success(request, f"'{service.name}' এখন {state} করা হয়েছে।")
    return redirect('/nishi-portal/?tab=services')


@require_POST
@staff_required_portal
def portal_package_save(request):
    """Add or update package pricing and features with file upload or URL."""
    package_id = request.POST.get('package_id')
    existing_img = None
    if package_id:
        package = get_object_or_404(Package, pk=package_id)
        existing_img = package.image
        form = PortalPackageForm(request.POST, request.FILES, instance=package)
        action_msg = "আপডেট"
    else:
        form = PortalPackageForm(request.POST, request.FILES)
        action_msg = "তৈরি"

    if form.is_valid():
        pkg = form.save(commit=False)
        resolved_img = process_image_upload(request, existing_img)
        if resolved_img:
            pkg.image = resolved_img
        if not pkg.slug:
            base_slug = slugify(pkg.name) or "package"
            pkg.slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
        pkg.save()
        messages.success(request, f"প্যাকেজ '{pkg.name}' সফলভাবে {action_msg} করা হয়েছে! ✨")
    else:
        messages.error(request, "প্যাকেজ ফর্মে ভুল রয়েছে। অনুগ্রহ করে চেক করুন।")
    
    return redirect('/nishi-portal/?tab=packages')


@require_POST
@staff_required_portal
def portal_gallery_save(request):
    """Add a new gallery photo to portfolio with file upload or URL."""
    form = PortalGalleryForm(request.POST, request.FILES)
    if form.is_valid():
        item = form.save(commit=False)
        resolved_img = process_image_upload(request)
        if resolved_img:
            item.image = resolved_img
        item.save()
        messages.success(request, f"নতুন ছবি '{item.title}' সফলভাবে গ্যালারিতে যোগ হয়েছে! 📸")
    else:
        messages.error(request, "ছবির লিঙ্ক বা তথ্যে সমস্যা রয়েছে।")
    return redirect('/nishi-portal/?tab=gallery')


@require_POST
@staff_required_portal
def portal_gallery_delete(request, pk):
    """Delete a gallery item."""
    item = get_object_or_404(GalleryItem, pk=pk)
    title = item.title
    item.delete()
    messages.success(request, f"ছবি '{title}' সফলভাবে মুছে ফেলা হয়েছে।")
    return redirect('/nishi-portal/?tab=gallery')


@require_POST
@staff_required_portal
def portal_profile_save(request):
    """Update salon phone, WhatsApp, address, and hours."""
    profile = SalonProfile.objects.first()
    if not profile:
        profile = SalonProfile.objects.create()
    form = PortalProfileForm(request.POST, instance=profile)
    if form.is_valid():
        profile = form.save(commit=False)
        if profile.phone:
            profile.phone_clean = re.sub(r'[\s\-\(\)]', '', profile.phone)
        profile.save()
        messages.success(request, "🌸 পার্লারের ফোন নম্বর, ঠিকানা এবং সময়সূচি সফলভাবে হালনাগাদ করা হয়েছে!")
    else:
        # Show specific field errors so user knows exactly what to fix
        error_msgs = []
        for field, errors in form.errors.items():
            field_name = form.fields.get(field).label if form.fields.get(field) else field
            error_msgs.append(f"{field_name}: {errors[0]}")
        messages.error(request, f"তথ্য সংরক্ষণে সমস্যা: {' | '.join(error_msgs)}")
    return redirect('/nishi-portal/?tab=profile')


@require_POST
@staff_required_portal
def portal_password_change(request):
    """Change username and/or password for the currently logged in owner."""
    user = request.user
    new_username = request.POST.get('username', '').strip()
    current_password = request.POST.get('current_password', '').strip()
    new_password = request.POST.get('new_password', '').strip()
    confirm_password = request.POST.get('confirm_password', '').strip()

    if not current_password:
        messages.error(request, "❌ অনুগ্রহ করে বর্তমান পাসওয়ার্ড দিন।")
        return redirect('/nishi-portal/?tab=profile')

    if not user.check_password(current_password):
        messages.error(request, "❌ আপনার বর্তমান পাসওয়ার্ডটি সঠিক নয়! দয়া করে সঠিক পাসওয়ার্ড দিন।")
        return redirect('/nishi-portal/?tab=profile')

    username_changed = False
    if new_username and new_username != user.username:
        from django.contrib.auth.models import User
        if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
            messages.error(request, f"❌ '{new_username}' ইউজারনেমটি ইতিমধ্যে ব্যবহৃত হচ্ছে। অন্য ইউজারনেম দিন।")
            return redirect('/nishi-portal/?tab=profile')
        user.username = new_username
        username_changed = True

    password_changed = False
    if new_password:
        if len(new_password) < 6:
            messages.error(request, "❌ নতুন পাসওয়ার্ড অন্তত ৬ অক্ষরের হতে হবে।")
            return redirect('/nishi-portal/?tab=profile')
        if new_password != confirm_password:
            messages.error(request, "❌ নতুন পাসওয়ার্ড ও কনফার্ম পাসওয়ার্ড দুটি মেলেনি!")
            return redirect('/nishi-portal/?tab=profile')
        user.set_password(new_password)
        password_changed = True

    user.save()
    if password_changed:
        update_session_auth_hash(request, user)  # Keep session active!

    msg_parts = []
    if username_changed:
        msg_parts.append(f"ইউজারনেম '{user.username}'")
    if password_changed:
        msg_parts.append("নতুন পাসওয়ার্ড")
    
    if msg_parts:
        messages.success(request, f"🌸 সফলভাবে আপনার {' এবং '.join(msg_parts)} আপডেট করা হয়েছে! পরবর্তী লগইনের সময় এটি ব্যবহার করুন।")
    else:
        messages.info(request, "কোনো পরিবর্তন করা হয়নি।")

    return redirect('/nishi-portal/?tab=profile')

