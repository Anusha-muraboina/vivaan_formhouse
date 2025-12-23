from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta
from .models import (
    RoomCategory, Room, Amenity, Offer, Booking, MainBanner,
    Testimonial, Gallery, ContactMessage,Coupon, VillaPricing
)
from .forms import BookingForm, ContactForm,TestimonialForm
from django.core.mail import send_mail

def home(request):
    """Homepage view"""
    banners = MainBanner.objects.filter(active=True).order_by("slot_position")
    featured_rooms = RoomCategory.objects.all()[:3]
    amenities = Amenity.objects.filter(is_featured=True)
    offers = Offer.objects.filter(
        is_active=True,
        valid_until__gte=datetime.now().date()
    )[:4]

    testimonials = Testimonial.objects.filter(
            is_featured=True
        ).order_by("slot_position")[:6]

    gallery_images = Gallery.objects.filter(
            is_featured=True
        ).order_by("slot_position")[:8]

    context = {
        'featured_rooms': featured_rooms,
        'amenities': amenities,
        "banners": banners,
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

from django.views.decorators.csrf import csrf_exempt










# utils/razorpay.py (recommended)
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)



# # views.py
# def razorpay_payment(request, booking_id):
#     booking = get_object_or_404(Booking, booking_id=booking_id)

#     # Safety check
#     if booking.payment_method == "partial_razorpay":
#         amount = booking.total_amount
#     elif booking.payment_method == "full_razorpay":
#         amount = booking.total_amount
#     else:
#         return redirect("booking_confirmation", booking_id=booking.booking_id)

#     return render(request, "resort/razorpay_payment.html", {
#         "booking": booking,
#         "amount": amount
#     })


# @csrf_exempt
# def create_razorpay_order(request):

#     if request.method != "POST":
#         return JsonResponse({"error": "Invalid request"}, status=400)

#     booking_id = request.POST.get("booking_id")
#     amount = request.POST.get("amount")

#     if not booking_id or not amount:
#         return JsonResponse({"error": "Missing data"}, status=400)

#     booking = get_object_or_404(Booking, booking_id=booking_id)

#     razorpay_amount = int(float(amount) * 100)

#     order = razorpay_client.order.create({
#         "amount": razorpay_amount,
#         "currency": "INR",
#         "payment_capture": 1
#     })

#     booking.transaction_id = order["id"]
#     booking.save(update_fields=["transaction_id"])

#     return JsonResponse({
#         "order_id": order["id"],
#         "key": settings.RAZORPAY_KEY_ID,
#         "amount": razorpay_amount,
#         "name": booking.guest_name,
#         "email": booking.guest_email,
#         "contact": booking.guest_phone,
#     })


# @csrf_exempt
# def verify_razorpay_payment(request):
#     data = request.POST

#     try:
#         razorpay_client.utility.verify_payment_signature({
#             "razorpay_order_id": data.get("razorpay_order_id"),
#             "razorpay_payment_id": data.get("razorpay_payment_id"),
#             "razorpay_signature": data.get("razorpay_signature")
#         })

#         booking = get_object_or_404(
#             Booking,
#             transaction_id=data.get("razorpay_order_id")
#         )

#         booking.payment_id = data.get("razorpay_payment_id")
#         booking.payment_status = "paid"
#         booking.status = "confirmed"
#         booking.save()

#         # ✅ SEND EMAIL AFTER PAYMENT SUCCESS
#         send_booking_emails(booking)

#         return JsonResponse({"status": "success"})

#     except Exception as e:
#         return JsonResponse({"status": "failed", "error": str(e)}, status=400)










def send_booking_emails(booking):
    
        # CC Emails
    cc_recipients = settings.CC_EMAIL
    # User Email
    user_subject = "Booking Confirmation – Vivaan Farmhouse"
    user_html = render_to_string("emails/user_booking_email.html", {
        "booking": booking
    })

    user_email = EmailMultiAlternatives(
        user_subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        [booking.guest_email],
        cc=cc_recipients  
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
        [settings.ADMIN_EMAIL], # configure in settings.py
        cc=cc_recipients  
    )
    admin_email.attach_alternative(admin_html, "text/html")
    admin_email.send()


# def room_detail(request, slug):
#     room_category = get_object_or_404(RoomCategory, slug=slug)

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
#             extra_guest_count = form.cleaned_data['extra_guest_count']

#             payment_method = request.POST.get("payment_method")

#             base_amount = calculate_booking_cost(
#                 check_in, check_out, guest_count, extra_guest_count
#             )

