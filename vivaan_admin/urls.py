from django.urls import path
# from .views import admin

from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from . import views
# from . import api_views

app_name = "vivaan_admin"   
urlpatterns = [

    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    
    # Bookings
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/create/', views.booking_create, name='booking_create'),
    path('bookings/detail/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('bookings/edit/<int:pk>/', views.booking_edit, name='booking_edit'),
    path('bookings/delete/<int:pk>/', views.booking_delete, name='booking_delete'),
    
    # Rooms & Pricing
    # path('rooms/', views.room_list, name='room_list'),
    # path('rooms/pricing/edit/', views.pricing_edit, name='pricing_edit'),
    # path('rooms/categories/edit/<int:pk>/', views.category_edit, name='category_edit'),
    
    
    path('rooms/', views.room_list, name='room_list'),

    path('rooms/add/', views.category_add, name='category_add'),
    path('rooms/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('rooms/delete/<int:pk>/', views.category_delete, name='category_delete'),

    path('pricing/add-edit/', views.pricing_add_edit, name='pricing_add_edit'),
    
    # Amenities
    path('amenities/', views.amenity_list, name='amenity_list'),
    path('amenities/create/', views.amenity_create, name='amenity_create'),
    path('amenities/edit/<int:pk>/', views.amenity_edit, name='amenity_edit'),
    path('amenities/delete/<int:pk>/', views.amenity_delete, name='amenity_delete'),
    
    # Banners
    path('banners/', views.banner_list, name='banner_list'),
    path('banners/create/', views.banner_create, name='banner_create'),
    path('banners/edit/<int:pk>/', views.banner_edit, name='banner_edit'),
    path('banners/delete/<int:pk>/', views.banner_delete, name='banner_delete'),
    
    # Blocked Dates
    path('blocked-dates/', views.blocked_date_list, name='blocked_date_list'),
    path('blocked-dates/create/', views.blocked_date_create, name='blocked_date_create'),
    path('blocked-dates/delete/<int:pk>/', views.blocked_date_delete, name='blocked_date_delete'),
    
    # Coupons
    path('coupons/', views.coupon_list, name='coupon_list'),
    path('coupons/create/', views.coupon_create, name='coupon_create'),
    path('coupons/delete/<int:pk>/', views.coupon_delete, name='coupon_delete'),
    
    # Testimonials
    path('testimonials/', views.testimonial_list, name='testimonial_list'),
    path('testimonials/delete/<int:pk>/', views.testimonial_delete, name='testimonial_delete'),
    
    # Gallery
    path('gallery/', views.gallery_list, name='gallery_list'),
    path('gallery/create/', views.gallery_create, name='gallery_create'),
    path('gallery/delete/<int:pk>/', views.gallery_delete, name='gallery_delete'),
    
    # Messages
    path('messages/', views.message_list, name='message_list'),
    
    # Users
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
]


















# urlpatterns = [
#     path('admin-test/', admin, name='admin_test'),
# ]


# from django.urls import path
# from . import views

# urlpatterns = [
#     path('admin-test/', admin, name='admin_test'),
#     path("", views.dashboard, name="admin_dashboard"),
#     path("bookings/", views.bookings, name="admin_booking_list"),
#     path("rooms/", views.rooms, name="admin_rooms"),
#     path("amenities/", views.amenities, name="admin_amenities"),
#     path("gallery/", views.gallery, name="admin_gallery"),
#     path("testimonials/", views.testimonials, name="admin_testimonials"),
#     path("offers/", views.offers, name="admin_offers"),
#     path("pricing/", views.pricing, name="admin_pricing"),
#     path("blocked-dates/", views.blocked_dates, name="admin_blocked_dates"),
#     path("messages/", views.messages, name="admin_messages"),
# ]
