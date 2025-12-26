from django import forms
from .models import Booking, ContactMessage ,Testimonial


class BookingForm(forms.ModelForm):
    coupon_code = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-transparent',
        'placeholder': 'Coupon Code (Optional)'
    }))
    payment_method = forms.ChoiceField(
        required=True,
        choices=Booking.PAYMENT_METHOD_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'space-y-2'
        })
    )
    class Meta:
        model = Booking
        fields = [
            'guest_name', 'guest_email', 'guest_phone', 'payment_method',
            'guest_count', 'check_in', 'check_out', 'special_requests','extra_guest_count',
        ]
        labels = {
            'guest_name': 'Full Name',
            'guest_email': 'Email Address',
            'guest_phone': 'Mobile Number',
            'guest_count': 'Number of Guests',
            'extra_guest_count': 'Extra Guest Count',
            'check_in': 'Check-in Date',
            'check_out': 'Check-out Date',
            'special_requests': 'Special Requests',
            'payment_method': 'Payment Method',
        }
        widgets = {
            'guest_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-transparent',
                'placeholder': 'Full Name'
            }),
            'guest_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-transparent',
                'placeholder': 'Email Address'
            }),
            'guest_phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-transparent',
                'placeholder': 'Phone Number'
            }),
            'guest_count': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-transparent',
                'min': '1',
                'readonly': 'readonly'
            }),
            'extra_guest_count': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-emerald-600 focus:border-transparent',
                'min': '0',
                'max': '5',
                'placeholder': 'Extra guests (max 5)'
            }),

            'check_in': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-transparent',
                'type': 'date'
            }),
            'check_out': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-transparent',
                'type': 'date'
            }),
            'special_requests': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-transparent',
                'rows': '4',
                'placeholder': 'Any special requests or requirements...'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out:
            if check_out <= check_in:
                raise forms.ValidationError('Check-out date must be after check-in date.')

        return cleaned_data

    def clean_guest_count(self):
        guest_count = self.cleaned_data.get("guest_count")

        if guest_count > 15:
            raise forms.ValidationError("Guest count cannot exceed 15.")

        return guest_count

    def clean_extra_guest_count(self):
        extra = self.cleaned_data.get("extra_guest_count")

        if extra > 5:
            raise forms.ValidationError("Extra guest count cannot exceed 5.")

        return extra

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-transparent',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-transparent',
                'placeholder': 'Your Email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-transparent',
                'placeholder': 'Your Phone'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-transparent',
                'placeholder': 'Subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-transparent',
                'rows': '5',
                'placeholder': 'Your Message'
            }),
        }





from .models import Amenity

class AmenityForm(forms.ModelForm):
    class Meta:
        model = Amenity
        fields = [
            'name',
            'icon',
            'description',
            'is_featured',
            'amenity_image',
            'slot_position',
        ]





from .models import BlockedDate

class BlockedDateForm(forms.ModelForm):
    class Meta:
        model = BlockedDate
        fields = ['start_date', 'end_date', 'reason']

        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'reason': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Maintenance'}),
        }



class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['guest_name', 'guest_location', 'rating', 'comment',  "slot_position", "is_featured"]
        widgets = {
            'guest_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-transparent',
                'placeholder': 'Your Name'
            }),
            'guest_location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-transparent',
                'placeholder': 'Where are you from?'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-transparent',
                'min': '1',
                'max': '5',
                'placeholder': 'Rating (1-5)'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-transparent',
                'rows': '4',
                'placeholder': 'Share your experience...'
            }),
             "slot_position": forms.NumberInput(attrs={
                "class": "form-input",
                "placeholder": "Display order (optional)"
            }),
            "is_featured": forms.CheckboxInput(attrs={
                "class": "form-checkbox"
            }),
        }
