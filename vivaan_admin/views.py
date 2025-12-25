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


@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def dashboard(request):
    today = timezone.now().date()
    seven_days_ago = today - timedelta(days=7)
    first_day_of_month = today.replace(day=1)

    # =======================
    # REVENUE CALCULATIONS
    # =======================

    overall_revenue = (
        Booking.objects.filter(
            payment_status__in=['paid', 'partial']
        ).aggregate(total=Sum('total_amount'))['total']
        or Decimal('0.00')
    )

    monthly_revenue = (
        Booking.objects.filter(
            payment_status__in=['paid', 'partial'],
            created_at__date__gte=first_day_of_month
        ).aggregate(total=Sum('total_amount'))['total']
        or Decimal('0.00')
    )

    weekly_revenue = (
        Booking.objects.filter(
            payment_status__in=['paid', 'partial'],
            created_at__date__gte=seven_days_ago
        ).aggregate(total=Sum('total_amount'))['total']
        or Decimal('0.00')
    )

    # =======================
    # OTHER STATS
    # =======================

    weekly_bookings = Booking.objects.filter(
        created_at__date__gte=seven_days_ago
    ).count()

    pending_bookings = Booking.objects.filter(status='pending').count()

    total_guests = (
        Booking.objects.filter(
            status__in=['confirmed', 'completed']
        ).aggregate(total=Sum('guest_count'))['total']
        or 0
    )

    recent_bookings = Booking.objects.all().order_by('-created_at')[:5]

    # =======================
    # CHART DATA (6 MONTHS)
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
        Booking.objects.filter(status='confirmed').count(),
        Booking.objects.filter(status='pending').count(),
        Booking.objects.filter(status='cancelled').count(),
        Booking.objects.filter(status='completed').count(),
    ]

    context = {
        "overall_revenue": overall_revenue,
        "monthly_revenue": monthly_revenue,
        "weekly_revenue": weekly_revenue,
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
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def booking_list(request):
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'adminpanel/booking_list.html', {'bookings': bookings})

@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def booking_create(request):
    if request.method == 'POST':
        Booking.objects.create(
            guest_name=request.POST.get('guest_name'),
            guest_email=request.POST.get('guest_email'),
            guest_phone=request.POST.get('guest_phone'),
            guest_count=request.POST.get('guest_count'),
            status=request.POST.get('status'),
            total_amount=request.POST.get('total_amount'),
            check_in=request.POST.get('check_in'),
            check_out=request.POST.get('check_out'),
            special_requests=request.POST.get('special_requests'),
            cancellation_reason=request.POST.get('cancellation_reason')
        )
        messages.success(request, "New booking created manually.")
        return redirect('vivaan_admin:booking_list')
    return render(request, 'adminpanel/booking_form.html')

@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def booking_edit(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.guest_name = request.POST.get('guest_name')
        booking.guest_email = request.POST.get('guest_email')
        booking.guest_phone = request.POST.get('guest_phone')
        booking.guest_count = request.POST.get('guest_count')
        booking.status = request.POST.get('status')
        booking.total_amount = request.POST.get('total_amount')
        booking.check_in = request.POST.get('check_in')
        booking.check_out = request.POST.get('check_out')
        booking.special_requests = request.POST.get('special_requests')
        booking.cancellation_reason = request.POST.get('cancellation_reason')
        booking.save()
        messages.success(request, f"Booking #{booking.booking_id} updated successfully.")
        return redirect('vivaan_admin:booking_list')
    return render(request, 'adminpanel/booking_form.html', {'booking': booking})

@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'adminpanel/booking_detail.html', {'booking': booking})

@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.delete()
    messages.success(request, "Booking deleted.")
    return redirect('vivaan_admin:booking_list')

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
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def amenity_list(request):
    amenities = Amenity.objects.all()
    return render(request, 'adminpanel/amenity_list.html', {'amenities': amenities})

@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def amenity_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Amenity.objects.create(name=name)
        messages.success(request, "Amenity created.")
        return redirect('vivaan_admin:amenity_list')
    return render(request, 'adminpanel/amenity_form.html')

