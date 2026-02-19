from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta
from .models import (
    RoomCategory, Amenity, Offer, Booking, MainBanner,BlockedDate,
    Testimonial, Gallery, ContactMessage,Coupon, VillaPricing
)
from .forms import BookingForm, ContactForm,TestimonialForm
from django.core.mail import send_mail
from django.db import IntegrityError, transaction



# from .models import VillaPricing, Booking, RoomCategory, Coupon


from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt

from decimal import Decimal
from datetime import datetime, timedelta

from django.urls import reverse
from django.contrib import messages

from .models import Booking, RoomCategory, VillaPricing, Coupon
from .forms import BookingForm
from django.conf import settings

import razorpay
import threading

import json
import hmac
import hashlib
# from django.conf import settings
from django.http import JsonResponse, HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from decimal import Decimal


def home(request):
      # ================= CONTACT FORM =================
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            contact_msg = form.save()

            context = {
                "name": contact_msg.name,
                "email": contact_msg.email,
                "phone": contact_msg.phone,
                "subject": contact_msg.subject,
                "message": contact_msg.message,
            }

            # ---------- ADMIN EMAIL ----------
            admin_html = render_to_string(
                "contact/admin_contact.html", context
            )

            admin_email = EmailMultiAlternatives(
                subject=f"New Contact Message: {contact_msg.subject}",
                body="",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.ADMIN_EMAIL],
            )
            admin_email.attach_alternative(admin_html, "text/html")
            admin_email.send()

            # ---------- USER EMAIL ----------
            user_html = render_to_string(
                "contact/user_contact.html", context
            )

            user_email = EmailMultiAlternatives(
                subject="Thank you for contacting Vivaan Farmhouse",
                body="",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[contact_msg.email],
            )
            user_email.attach_alternative(user_html, "text/html")
            user_email.send()

            messages.success(request, "Thank you! Your message has been sent successfully.")

            return redirect("home")  # reload same page

    else:
        form = ContactForm()
    """Homepage view"""
    banners = MainBanner.objects.filter(active=True).order_by("slot_position")
    seo_banner = banners.first()
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
        
                # ✅ SEO DATA
        "seo_title": seo_banner.page_title if seo_banner and seo_banner.page_title else "Vivaan Farmhouse – Elkatta, Hyderabad",
        "seo_description": seo_banner.meta_description if seo_banner else "",
        "seo_keywords": seo_banner.meta_keyword if seo_banner else "",
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










# utils/razorpay.py (recommended)

razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)




def send_booking_emails(booking, old_status=None):
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import render_to_string
    from django.conf import settings

    user_subject = None
    user_template = None

    # ================= PAYMENT FAILED =================
    if booking.payment_status == "failed":
        user_subject = "Payment Failed – Vivaan Farmhouse"
        user_template = "emails/payment_failed_user.html"

    # ================= FARMHOUSE BOOKING CREATED =================
    elif (
        booking.payment_method == "farmhouse"
        and booking.status == "pending"
        and old_status in [None, "pending"]
    ):
        user_subject = "Booking Received – Pay at Farmhouse"
        user_template = "emails/booking_pending_user.html"

    # ================= FARMHOUSE CONFIRMED =================
    elif (
        booking.payment_method == "farmhouse"
        and old_status == "pending"
        and booking.status == "confirmed"
    ):
        user_subject = "Booking Confirmed – Vivaan Farmhouse"
        user_template = "emails/user_booking_email.html"

    # ================= PARTIAL PAYMENT =================
    elif (
        booking.payment_method == "partial_razorpay"
        and booking.payment_status == "partial"
        and booking.status == "confirmed"
    ):
        user_subject = "Booking Confirmed – Partial Payment Received"
        user_template = "emails/partial_payment_confirmed.html"

    # ================= FULL PAYMENT =================
    elif (
        booking.payment_method == "full_razorpay"
        and booking.payment_status == "paid"
        and booking.status == "confirmed"
    ):
        user_subject = "Booking Confirmed – Payment Successful"
        user_template = "emails/full_payment_confirmed.html"

    # ================= CANCELLED =================
    elif old_status != booking.status and booking.status == "cancelled":
        user_subject = "Booking Cancelled – Vivaan Farmhouse"
        user_template = "emails/booking_cancelled_user.html"

    # ================= SEND USER EMAIL =================
    if user_subject and user_template:
        html = render_to_string(user_template, {"booking": booking})

        email = EmailMultiAlternatives(
            subject=user_subject,
            body="Booking update from Vivaan Farmhouse",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[booking.guest_email],
        )

        email.attach_alternative(html, "text/html")
        email.send(fail_silently=False)

    # ==============================
    # ADMIN EMAIL (ONLY CONFIRMED)
    # ==============================
    if booking.status in ["confirmed", "completed"]:

        admin_subject = f"Booking {booking.status.title()} – {booking.booking_id}"

        admin_template = (
            "emails/admin_booking_email.html"
            if booking.status == "confirmed"
            else "emails/booking_completed_admin.html"
        )

        admin_html = render_to_string(admin_template, {
            "booking": booking,
            "old_status": old_status,
        })

        admin_email = EmailMultiAlternatives(
            subject=admin_subject,
            body="Booking status update.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ADMIN_EMAIL],
            cc=settings.CC_EMAIL,
        )

        admin_email.attach_alternative(admin_html, "text/html")
        admin_email.send(fail_silently=False)


