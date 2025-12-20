from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta
from .models import (
    RoomCategory, Room, Amenity, Offer, Booking, 
    Testimonial, Gallery, ContactMessage,Coupon, VillaPricing
)
from .forms import BookingForm, ContactForm,TestimonialForm
from django.core.mail import send_mail

def home(request):
    """Homepage view"""
    featured_rooms = RoomCategory.objects.all()[:3]
    amenities = Amenity.objects.filter(is_featured=True)
    offers = Offer.objects.filter(is_active=True, valid_until__gte=datetime.now().date())[:4]
    testimonials = Testimonial.objects.filter(is_featured=True)[:6]
    gallery_images = Gallery.objects.filter(is_featured=True)[:8]
    
    context = {
        'featured_rooms': featured_rooms,
        'amenities': amenities,
        'offers': offers,
        'testimonials': testimonials,
        'gallery_images': gallery_images,
    }
    return render(request, 'resort/home.html', context)


def rooms(request):
    """Rooms listing view"""
    room_categories = RoomCategory.objects.all()
    
    # Filter by view type
    view_type = request.GET.get('view_type')
    if view_type:
        room_categories = room_categories.filter(view_type=view_type)
    
    # Filter by balcony
    has_balcony = request.GET.get('balcony')
    if has_balcony:
        room_categories = room_categories.filter(has_balcony=True)
    
    context = {
        'room_categories': room_categories,
    }
    return render(request, 'resort/rooms.html', context)


# def room_detail(request, slug):
#     """Room detail and booking view with date availability checking"""
#     room_category = get_object_or_404(RoomCategory, slug=slug)
#     available_rooms = room_category.rooms.filter(is_available=True)
    
#     # Get all booked dates for this room category
#     booked_dates = []
#     all_rooms_in_category = room_category.rooms.all()
    
#     # Get confirmed bookings for all rooms in this category
#     confirmed_bookings = Booking.objects.filter(
#         room__in=all_rooms_in_category,
#         status__in=['confirmed', 'pending'],
#         check_out__gte=datetime.now().date()
#     )
    
#     # Collect all booked date ranges
#     for booking in confirmed_bookings:
#         current_date = booking.check_in
#         while current_date < booking.check_out:
#             booked_dates.append(current_date.strftime('%Y-%m-%d'))
#             current_date += timedelta(days=1)
    
#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             check_in = form.cleaned_data['check_in']
#             check_out = form.cleaned_data['check_out']
            
#             # Check if any room is available for the selected dates
#             rooms_available = False
#             selected_room = None
            
#             for room in available_rooms:
#                 # Check if this room has any overlapping bookings
#                 overlapping_bookings = Booking.objects.filter(
#                     room=room,
#                     status__in=['confirmed', 'pending'],
#                     check_in__lt=check_out,
#                     check_out__gt=check_in
#                 )
                
#                 if not overlapping_bookings.exists():
#                     rooms_available = True
#                     selected_room = room
#                     break
            
#             if rooms_available and selected_room:
#                 booking = form.save(commit=False)
#                 booking.room = selected_room
                
#                 # Calculate total amount
#                 num_nights = (booking.check_out - booking.check_in).days
#                 booking.total_amount = room_category.base_price * num_nights
#                 booking.status = 'confirmed'
                
#                 booking.save()
#                 messages.success(request, f'Booking confirmed! Your booking ID is {booking.booking_id}')
#                 return redirect('booking_confirmation', booking_id=booking.booking_id)
#             else:
#                 messages.error(request, 'Sorry! All rooms are booked for the selected dates. Please choose different dates.')
#     else:
#         form = BookingForm()
    
#     context = {
#         'room_category': room_category,
#         'form': form,
#         'available_rooms_count': available_rooms.count(),
#         'booked_dates': booked_dates,
#     }
#     return render(request, 'resort/room_detail.html', context)

# def calculate_booking_cost(check_in, check_out):
#     """Calculate booking cost based on weekday/weekend pricing"""
#     pricing = VillaPricing.objects.first()
#     if not pricing:
#         pricing = VillaPricing.objects.create()
    
#     total_cost = 0
#     current_date = check_in
    
#     while current_date < check_out:
#         # 4 is Friday, 5 is Saturday (Weekend nights)
#         if current_date.weekday() in [4, 5]:
#             total_cost += pricing.weekend_price
#         else:
#             total_cost += pricing.weekday_price
#         current_date += timedelta(days=1)
            
