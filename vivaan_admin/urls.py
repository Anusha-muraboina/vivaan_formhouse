from django.urls import path
from .views import admin

# urlpatterns = [
#     path('admin-test/', admin, name='admin_test'),
# ]


from django.urls import path
from . import views

urlpatterns = [
    path('admin-test/', admin, name='admin_test'),
    path("", views.dashboard, name="admin_dashboard"),
    path("bookings/", views.bookings, name="admin_booking_list"),
    path("rooms/", views.rooms, name="admin_rooms"),
    path("amenities/", views.amenities, name="admin_amenities"),
    path("gallery/", views.gallery, name="admin_gallery"),
    path("testimonials/", views.testimonials, name="admin_testimonials"),
    path("offers/", views.offers, name="admin_offers"),
    path("pricing/", views.pricing, name="admin_pricing"),
    path("blocked-dates/", views.blocked_dates, name="admin_blocked_dates"),
    path("messages/", views.messages, name="admin_messages"),
]
