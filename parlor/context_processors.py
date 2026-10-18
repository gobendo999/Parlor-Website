from .models import SalonProfile

def salon_context(request):
    try:
        profile = SalonProfile.objects.first()
        if not profile:
            profile = SalonProfile.objects.create(
                name="Nishi Makeup Artist & Beauty Parlour",
                tagline="Your Beauty, Our Priority",
                sub_tagline="Makeup + Hair + Beauty • Enhance Your Natural Beauty",
                phone="+880 1904-423317",
                phone_clean="+8801904423317",
                facebook_url="https://www.facebook.com/profile.php?id=61595083298208",
                whatsapp_number="8801904423317",
                address="Studio Visit & Home/Venue Service, Dhaka, Bangladesh",
                business_hours="Every day: 10:00 AM - 08:30 PM",
                email="nishimakeupartist@gmail.com",
            )
    except Exception:
        profile = None

    return {
        'salon': profile,
        'salon_phone': '+880 1904-423317',
        'salon_phone_tel': 'tel:+8801904423317',
        'salon_facebook_url': 'https://www.facebook.com/profile.php?id=61595083298208',
        'salon_whatsapp_url': 'https://wa.me/8801904423317?text=Hello%20Nishi%20Makeup%20Artist,%20I%20would%20like%20to%20inquire%20about%20booking%20an%20appointment.',
    }