#     return total_cost












# from datetime import timedelta
# from decimal import Decimal
# from .models import VillaPricing

# def calculate_booking_cost(check_in, check_out, guest_count, extra_guest_count):
#     pricing = VillaPricing.objects.first()
#     if not pricing:
#         pricing = VillaPricing.objects.create()

#     total_cost = Decimal(0)
#     current_date = check_in

#     nights = (check_out - check_in).days

#     while current_date < check_out:
#         # if current_date.weekday() in [4, 5]:
#         if current_date.weekday() in [5, 6]:

#             total_cost += pricing.weekend_price
#         else:
#             total_cost += pricing.weekday_price

#         current_date += timedelta(days=1)

#     # Extra Guest Charges
#     extra_cost = Decimal(extra_guest_count) * pricing.extra_guest_price * nights

#     total_cost += extra_cost

#     return total_cost


# def room_detail(request, slug):
#     """Room detail and booking view with GLOBAL villa availability checking"""
    
#     room_category = get_object_or_404(RoomCategory, slug=slug)

#     # ---- GET ALL BOOKED DATES ---- #
#     booked_dates = []
#     current_bookings = Booking.objects.filter(
#         status__in=['confirmed', 'pending'],
#         check_out__gt=datetime.now().date()
#     )

#     for booking in current_bookings:
#         date = booking.check_in
#         while date < booking.check_out:
#             booked_dates.append(date.strftime("%Y-%m-%d"))
#             date += timedelta(days=1)

#     # ---- VILLA PRICING ---- #
#     pricing = VillaPricing.objects.first()
#     if not pricing:
#         pricing = VillaPricing.objects.create()

#     calculated_total = 0  # default for frontend JS

#     if request.method == "POST":
#         form = BookingForm(request.POST)

#         if form.is_valid():

#             check_in = form.cleaned_data['check_in']
#             check_out = form.cleaned_data['check_out']
#             guest_count = form.cleaned_data['guest_count']

#             # extra guest count (above 15)
#             extra_guest_count = max(0, guest_count - 15)

#             # detect payment method
#             payment_method = request.POST.get("payment_method")

#             # --- BASE COST (weekday/weekend + extra guest) --- #
#             base_amount = calculate_booking_cost(check_in, check_out, guest_count, extra_guest_count)

#             # --- TAX CALCULATION --- #
#             tax_rate = Decimal("0.00")  # 12% GST
#             tax_amount = base_amount * tax_rate

#             subtotal = base_amount + tax_amount

#             # ----- COUPON HANDLING ----- #
#             discount = Decimal(0)
#             coupon_code = form.cleaned_data.get("coupon_code")

#             if coupon_code:
#                 try:
#                     coupon = Coupon.objects.get(code__iexact=coupon_code, is_active=True)
#                     discount = coupon.discount_amount
#                 except:
#                     messages.warning(request, "Invalid coupon code.")

#             total_after_coupon = subtotal - discount

#             # expose to template JS
#             calculated_total = float(total_after_coupon)

#             # ---- SAVE BOOKING OBJECT ---- #
#             booking = form.save(commit=False)
#             booking.extra_guest_count = extra_guest_count
#             booking.sub_total = subtotal
#             booking.tax_price = tax_amount
#             booking.coupon_applied = None

#             # ==== PAYMENT LOGIC ====
#             if payment_method == "partial_razorpay":
#                 booking.total_amount = round(total_after_coupon * Decimal("0.30"), 2)
#                 booking.remaining_amount = round(total_after_coupon - booking.total_amount, 2)

#             elif payment_method == "full_razorpay":
#                 booking.total_amount = total_after_coupon
#                 booking.remaining_amount = 0

#             else:  # Pay at farmhouse
#                 booking.total_amount = 0
#                 booking.remaining_amount = total_after_coupon

#             booking.payment_method = payment_method
#             booking.status = "pending"

#             booking.save()

#             messages.success(request, "Booking request received. Proceed to payment if applicable.")
#             return redirect("booking_confirmation", booking_id=booking.booking_id)

#     else:
#         form = BookingForm()

