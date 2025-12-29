from django.shortcuts import render

# Create your views here.



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from resort.models import (
    Booking, RoomCategory, VillaPricing, ContactMessage,
    MainBanner, BlockedDate, Amenity, Coupon, Testimonial, Gallery
)
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta, date
import json
from resort.forms import AmenityForm
def is_admin(user):
    return user.is_authenticated and user.is_superuser

# --- Auth ---
def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('vivaan_admin:dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('vivaan_admin:dashboard')
            else:
                messages.error(request, "Access denied.")
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'adminpanel/login.html')

def admin_logout(request):
    logout(request)
    return redirect('vivaan_admin:login')

# --- Dashboard ---
# @login_required(login_url='vivaan_admin:login')
# @user_passes_test(is_admin, login_url='vivaan_admin:login')
# def dashboard(request):
#     today = timezone.now().date()
#     seven_days_ago = today - timedelta(days=7)
#     first_day_of_month = today.replace(day=1)

#     # Stats
#     total_revenue = Booking.objects.filter(status='confirmed').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
#     total_sales_count = Booking.objects.filter(status='confirmed').count()
#     networking_inquiries = ContactMessage.objects.count() # Interpreting 'networking' as inquiries
    
#     # Weekly Data
#     weekly_bookings = Booking.objects.filter(created_at__date__gte=seven_days_ago).count()
    
#     # Monthly Data
#     monthly_revenue = Booking.objects.filter(
#         status='confirmed', 
#         created_at__date__gte=first_day_of_month
#     ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

#     recent_bookings = Booking.objects.all().order_by('-created_at')[:5]
    
#     # Graphs
#     # 1. Booking vs Revenue Trend (Last 6 Months)
#     labels = []
#     revenue_data = []
#     booking_data = []
    
#     for i in range(5, -1, -1):
#         month_start = (today.replace(day=1) - timedelta(days=30*i)).replace(day=1)
#         month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
#         qs = Booking.objects.filter(created_at__date__gte=month_start, created_at__date__lte=month_end)
#         rev = qs.filter(status='confirmed').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
#         count = qs.count()
        
#         labels.append(month_start.strftime("%b"))
#         revenue_data.append(float(rev)) # Convert Decimal to float for JSON
#         booking_data.append(count)

#     context = {
#         'total_revenue': total_revenue,
#         'total_sales_count': total_sales_count,
#         'networking_inquiries': networking_inquiries,
#         'monthly_revenue': monthly_revenue,
#         'weekly_bookings': weekly_bookings,
#         'recent_bookings': recent_bookings,
#         'chart_labels': json.dumps(labels),
#         'revenue_data': json.dumps(revenue_data),
#         'booking_data': json.dumps(booking_data),
#     }
#     return render(request, 'adminpanel/dashboard.html', context)


# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required, user_passes_test
# from django.utils import timezone
# from django.db.models import Sum
# from datetime import timedelta
from decimal import Decimal
# import json

# from .models import Booking


# def is_admin(user):
#     return user.is_authenticated and user.is_superuser


# @login_required(login_url='vivaan_admin:login')
# @user_passes_test(is_admin, login_url='vivaan_admin:login')
# def dashboard(request):
#     today = timezone.now().date()
#     seven_days_ago = today - timedelta(days=7)
#     first_day_of_month = today.replace(day=1)

#     # =======================
#     # REVENUE CALCULATIONS
#     # =======================

#     overall_revenue = (
#         Booking.objects.filter(
#             payment_status__in=['paid', 'partial']
#         ).aggregate(total=Sum('total_amount'))['total']
#         or Decimal('0.00')
#     )


#     today = timezone.now().date()

#     weekly_start = today - timedelta(days=6)
#     monthly_start = today - timedelta(days=29)

#     today_revenue = Booking.objects.filter(
#         payment_status__in=['paid', 'partial'],
#         created_at__date=today
#     ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')

#     weekly_revenue = Booking.objects.filter(
#         payment_status__in=['paid', 'partial'],
#         created_at__date__gte=weekly_start,
#         created_at__date__lte=today
#     ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')

#     monthly_revenue = Booking.objects.filter(
#         payment_status__in=['paid', 'partial'],
#         created_at__date__gte=monthly_start,
#         created_at__date__lte=today
#     ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')

#     # monthly_revenue = (
#     #     Booking.objects.filter(
#     #         payment_status__in=['paid', 'partial'],
#     #         # created_at__date__gte=first_day_of_month
#     #     ).aggregate(total=Sum('total_amount'))['total']
#     #     or Decimal('0.00')
#     # )