#             # TAX
#             tax_rate = Decimal("0.00")
#             tax_amount = base_amount * tax_rate

#             subtotal = base_amount + tax_amount

#             # COUPON DISCOUNT
#             discount = Decimal(0)
#             coupon_code = form.cleaned_data.get("coupon_code")

#             if coupon_code:
#                 try:
#                     coupon = Coupon.objects.get(code__iexact=coupon_code, is_active=True)
#                     discount = coupon.discount_amount
#                 except Coupon.DoesNotExist:
#                     messages.warning(request, "Invalid coupon code.")

#             # Apply discount
#             total_after_coupon = subtotal - discount
#             calculated_total = float(total_after_coupon)

#             booking = form.save(commit=False)

#             booking.extra_guest_count = extra_guest_count
#             booking.sub_total = subtotal
#             booking.tax_price = tax_amount

#             # 👇 Store coupon discount here
#             booking.disc_price = discount

#             # PAYMENT LOGIC
#             if payment_method == "partial_razorpay":
#                 booking.total_amount = round(total_after_coupon * Decimal("0.30"), 2)
#                 booking.remaining_amount = round(total_after_coupon - booking.total_amount, 2)
#                 booking.payment_status = "partial"
#             elif payment_method == "full_razorpay":
#                 booking.total_amount = total_after_coupon
#                 booking.remaining_amount = 0
#                 booking.payment_status = "paid"

#             else:
#                 booking.total_amount = 0
#                 booking.remaining_amount = total_after_coupon
#                 booking.payment_status = "pending"

#             booking.payment_method = payment_method
            
            
#             booking.status = "pending"
#             booking.save()

#             # 🔥 Redirect to Razorpay if online payment
#             if payment_method in ["partial_razorpay", "full_razorpay"]:
#                 return redirect("razorpay_payment", booking_id=booking.booking_id)

#             # Pay at farmhouse
#             send_booking_emails(booking)
#             messages.success(request, "Booking request received!")
#             return redirect("booking_confirmation", booking_id=booking.booking_id)

#             # booking.status = "confirmed"
#             # booking.save()
#             # send_booking_emails(booking)
#             # messages.success(request, "Booking request received!")

#             # return redirect("booking_confirmation", booking_id=booking.booking_id)

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

# from django.http import JsonResponse

# def validate_coupon(request):
#     code = request.GET.get("code", "")
#     try:
#         coupon = Coupon.objects.get(code__iexact=code, is_active=True)
#         return JsonResponse({"valid": True, "discount": float(coupon.discount_amount)})
#     except:
#         return JsonResponse({"valid": False, "discount": 0})







from decimal import Decimal
from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib import messages

from .models import Booking, RoomCategory, VillaPricing, Coupon
from .forms import BookingForm



def room_detail(request, slug):
    room_category = get_object_or_404(RoomCategory, slug=slug)

    # ===== BOOKED DATES =====
    booked_dates = []
    bookings = Booking.objects.filter(
        status__in=["confirmed", "pending"],
        check_out__gt=datetime.now().date()
    )

    for b in bookings:
        d = b.check_in
        while d < b.check_out:
            booked_dates.append(d.strftime("%Y-%m-%d"))
            d += timedelta(days=1)

    pricing = VillaPricing.objects.first() or VillaPricing.objects.create()

    # ===== AJAX SUBMIT =====
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        form = BookingForm(request.POST)
        if not form.is_valid():
            return JsonResponse({"error": "Invalid form"}, status=400)

        payment_method = request.POST.get("payment_method")

        base_amount = calculate_booking_cost(
            form.cleaned_data["check_in"],
            form.cleaned_data["check_out"],
            form.cleaned_data["guest_count"],
            form.cleaned_data["extra_guest_count"],
        )

        discount = Decimal("0.00")
        if form.cleaned_data.get("coupon_code"):
            try:
                coupon = Coupon.objects.get(
                    code__iexact=form.cleaned_data["coupon_code"],
                    is_active=True
                )
                discount = coupon.discount_amount
            except Coupon.DoesNotExist:
                pass

        total = base_amount - discount

        # ================= CASH =================
        if payment_method == "farmhouse":
            booking = form.save(commit=False)
            booking.sub_total = base_amount
            booking.disc_price = discount
            booking.total_amount = 0
            booking.remaining_amount = total
            booking.payment_status = "pending"
            booking.status = "confirmed"
            booking.save()

            send_booking_emails(booking)

            return JsonResponse({
                "redirect": True,
                "url": reverse("booking_confirmation", args=[booking.booking_id])
            })

        # ================= RAZORPAY =================
        request.session["pending_booking"] = {
            "data": request.POST.dict(),
            "base": str(base_amount),
            "discount": str(discount),
            "total": str(total),
        }

        return JsonResponse({
            "razorpay": True,
            "amount": float(total)
        })

    # ===== NORMAL PAGE LOAD =====
    return render(request, "resort/room_detail.html", {
        "room_category": room_category,
        "form": BookingForm(),
        "booked_dates": booked_dates,
        "pricing": pricing,
        "extra_price": float(pricing.extra_guest_price),
    })