#     context = {
#         "room_category": room_category,
#         "form": form,
#         "booked_dates": booked_dates,
#         "pricing": pricing,
#         "calculated_total": calculated_total,  # 👈 important for JS
#         "extra_price": float(pricing.extra_guest_price),
#     }

#     return render(request, "resort/room_detail.html", context)

from datetime import timedelta, datetime
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import VillaPricing, Booking, RoomCategory, Coupon
from .forms import BookingForm


def calculate_booking_cost(check_in, check_out, guest_count, extra_guest_count):
    pricing = VillaPricing.objects.first()
    if not pricing:
        pricing = VillaPricing.objects.create()

    total_cost = Decimal(0)
    current_date = check_in

    nights = (check_out - check_in).days

    while current_date < check_out:

        # Weekend means Saturday (5) & Sunday (6)
        if current_date.weekday() in [5, 6]:
            total_cost += pricing.weekend_price
        else:
            total_cost += pricing.weekday_price

        current_date += timedelta(days=1)

    # Extra Guest Charges
    extra_cost = Decimal(extra_guest_count) * pricing.extra_guest_price * nights
    total_cost += extra_cost

    return total_cost



# def room_detail(request, slug):
#     room_category = get_object_or_404(RoomCategory, slug=slug)

#     # Get booked dates
#     booked_dates = []
#     current_bookings = Booking.objects.filter(
#         status__in=['confirmed', 'pending'],
#         check_out__gt=datetime.now().date()
#     )

#     for booking in current_bookings:
#         date = booking.check_in
#         while date < booking.check_out:
#             booked_dates.append(date.strftime("%Y-%m-%d"))
#             date += timedelta(days=1)

#     pricing = VillaPricing.objects.first()
#     if not pricing:
#         pricing = VillaPricing.objects.create()

#     calculated_total = 0

#     if request.method == "POST":
#         form = BookingForm(request.POST)

#         if form.is_valid():

#             check_in = form.cleaned_data['check_in']
#             check_out = form.cleaned_data['check_out']
#             guest_count = form.cleaned_data['guest_count']

#             # Use USER INPUT extra guest count
#             extra_guest_count = form.cleaned_data['extra_guest_count']

#             payment_method = request.POST.get("payment_method")

#             base_amount = calculate_booking_cost(
#                 check_in,
#                 check_out,
#                 guest_count,
#                 extra_guest_count
#             )

#             # TAX (currently set to 0)
#             tax_rate = Decimal("0.00")
#             tax_amount = base_amount * tax_rate

#             subtotal = base_amount + tax_amount

#             # COUPON
#             discount = Decimal(0)
#             coupon_code = form.cleaned_data.get("coupon_code")

#             if coupon_code:
#                 try:
#                     coupon = Coupon.objects.get(code__iexact=coupon_code, is_active=True)
#                     discount = coupon.discount_amount
#                 except Coupon.DoesNotExist:
#                     messages.warning(request, "Invalid coupon code.")

#             total_after_coupon = subtotal - discount

#             calculated_total = float(total_after_coupon)

#             booking = form.save(commit=False)

#             booking.extra_guest_count = extra_guest_count
#             booking.sub_total = subtotal
#             booking.tax_price = tax_amount

#             # Payment Logic
#             if payment_method == "partial_razorpay":
#                 booking.total_amount = round(total_after_coupon * Decimal("0.30"), 2)
#                 booking.remaining_amount = round(total_after_coupon - booking.total_amount, 2)

#             elif payment_method == "full_razorpay":
#                 booking.total_amount = total_after_coupon
#                 booking.remaining_amount = 0

#             else:  # Pay at farmhouse
#                 booking.total_amount = 0
#                 booking.remaining_amount = total_after_coupon

#             booking.payment_method = payment_method
#             booking.status = "pending"

#             booking.save()

#             messages.success(request, "Booking request received. Proceed to payment if applicable.")

#             return redirect("booking_confirmation", booking_id=booking.booking_id)

#     else:
#         form = BookingForm()

#     context = {
#         "room_category": room_category,
#         "form": form,
#         "booked_dates": booked_dates,
#         "pricing": pricing,
#         "calculated_total": calculated_total,
#         "extra_price": float(pricing.extra_guest_price),
#     }

#     return render(request, "resort/room_detail.html", context)