#     # weekly_revenue = (
#     #     Booking.objects.filter(
#     #         payment_status__in=['paid', 'partial'],
#     #         # created_at__date__gte=seven_days_ago
#     #     ).aggregate(total=Sum('total_amount'))['total']
#     #     or Decimal('0.00')
#     # )

#     # =======================
#     # OTHER STATS
#     # =======================

#     weekly_bookings = Booking.objects.filter(
#         created_at__date__gte=seven_days_ago
#     ).count()

#     pending_bookings = Booking.objects.filter(status='pending').count()

#     total_guests = (
#         Booking.objects.filter(
#             status__in=['confirmed', 'completed']
#         ).aggregate(total=Sum('guest_count'))['total']
#         or 0
#     )

#     recent_bookings = Booking.objects.all().order_by('-created_at')[:5]

#     # =======================
#     # CHART DATA (6 MONTHS)
#     # =======================

#     labels = []
#     booking_data = []

#     for i in range(5, -1, -1):
#         month_start = (today.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
#         month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)

#         count = Booking.objects.filter(
#             created_at__date__gte=month_start,
#             created_at__date__lte=month_end
#         ).count()

#         labels.append(month_start.strftime("%b"))
#         booking_data.append(count)

#     status_data = [
#         Booking.objects.filter(status='confirmed').count(),
#         Booking.objects.filter(status='pending').count(),
#         Booking.objects.filter(status='cancelled').count(),
#         Booking.objects.filter(status='completed').count(),
#     ]

#     context = {
#         "overall_revenue": overall_revenue,
#         "monthly_revenue": monthly_revenue,
#         "weekly_revenue": weekly_revenue,
#         "weekly_bookings": weekly_bookings,
#         "pending_bookings": pending_bookings,
#         "total_guests": total_guests,
#         "recent_bookings": recent_bookings,
#         "chart_labels": json.dumps(labels),
#         "chart_data": json.dumps(booking_data),
#         "status_data": json.dumps(status_data),
#     }

#     return render(request, "adminpanel/dashboard.html", context)
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta
from decimal import Decimal
import json

@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def dashboard(request):

    # =======================
    # DATE SETUP
    # =======================
    today = timezone.now().date()
    weekly_start = today - timedelta(days=6)     # last 7 days (incl today)
    monthly_start = today - timedelta(days=29)   # last 30 days (incl today)

    paid_filter = {
        "payment_status__in": ["paid", "partial"]
    }

    # =======================
    # REVENUE (BASED ON CHECK-IN DATE)
    # =======================

    overall_revenue = (
        Booking.objects.filter(**paid_filter)
        .aggregate(total=Sum("total_amount"))["total"]
        or Decimal("0.00")
    )

    today_revenue = (
        Booking.objects.filter(
            **paid_filter,
            check_in=today
        ).aggregate(total=Sum("total_amount"))["total"]
        or Decimal("0.00")
    )

    weekly_revenue = (
        Booking.objects.filter(
            **paid_filter,
            check_in__range=[weekly_start, today]
        ).aggregate(total=Sum("total_amount"))["total"]
        or Decimal("0.00")
    )

    monthly_revenue = (
        Booking.objects.filter(
            **paid_filter,
            check_in__range=[monthly_start, today]
        ).aggregate(total=Sum("total_amount"))["total"]
        or Decimal("0.00")
    )

    # =======================
    # OTHER STATS
    # =======================

    weekly_bookings = Booking.objects.filter(
        check_in__range=[weekly_start, today]
    ).count()

    pending_bookings = Booking.objects.filter(status="pending").count()

    total_guests = (
        Booking.objects.filter(
            status__in=["confirmed", "completed"]
        ).aggregate(total=Sum("guest_count"))["total"]
        or 0
    )

    recent_bookings = Booking.objects.all().order_by("-created_at")[:5]

    # =======================
    # CHART DATA (LAST 6 MONTHS – BY CREATED DATE)
    # =======================

    labels = []
    booking_data = []

    for i in range(5, -1, -1):
        month_start = (today.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        count = Booking.objects.filter(
            created_at__date__gte=month_start,
            created_at__date__lte=month_end
        ).count()

        labels.append(month_start.strftime("%b"))
        booking_data.append(count)

    status_data = [
        Booking.objects.filter(status="confirmed").count(),
        Booking.objects.filter(status="pending").count(),
        Booking.objects.filter(status="cancelled").count(),
        Booking.objects.filter(status="completed").count(),
    ]

    # =======================
    # CONTEXT
    # =======================

    context = {
        "overall_revenue": overall_revenue,
        "today_revenue": today_revenue,
        "weekly_revenue": weekly_revenue,
        "monthly_revenue": monthly_revenue,

        "weekly_bookings": weekly_bookings,
        "pending_bookings": pending_bookings,
        "total_guests": total_guests,
        "recent_bookings": recent_bookings,

        "chart_labels": json.dumps(labels),
        "chart_data": json.dumps(booking_data),
        "status_data": json.dumps(status_data),
    }

    return render(request, "adminpanel/dashboard.html", context)

# --- Bookings ---
from .forms import *

# LIST
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, "adminpanel/booking_list.html", {"bookings": bookings})


