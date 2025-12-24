from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse

def admin(request):
    return HttpResponse("sdfhjjhgasvbx")


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, "adminpanel/dashboard.html")

@login_required
def bookings(request):
    return render(request, "adminpanel/booking_list.html")

@login_required
def rooms(request):
    return render(request, "adminpanel/rooms.html")

@login_required
def amenities(request):
    return render(request, "adminpanel/amenities.html")

@login_required
def gallery(request):
    return render(request, "adminpanel/gallery.html")

@login_required
def testimonials(request):
    return render(request, "adminpanel/testimonials.html")

@login_required
def offers(request):
    return render(request, "adminpanel/offers.html")

@login_required
def pricing(request):
    return render(request, "adminpanel/pricing.html")

@login_required
def blocked_dates(request):
    return render(request, "adminpanel/blocked_dates.html")

@login_required
def messages(request):
    return render(request, "adminpanel/messages.html")
