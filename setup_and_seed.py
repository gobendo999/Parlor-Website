"""
Database migration & rich seed data initializer for Nishi Makeup Artist & Beauty Parlour.
"""

import os
import shutil
import sys
from pathlib import Path

# Setup Django environment
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beauty_parlor.settings')

import django
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User
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

def copy_uploaded_images():
    """Copy uploaded brand images from user upload folder to static/images/"""
    static_img_dir = BASE_DIR / 'static' / 'images'
    static_img_dir.mkdir(parents=True, exist_ok=True)
    
    src_dir = Path(r"C:\Users\HP\.gemini\antigravity\brain\328f9638-d077-4657-aae9-93ae30569fcd\.user_uploaded")
    
    mapping = {
        "media_1792225458825_6f40e1b8.png": "nishi_banner.png",
        "media_1792225467681_e4500146.jpg": "nishi_bridal_poster.jpg",
        "media_1792225545390_01b5577c.png": "nishi_fb_profile.png",
    }
    
    for src_name, dest_name in mapping.items():
        src_file = src_dir / src_name
        dest_file = static_img_dir / dest_name
        if src_file.exists():
            shutil.copy2(src_file, dest_file)
            print(f"Copied brand asset: {dest_name}")
        else:
            print(f"Source file not found: {src_file}")

def run_migrations():
    print("Running database migrations...")
    call_command('migrate', interactive=False)
    print("Migrations complete.")