from resort.views import calculate_booking_cost
from decimal import Decimal
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.db import transaction, IntegrityError
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

# from .models import Booking, BlockedDate, Coupon, VillaPricing
from .forms import AdminBookingForm
from resort.views import send_email_async
# vivaan_admin/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from datetime import timedelta
from decimal import Decimal

from resort.models import Booking, BlockedDate, VillaPricing
from .forms import AdminBookingForm




# @login_required(login_url="vivaan_admin:login")
# @user_passes_test(is_admin)
# def admin_booking_create(request):

#     # ================= BOOKED DATES =================
#     booked_dates = []
#     bookings = Booking.objects.filter(status__in=["confirmed", "pending"])

#     for b in bookings:
#         d = b.check_in
#         while d < b.check_out:
#             booked_dates.append(d.strftime("%Y-%m-%d"))
#             d += timedelta(days=1)

#     # ================= BLOCKED DATES =================
#     blocked_dates = []
#     for block in BlockedDate.objects.all():
#         d = block.start_date
#         while d <= block.end_date:
#             blocked_dates.append(d.strftime("%Y-%m-%d"))
#             d += timedelta(days=1)

#     pricing = VillaPricing.objects.first()

#     # ================= POST =================
#     if request.method == "POST":
#         form = AdminBookingForm(request.POST)

#         if form.is_valid():
#             booking = form.save(commit=False)

#             # 🔒 ADMIN OVERRIDES
#             booking.payment_method = "farmhouse"
#             booking.payment_status = "paid"
#             booking.status = "confirmed"

#             # 💰 PRICE CALCULATION
#             nights = (booking.check_out - booking.check_in).days
#             base = pricing.weekday_price * nights
#             extra = booking.extra_guest_count * pricing.extra_guest_price

#             booking.sub_total = base + extra
#             booking.disc_price = Decimal("0.00")
#             booking.total_amount = booking.sub_total
#             booking.remaining_amount = Decimal("0.00")

#             booking.save()

#             messages.success(request, "Booking created successfully")
#             return redirect("vivaan_admin:booking_list")

#     else:
#         form = AdminBookingForm()

#     return render(request, "adminpanel/booking_form.html", {
#         "form": form,
#         "booked_dates": booked_dates,
#         "blocked_dates": blocked_dates,
#     })


from resort.views import * 
# @login_required(login_url="vivaan_admin:login")
# @user_passes_test(is_admin)
# def admin_booking_create(request):

#     # ================= BOOKED DATES =================
#     booked_dates = []
#     bookings = Booking.objects.filter(status__in=["confirmed", "pending"])

#     for b in bookings:
#         d = b.check_in
#         while d < b.check_out:
#             booked_dates.append(d.strftime("%Y-%m-%d"))
#             d += timedelta(days=1)

#     # ================= BLOCKED DATES =================
#     blocked_dates = []
#     for block in BlockedDate.objects.all():
#         d = block.start_date
#         while d <= block.end_date:
#             blocked_dates.append(d.strftime("%Y-%m-%d"))
#             d += timedelta(days=1)

#     pricing = VillaPricing.objects.first()

#     if request.method == "POST":
#         form = AdminBookingForm(request.POST)

#         if form.is_valid():
#             booking = form.save(commit=False)

#             # ✅ DEFAULTS
#             booking.payment_status = booking.payment_status or "pending"
#             booking.payment_method = booking.payment_method or "farmhouse"
#             booking.status = booking.status or "confirmed"

#             # 💰 PRICE CALCULATION
#             nights = (booking.check_out - booking.check_in).days
#             base = pricing.weekday_price * nights
#             extra = (booking.extra_guest_count or 0) * pricing.extra_guest_price

#             booking.sub_total = base + extra
#             booking.disc_price = Decimal("0.00")
#             booking.total_amount = booking.sub_total
#             booking.remaining_amount = booking.total_amount