# def room_detail(request, slug):
#     room_category = get_object_or_404(RoomCategory, slug=slug)

#     # ===== BOOKED DATES =====
#     booked_dates = []
#     current_bookings = Booking.objects.filter(
#         status__in=["confirmed", "pending"],
#         check_out__gt=datetime.now().date()
#     )

#     for booking in current_bookings:
#         d = booking.check_in
#         while d < booking.check_out:
#             booked_dates.append(d.strftime("%Y-%m-%d"))
#             d += timedelta(days=1)


#     pricing = VillaPricing.objects.first() or VillaPricing.objects.create()
#     calculated_total = 0

#     # ===== AJAX SUBMIT (ONE PAGE PAYMENT) =====
#     if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
#         form = BookingForm(request.POST)

#         if not form.is_valid():
#             return JsonResponse({"error": "Invalid form"}, status=400)

#         check_in = form.cleaned_data["check_in"]
#         check_out = form.cleaned_data["check_out"]
#         guest_count = form.cleaned_data["guest_count"]
#         extra_guest_count = form.cleaned_data["extra_guest_count"]
#         payment_method = request.POST.get("payment_method")

#         base_amount = calculate_booking_cost(
#             check_in, check_out, guest_count, extra_guest_count
#         )

#         # ===== COUPON =====
#         discount = Decimal("0.00")
#         coupon_code = form.cleaned_data.get("coupon_code")
#         if coupon_code:
#             try:
#                 coupon = Coupon.objects.get(code__iexact=coupon_code, is_active=True)
#                 discount = coupon.discount_amount
#             except Coupon.DoesNotExist:
#                 pass

#         total = base_amount - discount

#         booking = form.save(commit=False)
#         booking.sub_total = base_amount
#         booking.disc_price = discount
#         booking.payment_method = payment_method
#         booking.status = "pending"

#         if payment_method == "partial_razorpay":
#             booking.total_amount = round(total * Decimal("0.30"), 2)
#             booking.remaining_amount = total - booking.total_amount
#             booking.payment_status = "partial"

#         elif payment_method == "full_razorpay":
#             booking.total_amount = total
#             booking.remaining_amount = 0
#             booking.payment_status = "paid"

#         else:  # Pay at farmhouse
#             booking.total_amount = 0
#             booking.remaining_amount = total
#             booking.payment_status = "pending"

#         booking.save()

#         # ===== CASH FLOW =====
#         if payment_method == "farmhouse":
#             send_booking_emails(booking)
#             return JsonResponse({
#                 "redirect": True,
#                 "url": reverse("booking_confirmation", args=[booking.booking_id])
#             })

#         # ===== ONLINE PAYMENT =====
#         return JsonResponse({
#             "razorpay": True,
#             "booking_id": booking.booking_id,
#             "amount": float(booking.total_amount)
#         })

#     # ===== NORMAL PAGE LOAD =====
#     form = BookingForm()
#     context = {
#         "room_category": room_category,
#         "form": form,
#         "booked_dates": booked_dates,
#         "pricing": pricing,
#         "calculated_total": calculated_total,
#         "extra_price": float(pricing.extra_guest_price),
#     }
#     return render(request, "resort/room_detail.html", context)


# # ================== RAZORPAY ==================


# @csrf_exempt
# def create_razorpay_order(request):
#     booking_id = request.POST.get("booking_id")
#     amount = request.POST.get("amount")

#     if not booking_id or not amount:
#         return JsonResponse({"error": "Missing data"}, status=400)

#     booking = get_object_or_404(Booking, booking_id=booking_id)

#     razorpay_amount = int(float(amount) * 100)

#     order = razorpay_client.order.create({
#         "amount": razorpay_amount,
#         "currency": "INR",
#         "payment_capture": 1
#     })

#     booking.transaction_id = order["id"]
#     booking.save(update_fields=["transaction_id"])