@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def amenity_edit(request, pk):
    amenity = get_object_or_404(Amenity, pk=pk)
    if request.method == 'POST':
        amenity.name = request.POST.get('name')
        amenity.save()
        messages.success(request, "Amenity updated.")
        return redirect('vivaan_admin:amenity_list')
    return render(request, 'adminpanel/amenity_form.html', {'amenity': amenity})

@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def amenity_delete(request, pk):
    amenity = get_object_or_404(Amenity, pk=pk)
    amenity.delete()
    messages.success(request, "Amenity deleted.")
    return redirect('vivaan_admin:amenity_list')

# --- Banners ---
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def banner_list(request):
    banners = MainBanner.objects.all()
    return render(request, 'adminpanel/banner_list.html', {'banners': banners})

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
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def blocked_date_list(request):
    blocked_dates = BlockedDate.objects.all()
    return render(request, 'adminpanel/blocked_date_list.html', {'blocked_dates': blocked_dates})

@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def blocked_date_create(request):
    if request.method == 'POST':
        BlockedDate.objects.create(
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            reason=request.POST.get('reason'),
            created_by=request.user
        )
        messages.success(request, "Date block added.")
        return redirect('vivaan_admin:blocked_date_list')
    return render(request, 'adminpanel/blocked_date_form.html')

@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def blocked_date_delete(request, pk):
    get_object_or_404(BlockedDate, pk=pk).delete()
    return redirect('vivaan_admin:blocked_date_list')

# --- Coupons ---
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def coupon_list(request):
    coupons = Coupon.objects.all()
    return render(request, 'adminpanel/coupon_list.html', {'coupons': coupons})

@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def coupon_create(request):
    if request.method == 'POST':
        Coupon.objects.create(
            code=request.POST.get('code'),
            discount_amount=request.POST.get('discount_amount'),
            valid_from=request.POST.get('valid_from'),
            valid_until=request.POST.get('valid_until')
        )
        return redirect('vivaan_admin:coupon_list')
    return render(request, 'adminpanel/coupon_form.html')

@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def coupon_delete(request, pk):
    get_object_or_404(Coupon, pk=pk).delete()
    return redirect('vivaan_admin:coupon_list')

# --- Gallery ---
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def gallery_list(request):
    photos = Gallery.objects.all()
    return render(request, 'adminpanel/gallery_list.html', {'photos': photos})

@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def gallery_create(request):
    if request.method == 'POST':
        Gallery.objects.create(
            title=request.POST.get('title'),
            category=request.POST.get('category'),
            image=request.FILES.get('image')
        )
        return redirect('vivaan_admin:gallery_list')
    return render(request, 'adminpanel/gallery_form.html')

@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def gallery_delete(request, pk):
    get_object_or_404(Gallery, pk=pk).delete()
    return redirect('vivaan_admin:gallery_list')

# --- Testimonials ---
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def testimonial_list(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'adminpanel/testimonial_list.html', {'testimonials': testimonials})

@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def testimonial_delete(request, pk):
    get_object_or_404(Testimonial, pk=pk).delete()
    return redirect('vivaan_admin:testimonial_list')

# --- Messages & Users (Existing) ---
@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def message_list(request):
    messages = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'adminpanel/message_list.html', {'messages': messages})

@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'adminpanel/user_list.html', {'users': users})

@login_required(login_url='vivaan_admin:login')
@user_passes_test(is_admin, login_url='vivaan_admin:login')
def user_create(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if User.objects.filter(username=username).exists():
            return render(request, 'adminpanel/user_form.html', {'error': 'Username already exists.'})

        user = User.objects.create_user(username=username, email=email, password=password)
        if role == 'superuser':
            user.is_superuser = True
            user.is_staff = True
        elif role == 'staff':
            user.is_staff = True
        
        user.save()
        messages.success(request, f"User {username} created successfully.")
        return redirect('vivaan_admin:user_list')

    return render(request, 'adminpanel/user_form.html')














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