#             booking.save()

#             # 📧 SEND EMAILS (ASYNC)
#             # send_email_async(booking)
#             send_email_async(booking, old_status=None)

#             messages.success(request, "Booking created and emails sent successfully")
#             return redirect("vivaan_admin:booking_list")

#     else:
#         form = AdminBookingForm()

#     return render(request, "adminpanel/booking_form.html", {
#         "form": form,
#         "booked_dates": booked_dates,
#         "blocked_dates": blocked_dates,
#     })



@login_required(login_url="vivaan_admin:login")
@user_passes_test(is_admin)
def admin_booking_create(request):

    booked_dates = []
    for b in Booking.objects.filter(status__in=["confirmed", "pending"]):
        d = b.check_in
        while d < b.check_out:
            booked_dates.append(d.strftime("%Y-%m-%d"))
            d += timedelta(days=1)

    blocked_dates = []
    for block in BlockedDate.objects.all():
        d = block.start_date
        while d <= block.end_date:
            blocked_dates.append(d.strftime("%Y-%m-%d"))
            d += timedelta(days=1)

    pricing = VillaPricing.objects.first()

    if request.method == "POST":
        form = AdminBookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)

            # ================= DEFAULTS =================
            booking.payment_status = booking.payment_status or "pending"
            booking.payment_method = booking.payment_method or "farmhouse"
            booking.status = booking.status or "confirmed"

            # ================= PRICE =================
            nights = (booking.check_out - booking.check_in).days
            base = pricing.weekday_price * nights
            extra = (booking.extra_guest_count or 0) * pricing.extra_guest_price

            sub_total = base + extra

            # ================= COUPON =================
            coupon = form.cleaned_data.get("coupon_code")
            discount = Decimal("0.00")

            if coupon:
                discount = coupon.discount_amount
                booking.disc_price = coupon

            booking.sub_total = sub_total
            booking.disc_price = discount
            booking.total_amount = sub_total - discount
            booking.remaining_amount = booking.total_amount

            booking.save()

            # ================= EMAIL =================
            send_email_async(booking, old_status=None)

            messages.success(request, "Booking created successfully")
            return redirect("vivaan_admin:booking_list")

    else:
        form = AdminBookingForm()

    return render(request, "adminpanel/booking_form.html", {
        "form": form,
        "booked_dates": booked_dates,
        "blocked_dates": blocked_dates,
    })





@login_required(login_url="vivaan_admin:login")
@user_passes_test(is_admin)
def booking_edit(request, pk):

    booking = get_object_or_404(Booking, pk=pk)
    old_status = booking.status  # 🔑 capture old status

    # ================= BOOKED DATES (EXCLUDE CURRENT) =================
    booked_dates = set()
    bookings = Booking.objects.filter(
        status__in=["confirmed", "pending"]
    ).exclude(pk=pk)

    for b in bookings:
        d = b.check_in
        while d < b.check_out:
            booked_dates.add(d.isoformat())
            d += timedelta(days=1)

    # ================= BLOCKED DATES =================
    blocked_dates = set()
    for block in BlockedDate.objects.all():
        d = block.start_date
        while d <= block.end_date:
            blocked_dates.add(d.isoformat())
            d += timedelta(days=1)

    form = AdminBookingForm(request.POST or None, instance=booking)

    if form.is_valid():
        updated_booking = form.save(commit=False)

        # Defaults (safe)
        updated_booking.payment_status = updated_booking.payment_status or "pending"
        updated_booking.payment_method = updated_booking.payment_method or "farmhouse"
        updated_booking.status = updated_booking.status or "confirmed"

        updated_booking.save()

        # 📧 SEND EMAIL ONLY IF STATUS CHANGED
        if old_status != updated_booking.status:
            send_booking_emails(updated_booking, old_status)


        messages.success(
            request,
            f"Booking {updated_booking.booking_id} updated successfully."
        )
        return redirect("vivaan_admin:booking_list")

    return render(request, "adminpanel/booking_form.html", {
        "form": form,
        "booking": booking,
        "booked_dates": sorted(booked_dates),
        "blocked_dates": sorted(blocked_dates),
    })


# DETAIL
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, "adminpanel/booking_detail.html", {"booking": booking})


# DELETE
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.delete()
    messages.success(request, "Booking deleted.")
    return redirect("vivaan_admin:booking_list")

# --- Rooms & Categories ---


# ================================
# ROOM CATEGORY LIST
# ================================
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.text import slugify
# from .models import RoomCategory, VillaPricing