#     return JsonResponse({
#         "order_id": order["id"],
#         "key": settings.RAZORPAY_KEY_ID,
#         "amount": razorpay_amount,
#         "name": booking.guest_name,
#         "email": booking.guest_email,
#         "contact": booking.guest_phone,
#     })
    
    
@csrf_exempt
def create_razorpay_order(request):
    amount = request.POST.get("amount")
    if not amount:
        return JsonResponse({"error": "Amount missing"}, status=400)

    order = razorpay_client.order.create({
        "amount": int(float(amount) * 100),
        "currency": "INR",
        "payment_capture": 1
    })

    return JsonResponse({
        "order_id": order["id"],
        "key": settings.RAZORPAY_KEY_ID,
        "amount": order["amount"]
    })

# @csrf_exempt
# def create_razorpay_order(request):
#     booking_id = request.POST.get("booking_id")
#     amount = request.POST.get("amount")

#     if not booking_id or not amount:
#         return JsonResponse({"error": "Missing data"}, status=400)

#     booking = get_object_or_404(Booking, booking_id=booking_id)

#     razorpay_amount = int(float(amount) * 100)

#     order = razorpay_client.order.create({
#         "amount": razorpay_amount,
#         "currency": "INR",
#         "payment_capture": 1
#     })

#     booking.transaction_id = order["id"]
#     booking.save(update_fields=["transaction_id"])

#     return JsonResponse({
#         "order_id": order["id"],
#         "key": settings.RAZORPAY_KEY_ID,
#         "amount": razorpay_amount,
#         "name": booking.guest_name,
#         "email": booking.guest_email,
#         "contact": booking.guest_phone,
#     })


# @csrf_exempt
# def verify_razorpay_payment(request):

#     razorpay_order_id = request.POST.get("razorpay_order_id")
#     razorpay_payment_id = request.POST.get("razorpay_payment_id")
#     razorpay_signature = request.POST.get("razorpay_signature")

#     # ✅ IMPORTANT: Check first
#     if not razorpay_order_id or not razorpay_payment_id or not razorpay_signature:
#         return JsonResponse({
#             "status": "failed",
#             "error": "Payment was not completed"
#         }, status=400)

#     try:
#         razorpay_client.utility.verify_payment_signature({
#             "razorpay_order_id": razorpay_order_id,
#             "razorpay_payment_id": razorpay_payment_id,
#             "razorpay_signature": razorpay_signature,
#         })

#         booking = get_object_or_404(
#             Booking,
#             transaction_id=razorpay_order_id
#         )

#         booking.payment_id = razorpay_payment_id
#         booking.payment_status = "paid"
#         booking.status = "confirmed"
#         booking.save()

#         send_booking_emails(booking)

#         return JsonResponse({"status": "success"})

#     except Exception as e:
#         return JsonResponse({
#             "status": "failed",
#             "error": str(e)
#         }, status=400)

@csrf_exempt
def verify_razorpay_payment(request):
    try:
        razorpay_client.utility.verify_payment_signature({
            "razorpay_order_id": request.POST["razorpay_order_id"],
            "razorpay_payment_id": request.POST["razorpay_payment_id"],
            "razorpay_signature": request.POST["razorpay_signature"],
        })

        session = request.session.get("pending_booking")
        if not session:
            return JsonResponse({"status": "failed", "error": "Session expired"}, status=400)

        data = session["data"]

        booking = Booking.objects.create(
            guest_name=data["guest_name"],
            guest_email=data["guest_email"],
            guest_phone=data["guest_phone"],
            guest_count=data["guest_count"],
            extra_guest_count=data.get("extra_guest_count", 0),
            check_in=data["check_in"],
            check_out=data["check_out"],
            sub_total=session["base"],
            disc_price=session["discount"],
            total_amount=session["total"],
            remaining_amount=0,
            payment_method=data["payment_method"],
            payment_status="paid",
            status="confirmed",
            transaction_id=request.POST["razorpay_order_id"],
            payment_id=request.POST["razorpay_payment_id"],
        )

        send_booking_emails(booking)

        del request.session["pending_booking"]

        return JsonResponse({
            "status": "success",
            "booking_id": booking.booking_id
        })

    except Exception as e:
        return JsonResponse({"status": "failed", "error": str(e)}, status=400)










def validate_coupon(request):
    code = request.GET.get("code", "")
    try:
        coupon = Coupon.objects.get(code__iexact=code, is_active=True)
        return JsonResponse({"valid": True, "discount": float(coupon.discount_amount)})
    except:
        return JsonResponse({"valid": False, "discount": 0})

def view_invoice(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    return render(request, "emails/invoice.html", {"booking": booking})






















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

