

from django import forms
from resort.models import Booking

class AdminBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "guest_name",
            "guest_email",
            "guest_phone",
            "guest_count",
            "extra_guest_count",
            "check_in",
            "check_out",
            "check_in_time",
            "check_out_time",
            "status",
            "payment_method",
            "payment_status",
            "total_amount",
            "remaining_amount",
            "special_requests",
            "cancellation_reason",
        ]

        widgets = {
            "guest_name": forms.TextInput(attrs={"class": "form-input"}),
            "guest_email": forms.EmailInput(attrs={"class": "form-input"}),
            "guest_phone": forms.TextInput(attrs={"class": "form-input"}),
            "guest_count": forms.NumberInput(attrs={"class": "form-input"}),
            "extra_guest_count": forms.NumberInput(attrs={"class": "form-input"}),
            "check_in": forms.DateInput(attrs={"type": "date", "class": "form-input"}),
            "check_out": forms.DateInput(attrs={"type": "date", "class": "form-input"}),
                        # Time fields ✅
            "check_in_time": forms.TimeInput(attrs={
                "type": "time",
                "class": "form-input"
            }),
            "check_out_time": forms.TimeInput(attrs={
                "type": "time",
                "class": "form-input"
            }),
            "status": forms.Select(attrs={"class": "form-input"}),
            "payment_method": forms.Select(attrs={"class": "form-input"}),
            "payment_status": forms.Select(attrs={"class": "form-input"}),
            "total_amount": forms.NumberInput(attrs={"class": "form-input"}),
            "remaining_amount": forms.NumberInput(attrs={"class": "form-input"}),
            "special_requests": forms.Textarea(attrs={"class": "form-input", "rows": 3}),
            "cancellation_reason": forms.Textarea(attrs={"class": "form-input", "rows": 3}),
        }


from django import forms
from resort.models import *

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = [
            "code",
            "discount_amount",
            "valid_from",
            "valid_until",
            "is_active",
        ]
        widgets = {
            "code": forms.TextInput(attrs={"class": "form-input", "placeholder": "SUMMER50"}),
            "discount_amount": forms.NumberInput(attrs={"class": "form-input"}),
            "valid_from": forms.DateInput(attrs={"type": "date", "class": "form-input"}),
            "valid_until": forms.DateInput(attrs={"type": "date", "class": "form-input"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-checkbox"}),
        }



class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = [
            "title",
            "category",
            "image",
            "is_featured",
            "slot_position",
        ]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Photo title"
            }),
            "category": forms.Select(attrs={
                "class": "form-select"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-input"
            }),
            "is_featured": forms.CheckboxInput(attrs={
                "class": "form-checkbox"
            }),
            "slot_position": forms.NumberInput(attrs={
                "class": "form-input",
                "placeholder": "Optional display order"
            }),
        }