# =========================
# LIST PAGE
# =========================
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def room_list(request):
    categories = RoomCategory.objects.all()
    pricing = VillaPricing.objects.first()
    return render(request, 'adminpanel/room_list.html', {
        'room_categories': categories,
        'pricing': pricing
    })


# =========================
# ADD ROOM CATEGORY
# =========================
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def category_add(request):
    if request.method == "POST":
        name = request.POST.get('name')
        RoomCategory.objects.create(
            name=name,
            slug=slugify(name),
            description=request.POST.get('description'),
            size_sqft=request.POST.get('size_sqft'),
            max_occupancy=request.POST.get('max_occupancy'),
            floor=request.POST.get('floor'),
            base_price=request.POST.get('base_price'),
            view_type=request.POST.get('view_type'),
            has_balcony=True if request.POST.get('has_balcony') else False,
            has_bathtub=True if request.POST.get('has_bathtub') else False,
            image=request.FILES.get('image')
        )
        messages.success(request, "Room category added successfully.")
        return redirect('vivaan_admin:room_list')

    return render(request, 'adminpanel/category_add.html')


# =========================
# EDIT ROOM CATEGORY
# =========================

@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def category_edit(request, pk):
    category = get_object_or_404(RoomCategory, pk=pk)

    if request.method == "POST":
        category.name = request.POST.get('name')
        category.slug = slugify(category.name)
        category.description = request.POST.get('description')
        category.base_price = request.POST.get('base_price')
        category.max_occupancy = request.POST.get('max_occupancy')
        category.size_sqft = request.POST.get('size_sqft')
        category.floor = request.POST.get('floor')
        category.view_type = request.POST.get('view_type')
        category.has_balcony = True if request.POST.get('has_balcony') else False
        category.has_bathtub = True if request.POST.get('has_bathtub') else False

        # Image update (only if new image uploaded)
        if request.FILES.get('image'):
            category.image = request.FILES.get('image')

        category.save()

        messages.success(request, "Room category updated successfully.")
        return redirect('vivaan_admin:room_list')

    return render(request, 'adminpanel/category_edit.html', {
        'category': category
    })

# =========================
# DELETE ROOM CATEGORY
# =========================
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def category_delete(request, pk):
    get_object_or_404(RoomCategory, pk=pk).delete()
    messages.success(request, "Room category deleted.")
    return redirect('vivaan_admin:room_list')


# =========================
# ADD / EDIT VILLA PRICING
# =========================
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def pricing_add_edit(request):
    pricing = VillaPricing.objects.first()

    if request.method == "POST":
        if not pricing:
            pricing = VillaPricing()

        pricing.weekday_price = request.POST.get('weekday_price')
        pricing.weekend_price = request.POST.get('weekend_price')
        pricing.extra_guest_price = request.POST.get('extra_guest_price')
        pricing.save()

        messages.success(request, "Villa pricing saved successfully.")
        return redirect('vivaan_admin:room_list')

    return render(request, 'adminpanel/pricing_form.html', {'pricing': pricing})


# ================================
# EDIT ROOM CATEGORY
# ================================
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def category_edit(request, pk):
    category = get_object_or_404(RoomCategory, pk=pk)

    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.base_price = request.POST.get('base_price')
        category.max_occupancy = request.POST.get('max_occupancy')
        category.size_sqft = request.POST.get('size_sqft')
        category.floor = request.POST.get('floor')
        category.view_type = request.POST.get('view_type')
        category.slug = slugify(category.name)
        category.save()

        messages.success(request, "Room category updated.")
        return redirect('vivaan_admin:room_list')

    return render(request, 'adminpanel/category_edit.html', {'category': category})


# ================================
# DELETE ROOM CATEGORY
# ================================
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def category_delete(request, pk):
    category = get_object_or_404(RoomCategory, pk=pk)
    category.delete()
    messages.success(request, "Room category deleted.")
    return redirect('vivaan_admin:room_list')


# ================================
# EDIT VILLA PRICING (SINGLE)
# ================================
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def pricing_edit(request):
    pricing = VillaPricing.objects.first() or VillaPricing.objects.create()

    if request.method == 'POST':
        pricing.weekday_price = request.POST.get('weekday_price')
        pricing.weekend_price = request.POST.get('weekend_price')
        pricing.extra_guest_price = request.POST.get('extra_guest_price')
        pricing.save()

        messages.success(request, "Villa pricing updated.")
        return redirect('vivaan_admin:room_list')

    return render(request, 'adminpanel/pricing_form.html', {'pricing': pricing})

