# Hotel Management System

A comprehensive Python-based hotel management system with multiple interfaces: command-line, Flask web application, and static web version.

## 🌟 Features

- View available rooms with pricing
- Create bookings with automatic price calculation
- Check-in customers
- Process payments
- Check-out customers (with payment validation)
- Data persistence (JSON for Python versions, localStorage for static version)
- Dark modern UI design

## 🚀 Technologies Used

- **Backend**: Python 3.x
- **Web Framework**: Flask
- **Frontend**: HTML5, CSS3, JavaScript (ES6)
- **Data Storage**: JSON / localStorage
- **Modules**: datetime, json, os

## 📦 Installation

Install Flask for the web versions:
```bash
pip install Flask
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

## 🎮 How to Run

### 1. Command-Line Version (Pure Python)
```bash
python hotel_management.py
```
Best for demonstrating core Python concepts to your professor.

### 2. Flask Web Application (Python Backend)
```bash
python app.py
```
Then visit: `http://127.0.0.1:5000`

### 3. Static Web Version (For Netlify)
Simply open `index.html` in your browser, or deploy to Netlify.

## 📁 Project Structure

```
hotel-management/
├── hotel_management.py    # CLI version (core Python logic)
├── app.py                 # Flask web application
├── requirements.txt       # Python dependencies
├── hotel_data.json       # Data storage (auto-generated)
├── index.html            # Static web version entry point
├── CODE_EXPLANATION.md   # Detailed code explanations
├── static/
│   ├── style.css         # Dark theme styling
│   └── script.js         # JavaScript logic for static version
└── templates/            # Flask HTML templates
    ├── base.html
    ├── index.html
    ├── rooms.html
    ├── book.html
    ├── bookings.html
    ├── checkin.html
    ├── payment.html
    └── checkout.html
```

## 🎓 Python Concepts Demonstrated

- **Object-Oriented Programming**: Classes (Room, Booking, Hotel)
- **File I/O**: JSON read/write operations
- **Data Structures**: Lists, dictionaries, list comprehensions
- **Date/Time Handling**: datetime module for calculations
- **Exception Handling**: try/except blocks
- **String Formatting**: f-strings
- **Flask Framework**: Routes, templates, forms, flash messages
- **Control Flow**: Loops, conditionals, functions

## 🌐 Live Demo

- **Netlify**: [Your Netlify URL]
- **GitHub**: https://github.com/sam02324/python-microproject

## 📖 Documentation

See `CODE_EXPLANATION.md` for detailed line-by-line explanations of the code.

## 🎯 Workflow

1. **View Rooms** → Browse available rooms
2. **Book Room** → Create booking (get Booking ID)
3. **Check-In** → Use Booking ID to check in
4. **Payment** → Process payment before checkout
5. **Check-Out** → Complete stay (requires payment)

## 🐛 Bug Fixes

- ✅ Check-out validation (requires payment)
- ✅ Dark vogue UI implementation
- ✅ Netlify deployment support

## 👨‍💻 Author

Created as a Python micro-project demonstrating web development and OOP concepts.

## 📝 License

Educational project - Free to use and modify.