def send_email_async(booking, old_status=None):
    threading.Thread(
        target=send_booking_emails,
        args=(booking, old_status),
        daemon=True
    ).start()


def room_detail(request, slug):
    room_category = get_object_or_404(RoomCategory, slug=slug)

    # ================= BOOKED DATES =================
    booked_dates = []

    confirmed_bookings = Booking.objects.filter(
        check_out__gt=datetime.now().date(),
        status="confirmed"
    )

    for booking in confirmed_bookings:
        d = booking.check_in
        while d < booking.check_out:
            booked_dates.append(d.strftime("%Y-%m-%d"))
            d += timedelta(days=1)

    # ================= BLOCKED DATES =================
    blocked_dates = []

    for block in BlockedDate.objects.all():
        d = block.start_date
        # while d <= block.end_date:
        while d < block.end_date: 
            blocked_dates.append(d.strftime("%Y-%m-%d"))
            d += timedelta(days=1)

    pricing = VillaPricing.objects.first() or VillaPricing.objects.create()

    # ================= AJAX BOOKING =================
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":

        form = BookingForm(request.POST)

        if not form.is_valid():
            return JsonResponse({
                "error": "Invalid form",
                "details": form.errors
            }, status=400)

        payment_method = request.POST.get("payment_method")

        # ================= PRICE =================
        base_amount = calculate_booking_cost(
            form.cleaned_data["check_in"],
            form.cleaned_data["check_out"],
            form.cleaned_data["guest_count"],
            form.cleaned_data["extra_guest_count"],
        )

        discount = Decimal("0.00")
        coupon = form.cleaned_data.get("coupon_code")
        if coupon:
            discount = coupon.discount_amount

        total = base_amount - discount

        # ================= CREATE BOOKING =================
        booking, created = Booking.objects.get_or_create(
    guest_email=form.cleaned_data["guest_email"],
    check_in=form.cleaned_data["check_in"],
    check_out=form.cleaned_data["check_out"],
    payment_method=payment_method,

    defaults={
        "guest_name": form.cleaned_data["guest_name"],
        "guest_phone": form.cleaned_data["guest_phone"],
        "guest_count": form.cleaned_data["guest_count"],
        "extra_guest_count": form.cleaned_data["extra_guest_count"],

        "sub_total": base_amount,
        "disc_price": discount,
        "total_amount": total,
        "remaining_amount": total,

        "payment_status": "pending",
        "status": "pending",
    }
)


        # ================= FARMHOUSE =================
        if payment_method == "farmhouse":

            # send booking received email
            send_email_async(booking, old_status=None)

            return JsonResponse({
                "redirect": True,
                "url": reverse("booking_confirmation", args=[booking.booking_id])
            })

        # ================= RAZORPAY =================
        if payment_method == "partial_razorpay":
            pay_now = (total * Decimal("0.30")).quantize(Decimal("1"))
        else:  # full payment
            pay_now = total

        # store only booking id
        request.session["booking_id"] = booking.booking_id
        request.session.modified = True

        return JsonResponse({
            "razorpay": True,
            "amount": float(pay_now)
        })
    seo_title = f"{room_category.name} | Vivaan Farmhouse"

    seo_description = (
        f"Book {room_category.name} at Vivaan Farmhouse. "
        f"Enjoy a private luxury farmhouse stay with premium amenities, "
        f"perfect for family outings, weekend getaways, and celebrations."
    )
    # ================= PAGE LOAD =================
    return render(request, "resort/room_detail.html", {
        "room_category": room_category,
        "form": BookingForm(),
        "booked_dates": booked_dates,
        "blocked_dates": blocked_dates,
        "pricing": pricing,
        "extra_price": float(pricing.extra_guest_price),
                # ✅ SEO
        "seo_title": seo_title,
        "seo_description": seo_description,
        
    })