# --- Amenities ---


# --- LIST ---
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def amenity_list(request):
    amenity_qs = Amenity.objects.all().order_by('-id')

    paginator = Paginator(amenity_qs, 10)  # 8 amenities per page
    page_number = request.GET.get('page')
    amenities = paginator.get_page(page_number)

    return render(request, 'adminpanel/amenity_list.html', {
        'amenities': amenities
    })
# --- CREATE ---
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def amenity_create(request):
    form = AmenityForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Amenity created successfully.")
        return redirect('vivaan_admin:amenity_list')
    return render(request, 'adminpanel/amenity_form.html', {'form': form})

# --- EDIT ---
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def amenity_edit(request, pk):
    amenity = get_object_or_404(Amenity, pk=pk)
    form = AmenityForm(request.POST or None, request.FILES or None, instance=amenity)
    if form.is_valid():
        form.save()
        messages.success(request, "Amenity updated successfully.")
        return redirect('vivaan_admin:amenity_list')
    return render(request, 'adminpanel/amenity_form.html', {'form': form, 'amenity': amenity})

# --- DELETE ---
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def amenity_delete(request, pk):
    amenity = get_object_or_404(Amenity, pk=pk)
    amenity.delete()
    messages.success(request, "Amenity deleted successfully.")
    return redirect('vivaan_admin:amenity_list')



# --- Banners ---
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def banner_list(request):
    banner_qs = MainBanner.objects.all().order_by('-id')

    paginator = Paginator(banner_qs, 10)  # 5 banners per page
    page_number = request.GET.get('page')
    banners = paginator.get_page(page_number)

    return render(request, 'adminpanel/banner_list.html', {
        'banners': banners
    })
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def banner_create(request):
    if request.method == 'POST':
        MainBanner.objects.create(
            title=request.POST.get('title'),
            subtitle=request.POST.get('subtitle'),
            page_title=request.POST.get('page_title'),
            meta_keyword=request.POST.get('meta_keyword'),
            meta_description=request.POST.get('meta_description'),
            slot_position=request.POST.get('slot_position') or 0,
            active=True if request.POST.get('active') else False,
            image=request.FILES.get('image'),
        )
        messages.success(request, "Banner created successfully.")
        return redirect('vivaan_admin:banner_list')

    return render(request, 'adminpanel/banner_form.html')

@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def banner_edit(request, pk):
    banner = get_object_or_404(MainBanner, pk=pk)

    if request.method == 'POST':
        banner.title = request.POST.get('title')
        banner.subtitle = request.POST.get('subtitle')
        banner.page_title = request.POST.get('page_title')
        banner.meta_keyword = request.POST.get('meta_keyword')
        banner.meta_description = request.POST.get('meta_description')
        banner.slot_position = request.POST.get('slot_position') or 0
        banner.active = True if request.POST.get('active') else False

        if request.FILES.get('image'):
            banner.image = request.FILES.get('image')

        banner.save()
        messages.success(request, "Banner updated successfully.")
        return redirect('vivaan_admin:banner_list')

    return render(request, 'adminpanel/banner_form.html', {'banner': banner})

@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def banner_delete(request, pk):
    get_object_or_404(MainBanner, pk=pk).delete()
    return redirect('vivaan_admin:banner_list')

# --- Blocked Dates ---
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def blocked_date_list(request):
    blocked_dates = BlockedDate.objects.all().order_by('-start_date')
    return render(request, 'adminpanel/blocked_date_list.html', {
        'blocked_dates': blocked_dates
    })
from resort.models import *
from resort.forms import *

@login_required(login_url="vivaan_admin:login")
@user_passes_test(is_admin)
def blocked_date_create(request):

    booked_dates = []
    for b in Booking.objects.filter(status__in=["confirmed", "pending"]):
        d = b.check_in
        while d < b.check_out:
            booked_dates.append(d.strftime("%Y-%m-%d"))
            d += timedelta(days=1)

    blocked_dates = []
    for block in BlockedDate.objects.all():
        d = block.start_date
        while d <= block.end_date:  # ✅ inclusive
            blocked_dates.append(d.strftime("%Y-%m-%d"))
            d += timedelta(days=1)

    if request.method == "POST":
        form = AdminBlockedDateForm(request.POST)
        if form.is_valid():
            blocked = form.save(commit=False)
            blocked.full_clean()   # 🔥 THIS WAS MISSING
            blocked.save()
            messages.success(request, "Dates blocked successfully.")
            return redirect("vivaan_admin:blocked_date_list")
    else:
        form = AdminBlockedDateForm()

    return render(request, "adminpanel/blocked_date_form.html", {
        "form": form,
        "booked_dates": booked_dates,
        "blocked_dates": blocked_dates,
    })

