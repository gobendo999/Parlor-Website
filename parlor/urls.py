from django.urls import path
from . import views

app_name = 'parlor'

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about_view, name='about'),
    path('artists/', views.artists_view, name='artists'),
    path('services/', views.services_view, name='services'),
    path('packages/', views.packages_view, name='packages'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('book/', views.book_appointment, name='book'),
    path('booking/confirmation/<str:reference>/', views.booking_confirmation, name='booking_confirmation'),
    path('track-booking/', views.track_booking, name='track_booking'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/update-status/<int:pk>/', views.update_appointment_status, name='update_status'),
    
    # Custom Hidden Salon CMS Portal (Nishi Makeup Studio)
    path('nishi-portal/login/', views.portal_login, name='portal_login'),
    path('nishi-portal/logout/', views.portal_logout, name='portal_logout'),
    path('nishi-portal/', views.portal_dashboard, name='portal_dashboard'),
    path('nishi-portal/appointment/<int:pk>/status/', views.portal_appointment_status, name='portal_appointment_status'),
    path('nishi-portal/service/save/', views.portal_service_save, name='portal_service_save'),
    path('nishi-portal/service/<int:pk>/toggle/', views.portal_service_toggle, name='portal_service_toggle'),
    path('nishi-portal/package/save/', views.portal_package_save, name='portal_package_save'),
    path('nishi-portal/gallery/save/', views.portal_gallery_save, name='portal_gallery_save'),
    path('nishi-portal/gallery/<int:pk>/delete/', views.portal_gallery_delete, name='portal_gallery_delete'),
    path('nishi-portal/profile/save/', views.portal_profile_save, name='portal_profile_save'),
    path('nishi-portal/password/change/', views.portal_password_change, name='portal_password_change'),
]
