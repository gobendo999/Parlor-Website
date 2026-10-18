# Nishi Makeup Artist & Beauty Parlour 👑✨
### Luxury Bridal, Occasion Artistry & Complete Parlour Management Web Platform

A website and booking management system built for **Nishi Makeup Artist & Beauty Parlour**, featuring a luxury golden aesthetic (`#D4AF37`, `#FFD700`, `#F7E7CE`, `#FFFDF5`, `#FFF4D6`, `#E8B4B8`, `#3B2618`).

---

## 🌟 Key Features & Architecture

### 1. Brand Identity & Visual Design
- **Color Theme:** Luxury Gold, Bright Gold, Warm Ivory, Champagne, Soft Cream, Rose Gold, and Deep Velvet Brown.
- **Brand Assets:** Official branding extracted from the studio's banners and posters with the tagline *"Your Beauty, Our Priority"* and *"Enhance Your Natural Beauty"*.
- **Typography:** Google Fonts `Playfair Display`, `Cormorant Garamond`, and `Montserrat`.

### 2. Homepage & Interactive Experience
- **Hero Section:** Full-width hero presentation with bridal photography, floating trust cards, trust statements, and dual action CTAs.
- **Metrics Counter Strip:** 500+ Royal Brides Glambassador, 8+ Years of Artistry, 100% Original International Cosmetics (MAC, Huda Beauty, Dior, NARS, Anastasia Beverly Hills, Kryolan, Charlotte Tilbury, Estée Lauder).
- **About Our Studio:** Studio story, clinical hygiene guarantee, personalized consultation, and vanity kit showcase.
- **Professional Artists:** Interactive cards with years of experience, specialties, ratings, portfolio preview modal, and **"Book This Artist"** one-click selector.
- **Makeup & Parlour Services (16 Services):**
  - Bridal Makeup, Reception, Engagement, Party, Birthday, Haldi & Mehendi, HD Makeup, Airbrush Makeup, Natural Glass Skin, Photoshoot, Guest Makeup, Hairstyling & Saree Draping.
  - **Deep Parlour Treatments:** 24K Golden Radiance Facial, Diamond Hydra Dermabrasion, L'Oréal Keratin & Hair Spa, Luxury Manicure & Pedicure Spa.
- **Luxury Packages (6 Packages):**
  - Basic Glam (৳1,500)
  - Party Glam (৳3,000)
  - Engagement Glam (৳5,000)
  - **Luxury Bridal (৳10,000)** - *Highlighted with golden "⭐ Most Popular & Bride's Choice" badge*
  - Pre-Bridal Radiance & Spa Ritual (৳7,500)
  - Royal 4K Airbrush Bridal Extravaganza (৳16,000)
  - *Clicking any package automatically preselects it in the booking form with real-time price & feature calculations.*
- **Appointment Booking System:**
  - Full client validation (Name, Phone number verification, Venue/Address, Artist, Service, Package, Date, Time Slot, Event Type, Notes, Agreement).
  - Past appointment date blocker.
  - Live calculated summary pane with real-time total.
  - Unique booking reference code generator (`NB-YYYY-XXXXXX`).
  - Booking status workflow: `Pending Verification` vs `Confirmed`.
  - Printable confirmation slip with WhatsApp message trigger.
- **Self-Service Tracker (`/track-booking/`):**
  - Clients can lookup their appointment anytime using their booking reference code or phone number.
- **Transformation Gallery:**
  - Filterable by Bridal, Reception, Engagement, Party, Haldi, Natural Glass Skin, and Hair/Draping with image lightbox zoom.
- **Customer Testimonials:**
  - Verified reviews with 5-star ratings and customer photos.
- **Contact Us Section:**
  - Direct Studio Hotline: **+880 1904-423317** (`tel:+8801904423317`)
  - Official Facebook Page: [Nishi Makeup Artist](https://www.facebook.com/profile.php?id=61595083298208)
  - Direct WhatsApp Chat: [Message on WhatsApp](https://wa.me/8801904423317)
  - Interactive contact message form & studio coordinates.

---

## 🛠️ Technology Stack
- **Backend:** Django (Python)
- **Frontend:** Pure HTML5, Modern CSS3 (Responsive Grid/Flexbox, Gold gradients), Vanilla JavaScript (No heavy external frontend frameworks required)
- **Database:** SQLite3 (`db.sqlite3`)

---

## 🚀 Quick Start Guide

### 1. Launch the Server
You can simply double-click `run_server.bat` or run:
```bash
python manage.py runserver 127.0.0.1:8000
```

### 2. Key URLs
- **Main Website:** `/`
- **Book Appointment:** `/book/`
- **Track Booking:** `/track-booking/`
- **Parlour Staff Portal:** `/nishi-portal/`
- **Django Admin:** `/admin/`

### 3. Creating an Admin Account
To create your secure admin credentials for the portal, run:
```bash
python manage.py createsuperuser
```

