# Generated manually for Nishi Makeup Artist & Beauty Parlour
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SalonProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Nishi Makeup Artist & Beauty Parlour', max_length=200)),
                ('tagline', models.CharField(default='Your Beauty, Our Priority', max_length=255)),
                ('sub_tagline', models.CharField(default='Makeup + Hair + Beauty • Enhance Your Natural Beauty', max_length=255)),
                ('phone', models.CharField(default='+880 1904-423317', max_length=50)),
                ('phone_clean', models.CharField(default='+8801904423317', max_length=50)),
                ('facebook_url', models.URLField(default='https://www.facebook.com/profile.php?id=61595083298208')),
                ('whatsapp_number', models.CharField(default='8801904423317', max_length=50)),
                ('address', models.CharField(default='Studio & Home/Venue Service, Dhaka, Bangladesh', max_length=300)),
                ('business_hours', models.CharField(default='Every day: 10:00 AM - 08:30 PM (Appointment Based)', max_length=200)),
                ('email', models.EmailField(blank=True, default='nishimakeupartist@gmail.com', max_length=254)),
                ('about_story', models.TextField(default='Welcome to Nishi Makeup Artist & Beauty Parlour...')),
                ('philosophy', models.TextField(default='Because every bride deserves to feel beautiful...')),
            ],
            options={
                'verbose_name': 'Salon Profile & Settings',
                'verbose_name_plural': 'Salon Profile & Settings',
            },
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('title', models.CharField(help_text='e.g. Lead Bridal Stylist & Creative Director', max_length=150)),
                ('experience_years', models.PositiveIntegerField(default=5)),
                ('specialties', models.CharField(help_text='Comma-separated e.g. Royal Bridal, 4K Airbrush, Bengali Traditional', max_length=255)),
                ('bio', models.TextField()),
                ('photo', models.CharField(help_text='URL or static path to artist image', max_length=500)),
                ('portfolio_previews', models.TextField(blank=True, help_text='Comma or newline separated image URLs for portfolio preview modal')),
                ('rating', models.DecimalField(decimal_places=1, default=4.9, max_digits=3)),
                ('completed_brides', models.PositiveIntegerField(default=350)),
                ('is_featured', models.BooleanField(default=True)),
                ('is_available', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='ServiceCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('icon', models.CharField(default='sparkles', help_text='Icon identifier e.g. sparkles, brush, hair, skin, nail', max_length=50)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Service Categories',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('badge_text', models.CharField(blank=True, help_text="e.g. 'Most Popular' or 'Best Seller' or 'Luxury Choice'", max_length=50)),
                ('is_popular', models.BooleanField(default=False)),
                ('price', models.DecimalField(decimal_places=0, help_text='Current price in BDT (৳)', max_digits=10)),
                ('original_price', models.DecimalField(blank=True, decimal_places=0, help_text='Original crossed-out price for discount', max_digits=10, null=True)),
                ('short_description', models.CharField(help_text='One line value proposition', max_length=255)),
                ('duration', models.CharField(default='2-3 Hours', max_length=100)),
                ('included_features', models.TextField(help_text='One feature per line')),
                ('bonus_perks', models.TextField(blank=True, help_text='Special bonus perks or touchup kits')),
                ('image', models.CharField(blank=True, help_text='Hero image for this package', max_length=500)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['order', 'price'],
            },
        ),
        migrations.CreateModel(
            name='GalleryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('category', models.CharField(choices=[('bridal', 'Bridal Transformations'), ('reception', 'Reception & Bou-Bhat'), ('engagement', 'Engagement & Ring Ceremony'), ('party', 'Party & Glamour Looks'), ('haldi', 'Haldi & Mehendi Vibes'), ('natural', 'Natural & Dewy HD Glass Skin'), ('hair', 'Hairstyling & Saree Draping')], default='bridal', max_length=30)),
                ('image', models.CharField(help_text='Image URL or static path', max_length=500)),
                ('caption', models.CharField(blank=True, max_length=255)),
                ('artist_tag', models.CharField(default='Nishi Makeup Artist', max_length=100)),
                ('is_featured', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=150)),
                ('customer_photo', models.CharField(blank=True, max_length=500)),
                ('service_received', models.CharField(help_text='e.g. Royal Bridal HD Makeup', max_length=150)),
                ('rating', models.PositiveSmallIntegerField(default=5)),
                ('feedback', models.TextField()),
                ('event_date', models.CharField(default='Recent Client', max_length=50)),
                ('is_verified', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ContactInquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('subject', models.CharField(default='Appointment & Service Inquiry', max_length=200)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_resolved', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('short_description', models.TextField(help_text='Short engaging summary of the service')),
                ('full_description', models.TextField(blank=True, help_text='Detailed description of the procedure and benefits')),
                ('starting_price', models.DecimalField(decimal_places=0, help_text='Price in BDT (৳)', max_digits=10)),
                ('duration', models.CharField(help_text='e.g. 90 mins, 2-3 hours', max_length=100)),
                ('image', models.CharField(help_text='URL or static path to service image', max_length=500)),
                ('is_featured', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='parlor.servicecategory')),
            ],
            options={
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_reference', models.CharField(editable=False, max_length=30, unique=True)),
                ('customer_name', models.CharField(max_length=150)),
                ('phone_number', models.CharField(max_length=30)),
                ('customer_address', models.TextField(help_text="Home/Venue address or 'Studio Visit'")),
                ('appointment_date', models.DateField()),
                ('preferred_time', models.CharField(choices=[('09:00 AM', '09:00 AM - Morning Slot'), ('11:00 AM', '11:00 AM - Mid-Day Slot'), ('01:30 PM', '01:30 PM - Early Afternoon Slot'), ('03:30 PM', '03:30 PM - Afternoon Slot'), ('05:30 PM', '05:30 PM - Evening Golden Hour Slot'), ('07:00 PM', '07:00 PM - Night Prime Slot')], default='03:30 PM', max_length=50)),
                ('event_type', models.CharField(choices=[('Bridal', 'Wedding / Bridal Ceremony'), ('Reception', 'Wedding Reception (Bou-Bhat)'), ('Engagement', 'Engagement / Ring Ceremony'), ('Haldi_Mehendi', 'Gaye Holud & Mehendi Night'), ('Party', 'Party & Evening Glamour'), ('Birthday', 'Birthday / Anniversary Event'), ('Photoshoot', 'Model / Portfolio Photoshoot'), ('Parlour_Treatment', 'Parlour Skincare & Hair Spa Ritual'), ('Other', 'Other Special Occasion')], default='Bridal', max_length=50)),
                ('special_requests', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('pending', 'Pending Request'), ('confirmed', 'Confirmed Appointment'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('estimated_amount', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('admin_notes', models.TextField(blank=True, help_text='Internal notes by salon management')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('package', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appointments', to='parlor.package')),
                ('preferred_artist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appointments', to='parlor.artist')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appointments', to='parlor.service')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
