from django.contrib import admin
from .models import (
    RoomCategory, Room, Amenity, Offer, Booking, Coupon,
    Testimonial, Gallery, ContactMessage,VillaPricing,MainBanner
)

admin.site.register(Coupon)
admin.site.register(MainBanner)
admin.site.register(VillaPricing)
@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'size_sqft', 'max_occupancy', 'base_price', 'view_type', 'has_balcony']
    list_filter = ['view_type', 'has_balcony', 'floor']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'category', 'is_available']
    list_filter = ['category', 'is_available']
    search_fields = ['room_number']


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_featured']
    list_filter = ['is_featured']
    search_fields = ['name']


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'discount_percentage', 'valid_from', 'valid_until', 'is_active']
    list_filter = ['is_active', 'valid_from']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'guest_name', 'room', 'check_in', 'check_out', 'status', 'total_amount']
    list_filter = ['status', 'check_in', 'check_out']
    search_fields = ['booking_id', 'guest_name', 'guest_email']
    readonly_fields = ['booking_id', 'created_at', 'updated_at']
    date_hierarchy = 'check_in'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['guest_name', 'rating', 'is_featured', 'created_at']
    list_filter = ['rating', 'is_featured']
    search_fields = ['guest_name', 'comment']


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'created_at']
    list_filter = ['category', 'is_featured']
    search_fields = ['title']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']



# admin.py
from .models import BlockedDate

@admin.register(BlockedDate)
class BlockedDateAdmin(admin.ModelAdmin):
    list_display = ("start_date", "end_date", "reason")
    list_filter = ("start_date",)
