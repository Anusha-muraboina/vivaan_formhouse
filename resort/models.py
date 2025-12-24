from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor.fields import RichTextField
from decimal import Decimal
from django.core.exceptions import ValidationError

class MainBanner(models.Model):
    """Main banner for the resort"""
    title = models.CharField(max_length=200,null=True,blank=True )
    subtitle = models.CharField(max_length=200,null=True,blank=True)
    image = models.ImageField(upload_to='banners/')
    page_title = models.CharField(max_length=200, null=True, blank=True)
    meta_keyword = models.CharField(max_length=200, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    slot_position = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.title
    
class RoomCategory(models.Model):
    """Different room categories in the resort"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = RichTextField()
    size_sqft = models.IntegerField()
    max_occupancy = models.IntegerField()
    floor = models.CharField(max_length=50)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='rooms/', null=True, blank=True)
    view_type = models.CharField(max_length=100, choices=[
        ('garden', 'Garden View'),
        ('valley', 'Valley View'),
        ('pool', 'Pool View'),
        ('standard', 'Standard'),
    ], default='standard')
    has_balcony = models.BooleanField(default=False)
    has_bathtub = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Room Categories'
        ordering = ['-base_price']

    def __str__(self):
        return self.name


# class Room(models.Model):
#     """Individual rooms in the resort"""
#     category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE, related_name='rooms')
#     room_number = models.CharField(max_length=10, unique=True)
#     is_available = models.BooleanField(default=True)

#     def __str__(self):
#         return f"{self.category.name} - Room {self.room_number}"


class Amenity(models.Model):
    """Resort amenities"""
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    amenity_image = models.ImageField(upload_to='amenities/', null=True, blank=True)
    slot_position = models.IntegerField(null=True, blank=True)
    class Meta:
        verbose_name_plural = 'Amenities'
        ordering = ['name']

    def __str__(self):
        return self.name


class Offer(models.Model):
    """Special offers and deals"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    discount_percentage = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    terms = models.TextField(blank=True)
    valid_from = models.DateField()
    valid_until = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Coupon(models.Model):
    """Discount coupons"""
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateField()
    valid_until = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.discount_amount}"


class VillaPricing(models.Model):
    """Global pricing for the entire villa"""
    weekday_price = models.DecimalField(max_digits=10, decimal_places=2, default=15000.00)
    weekend_price = models.DecimalField(max_digits=10, decimal_places=2, default=20000.00)
    extra_guest_price = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Weekday: {self.weekday_price}, Weekend: {self.weekend_price}"

    class Meta:
        verbose_name_plural = "Villa Pricing"



class Booking(models.Model):
    """Guest bookings"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('farmhouse', 'Pay at Farmhouse'),               # no online payment
        ('partial_razorpay', 'Pay 30% via Razorpay'),    # 30% online, 70% later
        ('full_razorpay', 'Full Payment via Razorpay'),  # 100% online
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('partial','partial'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    booking_id = models.CharField(max_length=20, unique=True, editable=False)
    # room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)

    guest_name = models.CharField(max_length=200)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=15)
    guest_count = models.IntegerField(default=15)
    extra_guest_count = models.IntegerField(default=0 ,null=True ,blank=True)
    
    check_in = models.DateField()
    check_in_time = models.TimeField(null=True, blank=True)
    check_out = models.DateField()
    check_out_time = models.TimeField(null=True, blank=True)

    special_requests = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2 ,null=True,blank=True)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    tax_price = models.DecimalField(max_digits=10, decimal_places=2 ,null=True,blank=True)
    offer_applied = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True)
    # coupon_applied = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True)
    disc_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))
    cancellation_reason = models.TextField(blank=True, null=True)
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='farmhouse'
    )
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)    
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     ordering = ['-created_at']
    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=["guest_email", "check_in", "check_out", "payment_method"],
                name="unique_booking_guest_dates"
            )
        ]
    def save(self, *args, **kwargs):
        if not self.booking_id:
            import random
            import string
            self.booking_id = 'SKR' + ''.join(random.choices(string.digits, k=8))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_id} - {self.guest_name}"

    @property
    def num_nights(self):
        return (self.check_out - self.check_in).days
    @property
    def final_total(self):
        return (self.sub_total or 0) - (self.disc_price or 0)


# models.py
class BlockedDate(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("End date must be after start date.")

        overlaps = BlockedDate.objects.filter(
            start_date__lte=self.end_date,
            end_date__gte=self.start_date
        ).exclude(pk=self.pk)

        if overlaps.exists():
            raise ValidationError("These dates overlap with an existing blocked range.")

    def __str__(self):
        return f"Blocked: {self.start_date} → {self.end_date}"


class Testimonial(models.Model):
    """Guest testimonials"""
    guest_name = models.CharField(max_length=200)
    guest_location = models.CharField(max_length=100, blank=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    comment = models.TextField()
    slot_position = models.IntegerField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.guest_name} - {self.rating} stars"


class Gallery(models.Model):
    """Resort gallery images"""
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=50, choices=[
        ('rooms', 'Rooms'),
        ('dining', 'Dining'),
        ('facilities', 'Facilities'),
        ('views', 'Views'),
        ('events', 'Events'),
    ], default='views')
    is_featured = models.BooleanField(default=False)
    slot_position = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Gallery'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    """Contact form messages"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