@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def blocked_date_edit(request, pk):

    blocked_date = get_object_or_404(BlockedDate, pk=pk)

    disabled_dates = set()

    # BOOKED DATES
    bookings = Booking.objects.filter(
        status__in=["confirmed", "pending"],
        check_out__gt=timezone.now().date()
    )

    for booking in bookings:
        d = booking.check_in
        while d < booking.check_out:
            disabled_dates.add(d.strftime("%Y-%m-%d"))
            d += timedelta(days=1)

    # BLOCKED DATES (EXCEPT CURRENT)
    blocks = BlockedDate.objects.exclude(pk=pk)
    for block in blocks:
        d = block.start_date
        while d <= block.end_date:
            disabled_dates.add(d.strftime("%Y-%m-%d"))
            d += timedelta(days=1)

    if request.method == "POST":
        form = AdminBlockedDateForm(request.POST, instance=blocked_date)
        if form.is_valid():
            form.save()
            messages.success(request, "Blocked date updated.")
            return redirect("vivaan_admin:blocked_date_list")
    else:
        form = AdminBlockedDateForm(instance=blocked_date)

    return render(request, "adminpanel/blocked_date_form.html", {
        "form": form,
        "blocked_date": blocked_date,
        "disabled_dates": list(disabled_dates)
    })

# DELETE
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def blocked_date_delete(request, pk):
    blocked = get_object_or_404(BlockedDate, pk=pk)
    blocked.delete()
    messages.success(request, "Blocked date removed.")
    return redirect('vivaan_admin:blocked_date_list')
# --- Coupons ---


@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def coupon_list(request):
    coupons = Coupon.objects.all().order_by("-created_at")
    return render(request, "adminpanel/coupon_list.html", {"coupons": coupons})


@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def coupon_create(request):
    form = CouponForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Coupon created successfully.")
        return redirect("vivaan_admin:coupon_list")
    return render(request, "adminpanel/coupon_form.html", {"form": form})


