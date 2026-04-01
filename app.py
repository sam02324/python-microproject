"""
Hotel Management System - Web Application
Flask-based web interface for hotel management
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'hotel_secret_key_12345'  # Change this in production

class Room:
    """Represents a hotel room with its properties"""
    
    def __init__(self, room_number, room_type, price_per_night, is_available=True):
        self.room_number = room_number
        self.room_type = room_type
        self.price_per_night = price_per_night
        self.is_available = is_available
    
    def to_dict(self):
        return {
            'room_number': self.room_number,
            'room_type': self.room_type,
            'price_per_night': self.price_per_night,
            'is_available': self.is_available
        }


class Booking:
    """Represents a booking with customer and room details"""
    
    def __init__(self, booking_id, customer_name, room_number, check_in_date, check_out_date, total_amount):
        self.booking_id = booking_id
        self.customer_name = customer_name
        self.room_number = room_number
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.total_amount = total_amount
        self.is_checked_in = False
        self.is_checked_out = False
        self.payment_status = "Pending"
    
    def to_dict(self):
        return {
            'booking_id': self.booking_id,
            'customer_name': self.customer_name,
            'room_number': self.room_number,
            'check_in_date': self.check_in_date,
            'check_out_date': self.check_out_date,
            'total_amount': self.total_amount,
            'is_checked_in': self.is_checked_in,
            'is_checked_out': self.is_checked_out,
            'payment_status': self.payment_status
        }


class Hotel:
    """Main hotel management system"""
    
    def __init__(self, name):
        self.name = name
        self.rooms = []
        self.bookings = []
        self.booking_counter = 1000
        self.data_file = "hotel_data.json"
        self.load_data()
    
    def add_room(self, room_number, room_type, price_per_night):
        """Add a new room to the hotel"""
        room = Room(room_number, room_type, price_per_night)
        self.rooms.append(room)
    
    def get_available_rooms(self):
        """Get all available rooms"""
        return [room for room in self.rooms if room.is_available]
    
    def calculate_nights(self, check_in, check_out):
        """Calculate number of nights between two dates"""
        date_format = "%Y-%m-%d"
        check_in_date = datetime.datetime.strptime(check_in, date_format)
        check_out_date = datetime.datetime.strptime(check_out, date_format)
        nights = (check_out_date - check_in_date).days
        return nights
    
    def create_booking(self, customer_name, room_number, check_in_date, check_out_date):
        """Create a new booking"""
        room = None
        for r in self.rooms:
            if r.room_number == room_number:
                room = r
                break
        
        if not room or not room.is_available:
            return None
        
        nights = self.calculate_nights(check_in_date, check_out_date)
        if nights <= 0:
            return None
        
        total_amount = nights * room.price_per_night
        
        booking_id = self.booking_counter
        self.booking_counter += 1
        
        booking = Booking(booking_id, customer_name, room_number, check_in_date, check_out_date, total_amount)
        self.bookings.append(booking)
        room.is_available = False
        
        self.save_data()
        return booking
    
    def check_in(self, booking_id):
        """Check-in a customer"""
        booking = self.find_booking(booking_id)
        
        if not booking or booking.is_checked_in:
            return False
        
        booking.is_checked_in = True
        self.save_data()
        return True
    
    def check_out(self, booking_id):
        """Check-out a customer"""
        booking = self.find_booking(booking_id)
        
        if not booking or not booking.is_checked_in or booking.is_checked_out:
            return False
        
        if booking.payment_status != "Paid":
            return False
        
        booking.is_checked_out = True
        
        for room in self.rooms:
            if room.room_number == booking.room_number:
                room.is_available = True
                break
        
        self.save_data()
        return True
    
    def process_payment(self, booking_id, amount_paid):
        """Process payment for a booking"""
        booking = self.find_booking(booking_id)
        
        if not booking or booking.payment_status == "Paid":
            return False
        
        if amount_paid < booking.total_amount:
            return False
        
        booking.payment_status = "Paid"
        self.save_data()
        return True
    
    def find_booking(self, booking_id):
        """Find a booking by ID"""
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                return booking
        return None
    
    def save_data(self):
        """Save hotel data to file"""
        data = {
            'booking_counter': self.booking_counter,
            'rooms': [r.to_dict() for r in self.rooms],
            'bookings': [b.to_dict() for b in self.bookings]
        }
        
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)
    
    def load_data(self):
        """Load hotel data from file"""
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            self.booking_counter = data.get('booking_counter', 1000)
            
            for room_data in data.get('rooms', []):
                room = Room(
                    room_data['room_number'],
                    room_data['room_type'],
                    room_data['price_per_night'],
                    room_data['is_available']
                )
                self.rooms.append(room)
            
            for booking_data in data.get('bookings', []):
                booking = Booking(
                    booking_data['booking_id'],
                    booking_data['customer_name'],
                    booking_data['room_number'],
                    booking_data['check_in_date'],
                    booking_data['check_out_date'],
                    booking_data['total_amount']
                )
                booking.is_checked_in = booking_data['is_checked_in']
                booking.is_checked_out = booking_data['is_checked_out']
                booking.payment_status = booking_data['payment_status']
                self.bookings.append(booking)
        
        except Exception as e:
            print(f"Error loading data: {e}")


# Initialize hotel
hotel = Hotel("Grand Plaza Hotel")

# Add rooms if starting fresh
if not hotel.rooms:
    hotel.add_room(101, "Single", 100)
    hotel.add_room(102, "Single", 100)
    hotel.add_room(201, "Double", 150)
    hotel.add_room(202, "Double", 150)
    hotel.add_room(301, "Suite", 250)
    hotel.add_room(302, "Suite", 250)
    hotel.save_data()


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html', hotel_name=hotel.name)


@app.route('/rooms')
def view_rooms():
    """View available rooms"""
    available_rooms = hotel.get_available_rooms()
    return render_template('rooms.html', rooms=available_rooms, hotel_name=hotel.name)


@app.route('/book', methods=['GET', 'POST'])
def book_room():
    """Create a booking"""
    if request.method == 'POST':
        customer_name = request.form.get('customer_name')
        room_number = int(request.form.get('room_number'))
        check_in = request.form.get('check_in')
        check_out = request.form.get('check_out')
        
        booking = hotel.create_booking(customer_name, room_number, check_in, check_out)
        
        if booking:
            flash(f'Booking successful! Your Booking ID is: {booking.booking_id}', 'success')
            return redirect(url_for('view_bookings'))
        else:
            flash('Booking failed! Please check room availability and dates.', 'error')
    
    available_rooms = hotel.get_available_rooms()
    return render_template('book.html', rooms=available_rooms, hotel_name=hotel.name)


@app.route('/bookings')
def view_bookings():
    """View all bookings"""
    return render_template('bookings.html', bookings=hotel.bookings, hotel_name=hotel.name)


@app.route('/checkin', methods=['GET', 'POST'])
def check_in():
    """Check-in page"""
    if request.method == 'POST':
        booking_id = int(request.form.get('booking_id'))
        
        if hotel.check_in(booking_id):
            flash(f'Check-in successful for Booking ID: {booking_id}', 'success')
        else:
            flash('Check-in failed! Please verify booking ID.', 'error')
        
        return redirect(url_for('view_bookings'))
    
    return render_template('checkin.html', hotel_name=hotel.name)


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    """Payment processing page"""
    if request.method == 'POST':
        booking_id = int(request.form.get('booking_id'))
        amount_paid = float(request.form.get('amount_paid'))
        
        booking = hotel.find_booking(booking_id)
        
        if booking and hotel.process_payment(booking_id, amount_paid):
            flash(f'Payment successful for Booking ID: {booking_id}', 'success')
        else:
            flash('Payment failed! Please check booking ID and amount.', 'error')
        
        return redirect(url_for('view_bookings'))
    
    return render_template('payment.html', hotel_name=hotel.name)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Check-out page"""
    if request.method == 'POST':
        booking_id = int(request.form.get('booking_id'))
        
        if hotel.check_out(booking_id):
            flash(f'Check-out successful for Booking ID: {booking_id}', 'success')
        else:
            flash('Check-out failed! Ensure payment is completed.', 'error')
        
        return redirect(url_for('view_bookings'))
    
    return render_template('checkout.html', hotel_name=hotel.name)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
