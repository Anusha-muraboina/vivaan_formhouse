from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('rooms/', views.rooms, name='rooms'),
    path('room/<slug:slug>/', views.room_detail, name='room_detail'),
    path('booking/<str:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    # path('amenities/', views.amenities_view, name='amenities'),
    # path('offers/', views.offers_view, name='offers'),
    # path('gallery/', views.gallery_view, name='gallery'),
    path('contact/', views.contact, name='contact'),
    # path('about/', views.about, name='about'),
    path('cancel-booking/', views.cancel_booking, name='cancel_booking'),
    # path('reviews/', views.leave_review, name='leave_review'),
    path("invoice/<booking_id>/", views.view_invoice, name="view_invoice"),
    path("validate-coupon/", views.validate_coupon, name="validate_coupon"),
    
    
    path("create-razorpay-order/", views.create_razorpay_order, name="create_razorpay_order"),
    # path("verify-payment/", views.verify_razorpay_payment, name="verify_payment"),
    
        # Razorpay
    path("razorpay/webhook/", views.razorpay_webhook, name="razorpay_webhook"),
    
    path("payment-processing/", views.payment_processing, name="payment_processing"),
    path("check-booking-status/", views.check_booking_status, name="check_booking_status"),

]