from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_booking_emails(booking):
    # User Email
    user_subject = "Booking Confirmation – Vivaan Farmhouse"
    user_html = render_to_string("emails/user_booking_email.html", {
        "booking": booking
    })

    user_email = EmailMultiAlternatives(
        user_subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        [booking.guest_email]
    )
    user_email.attach_alternative(user_html, "text/html")
    user_email.send()

    # Admin Email
    admin_subject = "New Booking Received"
    admin_html = render_to_string("emails/admin_booking_email.html", {
        "booking": booking
    })

    admin_email = EmailMultiAlternatives(
        admin_subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL]  # configure in settings.py
    )
    admin_email.attach_alternative(admin_html, "text/html")
    admin_email.send()


def room_detail(request, slug):
    room_category = get_object_or_404(RoomCategory, slug=slug)

    booked_dates = []
    current_bookings = Booking.objects.filter(
        status__in=['confirmed', 'pending'],
        check_out__gt=datetime.now().date()
    )

    for booking in current_bookings:
        date = booking.check_in
        while date < booking.check_out:
            booked_dates.append(date.strftime("%Y-%m-%d"))
            date += timedelta(days=1)

    pricing = VillaPricing.objects.first()
    if not pricing:
        pricing = VillaPricing.objects.create()

    calculated_total = 0

    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():

            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']
            guest_count = form.cleaned_data['guest_count']
            extra_guest_count = form.cleaned_data['extra_guest_count']

            payment_method = request.POST.get("payment_method")

            base_amount = calculate_booking_cost(
                check_in, check_out, guest_count, extra_guest_count
            )

            # TAX
            tax_rate = Decimal("0.00")
            tax_amount = base_amount * tax_rate

            subtotal = base_amount + tax_amount

            # COUPON DISCOUNT
            discount = Decimal(0)
            coupon_code = form.cleaned_data.get("coupon_code")

            if coupon_code:
                try:
                    coupon = Coupon.objects.get(code__iexact=coupon_code, is_active=True)
                    discount = coupon.discount_amount
                except Coupon.DoesNotExist:
                    messages.warning(request, "Invalid coupon code.")

            # Apply discount
            total_after_coupon = subtotal - discount
            calculated_total = float(total_after_coupon)

            booking = form.save(commit=False)

            booking.extra_guest_count = extra_guest_count
            booking.sub_total = subtotal
            booking.tax_price = tax_amount

            # 👇 Store coupon discount here
            booking.disc_price = discount

            # PAYMENT LOGIC
            if payment_method == "partial_razorpay":
                booking.total_amount = round(total_after_coupon * Decimal("0.30"), 2)
                booking.remaining_amount = round(total_after_coupon - booking.total_amount, 2)

            elif payment_method == "full_razorpay":
                booking.total_amount = total_after_coupon
                booking.remaining_amount = 0

            else:
                booking.total_amount = 0
                booking.remaining_amount = total_after_coupon

            booking.payment_method = payment_method
            booking.status = "pending"
            booking.save()
            send_booking_emails(booking)
            messages.success(request, "Booking request received!")

            return redirect("booking_confirmation", booking_id=booking.booking_id)

    else:
        form = BookingForm()

    context = {
        "room_category": room_category,
        "form": form,
        "booked_dates": booked_dates,
        "pricing": pricing,
        "calculated_total": calculated_total,
        "extra_price": float(pricing.extra_guest_price),
    }

    return render(request, "resort/room_detail.html", context)




