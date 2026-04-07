# Hotel Management System

A Python Flask web application for hotel room management with booking, check-in/out, and payment processing.

## Features

- View available rooms with pricing
- Create bookings with automatic price calculation
- Check-in customers
- Process payments
- Check-out customers
- Data persistence using JSON file
- Dark modern UI design

## Technologies Used

- Python 3.x
- Flask (Web Framework)
- HTML5/CSS3
- JSON for data storage

## Installation

1. Install Flask:
```bash
pip install Flask
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

## How to Run

```bash
python app.py
```

Then open your browser and visit: `http://127.0.0.1:5000`

## Project Structure

```
hotel-management/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── hotel_data.json       # Data storage (auto-generated)
├── static/
│   └── style.css         # CSS styling
└── templates/            # HTML templates
    ├── base.html
    ├── index.html
    ├── rooms.html
    ├── book.html
    ├── bookings.html
    ├── checkin.html
    ├── payment.html
    └── checkout.html
```

## Python Concepts Used

- Object-Oriented Programming (Classes: Room, Booking, Hotel)
- Flask web framework (Routes, Templates, Forms)
- File I/O (JSON for data persistence)
- datetime module for date calculations
- List comprehensions
- Exception handling