def seed_data():
    print("Seeding Nishi Makeup Artist & Beauty Parlour data...")

    # 1. Salon Profile
    profile, created = SalonProfile.objects.get_or_create(id=1)
    profile.name = "Nishi Makeup Artist & Beauty Parlour"
    profile.tagline = "Your Beauty, Our Priority"
    profile.sub_tagline = "Makeup + Hair + Beauty • Enhance Your Natural Beauty"
    profile.phone = "+880 1904-423317"
    profile.phone_clean = "+8801904423317"
    profile.facebook_url = "https://www.facebook.com/profile.php?id=61595083298208"
    profile.whatsapp_number = "8801904423317"
    profile.address = "Dhanmondi & Mirpur Studio / Home & Venue Booking Available, Dhaka, Bangladesh"
    profile.business_hours = "Every day: 10:00 AM - 08:30 PM (Appointment Based)"
    profile.email = "nishimakeupartist@gmail.com"
    profile.about_story = (
        "Founded by lead artist Nishi, Nishi Makeup Artist & Beauty Parlour is a premier bridal and luxury beauty destination "
        "crafted for women who desire elegance, sophistication, and flawless glam. We combine international cosmetics "
        "with personalized facial contouring, signature eye artistry, and royal bridal draping. Whether it's your dream wedding day, "
        "a vibrant mehendi night, or a rejuvenating parlour skincare ritual, we bring out the best version of your innate grace."
    )
    profile.philosophy = (
        "Makeup is not just a look, it's a feeling ♡. Because every bride deserves to feel beautiful, confident, and celebrated. "
        "We maintain the highest clinical hygiene protocols, customized color matching for all Asian skin tones, and gentle hair/skin treatments."
    )
    profile.save()
    print("[OK] Salon profile updated.")

    # 2. Superuser admin account
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'nishimakeupartist@gmail.com', 'admin123')
        print("[OK] Created Superuser: admin / admin123")

    # 3. Artists (Only Lead Artist Nishi Sultana - no extra artists)
    Artist.objects.all().delete()
    artists_data = [
        {
            "name": "Nishi Sultana",
            "title": "Founder, Lead Bridal Stylist & Creative Director",
            "experience_years": 8,
            "specialties": "Royal Bengali Bridal, 4K HD Airbrush, Smokey Cut-Crease, Dewy Glass Skin",
            "bio": "Certified master makeup artist with over 8 years of luxury bridal experience. Nishi has glammed over 500+ brides across Bangladesh. Known for her signature glowing base, sculpted eye artistry, and timeless bridal transformations.",
            "photo": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=800&q=80",
            "portfolio_previews": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?auto=format&fit=crop&w=800&q=80,https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80,https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=800&q=80",
            "rating": 5.0,
            "completed_brides": 520,
            "is_featured": True,
            "is_available": True,
            "order": 1,
        },
    ]
    for ad in artists_data:
        Artist.objects.create(**ad)
    print("[OK] Created Lead Artist Nishi Sultana (no extra artists).")

    # 4. Service Categories (Real Beauty Parlour Categories)
    ServiceCategory.objects.all().delete()
    cat_facial = ServiceCategory.objects.create(name="Facial & Skin Care", slug="facial-skin-care", icon="sparkles", description="Rejuvenating facials, skin polishing, and clinical radiance rituals", order=1)
    cat_hair = ServiceCategory.objects.create(name="Hair Care", slug="hair-care", icon="scissors", description="Haircut, styling, spa therapy, rebonding, and protein treatments", order=2)
    cat_makeup = ServiceCategory.objects.create(name="Makeup & Bridal", slug="makeup-bridal", icon="heart", description="Royal bridal artistry, reception glam, party looks, and HD makeup", order=3)
    cat_waxing = ServiceCategory.objects.create(name="Threading & Waxing", slug="threading-waxing", icon="droplets", description="Precision eyebrow threading and painless smooth waxing rituals", order=4)
    cat_nail = ServiceCategory.objects.create(name="Hand, Feet & Nail Care", slug="hand-feet-nail-care", icon="sparkles", description="Relaxing manicures, pedicures, nail polish, and custom nail art", order=5)
    cat_special = ServiceCategory.objects.create(name="Special Services", slug="special-services", icon="star", description="Intricate bridal mehendi, pre-bridal packages, and occasion styling", order=6)
    print("[OK] Created 6 Realistic Service Categories.")

    # 5. Services List
    Service.objects.all().delete()
    services_data = [
        # --- 01. Facial & Skin Care ---
        {
            "category": cat_facial,
            "name": "Basic Facial",
            "slug": "basic-facial",
            "short_description": "Gentle cleansing, steam, blackhead removal, light massage, and soothing hydrating pack.",
            "full_description": "Ideal for regular monthly skincare maintenance. Includes double cleansing, gentle steam exfoliation, comedone extraction, facial cream massage, and refreshing cucumber pack.",
            "starting_price": 800,
            "duration": "45 Mins",
            "image": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 1,
        },
        {
            "category": cat_facial,
            "name": "Herbal / Fruit Facial",
            "slug": "herbal-fruit-facial",
            "short_description": "100% natural fruit extracts and herbal packs to restore natural glow and nourishment.",
            "full_description": "Rich in antioxidants and natural vitamins. Fresh papaya, orange, and herbal extracts soothe sunburn, even out skin tone, and replenish hydration.",
            "starting_price": 1200,
            "duration": "50 Mins",
            "image": "https://images.unsplash.com/photo-1512290900672-1f4144490f23?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 2,
        },
        {
            "category": cat_facial,
            "name": "Gold Facial",
            "slug": "gold-facial",
            "short_description": "24K gold dust and collagen peptide infusion for royal bridal glow and firmness.",
            "full_description": "Luxurious gold leaf essence, deep penetration massage, vacuum pore cleansing, and peel-off gold mask that imparts instantaneous luminous radiance.",
            "starting_price": 2000,
            "duration": "60 Mins",
            "image": "https://images.unsplash.com/photo-1512290903022-79965d078e63?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 3,
        },
        {
            "category": cat_facial,
            "name": "Deep Cleansing Facial",
            "slug": "deep-cleansing-facial",
            "short_description": "Intensive pore detoxification, ultrasonic scrub, and sebum regulation for clear skin.",
            "full_description": "Designed for oily, acne-prone, or congested skin. Uses ultrasonic vibration peeling, antibacterial tea tree treatment, high frequency sterilization, and purifying clay mask.",
            "starting_price": 1500,
            "duration": "60 Mins",
            "image": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 4,
        },
        {
            "category": cat_facial,
            "name": "Face Cleanup",
            "slug": "face-cleanup",
            "short_description": "Quick, effective cleanse, scrub, steam, and pack for instant rejuvenation.",
            "full_description": "A quick instant pick-me-up. Removes accumulated daily pollutants, dead cells, and surface oil, leaving your face fresh, clean, and energized.",
            "starting_price": 600,
            "duration": "30 Mins",
            "image": "https://images.unsplash.com/photo-1506152983158-b4a74a01c721?auto=format&fit=crop&w=800&q=80",
            "is_featured": False,
            "order": 5,
        },
        {
            "category": cat_facial,
            "name": "Face Mask & Skin Polishing",
            "slug": "face-mask-skin-polishing",
            "short_description": "Micro-exfoliation dead cell polish combined with customized botanical mask.",
            "full_description": "Diamond crystal scrub gently polishes the superficial skin layer to diminish dullness and fine lines, followed by a deeply hydrating collagen rubber mask.",
            "starting_price": 1200,
            "duration": "45 Mins",
            "image": "https://images.unsplash.com/photo-1598256989800-fe5f95da9787?auto=format&fit=crop&w=800&q=80",
            "is_featured": False,
            "order": 6,
        },
        {
            "category": cat_facial,
            "name": "Hydra Facial & Glow Treatment",
            "slug": "hydra-facial-glow",
            "short_description": "Advanced vortex-suction hydradermabrasion, hyaluronic acid infusion, and cold hammer.",
            "full_description": "The ultimate red-carpet facial. Deep vacuum pore extraction paired with active serum infusion and cryo-cold tightening for dewy, glass-like skin.",
            "starting_price": 3500,
            "duration": "75 Mins",
            "image": "https://images.unsplash.com/photo-1516975080664-ed2fc6a32937?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 7,
        },
        {
            "category": cat_facial,
            "name": "Anti-Tan & De-Tan Brightening Facial",
            "slug": "anti-tan-facial",
            "short_description": "Specially formulated kojic acid and lactic milk pack to reverse harsh sun tanning.",
            "full_description": "Effectively targets dark spots, tan lines, and pigmentation caused by sun exposure. Leaves skin noticeably lighter, fresher, and radiant.",
            "starting_price": 1500,
            "duration": "50 Mins",
            "image": "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=800&q=80",
            "is_featured": False,
            "order": 8,
        },

        # --- 02. Hair Care ---
        {
            "category": cat_hair,
            "name": "Haircut & Trimming",
            "slug": "haircut-trimming",
            "short_description": "Layer cut, step cut, feather cut, or split-end trimming tailored to your face structure.",
            "full_description": "Includes consultation on haircut style, precision section cutting, split-end removal, and quick styling.",
            "starting_price": 350,
            "duration": "30 Mins",
            "image": "https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 9,
        },
        {
            "category": cat_hair,
            "name": "Hair Wash & Blow Dry",
            "slug": "hair-wash-blow-dry",
            "short_description": "Luxury shampoo cleanse, deep conditioning rinse, and bouncy salon blowout.",
            "full_description": "Gentle scalp massage with premium salon shampoo, nourishing conditioner, heat protectant serum, and round brush blow dry styling for volume and shine.",
            "starting_price": 450,
            "duration": "30 Mins",
            "image": "https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?auto=format&fit=crop&w=800&q=80",
            "is_featured": False,
            "order": 10,
        },
        {
            "category": cat_hair,
            "name": "Hair Styling",
            "slug": "hair-styling-curls-straight",
            "short_description": "Glamorous curls, sleek straight pressing, messy bun, or textured party hairdo.",
            "full_description": "Professional thermal styling using ceramic irons, curling wands, and humidity-resistant hair setting sprays that last all night.",
            "starting_price": 800,
            "duration": "45 Mins",
            "image": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 11,
        },
        {
            "category": cat_hair,
            "name": "Hair Spa",
            "slug": "hair-spa-therapy",
            "short_description": "Intensive scalp massage, cream bath therapy, steam infusion, and frizz reduction.",
            "full_description": "Nourishes the hair roots, stimulates blood circulation, restores moisture to dry strands, and eliminates daily stress.",
            "starting_price": 1500,
            "duration": "60 Mins",
            "image": "https://images.unsplash.com/photo-1582095133179-bfd08e2fc6b3?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 12,
        },
        {
            "category": cat_hair,
            "name": "Hair Coloring",
            "slug": "hair-coloring",
            "short_description": "Root touch-up, global hair color, balayage, or trendy fashion highlights.",
            "full_description": "Using ammonia-free, high-shine professional hair color (L'Oréal / Wella) that protects hair keratin while delivering rich vibrant color.",
            "starting_price": 2500,
            "duration": "2 Hours",
            "image": "https://images.unsplash.com/photo-1607779097040-26e80aa78e66?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 13,
        },
        {
            "category": cat_hair,
            "name": "Hair Protein Treatment",
            "slug": "hair-protein-treatment",
            "short_description": "Deep protein reconstruction for chemically damaged, brittle, or thinning hair.",
            "full_description": "Fortifies weakened hair cuticles with hydrolyzed wheat and silk proteins, preventing hair breakage and restoring elasticity.",
            "starting_price": 1800,
            "duration": "1.5 Hours",
            "image": "https://images.unsplash.com/photo-1519699047748-de8e457a634e?auto=format&fit=crop&w=800&q=80",
            "is_featured": False,
            "order": 14,
        },
        {
            "category": cat_hair,
            "name": "Hair Smoothening / Rebonding",
            "slug": "hair-smoothening-rebonding",
            "short_description": "Permanent silk-straight rebonding or soft natural smoothening with glossy finish.",
            "full_description": "Transforms frizzy, curly, or unruly hair into pin-straight, ultra-glossy, manageable tresses with long-lasting salon finish.",
            "starting_price": 5000,
            "duration": "3 - 4 Hours",
            "image": "https://images.unsplash.com/photo-1562322140-8baeececf3df?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 15,
        },
        {
            "category": cat_hair,
            "name": "Brazilian Keratin Treatment",
            "slug": "brazilian-keratin-treatment",
            "short_description": "Frizz-free smoothness, anti-humidity seal, and natural bounce without harsh chemicals.",
            "full_description": "Infuses pure liquid keratin deep into the cortex to tame unruly frizz for up to 4-6 months while keeping hair soft and bouncy.",
            "starting_price": 4500,
            "duration": "2.5 - 3 Hours",
            "image": "https://images.unsplash.com/photo-1522337660859-02fbefca4702?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 16,
        },

        # --- 03. Makeup & Bridal ---
        {
            "category": cat_makeup,
            "name": "Bridal Makeup",
            "slug": "bridal-makeup",
            "short_description": "Our signature royal bridal look with HD foundation, waterproof eye artistry, and customized glow.",
            "full_description": "Includes luxury skin prep, HD 3D base matching your tone, waterproof kajal, 3D mink lashes, contouring, highlighting, designer lip sculpting, jewelry setting, and 16-hour sweat-proof stay.",
            "starting_price": 12000,
            "duration": "3 - 3.5 Hours",
            "image": "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 17,
        },
        {
            "category": cat_makeup,
            "name": "Holud Makeup",
            "slug": "holud-makeup",
            "short_description": "Vibrant, sun-kissed, floral-themed makeup for Gaye Holud with fresh flower setting.",
            "full_description": "Sweat-resistant dewy base, warm golden tones, yellow/orange pop eyeshadow, floral jewelry setting, and braided hairstyle.",
            "starting_price": 5000,
            "duration": "2 Hours",
            "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 18,
        },
        {
            "category": cat_makeup,
            "name": "Reception Makeup",
            "slug": "reception-makeup",
            "short_description": "Modern glamour look featuring glass-skin finish, glittering cut-crease, and graceful evening hair styling.",
            "full_description": "Designed for Bou-Bhat and evening wedding receptions. High-impact soft shimmer eyes, camera-ready dewy glow, and royal hair styling with accessories.",
            "starting_price": 10000,
            "duration": "2.5 - 3 Hours",
            "image": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 19,
        },
        {
            "category": cat_makeup,
            "name": "Party Makeup",
            "slug": "party-makeup",
            "short_description": "Glamorous and chic party makeover with defined eyes, sculpted cheekbones, and long-lasting finish.",
            "full_description": "Perfect for wedding guests, galas, and festive dinners. Includes complete facial makeup, natural lashes, and signature hairstyling.",
            "starting_price": 3000,
            "duration": "1.5 Hours",
            "image": "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 20,
        },
        {
            "category": cat_makeup,
            "name": "Engagement Makeup",
            "slug": "engagement-makeup",
            "short_description": "Romantic pastel or bold engagement look tailored to match your ring ceremony outfit.",
            "full_description": "Soft luminous coverage, winged eyeliner, rosy blush, elegant curls or half-up bridal bun, and veil/dupatta draping.",
            "starting_price": 6000,
            "duration": "2 Hours",
            "image": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 21,
        },
        {
            "category": cat_makeup,
            "name": "HD Makeup",
            "slug": "hd-makeup",
            "short_description": "High-Definition micro-fine pigment makeup that looks completely natural to both human eye and 4K lenses.",
            "full_description": "Uses luxury light-diffusing HD makeup formulas (Kryolan, Make Up For Ever, MAC Studio Fix) that mask pores and blemishes seamlessly.",
            "starting_price": 4500,
            "duration": "2 Hours",
            "image": "https://images.unsplash.com/photo-1503236823255-94609f598e71?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 22,
        },
        {
            "category": cat_makeup,
            "name": "Saree Draping & Hair Setting",
            "slug": "saree-draping-hair-setting",
            "short_description": "Royal saree draping (Jamdani, Katan, Lehenga style) plus intricate updos, curls, or braids.",
            "full_description": "Expert pleat ironing and pinning, can-can setting, heavy pallu support, paired with royal floral bun or Hollywood waves.",
            "starting_price": 1200,
            "duration": "45 Mins",
            "image": "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 23,
        },
        {
            "category": cat_makeup,
            "name": "4K Airbrush Bridal Makeup",
            "slug": "airbrush-bridal-makeup",
            "short_description": "Ultra-fine silicone airbrush mist for weightless, water-resistant, 24-hour HD perfection.",
            "full_description": "The gold standard in luxury bridal beauty. Hypoallergenic, poreless finish with zero caking, ideal for long wedding ceremonies.",
            "starting_price": 16000,
            "duration": "3.5 Hours",
            "image": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 24,
        },

        # --- 04. Threading & Waxing ---
        {
            "category": cat_waxing,
            "name": "Eyebrow Threading",
            "slug": "eyebrow-threading",
            "short_description": "Precision organic cotton thread eyebrow shaping according to your facial structure.",
            "full_description": "Neat arch defining, trimming stray hairs, followed by soothing rose water or aloe vera gel massage.",
            "starting_price": 80,
            "duration": "15 Mins",
            "image": "https://images.unsplash.com/photo-1588516903720-8ceb67f9ef84?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 25,
        },
        {
            "category": cat_waxing,
            "name": "Upper Lip Threading",
            "slug": "upper-lip-threading",
            "short_description": "Quick and clean hair removal from the upper lip area with soothing post-care.",
            "full_description": "Gentle thread epilation ensuring smooth lipstick application and zero dark hair shadows.",
            "starting_price": 50,
            "duration": "10 Mins",
            "image": "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?auto=format&fit=crop&w=800&q=80",
            "is_featured": False,
            "order": 26,
        },
        {
            "category": cat_waxing,
            "name": "Full Face Threading",
            "slug": "full-face-threading",
            "short_description": "Complete facial threading including brows, upper lip, chin, sideburns, and forehead.",
            "full_description": "Removes peach fuzz and dead surface cells, allowing skincare and makeup foundation to glide on like glass.",
            "starting_price": 250,
            "duration": "25 Mins",
            "image": "https://images.unsplash.com/photo-1515377905703-c4788e51af15?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 27,
        },
        {
            "category": cat_waxing,
            "name": "Underarm Waxing",
            "slug": "underarm-waxing",
            "short_description": "Gentle chocolate or Rica wax application for soft, dark-shadow-free underarms.",
            "full_description": "Removes hair from the root, reduces ingrown hairs, and delays regrowth for 3-4 weeks.",
            "starting_price": 300,
            "duration": "20 Mins",
            "image": "https://images.unsplash.com/photo-1519823551278-64ac92734fb1?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 28,
        },
        {
            "category": cat_waxing,
            "name": "Half / Full Arms Waxing",
            "slug": "arms-waxing",
            "short_description": "Smooth hair removal for arms with hydrating after-wax calming lotion.",
            "full_description": "Exfoliates dead skin cells while pulling out hair, leaving arms soft, smooth, and naturally brightened.",
            "starting_price": 600,
            "duration": "35 Mins",
            "image": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=800&q=80",
            "is_featured": False,
            "order": 29,
        },
        {
            "category": cat_waxing,
            "name": "Half / Full Legs Waxing",
            "slug": "legs-waxing",
            "short_description": "Silk-smooth waxing for legs with zero sticky residue and anti-tan effect.",
            "full_description": "Professional waxing treatment eliminating tan lines and coarse hair, completed with calming cooling lotion.",
            "starting_price": 800,
            "duration": "40 Mins",
            "image": "https://images.unsplash.com/photo-1519824145371-296894a0daa9?auto=format&fit=crop&w=800&q=80",
            "is_featured": False,
            "order": 30,
        },
        {
            "category": cat_waxing,
            "name": "Full Body Rica Waxing",
            "slug": "full-body-waxing",
            "short_description": "Italian Rica liposoluble wax for full body smooth glow with minimum discomfort.",
            "full_description": "Colophony-free Italian wax that nourishes sensitive skin while removing hair and tan from full body.",
            "starting_price": 2800,
            "duration": "1.5 Hours",
            "image": "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 31,
        },

        # --- 05. Hand, Feet & Nail Care ---
        {
            "category": cat_nail,
            "name": "Manicure",
            "slug": "basic-manicure",
            "short_description": "Hand soak, nail shaping, cuticle trimming, exfoliating scrub, and hand massage.",
            "full_description": "Complete hand pampering ritual leaving nails clean, healthy, and perfectly manicured.",
            "starting_price": 700,
            "duration": "40 Mins",
            "image": "https://images.unsplash.com/photo-1632345031435-8727f6897d53?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 32,
        },
        {
            "category": cat_nail,
            "name": "Pedicure",
            "slug": "basic-pedicure",
            "short_description": "Aromatic foot bath, heel callous scrubbing, dead skin scraping, and relaxing massage.",
            "full_description": "Soothes tired feet, heals cracked heels, cleans cuticles, and provides deep moisturizing relief.",
            "starting_price": 800,
            "duration": "45 Mins",
            "image": "https://images.unsplash.com/photo-1519014816548-bf5fe059798b?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 33,
        },
        {
            "category": cat_nail,
            "name": "Nail Polish",
            "slug": "nail-polish-application",
            "short_description": "Quick application of high-shine, chip-resistant designer nail polish.",
            "full_description": "Base coat, two coats of your chosen vibrant or nude nail lacquer, finished with a quick-dry top coat.",
            "starting_price": 150,
            "duration": "15 Mins",
            "image": "https://images.unsplash.com/photo-1604654894610-df63bc536371?auto=format&fit=crop&w=800&q=80",
            "is_featured": False,
            "order": 34,
        },
        {
            "category": cat_nail,
            "name": "Nail Art",
            "slug": "designer-nail-art",
            "short_description": "Custom creative designs, glitter accents, ombré gradients, and stone embellishments.",
            "full_description": "Handcrafted nail artistry customized to match your bridal saree, lehenga, or party outfit.",
            "starting_price": 600,
            "duration": "30 Mins",
            "image": "https://images.unsplash.com/photo-1522337094346-29b35b66e360?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 35,
        },
        {
            "category": cat_nail,
            "name": "Hand & Foot Scrub",
            "slug": "hand-foot-scrub",
            "short_description": "De-tan herbal polishing scrub to remove sun tan and rough dead skin.",
            "full_description": "Walnut and apricot kernel exfoliator with brightening essential oils to revive dull hands and feet.",
            "starting_price": 500,
            "duration": "30 Mins",
            "image": "https://images.unsplash.com/photo-1515377905703-c4788e51af15?auto=format&fit=crop&w=800&q=80",
            "is_featured": False,
            "order": 36,
        },
        {
            "category": cat_nail,
            "name": "Luxury Spa Mani-Pedi Duo",
            "slug": "luxury-spa-mani-pedi",
            "short_description": "Herbal salt soak, paraffin wax mask, hot towel wrap, and deep massage for hands & feet.",
            "full_description": "The ultimate salon pampering combo. Leaves hands and feet silky soft, de-tanned, and glowing.",
            "starting_price": 1800,
            "duration": "75 Mins",
            "image": "https://images.unsplash.com/photo-1512290900672-1f55b9a47318?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 37,
        },

        # --- 06. Special Services ---
        {
            "category": cat_special,
            "name": "Mehendi Design",
            "slug": "mehendi-design",
            "short_description": "Arabic, Indian mandala, or minimalist trendy henna designs for palm and back.",
            "full_description": "100% natural organic henna cones ensuring dark, rich stain without chemical burns or allergic reactions.",
            "starting_price": 800,
            "duration": "45 - 60 Mins",
            "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 38,
        },
        {
            "category": cat_special,
            "name": "Pre-Bridal Care",
            "slug": "pre-bridal-care",
            "short_description": "Comprehensive pre-wedding pampering: Gold facial, full body polish, hair spa, and mani-pedi.",
            "full_description": "All-in-one head-to-toe bride preparation done 2-3 days before wedding ceremonies for maximum glow.",
            "starting_price": 6500,
            "duration": "3 Hours",
            "image": "https://images.unsplash.com/photo-1512290900672-1f4144490f23?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 39,
        },
        {
            "category": cat_special,
            "name": "Bridal Hair Styling",
            "slug": "bridal-hair-styling",
            "short_description": "Royal bridal bun with fresh rose setting, matha patti pinning, and donut volume.",
            "full_description": "Architecturally sculpted updos that securely hold heavy tikli, jhamor, and veil all day.",
            "starting_price": 2500,
            "duration": "60 Mins",
            "image": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 40,
        },
        {
            "category": cat_special,
            "name": "Party Hairstyle",
            "slug": "party-hairstyle",
            "short_description": "Messy braided bun, voluminous beach waves, waterfall braid, or sleek ponytail.",
            "full_description": "Trendy, chic hairstyles tailored to suit contemporary western gowns, sarees, or salwar kameez.",
            "starting_price": 1000,
            "duration": "45 Mins",
            "image": "https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=800&q=80",
            "is_featured": False,
            "order": 41,
        },
        {
            "category": cat_special,
            "name": "Special Occasion Makeover",
            "slug": "special-occasion-makeover",
            "short_description": "Full makeover for anniversaries, convocations, award nights, or stage performances.",
            "full_description": "Camera-ready makeup, hairstyle, and attire styling customized for your important milestone.",
            "starting_price": 4000,
            "duration": "2 Hours",
            "image": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 42,
        },
        {
            "category": cat_special,
            "name": "Royal Bridal Mehendi (Both Hands & Feet)",
            "slug": "royal-bridal-mehendi",
            "short_description": "Intricate elbow-length bridal henna with groom name motif, bride-groom portraits, and jali work.",
            "full_description": "Detailed traditional bridal mehendi with dark organic essential oil clove infusion for deepest color.",
            "starting_price": 4000,
            "duration": "2.5 - 3 Hours",
            "image": "https://images.unsplash.com/photo-1598256989800-fe5f95da9787?auto=format&fit=crop&w=800&q=80",
            "is_featured": True,
            "order": 43,
        },
    ]
    for s_data in services_data:
        Service.objects.create(**s_data)
    print(f"[OK] Created {len(services_data)} Real Beauty Parlour & Makeup Services.")

    # 6. Party & Occasion Makeup Packages (User Specified 9 Luxury Packages)
    Package.objects.all().delete()
    packages_data = [
        {
            "name": "Birthday Party Package",
            "slug": "birthday-party-package",
            "badge_text": "Birthday Special",
            "is_popular": False,
            "price": 1500,
            "original_price": 2500,
            "short_description": "Soft party makeup with simple hairstyle, defined eye makeup, and basic clean finishing.",
            "duration": "1 - 1.5 Hours",
            "included_features": (
                "Soft Party Makeup\n"
                "Simple Hairstyle\n"
                "Eye Makeup\n"
                "Basic Finishing"
            ),
            "bonus_perks": "Complimentary Touch-up Sponge & Glow Mist",
            "image": "https://images.openai.com/static-rsc-4/LhztRzamost2LXH2vXVqYQ7NOta12j0UGJ60MGMN7vKJIMN3Btjxi1cGR1oRPzBNsiuTIHX5GtJvKFbqVhJO7Vs0tO5YBQ8kKLESsabtDRwf3tBQ_SHkUJXEjUfyCPamGGWtfzdhTuq-UkSPx1ZPolqbOAMvXySDVFuQU9gKfrs?purpose=inline",
            "order": 1,
        },
        {
            "name": "Engagement Makeup Package",
            "slug": "engagement-makeup-package",
            "badge_text": "Ring Ceremony",
            "is_popular": False,
            "price": 3000,
            "original_price": 6000,
            "short_description": "Glam makeup, professional hairstyle, defined eye makeup with lashes, and saree/outfit draping.",
            "duration": "2 Hours",
            "included_features": (
                "Glam Makeup\n"
                "Professional Hairstyle\n"
                "Eye Makeup & Lashes\n"
                "Saree / Outfit Draping"
            ),
            "bonus_perks": "Complimentary False Lashes & Jewelry Pinning",
            "image": "https://images.openai.com/static-rsc-4/Ivw3SR93HBzAwz1sO3-TFGCi50q0Ou4wde8Q3oVXyukXrNKi9mruIpnIoecLYK2VZGSj3LqC8PPxTvNdeR5DcfXyzT5iz3PTT2idP-7uLXFqVgoHJ0hmN4Tkn70Dv7d8kYTbo7-iINkqonYa5s0Y5rgLmSUieSsqPn8Lb7Ho6p8?purpose=inline",
            "order": 2,
        },
        {
            "name": "Gaye Holud Package",
            "slug": "gaye-holud-package",
            "badge_text": "Holud Special",
            "is_popular": False,
            "price": 2500,
            "original_price": 5000,
            "short_description": "Vibrant Haldi makeup look with floral hairstyle, eye makeup, and festive saree draping.",
            "duration": "2 Hours",
            "included_features": (
                "Haldi Makeup Look\n"
                "Floral Hairstyle\n"
                "Eye Makeup\n"
                "Saree Draping"
            ),
            "bonus_perks": "Floral Jewelry Setting & Dupatta Pinning",
            "image": "https://images.openai.com/static-rsc-4/peX50PNcR8cfUElXQBDyglHkm0mHIzxTcWnjuvkRLJ6AYj2vMULyYlWnlKqc-byTWCpq0B8Esq7Algvh3m409lOfEuwJWgC79m--GKcdONhpGNHvayo-ksNeG1KCVmr_m91AQFiGSHYnSTgjelDgxHSHLr85ql0BpNrBZRUIY7A?purpose=inline",
            "order": 3,
        },
        {
            "name": "Reception Party Package",
            "slug": "reception-party-package",
            "badge_text": "Evening Glam",
            "is_popular": False,
            "price": 3000,
            "original_price": 6000,
            "short_description": "Glam reception makeup, elegant hairstyle, lashes, and designer outfit draping.",
            "duration": "2 Hours",
            "included_features": (
                "Glam Makeup\n"
                "Elegant Hairstyle\n"
                "Eye Makeup & Lashes\n"
                "Outfit Draping"
            ),
            "bonus_perks": "Long-Lasting Setting Mist & 3D Mink Lashes",
            "image": "https://images.openai.com/static-rsc-4/DrdjymEtcSp8ZXy_tBto8zeiPf4U_ck53jhKsuW7IZOuCCdn-o92077ZwZCtXgtXAvHTyJlR7LvhNQguO4kWgwQVTSzzNJgz5lQFMSIGNzW7SyFWjulNly4AzXy378Dqi0bZMDom98YaTulrvdF7SWd0xxBYdcLvSJYVdOH1AdQ?purpose=inline",
            "order": 4,
        },
        {
            "name": "Wedding Bridal Package",
            "slug": "wedding-bridal-package",
            "badge_text": "👑 Royal Bridal Choice",
            "is_popular": True,
            "price": 8000,
            "original_price": 20000,
            "short_description": "Complete royal bridal transformation with bridal makeup, hairstyle, lehenga/saree draping, lashes, and premium finishing.",
            "duration": "3 - 3.5 Hours",
            "included_features": (
                "Bridal Makeup\n"
                "Bridal Hairstyle\n"
                "Saree / Lehenga Draping\n"
                "Premium Finishing\n"
                "False Eyelashes"
            ),
            "bonus_perks": "Bridal Luxury Emergency Touch-up Kit Included ♡",
            "image": "https://images.openai.com/static-rsc-4/UW45qtCgj64Wv54DSyy79mbNagZVfGVkxLFxoW5Aw_eml-6aenTucaAmSmWyuVZherPKRpMmpbbs_i0H44X7dPfYTfa4nD9WA6hDR9IdEcJwxORyF77DSS15B30QTL-HHH1C2GwLffXrBIWBWNChZWr9VqNaJyoUueueSCbjPxw?purpose=inline",
            "order": 5,
        },
        {
            "name": "Anniversary Package",
            "slug": "anniversary-package",
            "badge_text": "Anniversary Special",
            "is_popular": False,
            "price": 2000,
            "original_price": 4000,
            "short_description": "Elegant soft glam makeup, hairstyle, eye makeup, and long-lasting finishing touch-up.",
            "duration": "1.5 Hours",
            "included_features": (
                "Elegant Soft Glam Makeup\n"
                "Hairstyling\n"
                "Eye Makeup\n"
                "Finishing & Touch-up"
            ),
            "bonus_perks": "Dewy Highlighter Glow & Setting Spray",
            "image": "https://images.openai.com/static-rsc-4/PyF12rvcc83ecIkSuqN_-LS0HROLg1VuCo4ceIThktvydQUMVdCxJBPwKGvE_qlD5RzwS5Bip2ND6md_nOOOS1kSqXm9GcwOz7_eMjXQHHG-ta49TMbEoT2UVkxHdAj9pbknawjkgOA6-sfRF9gNwceBTQExqipjLfPdFeJosPs?purpose=inline",
            "order": 6,
        },
        {
            "name": "Corporate & Formal Event Package",
            "slug": "corporate-formal-event-package",
            "badge_text": "Executive Elegance",
            "is_popular": False,
            "price": 1200,
            "original_price": 2500,
            "short_description": "Polished natural makeup with simple hairstyle and light eye makeup for professional occasions.",
            "duration": "1 Hour",
            "included_features": (
                "Natural Makeup\n"
                "Simple Hairstyle\n"
                "Light Eye Makeup\n"
                "Professional Look"
            ),
            "bonus_perks": "Matte Anti-Shine Finish for High Flash Photography",
            "image": "https://images.openai.com/static-rsc-4/ceeWRdqzJ6b7-wp5u8vadAEt39ec7OA1nxQLDqzUxJ-Je-Xk_6xYhQVT1zTEnzekqzTCiBgaaImPqX9jFj1n_azOKfuL2smYmGvQPyxI213YY8um3CO4yHX71yRre5NJMCZRNP5InlYbq9MTvHsZZ6X_KbAy2WJL8tif8a2XHXE?purpose=inline",
            "order": 7,
        },
        {
            "name": "Bridesmaid Package",
            "slug": "bridesmaid-package",
            "badge_text": "Bridal Squad / জন",
            "is_popular": False,
            "price": 1500,
            "original_price": 3000,
            "short_description": "Chic party makeup with hairstyle, eye makeup, and basic finishing per person.",
            "duration": "1 Hour / Person",
            "included_features": (
                "Party Makeup\n"
                "Hairstyle\n"
                "Eye Makeup\n"
                "Basic Finishing"
            ),
            "bonus_perks": "Group Discount for 3+ Bridesmaids",
            "image": "https://images.openai.com/static-rsc-4/CDQ5gQ4JdeqGDNXw1zAvxvKLs0CX4to34he1_BkzTfnNXeiexVQL2Lyo-AOEjlwYBJYeswOPYRWPGJxFJLwxNfI37y7j5Tr3aakMGtb3McV_sh9_jv6qeztZnP71RExrRN7VrhrOrs3xDJwBW6NIxoD_5bleTsKwaCdgYSuceTQ?purpose=inline",
            "order": 8,
        },
        {
            "name": "Eid & Festive Makeup Package",
            "slug": "eid-festive-makeup-package",
            "badge_text": "Eid & Festive",
            "is_popular": False,
            "price": 1000,
            "original_price": 2500,
            "short_description": "Glowing festive makeup with simple hairstyle, eye makeup, and radiant finish.",
            "duration": "45 Mins - 1 Hour",
            "included_features": (
                "Festive Makeup\n"
                "Simple Hairstyle\n"
                "Eye Makeup\n"
                "Finishing"
            ),
            "bonus_perks": "Waterproof Eye Shimmer & Lip Gloss",
            "image": "https://images.openai.com/static-rsc-4/n4VrHYmpWSmAg9fuA9DJqWrmQm1b_XZXKoJab5hjMQ_6JWRcEaopoHcOaUlkUe4D8onn9HzBbj2oLyG_F2EGQru4S7So562BMGrFlDoAbGfMQpfgIJWdIHlK_37170cgRUIS1zwmycAXSTrG3GcPhVm9J--RRAXvJ2iNG2bb70s?purpose=inline",
            "order": 9,
        },
    ]
    for p_data in packages_data:
        Package.objects.create(**p_data)
    print(f"[OK] Created {len(packages_data)} Party & Occasion Makeup Packages.")

    # 7. Portfolio Gallery Transformations
    GalleryItem.objects.all().delete()
    gallery_data = [
        {
            "title": "Royal Crimson Bengali Bridal",
            "category": "bridal",
            "image": "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80",
            "caption": "Signature bold eye with winged liner, red lips, and traditional Katan mathapatti setting.",
            "artist_tag": "Nishi Sultana",
        },
        {
            "title": "Pastel Pink Engagement Elegance",
            "category": "engagement",
            "image": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=800&q=80",
            "caption": "Soft rose gold lids, flushed cheeks, and romantic textured Hollywood waves.",
            "artist_tag": "Tanha Rahman",
        },
        {
            "title": "Emerald Green Reception Glam",
            "category": "reception",
            "image": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?auto=format&fit=crop&w=800&q=80",
            "caption": "Dewy glass skin, smokey emerald eye tint, and sparkling highlighter.",
            "artist_tag": "Nishi Sultana",
        },
        {
            "title": "Sun-Kissed Haldi & Mehendi Vibes",
            "category": "haldi",
            "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=80",
            "caption": "Vibrant marigold yellow eye highlights, floral jewelry, and jasmine hair braiding.",
            "artist_tag": "Sabrina Akter",
        },
        {
            "title": "Cocktail Evening Party Glamour",
            "category": "party",
            "image": "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?auto=format&fit=crop&w=800&q=80",
            "caption": "Smokey bronze lids, sculpted cheeks, and velvet nude matte lip.",
            "artist_tag": "Tanha Rahman",
        },
        {
            "title": "No-Makeup Dewy HD Glass Skin",
            "category": "natural",
            "image": "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?auto=format&fit=crop&w=800&q=80",
            "caption": "Subtle radiant glow, feathered natural brows, and glossy peach pout.",
            "artist_tag": "Farhana Mehedi",
        },
        {
            "title": "Royal Floral Bun & Jamdani Saree Draping",
            "category": "hair",
            "image": "https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=800&q=80",
            "caption": "Textured bridal chignon wrapped in baby's breath and secure pleat draping.",
            "artist_tag": "Sabrina Akter",
        },
        {
            "title": "Golden Glam Reception Queen",
            "category": "reception",
            "image": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&w=800&q=80",
            "caption": "Champagne shimmer eyelids paired with warm berry velvet lips.",
            "artist_tag": "Nishi Sultana",
        },
    ]
    for g_data in gallery_data:
        GalleryItem.objects.create(**g_data)
    print(f"[OK] Created {len(gallery_data)} Gallery Showcase items.")

    # 8. Testimonials
    Testimonial.objects.all().delete()
    reviews_data = [
        {
            "customer_name": "Sumaiya Afreen",
            "customer_photo": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=200&q=80",
            "service_received": "Luxury Bridal Package",
            "rating": 5,
            "feedback": "Nishi apu made my wedding day magical! The makeup did not budge for even a second through 12 hours of teary moments and photography lights. Everyone praised my natural glow and how lightweight it felt. Best decision ever!",
            "event_date": "Wedding Ceremony (Mirpur DOHS)",
            "is_verified": True,
            "is_featured": True,
        },
        {
            "customer_name": "Dr. Maliha Tabassum",
            "customer_photo": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80",
            "service_received": "Engagement Glam & Hair Artistry",
            "rating": 5,
            "feedback": "I was very nervous about makeup making me look like someone else, but Tanha and Nishi understood my vision perfectly. It was soft, graceful, and regal. The saree draping was immaculate!",
            "event_date": "Engagement Ceremony (Dhanmondi)",
            "is_verified": True,
            "is_featured": True,
        },
        {
            "customer_name": "Nawshin Tasnim",
            "customer_photo": "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=200&q=80",
            "service_received": "Haldi & Mehendi Vibes",
            "rating": 5,
            "feedback": "The floral styling and eye makeup were so vivid and vibrant. All my friends asked where I got dolled up from. Booking online was effortless and the team arrived right on schedule.",
            "event_date": "Mehendi Gala (Gulshan)",
            "is_verified": True,
            "is_featured": True,
        },
        {
            "customer_name": "Farzana Haque",
            "customer_photo": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=200&q=80",
            "service_received": "Pre-Bridal Radiance & 24K Gold Facial",
            "rating": 5,
            "feedback": "The facial and hair spa gave my tired skin an incredible glass glow before my wedding week. The studio was clean, hygienic, and relaxing with soothing ambiance.",
            "event_date": "Pre-Wedding Skincare",
            "is_verified": True,
            "is_featured": True,
        },
    ]
    for r_data in reviews_data:
        Testimonial.objects.create(**r_data)
    print(f"[OK] Created {len(reviews_data)} Verified Customer Testimonials.")

    # 9. Sample Initial Appointment for demonstration
    if not Appointment.objects.exists():
        from datetime import date, timedelta
        Appointment.objects.create(
            booking_reference="NB-2026-GLAM01",
            customer_name="Nusrat Jahan",
            phone_number="+8801904423317",
            customer_address="House 42, Road 11, Dhanmondi, Dhaka",
            preferred_artist=Artist.objects.first(),
            package=Package.objects.filter(is_popular=True).first(),
            appointment_date=date.today() + timedelta(days=7),
            preferred_time="03:30 PM",
            event_type="Bridal",
            special_requests="Crimson lehenga with antique gold jewelry. Please include extra veil pinning.",
            status="confirmed",
            estimated_amount=10000,
        )
        print("[OK] Created sample confirmed appointment NB-2026-GLAM01.")

    print("\n[OK] Database setup and rich seed data completed successfully!")

if __name__ == '__main__':
    copy_uploaded_images()
    run_migrations()
    seed_data()
