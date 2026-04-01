# Hotel Management System

A Python-based hotel management web application for room selection, booking, check-in/out, and payment processing.

## Features

- View available rooms with pricing
- Create bookings with automatic price calculation
- Check-in customers
- Process payments
- Check-out customers
- Persistent data storage using JSON
- Web-based interface using Flask
- Input validation and error handling

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

Or install Flask directly:
```bash
pip install Flask
```

## How to Run

### Web Application (Recommended)
```bash
python app.py
```
Then open your browser and go to: `http://127.0.0.1:5000`

### Command Line Version
```bash
python hotel_management.py
```

## System Flow

1. **View Rooms** - Browse available rooms with types and prices
2. **Create Booking** - Book a room by providing customer details and dates (Note the Booking ID!)
3. **Check-In** - Check-in using booking ID
4. **Payment** - Process payment before check-out
5. **Check-Out** - Complete stay and free up the room

## Project Structure

```
hotel-management/
├── app.py                  # Flask web application
├── hotel_management.py     # Command-line version
├── requirements.txt        # Python dependencies
├── hotel_data.json        # Data storage (auto-generated)
├── templates/             # HTML templates
│   ├── base.html         # Base template with styling
│   ├── index.html        # Home page
│   ├── rooms.html        # Available rooms page
│   ├── book.html         # Booking form
│   ├── bookings.html     # View all bookings
│   ├── checkin.html      # Check-in page
│   ├── payment.html      # Payment page
│   └── checkout.html     # Check-out page
└── README.md             # This file
```

## Code Structure

- `Room` class - Manages individual room properties
- `Booking` class - Handles booking information and status
- `Hotel` class - Main system with all operations
- Flask routes - Handle web requests and responses
- Data persistence using JSON file

## Key Concepts Used

- Object-Oriented Programming (Classes and Objects)
- Flask web framework (Routes, Templates, Forms)
- File I/O (JSON for data persistence)
- Date/Time handling
- List comprehensions
- Exception handling
- HTML/CSS for frontend
- Jinja2 templating
