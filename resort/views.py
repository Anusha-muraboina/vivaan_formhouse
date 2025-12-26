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

from datetime import timedelta, datetime
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import VillaPricing, Booking, RoomCategory, Coupon
from .forms import BookingForm

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt

from decimal import Decimal
from datetime import datetime, timedelta
from django.http import JsonResponse

from django.urls import reverse
from django.contrib import messages

from .models import Booking, RoomCategory, VillaPricing, Coupon
from .forms import BookingForm

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from .forms import ContactForm




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
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)










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
        # cc=cc_recipients  
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







import threading

def send_email_async(booking):
    threading.Thread(
        target=send_booking_emails,
        args=(booking,),
        daemon=True
    ).start()



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
    # ===== BLOCKED DATES (ADMIN) =====
    # blocked_dates = []
    # blocks = BlockedDate.objects.all()

    # for block in blocks:
    #     d = block.start_date
    #     while d <= block.end_date:
    #         blocked_dates.append(d.strftime("%Y-%m-%d"))
    #         d += timedelta(days=1)
    # pricing = VillaPricing.objects.first() or VillaPricing.objects.create()


# ===== BLOCKED DATES (ADMIN) — FIXED =====
# ===== BLOCKED DATES (ADMIN) — FINAL FIX =====
    blocked_dates = []
    blocks = BlockedDate.objects.all()

    for block in blocks:
        current = block.start_date
        while current <= block.end_date:   # ✅ MUST BE <=
            blocked_dates.append(current.strftime("%Y-%m-%d"))
            current += timedelta(days=1)

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

        if payment_method == "farmhouse":
            try:
                with transaction.atomic():
                    booking = form.save(commit=False)
                    booking.sub_total = base_amount
                    booking.disc_price = discount
                    booking.total_amount = 0
                    booking.remaining_amount = total
                    booking.payment_status = "pending"
                    booking.status = "confirmed"
                    booking.save()

                send_email_async(booking)

                return JsonResponse({
                    "redirect": True,
                    "url": reverse("booking_confirmation", args=[booking.booking_id])
                })

            except IntegrityError:
                # booking already exists, fetch it
                booking = Booking.objects.get(
                    guest_email=form.cleaned_data["guest_email"],
                    check_in=form.cleaned_data["check_in"],
                    check_out=form.cleaned_data["check_out"],
                    payment_method="farmhouse"
                )

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
        "blocked_dates": blocked_dates, 
        "pricing": pricing,
        "extra_price": float(pricing.extra_guest_price),
    })


    
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
    # store order id in session
    # request.session["razorpay_order_id"] = order["id"]
    # request.session.modified = True
    return JsonResponse({
        "order_id": order["id"],
        "key": settings.RAZORPAY_KEY_ID,
        "amount": order["amount"]
    })

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

        send_email_async(booking)

        del request.session["pending_booking"]

        return JsonResponse({
            "status": "success",
            "booking_id": booking.booking_id
        })

    except Exception as e:
        return JsonResponse({"status": "failed", "error": str(e)}, status=400)




import json
import hmac
import hashlib
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal

@csrf_exempt
def razorpay_webhook(request):
    """
    Razorpay Webhook Handler
    Handles:
    - payment.captured
    - payment.failed
    """

    webhook_secret = settings.RAZORPAY_WEBHOOK_SECRET
    received_signature = request.headers.get("X-Razorpay-Signature")

    payload = request.body

    # 🔐 VERIFY SIGNATURE
    expected_signature = hmac.new(
        bytes(webhook_secret, "utf-8"),
        payload,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, received_signature):
        return HttpResponse("Invalid signature", status=400)

    # ✅ Parse JSON
    data = json.loads(payload)
    event = data.get("event")

    # ===============================
    # PAYMENT CAPTURED
    # ===============================
    if event == "payment.captured":
        payment = data["payload"]["payment"]["entity"]

        payment_id = payment["id"]
        order_id = payment["order_id"]
        amount = Decimal(payment["amount"]) / 100  # paise → rupees
        email = payment.get("email")

        try:
            booking = Booking.objects.get(
                transaction_id=order_id,
                payment_status="pending"
            )

            booking.payment_status = "paid"
            booking.status = "confirmed"
            booking.payment_id = payment_id
            booking.remaining_amount = Decimal("0.00")
            booking.total_amount = amount
            booking.save()

            # 📧 Send confirmation emails
            send_email_async(booking)

            return JsonResponse({"status": "payment captured"})

        except Booking.DoesNotExist:
            return JsonResponse({"error": "Booking not found"}, status=404)

    # ===============================
    # PAYMENT FAILED
    # ===============================
    if event == "payment.failed":
        payment = data["payload"]["payment"]["entity"]

        order_id = payment["order_id"]

        Booking.objects.filter(
            transaction_id=order_id
        ).update(
            payment_status="failed",
            status="cancelled"
        )

        return JsonResponse({"status": "payment failed handled"})

    return JsonResponse({"status": "event ignored"})




def payment_processing(request):
    return render(request, "resort/payment_processing.html")


def check_booking_status(request):
    order_id = request.GET.get("order_id")

    booking = Booking.objects.filter(
        transaction_id=order_id,
        payment_status="paid"
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

