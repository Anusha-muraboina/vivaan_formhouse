from django.core.management.base import BaseCommand
from django.utils.text import slugify
from datetime import datetime, timedelta
from resort.models import (
    RoomCategory, Room, Amenity, Offer, Testimonial
)


class Command(BaseCommand):
    help = 'Populate database with dummy data for Vivaan Farmhouse'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting to populate database...')

        # Clear existing data
        self.stdout.write('Clearing existing data...')
        RoomCategory.objects.all().delete()
        Amenity.objects.all().delete()
        Offer.objects.all().delete()
        Testimonial.objects.all().delete()

        # Create Room Categories
        self.stdout.write('Creating room categories...')
        rooms_data = [
            {
                'name': 'Deluxe Garden View – Ground Floor',
                'description': 'This 200 sq. ft. room offers a cosy hideaway for two, complete with a private bathtub and soothing garden views. A one-of-a-kind retreat, perfect for peaceful pauses and unhurried evenings.',
                'size_sqft': 200,
                'max_occupancy': 2,
                'floor': 'Ground Floor',
                'base_price': 3500,
                'view_type': 'garden',
                'has_balcony': False,
                'has_bathtub': True,
            },
            {
                'name': 'Deluxe Garden View – First Floor',
                'description': 'With 230 sq. ft. of space, this room accommodates up to three guests and offers gentle views of the garden from its first-floor perch. A single, serene retreat made for quiet moments and nature\'s soft embrace.',
                'size_sqft': 230,
                'max_occupancy': 3,
                'floor': 'First Floor',
                'base_price': 3800,
                'view_type': 'garden',
                'has_balcony': False,
                'has_bathtub': False,
            },
            {
                'name': 'Standard Room – Ground Floor',
                'description': 'Simple yet soothing, these 230 sq. ft. rooms accommodate four guests, making them ideal for families. With four rooms available, each provides a comforting space that offers all the essentials with a touch of warmth.',
                'size_sqft': 230,
                'max_occupancy': 4,
                'floor': 'Ground Floor',
                'base_price': 3200,
                'view_type': 'standard',
                'has_balcony': False,
                'has_bathtub': False,
            },
            {
                'name': 'Deluxe Valley View Room with Balcony – First Floor',
                'description': 'Spread across 250 sq. ft., these four rooms offer a serene escape for up to four guests, with private balconies overlooking the lush Mahabaleshwar valley. Wake up to drifting clouds or unwind as the sunset paints the hills in gold.',
                'size_sqft': 250,
                'max_occupancy': 4,
                'floor': 'First Floor',
                'base_price': 4500,
                'view_type': 'valley',
                'has_balcony': True,
                'has_bathtub': False,
            },
            {
                'name': 'Deluxe Valley View Room with Balcony – Ground Floor',
                'description': 'These 250 sq. ft. rooms are designed for up to four guests, offering uninterrupted views of the valley from a private balcony. Set beside the rolling greens, all four rooms in this category promise a tranquil escape worthy of your travel diaries.',
                'size_sqft': 250,
                'max_occupancy': 4,
                'floor': 'Ground Floor',
                'base_price': 4300,
                'view_type': 'valley',
                'has_balcony': True,
                'has_bathtub': False,
            },
            {
                'name': 'Superior Valley View Room with Balcony – First Floor',
                'description': 'Spanning 250 sq. ft., these rooms are perfect for four guests, offering breathtaking valley views and cool breezes from their private balconies. With five rooms available, each provides a peaceful retreat, where the captivating landscape invites you to relax and lose yourself in nature\'s embrace.',
                'size_sqft': 250,
                'max_occupancy': 4,
                'floor': 'First Floor',
                'base_price': 4800,
                'view_type': 'valley',
                'has_balcony': True,
                'has_bathtub': False,
            },
            {
                'name': 'Tranquil Terrace with Balcony – First Floor',
                'description': 'Spanning 270 sq. ft., this room accommodates up to three guests, offering a generous balcony and a spacious washroom for a truly relaxing stay. A one-of-a-kind retreat, designed for leisurely mornings and intimate evening moments.',
                'size_sqft': 270,
                'max_occupancy': 3,
                'floor': 'First Floor',
                'base_price': 5000,
                'view_type': 'valley',
                'has_balcony': True,
                'has_bathtub': True,
            },
            {
                'name': 'Penthouse Suite with Balcony – Pool & Valley View – First Floor',
                'description': 'A spacious 370 sq. ft. haven designed for up to six guests, this suite combines panoramic views of the valley and infinity pool from its private balcony. With just one such room, it promises an indulgent, sky-kissed retreat.',
                'size_sqft': 370,
                'max_occupancy': 6,
                'floor': 'First Floor',
                'base_price': 7500,
                'view_type': 'pool',
                'has_balcony': True,
                'has_bathtub': True,
            },
        ]

        for room_data in rooms_data:
            slug = slugify(room_data['name'])
            room_category = RoomCategory.objects.create(
                slug=slug,
                **room_data
            )
            
            # Create 2-4 actual rooms for each category
            num_rooms = 3 if room_data['max_occupancy'] <= 3 else 4
            for i in range(1, num_rooms + 1):
                Room.objects.create(
                    category=room_category,
                    room_number=f"{room_category.id}{i:02d}",
                    is_available=True
                )
            
            self.stdout.write(f'  Created: {room_data["name"]}')

        # Create Amenities
        self.stdout.write('Creating amenities...')
        amenities_data = [
            {'name': 'King Size Bed', 'is_featured': True},
            {'name': 'Swimming Pool', 'is_featured': True},
            {'name': 'Multi-cuisine Food', 'is_featured': True},
            {'name': 'Rooms with Attached Balcony', 'is_featured': True},
            {'name': 'Attached Strawberry Farm', 'is_featured': True},
            {'name': 'Airport Shuttle', 'is_featured': True},
            {'name': 'Cab Rental', 'is_featured': True},
            {'name': 'Board Games', 'is_featured': True},
            {'name': 'Bonfire', 'is_featured': True},
            {'name': 'Laundry Service', 'is_featured': True},
            {'name': 'Music System', 'is_featured': True},
            {'name': 'Free WiFi', 'is_featured': True},
            {'name': '24-hour Room Service', 'is_featured': False},
            {'name': 'Parking', 'is_featured': True},
            {'name': 'Packed Breakfast', 'is_featured': False},
        ]

        for amenity_data in amenities_data:
            Amenity.objects.create(**amenity_data)
            self.stdout.write(f'  Created amenity: {amenity_data["name"]}')

        # Create Offers
        self.stdout.write('Creating offers...')
        today = datetime.now().date()
        
        offers_data = [
            {
                'title': 'Direct Booking Offer',
                'description': 'Enjoy exclusive savings by booking your stay directly on our official website. Lock in a 20% discount and make your getaway even more rewarding—from the very first click.',
                'discount_percentage': 20,
                'terms': 'Valid only on direct bookings through our website. Cannot be combined with other offers.',
                'valid_from': today,
                'valid_until': today + timedelta(days=90),
            },
            {
                'title': 'Early Bird Offer',
                'description': 'Plan ahead and save! Book 2 or more days before check-in to grab a 5% discount. It\'s the smart choice for travellers who love locking in their vacation early and scoring great deals.',
                'discount_percentage': 5,
                'terms': 'Must be booked at least 2 days before check-in date.',
                'valid_from': today,
                'valid_until': today + timedelta(days=120),
            },
            {
                'title': 'Long Stay Offer',
                'description': 'Enjoy a serene escape by staying with us for 3 or more consecutive days and unlock a 5% discount on your entire booking. Perfect for those who want to fully relax and soak in the beauty of Mahabaleshwar at their own pace.',
                'discount_percentage': 5,
                'terms': 'Minimum 3 nights stay required. Discount applied to total booking amount.',
                'valid_from': today,
                'valid_until': today + timedelta(days=180),
            },
            {
                'title': 'Last Minute Offer',
                'description': 'Need a spontaneous trip? Book your stay just 1 day before check-in and still benefit from a 5% discount. Enjoy the convenience of last-minute plans without missing out on great savings at Vivaan Farmhouse.',
                'discount_percentage': 5,
                'terms': 'Valid for bookings made within 24 hours of check-in. Subject to availability.',
                'valid_from': today,
                'valid_until': today + timedelta(days=60),
            },
        ]

        for offer_data in offers_data:
            slug = slugify(offer_data['title'])
            Offer.objects.create(slug=slug, **offer_data)
            self.stdout.write(f'  Created offer: {offer_data["title"]}')

        # Create Testimonials
        self.stdout.write('Creating testimonials...')
        testimonials_data = [
            {
                'guest_name': 'Raj Sharma',
                'guest_location': 'Mumbai, Maharashtra',
                'rating': 5,
                'comment': 'Absolutely stunning views and impeccable service! The valley view from our balcony was breathtaking. The strawberry plucking experience was a delightful surprise. Highly recommended for a peaceful getaway.',
                'is_featured': True,
            },
            {
                'guest_name': 'Priya Patel',
                'guest_location': 'Pune, Maharashtra',
                'rating': 5,
                'comment': 'Perfect place for a romantic weekend. The room was spacious and well-maintained. Food at the restaurant was delicious. Will definitely visit again!',
                'is_featured': True,
            },
            {
                'guest_name': 'Amit Kumar',
                'guest_location': 'Delhi',
                'rating': 4,
                'comment': 'Great location, friendly staff, and beautiful surroundings. The infinity pool overlooking the valley is a must-experience. Only minor issue was the WiFi speed, but overall a fantastic stay.',
                'is_featured': True,
            },
            {
                'guest_name': 'Sneha Reddy',
                'guest_location': 'Bangalore, Karnataka',
                'rating': 5,
                'comment': 'One of the best resorts we\'ve stayed at in Mahabaleshwar. The staff went above and beyond to make our anniversary special. Thank you for the wonderful memories!',
                'is_featured': True,
            },
            {
                'guest_name': 'Vikram Singh',
                'guest_location': 'Hyderabad, Telangana',
                'rating': 5,
                'comment': 'Excellent hospitality and pristine rooms. The bonfire night was magical. Perfect for families and couples alike. The kids loved the strawberry farm!',
                'is_featured': True,
            },
            {
                'guest_name': 'Meera Joshi',
                'guest_location': 'Ahmedabad, Gujarat',
                'rating': 4,
                'comment': 'Lovely resort with amazing views. Breakfast spread was good and the staff was very courteous. Would love to come back during the monsoon season.',
                'is_featured': True,
            },
        ]

        for testimonial_data in testimonials_data:
            Testimonial.objects.create(**testimonial_data)
            self.stdout.write(f'  Created testimonial from: {testimonial_data["guest_name"]}')

        self.stdout.write(self.style.SUCCESS('\nDatabase populated successfully!'))
        self.stdout.write(f'  Room Categories: {RoomCategory.objects.count()}')
        self.stdout.write(f'  Rooms: {Room.objects.count()}')
        self.stdout.write(f'  Amenities: {Amenity.objects.count()}')
        self.stdout.write(f'  Offers: {Offer.objects.count()}')
        self.stdout.write(f'  Testimonials: {Testimonial.objects.count()}')
