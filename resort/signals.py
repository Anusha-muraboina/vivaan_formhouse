# bookings/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Booking
from resort.views import send_email_async


@receiver(pre_save, sender=Booking)
def booking_status_change(sender, instance, **kwargs):

    if not instance.pk:
        return

    try:
        old = Booking.objects.get(pk=instance.pk)
    except Booking.DoesNotExist:
        return

    status_changed = old.status != instance.status
    payment_changed = old.payment_status != instance.payment_status

    if status_changed or payment_changed:
        send_email_async(instance)   # ✅ ASYNC ONLY
