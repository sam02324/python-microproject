# Hotel Management System

A Python-based hotel management system with both command-line and web interfaces for room booking, check-in/out, and payment processing.

## Features

- View available rooms with pricing
- Create bookings with automatic price calculation
- Check-in customers
- Process payments
- Check-out customers
- Data persistence using JSON file
- Dark modern UI for web version

## Technologies Used

- Python 3.x
- Flask (Web Framework)
- HTML5/CSS3
- JSON for data storage
- datetime module

## Installation

Install Flask for the web version:
```bash
pip install Flask
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

## How to Run

### Command-Line Version (Core Python Logic)
```bash
python hotel_management.py
```

### Web Version (Flask)
```bash
python app.py
```
Then open your browser and visit: `http://127.0.0.1:5000`

## Project Structure

```
hotel-management/
├── hotel_management.py    # Command-line version (core logic)
├── app.py                 # Flask web application
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

## Python Concepts Demonstrated

- Object-Oriented Programming (Classes: Room, Booking, Hotel)
- File I/O (JSON for data persistence)
- datetime module for date calculations
- List comprehensions
- Exception handling
- Flask web framework (Routes, Templates, Forms)
- String formatting
- Control flow (loops, conditionals)
