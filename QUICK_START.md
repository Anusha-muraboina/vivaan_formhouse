# 🏨 STRAWBERRY KING RESORT - QUICK START GUIDE

## ✅ Project Successfully Set Up!

Your Django resort booking application is ready to use!

---

## 🚀 SERVER IS RUNNING

**Website URL**: http://127.0.0.1:8000/
**Admin Panel**: http://127.0.0.1:8000/admin/

### Admin Credentials:
- **Username**: `admin`
- **Password**: `admin123`

---

## 📋 What's Been Created

### ✨ Database (Already Populated with Dummy Data)
- ✅ **8 Room Categories** (from ₹3,200 to ₹7,500/night)
- ✅ **29 Individual Rooms** (across all categories)
- ✅ **15 Amenities** (Swimming Pool, WiFi, etc.)
- ✅ **4 Special Offers** (Direct Booking 20% off, etc.)
- ✅ **6 Guest Testimonials** (5-star reviews)

### 📄 All Pages Created
1. **Homepage** (/) - Hero, rooms, offers, testimonials
2. **Rooms** (/rooms/) - All room categories with filters
3. **Room Detail** (/room/<slug>/) - Booking form
4. **Booking Confirmation** (/booking/<id>/)
5. **About** (/about/) - Resort story
6. **Amenities** (/amenities/) - Facilities showcase
7. **Offers** (/offers/) - Special deals
8. **Gallery** (/gallery/) - Photo gallery
9. **Contact** (/contact/) - Contact form

---

## 🎯 HOW TO USE

### For Testing (User Side):
1. Open browser: http://127.0.0.1:8000/
2. Browse rooms, amenities, offers
3. Book a room from a room detail page
4. Fill the booking form and submit
5. View booking confirmation

### For Management (Admin Side):
1. Open browser: http://127.0.0.1:8000/admin/
2. Login with admin/admin123
3. Manage:
   - Room categories & rooms
   - Bookings (view/update status)
   - Amenities
   - Special offers
   - Testimonials
   - Gallery images
   - Contact messages

---

## 💡 ROOM CATEGORIES AVAILABLE

| Room Type | Size | Guests | Price | Features |
|-----------|------|--------|-------|----------|
| Deluxe Garden View (GF) | 200 sq ft | 2 | ₹3,500 | Garden View, Bathtub |
| Deluxe Garden View (FF) | 230 sq ft | 3 | ₹3,800 | Garden View |
| Standard Room | 230 sq ft | 4 | ₹3,200 | Family Room |
| Deluxe Valley View (FF) | 250 sq ft | 4 | ₹4,500 | Valley View, Balcony |
| Deluxe Valley View (GF) | 250 sq ft | 4 | ₹4,300 | Valley View, Balcony |
| Superior Valley View | 250 sq ft | 4 | ₹4,800 | Premium Valley View |
| Tranquil Terrace | 270 sq ft | 3 | ₹5,000 | Terrace, Bathtub |
| Penthouse Suite | 370 sq ft | 6 | ₹7,500 | Pool & Valley View |

---

## 🎁 ACTIVE OFFERS

1. **Direct Booking Offer** - 20% discount
2. **Early Bird Offer** - 5% off (book 2+ days ahead)
3. **Long Stay Offer** - 5% off (3+ nights)
4. **Last Minute Offer** - 5% off (same day booking)

---

## 🛠️ COMMANDS REFERENCE

### Start Server:
```powershell
.\venv\Scripts\python.exe manage.py runserver
```

### Stop Server:
Press `CTRL+C` in terminal

### Create New Admin User:
```powershell
.\venv\Scripts\python.exe manage.py createsuperuser
```

### Repopulate Data:
```powershell
.\venv\Scripts\python.exe manage.py populate_data
```

### Make Database Changes:
```powershell
.\venv\Scripts\python.exe manage.py makemigrations
.\venv\Scripts\python.exe manage.py migrate
```

---

## 📱 FEATURES

### Frontend:
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Beautiful Tailwind CSS styling
- ✅ Smooth animations and hover effects
- ✅ Premium color scheme (Red & Gold theme)
- ✅ Custom fonts (Playfair Display + Inter)
- ✅ Font Awesome icons

### Backend:
- ✅ Django 4.2.7
- ✅ SQLite database
- ✅ Room booking system
- ✅ Offer management
- ✅ Contact form
- ✅ Admin panel
- ✅ Auto-generated booking IDs

### Models:
- ✅ RoomCategory (room types)
- ✅ Room (individual rooms)
- ✅ Booking (reservations)
- ✅ Amenity (facilities)
- ✅ Offer (discounts)
- ✅ Testimonial (reviews)
- ✅ Gallery (photos)
- ✅ ContactMessage (inquiries)

---

## 🎨 CUSTOMIZATION

### Change Colors:
Edit `templates/resort/base.html`:
```css
:root {
    --primary-red: #DC2626;  /* Main color */
    --primary-dark: #991B1B; /* Dark variant */
    --accent-gold: #F59E0B;  /* Accent color */
}
```

### Add Content:
Use Django Admin Panel at http://127.0.0.1:8000/admin/

---

## 📂 PROJECT STRUCTURE

```
resort-booking/
├── resort_project/     # Main Django project
├── resort/            # Main app
│   ├── models.py      # Database models
│   ├── views.py       # Page views
│   ├── urls.py        # URL patterns
│   ├── forms.py       # Booking/Contact forms
│   ├── admin.py       # Admin config
│   └── management/    # Custom commands
├── templates/resort/  # HTML templates
├── static/           # CSS, JS, images
├── media/            # Uploaded files
├── venv/             # Virtual environment
└── db.sqlite3        # Database
```

---

## 🌟 NEXT STEPS

1. **Browse the Website**: http://127.0.0.1:8000/
2. **Login to Admin**: http://127.0.0.1:8000/admin/
3. **Test Booking**: Create a test reservation
4. **Customize Content**: Add your own rooms, images, offers
5. **Upload Images**: Add gallery photos via admin panel

---

## 🔒 SECURITY NOTE

⚠️ **IMPORTANT**: This is a development setup!
- Change `SECRET_KEY` in `resort_project/settings.py`
- Change admin password before production
- Set `DEBUG = False` in production
- Use PostgreSQL/MySQL for production
- Configure proper static file serving

---

## 📞 SUPPORT

If you need help:
1. Check the README.md file
2. Review Django documentation
3. Check the code comments
4. Test in admin panel first

---

## ✅ CHECKLIST

- [x] Virtual environment created
- [x] Dependencies installed
- [x] Database migrated
- [x] Dummy data populated
- [x] Admin user created
- [x] Server running
- [ ] Browse website
- [ ] Test booking
- [ ] Explore admin panel
- [ ] Customize content

---

**🎉 Enjoy your Strawberry King Resort booking system!**

Made with Django, Tailwind CSS, and ❤️
