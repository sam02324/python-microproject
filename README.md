# Hotel Management System

A comprehensive Python hotel management system with CLI, Flask web app, and static web versions.

## Features

- View available rooms
- Create bookings with automatic pricing
- Check-in/Check-out management
- Payment processing
- Data persistence
- Dark modern UI

## Installation

```bash
pip install Flask
```

## How to Run

### Python CLI Version
```bash
python hotel_management.py
```

### Flask Web Version
```bash
python app.py
```
Visit: http://127.0.0.1:5000

### Static Web Version
Open `index.html` in browser or deploy to Netlify

## Technologies

- Python 3.x
- Flask
- HTML/CSS/JavaScript
- JSON/localStorage

## Project Structure

```
├── hotel_management.py    # CLI version
├── app.py                 # Flask version
├── index.html            # Static version
├── static/
│   ├── style.css
│   └── script.js
└── templates/            # Flask templates
```

## Python Concepts

- OOP (Classes: Room, Booking, Hotel)
- File I/O (JSON)
- datetime module
- List comprehensions
- Exception handling
- Flask framework
