"""
Hotel Management System
A simple system for room selection, booking, check-in/out, and payment processing
"""

import datetime
import json
import os

class Room:
    """Represents a hotel room with its properties"""
    
    def __init__(self, room_number, room_type, price_per_night, is_available=True):
        self.room_number = room_number
        self.room_type = room_type
        self.price_per_night = price_per_night
        self.is_available = is_available
    
    def __str__(self):
        status = "Available" if self.is_available else "Occupied"
        return f"Room {self.room_number} | Type: {self.room_type} | Price: ${self.price_per_night}/night | Status: {status}"


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
    
    def __str__(self):
        return f"Booking ID: {self.booking_id} | Customer: {self.customer_name} | Room: {self.room_number} | Check-in: {self.check_in_date} | Check-out: {self.check_out_date}"


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
        print(f"Room {room_number} added successfully!")
    
    def display_available_rooms(self):
        """Display all available rooms"""
        available_rooms = [room for room in self.rooms if room.is_available]
        
        if not available_rooms:
            print("\nNo rooms available at the moment.")
            return
        
        print("\n" + "="*60)
        print("AVAILABLE ROOMS")
        print("="*60)
        for room in available_rooms:
            print(room)
        print("="*60)
    
    def calculate_nights(self, check_in, check_out):
        """Calculate number of nights between two dates"""
        date_format = "%Y-%m-%d"
        check_in_date = datetime.datetime.strptime(check_in, date_format)
        check_out_date = datetime.datetime.strptime(check_out, date_format)
        nights = (check_out_date - check_in_date).days
        return nights
    
    def create_booking(self, customer_name, room_number, check_in_date, check_out_date):
        """Create a new booking"""
        # Find the room
        room = None
        for r in self.rooms:
            if r.room_number == room_number:
                room = r
                break
        
        if not room:
            print(f"Room {room_number} does not exist!")
            return None
        
        if not room.is_available:
            print(f"Room {room_number} is not available!")
            return None
        
        # Calculate total amount
        nights = self.calculate_nights(check_in_date, check_out_date)
        if nights <= 0:
            print("Invalid dates! Check-out must be after check-in.")
            return None
        
        total_amount = nights * room.price_per_night
        
        # Create booking
        booking_id = self.booking_counter
        self.booking_counter += 1
        
        booking = Booking(booking_id, customer_name, room_number, check_in_date, check_out_date, total_amount)
        self.bookings.append(booking)
        room.is_available = False
        
        print(f"\nBooking created successfully!")
        print(f"Booking ID: {booking_id}")
        print(f"Customer: {customer_name}")
        print(f"Room: {room_number}")
        print(f"Nights: {nights}")
        print(f"Total Amount: ${total_amount}")
        
        self.save_data()
        return booking
    
    def check_in(self, booking_id):
        """Check-in a customer"""
        booking = self.find_booking(booking_id)
        
        if not booking:
            print(f"Booking ID {booking_id} not found!")
            return False
        
        if booking.is_checked_in:
            print("Customer already checked in!")
            return False
        
        booking.is_checked_in = True
        print(f"\nCheck-in successful for {booking.customer_name}!")
        print(f"Room Number: {booking.room_number}")
        print(f"Enjoy your stay!")
        
        self.save_data()
        return True
    
    def check_out(self, booking_id):
        """Check-out a customer"""
        booking = self.find_booking(booking_id)
        
        if not booking:
            print(f"Booking ID {booking_id} not found!")
            return False
        
        if not booking.is_checked_in:
            print("Customer has not checked in yet!")
            return False
        
        if booking.is_checked_out:
            print("Customer already checked out!")
            return False
        
        if booking.payment_status != "Paid":
            print(f"\nPayment pending! Amount due: ${booking.total_amount}")
            return False
        
        booking.is_checked_out = True
        
        # Make room available again
        for room in self.rooms:
            if room.room_number == booking.room_number:
                room.is_available = True
                break
        
        print(f"\nCheck-out successful for {booking.customer_name}!")
        print(f"Thank you for staying at {self.name}!")
        
        self.save_data()
        return True
    
    def process_payment(self, booking_id, amount_paid):
        """Process payment for a booking"""
        booking = self.find_booking(booking_id)
        
        if not booking:
            print(f"Booking ID {booking_id} not found!")
            return False
        
        if booking.payment_status == "Paid":
            print("Payment already completed!")
            return False
        
        if amount_paid < booking.total_amount:
            print(f"Insufficient amount! Total due: ${booking.total_amount}")
            return False
        
        booking.payment_status = "Paid"
        change = amount_paid - booking.total_amount
        
        print(f"\nPayment successful!")
        print(f"Amount Paid: ${amount_paid}")
        print(f"Total Amount: ${booking.total_amount}")
        if change > 0:
            print(f"Change: ${change}")
        
        self.save_data()
        return True
    
    def find_booking(self, booking_id):
        """Find a booking by ID"""
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                return booking
        return None
    
    def display_all_bookings(self):
        """Display all bookings"""
        if not self.bookings:
            print("\nNo bookings found.")
            return
        
        print("\n" + "="*60)
        print("ALL BOOKINGS")
        print("="*60)
        for booking in self.bookings:
            print(booking)
            print(f"  Checked In: {booking.is_checked_in} | Checked Out: {booking.is_checked_out} | Payment: {booking.payment_status}")
        print("="*60)
    
    def save_data(self):
        """Save hotel data to file"""
        data = {
            'booking_counter': self.booking_counter,
            'rooms': [
                {
                    'room_number': r.room_number,
                    'room_type': r.room_type,
                    'price_per_night': r.price_per_night,
                    'is_available': r.is_available
                } for r in self.rooms
            ],
            'bookings': [
                {
                    'booking_id': b.booking_id,
                    'customer_name': b.customer_name,
                    'room_number': b.room_number,
                    'check_in_date': b.check_in_date,
                    'check_out_date': b.check_out_date,
                    'total_amount': b.total_amount,
                    'is_checked_in': b.is_checked_in,
                    'is_checked_out': b.is_checked_out,
                    'payment_status': b.payment_status
                } for b in self.bookings
            ]
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
            
            # Load rooms
            for room_data in data.get('rooms', []):
                room = Room(
                    room_data['room_number'],
                    room_data['room_type'],
                    room_data['price_per_night'],
                    room_data['is_available']
                )
                self.rooms.append(room)
            
            # Load bookings
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


def display_menu():
    """Display the main menu"""
    print("\n" + "="*60)
    print(f"{'HOTEL MANAGEMENT SYSTEM':^60}")
    print("="*60)
    print("1. View Available Rooms")
    print("2. Create Booking")
    print("3. Check-In")
    print("4. Process Payment")
    print("5. Check-Out")
    print("6. View All Bookings")
    print("7. Exit")
    print("="*60)


def main():
    """Main function to run the hotel management system"""
    hotel = Hotel("Grand Plaza Hotel")
    
    # Initialize with some rooms if starting fresh
    if not hotel.rooms:
        hotel.add_room(101, "Single", 100)
        hotel.add_room(102, "Single", 100)
        hotel.add_room(201, "Double", 150)
        hotel.add_room(202, "Double", 150)
        hotel.add_room(301, "Suite", 250)
        hotel.add_room(302, "Suite", 250)
        hotel.save_data()
    
    print(f"\nWelcome to {hotel.name}!")
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            hotel.display_available_rooms()
        
        elif choice == "2":
            print("\n--- CREATE BOOKING ---")
            customer_name = input("Enter customer name: ").strip()
            
            hotel.display_available_rooms()
            
            try:
                room_number = int(input("\nEnter room number: "))
                check_in = input("Enter check-in date (YYYY-MM-DD): ").strip()
                check_out = input("Enter check-out date (YYYY-MM-DD): ").strip()
                
                hotel.create_booking(customer_name, room_number, check_in, check_out)
            except ValueError:
                print("Invalid input! Please enter correct values.")
        
        elif choice == "3":
            print("\n--- CHECK-IN ---")
            try:
                booking_id = int(input("Enter booking ID: "))
                hotel.check_in(booking_id)
            except ValueError:
                print("Invalid booking ID!")
        
        elif choice == "4":
            print("\n--- PROCESS PAYMENT ---")
            try:
                booking_id = int(input("Enter booking ID: "))
                booking = hotel.find_booking(booking_id)
                
                if booking:
                    print(f"Total Amount Due: ${booking.total_amount}")
                    amount_paid = float(input("Enter amount paid: $"))
                    hotel.process_payment(booking_id, amount_paid)
                else:
                    print("Booking not found!")
            except ValueError:
                print("Invalid input!")
        
        elif choice == "5":
            print("\n--- CHECK-OUT ---")
            try:
                booking_id = int(input("Enter booking ID: "))
                hotel.check_out(booking_id)
            except ValueError:
                print("Invalid booking ID!")
        
        elif choice == "6":
            hotel.display_all_bookings()
        
        elif choice == "7":
            print(f"\nThank you for using {hotel.name} Management System!")
            print("Goodbye!")
            break
        
        else:
            print("\nInvalid choice! Please select 1-7.")


if __name__ == "__main__":
    main()