@csrf_exempt
def create_razorpay_order(request):

    booking_id = request.session.get("booking_id")

    if not booking_id:
        return JsonResponse({"error": "Booking not found"}, status=400)

    booking = get_object_or_404(Booking, booking_id=booking_id)

    amount = booking.total_amount

    if booking.payment_method == "partial_razorpay":
        amount = booking.total_amount * Decimal("0.30")

    order = razorpay_client.order.create({
        "amount": int(amount * 100),
        "currency": "INR",
        "payment_capture": 1
    })

    booking.transaction_id = order["id"]
    booking.save(update_fields=["transaction_id"])

    return JsonResponse({
        "order_id": order["id"],
        "key": settings.RAZORPAY_KEY_ID,
        "amount": order["amount"]
    })




@csrf_exempt
def razorpay_webhook(request):

    payload = json.loads(request.body)
    event = payload.get("event")

    if event == "payment.captured":

        payment = payload["payload"]["payment"]["entity"]
        booking = Booking.objects.filter(
            transaction_id=payment["order_id"]
        ).first()

        if booking:
            old_status = booking.status

            if booking.payment_method == "partial_razorpay":
                booking.payment_status = "partial"
                booking.remaining_amount = booking.total_amount * Decimal("0.70")
            else:
                booking.payment_status = "paid"
                booking.remaining_amount = Decimal("0.00")

            booking.status = "confirmed"
            booking.payment_id = payment["id"]
            booking.save()

            send_email_async(booking, old_status)

    elif event == "payment.failed":

        payment = payload["payload"]["payment"]["entity"]
        booking = Booking.objects.filter(
            transaction_id=payment["order_id"]
        ).first()

        if booking:
            booking.payment_status = "failed"
            booking.status = "cancelled"
            booking.save()

            send_email_async(booking)
#     except Exception as e:
#         print("Webhook error:", e)

    return HttpResponse("OK")



def payment_processing(request):
    return render(request, "resort/payment_processing.html")


def check_booking_status(request):

    booking_id = request.session.get("booking_id")

    if not booking_id:
        return JsonResponse({"ready": False})

    booking = Booking.objects.filter(
        booking_id=booking_id,
        status="confirmed"
    ).first()

    if booking:
        return JsonResponse({
            "ready": True,
            "booking_id": booking.booking_id
        })

    return JsonResponse({"ready": False})


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


def cancel_booking(request):
        # ✅ SEO (works with your base.html)
    seo_context = {
        "seo_title": "Cancel Booking Online | Vivaan Farmhouse",
        "seo_description": (
            "Cancel your Vivaan Farmhouse booking online easily. "
            "Check cancellation policy, refund eligibility, and manage your reservation securely."
        ),
       
    }
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
            
    return render(request, 'resort/cancel_booking.html' ,seo_context)




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
                # ✅ SEO
        "seo_title": "Guest Reviews & Ratings | Vivaan Farmhouse",
        "seo_description": (
            "Read real guest reviews of Vivaan Farmhouse. "
            "See customer experiences, ratings, and share your stay feedback online."
        ),
    }
    return render(request, 'resort/leave_review.html', context)

