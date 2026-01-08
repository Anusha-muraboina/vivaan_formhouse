# Vivaan Farmhouse - Django Booking System

A complete Django-based resort booking website inspired by Vivaan Farmhouse, Hyderabad. Features a beautiful, responsive design with Tailwind CSS.

## Features

- 🏨 **Room Management**: Multiple room categories with detailed information
- 📅 **Booking System**: Easy-to-use booking form with validation
- 🎁 **Special Offers**: Dynamic offers management with discount system
- 🖼️ **Photo Gallery**: Beautiful image gallery with category filters
- ⭐ **Testimonials**: Guest reviews and ratings
- 🎯 **Amenities Showcase**: Comprehensive facilities listing
- 📱 **Responsive Design**: Mobile-first design with Tailwind CSS
- 🎨 **Modern UI**: Premium design with animations and hover effects
- 👨‍💼 **Admin Panel**: Full-featured Django admin for content management

## Tech Stack

- **Backend**: Python 3.x, Django 4.2.7
- **Frontend**: HTML5, Tailwind CSS 3.x, JavaScript
- **Database**: SQLite (default, can be changed to PostgreSQL/MySQL)
- **Icons**: Font Awesome 6.4.0
- **Fonts**: Google Fonts (Playfair Display, Inter)

## Installation & Setup

### 1. Create Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run Migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Admin)

```powershell
python manage.py createsuperuser
```

Follow the prompts to create an admin account:
- Username: admin (or your choice)
- Email: admin@example.com
- Password: (create a secure password)

### 5. Populate Dummy Data

```powershell
python manage.py populate_data
```

This will create:
- 8 Room Categories with multiple rooms each
- 15 Amenities
- 4 Special Offers
- 6 Guest Testimonials

### 6. Run Development Server

```powershell
python manage.py runserver
```

The website will be available at: **http://127.0.0.1:8000/**

Admin panel at: **http://127.0.0.1:8000/admin/**

## Project Structure

```
resort-booking/
├── resort_project/          # Main project settings
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URL configuration
│   ├── wsgi.py             # WSGI configuration
│   └── asgi.py             # ASGI configuration
├── resort/                  # Main app
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # App URL patterns
│   ├── forms.py            # Django forms
│   ├── admin.py            # Admin configuration
│   └── management/         # Management commands
│       └── commands/
│           └── populate_data.py
├── templates/              # HTML templates
│   └── resort/
│       ├── base.html       # Base template
│       ├── home.html       # Homepage
│       ├── rooms.html      # Rooms listing
│       ├── room_detail.html
│       ├── booking_confirmation.html
│       ├── about.html
│       ├── amenities.html
│       ├── offers.html
│       ├── gallery.html
│       └── contact.html
├── static/                 # Static files (CSS, JS, images)
├── media/                  # User uploaded media
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Pages

1. **Homepage** (`/`) - Hero section, featured rooms, amenities, offers, testimonials
2. **Rooms** (`/rooms/`) - All room categories with filters
3. **Room Detail** (`/room/<slug>/`) - Detailed room info with booking form
4. **Booking Confirmation** (`/booking/<id>/`) - Booking success page
5. **About** (`/about/`) - Resort information and story
6. **Amenities** (`/amenities/`) - Full amenities list
7. **Offers** (`/offers/`) - Current promotional offers
8. **Gallery** (`/gallery/`) - Photo gallery with categories
9. **Contact** (`/contact/`) - Contact form and information

## Models

### RoomCategory
- Room types with pricing, descriptions, amenities
- Fields: name, slug, description, size, occupancy, price, view type, etc.

### Room
- Individual room units
- Linked to room categories
- Availability tracking

### Booking
- Guest booking information
- Auto-generated booking IDs
- Status tracking (pending, confirmed, cancelled, completed)

### Amenity
- Resort facilities and services

### Offer
- Special deals with discount percentages
- Date-based validity

### Testimonial
- Guest reviews with ratings

### Gallery
- Photo gallery with categorization

### ContactMessage
- Contact form submissions

## Admin Features

Access the admin panel at `/admin/` with your superuser credentials.

**Manage:**
- Room categories and individual rooms
- Bookings (view, update status, manage)
- Amenities
- Special offers
- Testimonials
- Gallery images
- Contact messages

## Customization

### Colors
Edit the CSS variables in `templates/resort/base.html`:
```css
:root {
    --primary-red: #DC2626;
    --primary-dark: #991B1B;
    --accent-gold: #F59E0B;
}
```

### Content
Use the Django admin panel to:
- Add/edit room categories
- Update pricing
- Manage offers
- Add testimonials
- Upload gallery images

## Room Categories Included

1. Deluxe Garden View – Ground Floor (200 sq ft, 2 guests)
2. Deluxe Garden View – First Floor (230 sq ft, 3 guests)
3. Standard Room – Ground Floor (230 sq ft, 4 guests)
4. Deluxe Valley View with Balcony – First Floor (250 sq ft, 4 guests)
5. Deluxe Valley View with Balcony – Ground Floor (250 sq ft, 4 guests)
6. Superior Valley View with Balcony – First Floor (250 sq ft, 4 guests)
7. Tranquil Terrace with Balcony – First Floor (270 sq ft, 3 guests)
8. Penthouse Suite with Pool & Valley View (370 sq ft, 6 guests)

## Special Offers

- **Direct Booking Offer** - 20% discount on direct bookings
- **Early Bird Offer** - 5% off when booking 2+ days in advance
- **Long Stay Offer** - 5% off for 3+ nights
- **Last Minute Offer** - 5% off for same-day bookings

## Support

For issues or questions:
- Create an issue on GitHub
- Email: support@example.com

## License

This project is for demonstration purposes. Customize as needed for your use case.

## Credits

- Design inspired by [Vivaan Farmhouse](https://www.strawberrykingresort.com/)
- Built with Django and Tailwind CSS
- Icons by Font Awesome
- Fonts by Google Fonts

---

**Enjoy building with Django!** 🎉
