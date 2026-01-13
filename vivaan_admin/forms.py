

from django import forms
from resort.models import *

from decimal import Decimal
from django.utils import timezone

class AdminBookingForm(forms.ModelForm):
    coupon_code = forms.CharField(
        required=False,
        label="Coupon Code",
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "Enter coupon code (optional)"
        })
    )
    class Meta:
        model = Booking
        fields = [
            # Guest info
            "guest_name",
            "guest_email",
            "guest_phone",

            # Guests
            "guest_count",
            "extra_guest_count",

            # Dates
            "check_in",
            "check_out",

            "check_in_time",
            "check_out_time",
            
            # Status & payment (ADMIN ONLY)
            "payment_method",
            "payment_status",
            "status",
            "cancellation_reason",

            # Optional
            "special_requests",
        ]

        widgets = {
            "guest_name": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Guest name"
            }),
            "guest_email": forms.EmailInput(attrs={
                "class": "form-input",
                "placeholder": "Email"
            }),
            "guest_phone": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Phone number"
            }),
            "guest_count": forms.NumberInput(attrs={
                "class": "form-input",
                "min": 1
            }),
            "extra_guest_count": forms.NumberInput(attrs={
                "class": "form-input",
                "min": 0
            }),

            "check_in": forms.TextInput(attrs={
                "class": "form-input",
                "autocomplete": "off",
                "placeholder": "YYYY-MM-DD"
            }),
            "check_out": forms.TextInput(attrs={
                "class": "form-input",
                "autocomplete": "off",
                "placeholder": "YYYY-MM-DD"
            }),
            "check_in_time": forms.TimeInput(attrs={
                "class": "form-input",
                "type": "time"
            }),
            "check_out_time": forms.TimeInput(attrs={
                "class": "form-input",
                "type": "time"
            }),
            "payment_method": forms.Select(attrs={
                "class": "form-select"
            }),
            "payment_status": forms.Select(attrs={
                "class": "form-select"
            }),
            "status": forms.Select(attrs={
                "class": "form-select"
            }),

            "cancellation_reason": forms.Textarea(attrs={
                "class": "form-input",
                "rows": 3,
                "placeholder": "Reason (required if cancelled)"
            }),

            "special_requests": forms.Textarea(attrs={
                "class": "form-input",
                "rows": 3
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        status = cleaned_data.get("status")
        cancel_reason = cleaned_data.get("cancellation_reason")

        # 🔒 Require reason when cancelled
        if status == "cancelled" and not cancel_reason:
            self.add_error(
                "cancellation_reason",
                "Cancellation reason is required when status is cancelled."
            )

        return cleaned_data
    def clean_coupon_code(self):
            code = self.cleaned_data.get("coupon_code")
            if not code:
                return None

            try:
                coupon = Coupon.objects.get(
                    code__iexact=code,
                    is_active=True,
                    valid_from__lte=timezone.now().date(),
                    valid_until__gte=timezone.now().date()
                )
                return coupon
            except Coupon.DoesNotExist:
                raise forms.ValidationError("Invalid or expired coupon code.")



# class AdminBookingForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         fields = "__all__"
#         widgets = {
#             "check_in": forms.TextInput(attrs={
#                 "class": "form-input",
#                 "autocomplete": "off"
#             }),
#             "check_out": forms.TextInput(attrs={
#                 "class": "form-input",
#                 "autocomplete": "off"
#             }),
#         }



class AdminBlockedDateForm(forms.ModelForm):
    class Meta:
        model = BlockedDate
        fields = ['start_date', 'end_date', 'reason']

        widgets = {
            'start_date': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Select start date'
            }),
            'end_date': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Select end date'
            }),
            'reason': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Maintenance'
            }),
        }







# class AdminBookingForm(forms.ModelForm):

#     class Meta:
#         model = Booking
#         fields = [
#             "guest_name", "guest_email", "guest_phone",
#             "guest_count", "extra_guest_count",
#             "check_in", "check_out",
#             "special_requests",
#         ]

#         widgets = {
# "check_in": forms.TextInput(attrs={
#     "class": "form-control",
#     "placeholder": "Select check-in date",
# }),
# "check_out": forms.TextInput(attrs={
#     "class": "form-control",
#     "placeholder": "Select check-out date",
# }),

#         }


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
                "class": "w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500",
                "placeholder": "Photo title"
            }),
            "category": forms.Select(attrs={
                "class": "w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "w-full px-3 py-2 border rounded-lg"
            }),
            "is_featured": forms.CheckboxInput(attrs={
                "class": "h-4 w-4 text-indigo-600 rounded"
            }),
            "slot_position": forms.NumberInput(attrs={
                "class": "w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500",
                "placeholder": "Optional display order"
            }),
        }

# class GalleryForm(forms.ModelForm):
#     class Meta:
#         model = Gallery
#         fields = [
#             "title",
#             "category",
#             "image",
#             "is_featured",
#             "slot_position",
#         ]
#         widgets = {
#             "title": forms.TextInput(attrs={
#                 "class": "form-input",
#                 "placeholder": "Photo title"
#             }),
#             "category": forms.Select(attrs={
#                 "class": "form-select"
#             }),
#             "image": forms.ClearableFileInput(attrs={
#                 "class": "form-input"
#             }),
#             "is_featured": forms.CheckboxInput(attrs={
#                 "class": "form-checkbox"
#             }),
#             "slot_position": forms.NumberInput(attrs={
#                 "class": "form-input",
#                 "placeholder": "Optional display order"
#             }),
#         }