@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def coupon_edit(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    form = CouponForm(request.POST or None, instance=coupon)
    if form.is_valid():
        form.save()
        messages.success(request, "Coupon updated successfully.")
        return redirect("vivaan_admin:coupon_list")
    return render(request, "adminpanel/coupon_form.html", {
        "form": form,
        "coupon": coupon
    })


@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def coupon_delete(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    coupon.delete()
    messages.success(request, "Coupon deleted.")
    return redirect("vivaan_admin:coupon_list")

# --- Gallery ---
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def gallery_list(request):
    photos = Gallery.objects.all()
    return render(request, "adminpanel/gallery_list.html", {
        "photos": photos
    })


@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def gallery_create(request):
    form = GalleryForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Gallery image added successfully.")
        return redirect("vivaan_admin:gallery_list")

    return render(request, "adminpanel/gallery_form.html", {
        "form": form
    })


@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def gallery_edit(request, pk):
    photo = get_object_or_404(Gallery, pk=pk)
    form = GalleryForm(request.POST or None, request.FILES or None, instance=photo)

    if form.is_valid():
        form.save()
        messages.success(request, "Gallery image updated successfully.")
        return redirect("vivaan_admin:gallery_list")

    return render(request, "adminpanel/gallery_form.html", {
        "form": form,
        "photo": photo
    })


@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def gallery_delete(request, pk):
    photo = get_object_or_404(Gallery, pk=pk)
    photo.delete()
    messages.success(request, "Gallery image deleted.")
    return redirect("vivaan_admin:gallery_list")

# --- Testimonials ---
from django.core.paginator import Paginator

@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def testimonial_list(request):
    testimonials_qs = Testimonial.objects.all().order_by("-created_at")

    paginator = Paginator(testimonials_qs, 3)  # 6 testimonials per page
    page_number = request.GET.get("page")
    testimonials = paginator.get_page(page_number)

    return render(request, "adminpanel/testimonial_list.html", {
        "testimonials": testimonials
    })


@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def testimonial_create(request):
    form = TestimonialForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Testimonial added successfully.")
        return redirect("vivaan_admin:testimonial_list")

    return render(request, "adminpanel/testimonial_form.html", {
        "form": form
    })


@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def testimonial_edit(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    form = TestimonialForm(request.POST or None, instance=testimonial)

    if form.is_valid():
        form.save()
        messages.success(request, "Testimonial updated successfully.")
        return redirect("vivaan_admin:testimonial_list")

    return render(request, "adminpanel/testimonial_form.html", {
        "form": form,
        "testimonial": testimonial
    })


@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def testimonial_delete(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.delete()
    messages.success(request, "Testimonial deleted.")
    return redirect("vivaan_admin:testimonial_list")

# --- Messages & Users (Existing) ---
# LIST
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def message_list(request):
    qs = ContactMessage.objects.all()

    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page")
    messages_page = paginator.get_page(page_number)

    return render(request, 'adminpanel/message_list.html', {
        'messages': messages_page
    })

@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def message_create(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message"),
            is_read=True  # admin-added messages are read
        )
        messages.success(request, "Message added successfully.")
        return redirect("vivaan_admin:message_list")

    return render(request, "adminpanel/message_form.html")

# VIEW / DETAIL
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def message_detail(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)

    if not msg.is_read:
        msg.is_read = True
        msg.save()

    return render(request, 'adminpanel/message_detail.html', {
        'message': msg
    })


# DELETE
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def message_delete(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.delete()
    messages.success(request, "Message deleted successfully.")
    return redirect('vivaan_admin:message_list')



# LIST
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'adminpanel/user_list.html', {'users': users})


# CREATE
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def user_create(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('vivaan_admin:user_create')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        if role == "superuser":
            user.is_superuser = True
            user.is_staff = True
        elif role == "staff":
            user.is_staff = True

        user.save()
        messages.success(request, f"User {username} created successfully.")
        return redirect('vivaan_admin:user_list')

    return render(request, 'adminpanel/user_form.html')


# EDIT
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        role = request.POST.get('role')

        user.is_superuser = False
        user.is_staff = False

        if role == "superuser":
            user.is_superuser = True
            user.is_staff = True
        elif role == "staff":
            user.is_staff = True

        password = request.POST.get('password')
        if password:
            user.set_password(password)

        user.save()
        messages.success(request, "User updated successfully.")
        return redirect('vivaan_admin:user_list')

    return render(request, 'adminpanel/user_form.html', {'edit_user': user})


# DELETE
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin)
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)

    if user == request.user:
        messages.error(request, "You cannot delete your own account.")
    else:
        user.delete()
        messages.success(request, "User deleted successfully.")

    return redirect('vivaan_admin:user_list')






# @login_required(login_url='vivaan_admin:login')
# @user_passes_test(is_admin, login_url='vivaan_admin:login')
# def user_list(request):
#     users = User.objects.all().order_by('-date_joined')
#     return render(request, 'adminpanel/user_list.html', {'users': users})

# @login_required(login_url='vivaan_admin:login')
# @user_passes_test(is_admin, login_url='vivaan_admin:login')
# def user_create(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         role = request.POST.get('role')

#         if User.objects.filter(username=username).exists():
#             return render(request, 'adminpanel/user_form.html', {'error': 'Username already exists.'})

#         user = User.objects.create_user(username=username, email=email, password=password)
#         if role == 'superuser':
#             user.is_superuser = True
#             user.is_staff = True
#         elif role == 'staff':
#             user.is_staff = True
        
#         user.save()
#         messages.success(request, f"User {username} created successfully.")
#         return redirect('vivaan_admin:user_list')

#     return render(request, 'adminpanel/user_form.html')














# from django.http import HttpResponse

# def admin(request):
#     return HttpResponse("sdfhjjhgasvbx")


# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required

# @login_required
# def dashboard(request):
#     return render(request, "vivaan_admin/dashboard.html")

# @login_required
# def bookings(request):
#     return render(request, "vivaan_admin/booking_list.html")

# @login_required
# def rooms(request):
#     return render(request, "vivaan_admin/rooms.html")

# @login_required
# def amenities(request):
#     return render(request, "vivaan_admin/amenities.html")

# @login_required
# def gallery(request):
#     return render(request, "vivaan_admin/gallery.html")

# @login_required
# def testimonials(request):
#     return render(request, "vivaan_admin/testimonials.html")

# @login_required
# def offers(request):
#     return render(request, "vivaan_admin/offers.html")

# @login_required
# def pricing(request):
#     return render(request, "vivaan_admin/pricing.html")

# @login_required
# def blocked_dates(request):
#     return render(request, "vivaan_admin/blocked_dates.html")

# @login_required
# def messages(request):
#     return render(request, "vivaan_admin/messages.html")