def view_invoice(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    return render(request, "emails/invoice.html", {"booking": booking})






# def room_detail(request, slug):
#     """Room detail and booking view with GLOBAL villa availability checking"""
#     room_category = get_object_or_404(RoomCategory, slug=slug)
    
#     # Get all booked dates for the ENTIRE VILLA
#     booked_dates = []
    
#     # Get all confirmed/pending bookings that are active
#     # We ignore the specific room, as any booking blocks the villa
#     current_bookings = Booking.objects.filter(
#         status__in=['confirmed', 'pending'],
#         check_out__gt=datetime.now().date()
#     )
    
#     # Collect all booked date ranges
#     for booking in current_bookings:
#         current_date = booking.check_in
#         while current_date < booking.check_out:
#             booked_dates.append(current_date.strftime('%Y-%m-%d'))
#             current_date += timedelta(days=1)
    
#     # Pricing info for display
#     pricing = VillaPricing.objects.first()
#     if not pricing:
#         pricing = VillaPricing.objects.create()

#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             check_in = form.cleaned_data['check_in']
#             check_out = form.cleaned_data['check_out']
#             coupon_code = form.cleaned_data.get('coupon_code')
            
#             # Check ID check_out > check_in (handled in form clean but good to be safe)
            
#             # GLOBAL AVAILABILITY CHECK
#             # Check if ANY booking overlaps with the requested dates
#             overlapping_bookings = Booking.objects.filter(
#                 status__in=['confirmed', 'pending'],
#                 check_in__lt=check_out, 
#                 check_out__gt=check_in
#             )
            
#             if overlapping_bookings.exists():
#                  messages.error(request, 'Sorry! The entire villa is already booked for these dates. Please choose different dates.')
#             else:
#                 booking = form.save(commit=False)
#                 # booking.room is NULLABLE now, so we don't assign it (or we could assign a dummy)
#                 booking.room = None 
                
#                 # Calculate total amount
#                 base_amount = calculate_booking_cost(check_in, check_out)
#                 discount = 0
                
#                 # Handle Coupon
#                 if coupon_code:
#                     try:
#                         coupon = Coupon.objects.get(code__iexact=coupon_code, is_active=True, valid_until__gte=datetime.now().date())
#                         if coupon.valid_from <= datetime.now().date():
#                             discount = coupon.discount_amount
#                             booking.coupon_applied = coupon
#                             messages.success(request, f'Coupon {coupon.code} applied! Saved {discount}')
#                         else:
#                              messages.warning(request, 'Coupon is not yet valid.')
#                     except Coupon.DoesNotExist:
#                         messages.warning(request, 'Invalid coupon code.')

#                 booking.total_amount = max(0, base_amount - discount)
#                 booking.status = 'confirmed' # Or pending
                
#                 booking.save()

#                 # Send Confirmation Email
#                 subject = f"Booking Confirmed - {booking.booking_id}"
#                 message = f"""
#                 Dear {booking.guest_name},

#                 Thank you for booking with Vivaan Farmhouse!

#                 Your booking details:
#                 Booking ID: {booking.booking_id}
#                 Check-in: {booking.check_in} {f"({booking.check_in_time})" if booking.check_in_time else ""}
#                 Check-out: {booking.check_out} {f"({booking.check_out_time})" if booking.check_out_time else ""}
#                 Total Amount: ₹{booking.total_amount}

#                 We look forward to hosting you.
                
#                 Regards,
#                 Vivaan Farmhouse Team
#                 """


#                 recipient_list = [booking.guest_email]
                
#                 try:
#                     send_mail(
#                         subject, 
#                         message, 
#                         'reservations@vivaanfarmhouse.com', # From email 
#                         recipient_list, 

#                         fail_silently=True # Prevent error if email backend is not configured correctly
#                     )
#                 except Exception as e:
#                     print(f"Error sending email: {e}")

#                 messages.success(request, f'Booking confirmed! Your booking ID is {booking.booking_id}')
#                 return redirect('booking_confirmation', booking_id=booking.booking_id)

#     else:
#         form = BookingForm()
    
#     context = {
#         'room_category': room_category,
#         'form': form,
#         'booked_dates': booked_dates,
#         'pricing': pricing,
#     }
#     return render(request, 'resort/room_detail.html', context)


def booking_confirmation(request, booking_id):
    """Booking confirmation view"""
    booking = get_object_or_404(Booking, booking_id=booking_id)
    context = {
        'booking': booking,
    }
    return render(request, 'resort/booking_confirmation.html', context)


def amenities_view(request):
    """Amenities view"""
    amenities = Amenity.objects.all()
    context = {
        'amenities': amenities,
    }
    return render(request, 'resort/amenities.html', context)


def offers_view(request):
    """Offers view"""
    active_offers = Offer.objects.filter(
        is_active=True, 
        valid_until__gte=datetime.now().date()
    )
    context = {
        'offers': active_offers,
    }
    return render(request, 'resort/offers.html', context)


def gallery_view(request):
    """Gallery view"""
    category = request.GET.get('category')
    if category:
        images = Gallery.objects.filter(category=category)
    else:
        images = Gallery.objects.all()
    
    context = {
        'images': images,
        'categories': Gallery._meta.get_field('category').choices,
    }
    return render(request, 'resort/gallery.html', context)


# def contact(request):
#     """Contact view"""
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
#             return redirect('contact')
#     else:
#         form = ContactForm()
    
#     context = {
#         'form': form,
#     }
#     return render(request, 'resort/contact.html', context)

# def contact(request):
#     """Contact view"""
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             contact_msg = form.save()
            
#             # Send Email to Admin
#             try:
#                 subject = f"New Contact Message: {contact_msg.subject}"
#                 message = f"""
#                 You have received a new contact message.

#                 From: {contact_msg.name} ({contact_msg.email})
#                 Phone: {contact_msg.phone}
#                 Subject: {contact_msg.subject}
                
#                 Message:
#                 {contact_msg.message}
#                 """
#                 # Send to admin email (you can configure this in settings or use hardcoded for now)
#                 admin_email = 'admin@vivaanfarmhouse.com' 
#                 send_mail(
#                     subject, 
#                     message, 
#                     'website@vivaanfarmhouse.com', 
#                     [admin_email], 
 
#                     fail_silently=True
#                 )
#             except Exception as e:
#                 print(f"Error sending contact email: {e}")

#             messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
#             return redirect('contact')

#     else:
#         form = ContactForm()
    
#     context = {
#         'form': form,
#     }
#     return render(request, 'resort/contact.html', context)







from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from .forms import ContactForm


def contact(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            contact_msg = form.save()

            context = {
                'name': contact_msg.name,
                'email': contact_msg.email,
                'phone': contact_msg.phone,
                'subject': contact_msg.subject,
                'message': contact_msg.message
            }

            # ========== SEND EMAIL TO ADMIN ==========

            admin_html = render_to_string("contact/admin_contact.html", context)

            admin_email = EmailMultiAlternatives(
                subject=f"New Contact Message: {contact_msg.subject}",
                body="",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.ADMIN_EMAIL],
            )
            admin_email.attach_alternative(admin_html, "text/html")
            admin_email.send()

            # ========== SEND EMAIL TO USER ==========

            user_html = render_to_string("contact/user_contact.html", context)

            user_email = EmailMultiAlternatives(
                subject="Thank You for Contacting Strawberry King Resort",
                body="",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[contact_msg.email],
            )
            user_email.attach_alternative(user_html, "text/html")
            user_email.send()

            # messages.success(request, "Thank you! Your message has been sent.")
            return redirect('home')

    else:
        form = ContactForm()

    return render(request, 'resort/home.html', {'form': form})


def about(request):
    """About view"""
    return render(request, 'resort/about.html')



def cancel_booking(request):
    """View to search and cancel a booking"""
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        email = request.POST.get('email')
        
        try:
            booking = Booking.objects.get(booking_id=booking_id, guest_email=email)
            
            # Check if booking can be cancelled (e.g., checks against current time)
            if booking.status == 'cancelled':
                messages.error(request, 'This booking is already cancelled.')
            elif booking.check_in <= datetime.now().date():
                 messages.error(request, 'Cannot cancel a booking that has already started or passed.')
            else:
                booking.status = 'cancelled'
                booking.cancellation_reason = request.POST.get('reason', '')
                booking.save()

                
                # Send Cancellation Email
                try:
                    subject = f"Booking Cancelled - {booking.booking_id}"
                    message = f"""
                    Dear {booking.guest_name},

                    Your booking with ID {booking.booking_id} has been successfully cancelled.
                    
                    Reason: {booking.cancellation_reason}

                    We hope to greet you at Vivaan Farmhouse in the future.


                    Regards,
                    Vivaan Farmhouse Team
                    """
                    send_mail(
                        subject, 
                        message, 
                        'reservations@vivaanfarmhouse.com', 

                        [booking.guest_email], 
                        fail_silently=True
                    )
                except Exception as e:
                    print(f"Error sending cancellation email: {e}")

                messages.success(request, 'Booking successfully cancelled.')
                return redirect('booking_confirmation', booking_id=booking.booking_id)

        except Booking.DoesNotExist:
            messages.error(request, 'No booking found with these details. Please check your Booking ID and Email.')
            
    return render(request, 'resort/cancel_booking.html')




def leave_review(request):
    """View to list reviews and submit a new one"""
    reviews = Testimonial.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your review!')
            return redirect('leave_review')
    else:
        form = TestimonialForm()
    
    context = {
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'resort/leave_review.html', context)

