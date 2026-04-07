class Room {
    constructor(roomNumber, roomType, pricePerNight, isAvailable = true) {
        this.roomNumber = roomNumber;
        this.roomType = roomType;
        this.pricePerNight = pricePerNight;
        this.isAvailable = isAvailable;
    }
}

class Booking {
    constructor(bookingId, customerName, roomNumber, checkInDate, checkOutDate, totalAmount) {
        this.bookingId = bookingId;
        this.customerName = customerName;
        this.roomNumber = roomNumber;
        this.checkInDate = checkInDate;
        this.checkOutDate = checkOutDate;
        this.totalAmount = totalAmount;
        this.isCheckedIn = false;
        this.isCheckedOut = false;
        this.paymentStatus = "Pending";
    }
}

class Hotel {
    constructor(name) {
        this.name = name;
        this.rooms = [];
        this.bookings = [];
        this.bookingCounter = 1000;
        this.loadData();
        
        if (this.rooms.length === 0) {
            this.addRoom(101, "Single", 100);
            this.addRoom(102, "Single", 100);
            this.addRoom(201, "Double", 150);
            this.addRoom(202, "Double", 150);
            this.addRoom(301, "Suite", 250);
            this.addRoom(302, "Suite", 250);
            this.saveData();
        }
    }
    
    addRoom(roomNumber, roomType, pricePerNight) {
        this.rooms.push(new Room(roomNumber, roomType, pricePerNight));
    }
    
    getAvailableRooms() {
        return this.rooms.filter(room => room.isAvailable);
    }
    
    calculateNights(checkIn, checkOut) {
        const checkInDate = new Date(checkIn);
        const checkOutDate = new Date(checkOut);
        const nights = Math.floor((checkOutDate - checkInDate) / (1000 * 60 * 60 * 24));
        return nights;
    }
    
    createBooking(customerName, roomNumber, checkInDate, checkOutDate) {
        const room = this.rooms.find(r => r.roomNumber === roomNumber);
        
        if (!room || !room.isAvailable) {
            return null;
        }
        
        const nights = this.calculateNights(checkInDate, checkOutDate);
        if (nights <= 0) {
            return null;
        }
        
        const totalAmount = nights * room.pricePerNight;
        const bookingId = this.bookingCounter++;
        
        const booking = new Booking(bookingId, customerName, roomNumber, checkInDate, checkOutDate, totalAmount);
        this.bookings.push(booking);
        room.isAvailable = false;
        
        this.saveData();
        return booking;
    }
    
    checkIn(bookingId) {
        const booking = this.findBooking(bookingId);
        if (!booking || booking.isCheckedIn) {
            return false;
        }
        
        booking.isCheckedIn = true;
        this.saveData();
        return true;
    }
    
    processPayment(bookingId, amountPaid) {
        const booking = this.findBooking(bookingId);
        if (!booking || booking.paymentStatus === "Paid") {
            return false;
        }
        
        if (amountPaid < booking.totalAmount) {
            return false;
        }
        
        booking.paymentStatus = "Paid";
        this.saveData();
        return true;
    }
    
    checkOut(bookingId) {
        const booking = this.findBooking(bookingId);
        if (!booking || booking.isCheckedOut) {
            return { success: false, message: "Booking not found or already checked out!" };
        }
        
        if (booking.paymentStatus !== "Paid") {
            return { success: false, message: "Payment must be completed before check-out!" };
        }
        
        booking.isCheckedOut = true;
        
        const room = this.rooms.find(r => r.roomNumber === booking.roomNumber);
        if (room) {
            room.isAvailable = true;
        }
        
        this.saveData();
        return { success: true, message: "Check-out successful!" };
    }
    
    findBooking(bookingId) {
        return this.bookings.find(b => b.bookingId === bookingId);
    }
    
    saveData() {
        const data = {
            bookingCounter: this.bookingCounter,
            rooms: this.rooms,
            bookings: this.bookings
        };
        localStorage.setItem('hotelData', JSON.stringify(data));
    }
    
    loadData() {
        const data = localStorage.getItem('hotelData');
        if (data) {
            const parsed = JSON.parse(data);
            this.bookingCounter = parsed.bookingCounter || 1000;
            
            this.rooms = parsed.rooms.map(r => 
                new Room(r.roomNumber, r.roomType, r.pricePerNight, r.isAvailable)
            );
            
            this.bookings = parsed.bookings.map(b => {
                const booking = new Booking(
                    b.bookingId, b.customerName, b.roomNumber,
                    b.checkInDate, b.checkOutDate, b.totalAmount
                );
                booking.isCheckedIn = b.isCheckedIn;
                booking.isCheckedOut = b.isCheckedOut;
                booking.paymentStatus = b.paymentStatus;
                return booking;
            });
        }
    }
}

const hotel = new Hotel("Grand Plaza Hotel");

function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.getElementById(sectionId).classList.add('active');
    event.target.classList.add('active');
    
    if (sectionId === 'rooms') displayRooms();
    if (sectionId === 'book') loadBookingForm();
    if (sectionId === 'bookings') displayBookings();
}

function showAlert(message, type = 'success') {
    const alertContainer = document.getElementById('alert-container');
    const alert = document.createElement('div');
    alert.className = `flash ${type}`;
    alert.textContent = message;
    
    alertContainer.appendChild(alert);
    
    setTimeout(() => {
        alert.remove();
    }, 4000);
}

function displayRooms() {
    const roomsList = document.getElementById('rooms-list');
    const availableRooms = hotel.getAvailableRooms();
    
    if (availableRooms.length === 0) {
        roomsList.innerHTML = '<p class="empty-message">No rooms available at the moment.</p>';
        return;
    }
    
    roomsList.innerHTML = '<div class="rooms-grid">' + availableRooms.map(room => `
        <div class="room-card">
            <h3>Room ${room.roomNumber}</h3>
            <p><strong>Type:</strong> ${room.roomType}</p>
            <p><strong>Price:</strong> $${room.pricePerNight} per night</p>
            <span class="badge badge-success">Available</span>
        </div>
    `).join('') + '</div>';
}

function loadBookingForm() {
    const roomSelect = document.getElementById('room_select');
    const availableRooms = hotel.getAvailableRooms();
    
    if (!roomSelect) return;
    
    roomSelect.innerHTML = '<option value="">-- Select a Room --</option>' +
        availableRooms.map(room => 
            `<option value="${room.roomNumber}">Room ${room.roomNumber} - ${room.roomType} - $${room.pricePerNight}/night</option>`
        ).join('');
    
    const today = new Date().toISOString().split('T')[0];
    const checkInInput = document.getElementById('check_in');
    const checkOutInput = document.getElementById('check_out');
    
    if (checkInInput) checkInInput.min = today;
    if (checkOutInput) checkOutInput.min = today;
}

function updatePricePreview() {
    const roomSelect = document.getElementById('room_select');
    const checkInInput = document.getElementById('check_in');
    const checkOutInput = document.getElementById('check_out');
    const pricePreview = document.getElementById('price-preview');
    
    if (!roomSelect || !checkInInput || !checkOutInput || !pricePreview) return;
    
    const roomNumber = parseInt(roomSelect.value);
    const checkIn = checkInInput.value;
    const checkOut = checkOutInput.value;
    
    if (roomNumber && checkIn && checkOut) {
        const room = hotel.rooms.find(r => r.roomNumber === roomNumber);
        if (room) {
            const nights = hotel.calculateNights(checkIn, checkOut);
            if (nights > 0) {
                const total = nights * room.pricePerNight;
                pricePreview.innerHTML = `Total: ${nights} night(s) × $${room.pricePerNight} = $${total}`;
                pricePreview.style.display = 'block';
            } else {
                pricePreview.innerHTML = '';
                pricePreview.style.display = 'none';
            }
        }
    } else {
        pricePreview.innerHTML = '';
        pricePreview.style.display = 'none';
    }
}

function displayBookings() {
    const bookingsList = document.getElementById('bookings-list');
    
    if (hotel.bookings.length === 0) {
        bookingsList.innerHTML = '<p class="empty-message">No bookings found.</p>';
        return;
    }
    
    bookingsList.innerHTML = `
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Booking ID</th>
                        <th>Customer</th>
                        <th>Room</th>
                        <th>Check-In</th>
                        <th>Check-Out</th>
                        <th>Amount</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    ${hotel.bookings.map(booking => `
                        <tr>
                            <td><strong>${booking.bookingId}</strong></td>
                            <td>${booking.customerName}</td>
                            <td>${booking.roomNumber}</td>
                            <td>${booking.checkInDate}</td>
                            <td>${booking.checkOutDate}</td>
                            <td>$${booking.totalAmount}</td>
                            <td>
                                ${booking.isCheckedOut ? '<span class="badge badge-info">Checked Out</span>' :
                                  booking.isCheckedIn ? '<span class="badge badge-success">Checked In</span>' :
                                  '<span class="badge badge-warning">Booked</span>'}
                                ${booking.paymentStatus === "Paid" ? 
                                  '<span class="badge badge-success">Paid</span>' :
                                  '<span class="badge badge-danger">Pending</span>'}
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
}

document.addEventListener('DOMContentLoaded', () => {
    const checkInInput = document.getElementById('check_in');
    const checkOutInput = document.getElementById('check_out');
    const roomSelect = document.getElementById('room_select');
    
    if (checkInInput) checkInInput.addEventListener('change', updatePricePreview);
    if (checkOutInput) checkOutInput.addEventListener('change', updatePricePreview);
    if (roomSelect) roomSelect.addEventListener('change', updatePricePreview);
    
    const bookingForm = document.getElementById('booking-form');
    if (bookingForm) {
        bookingForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const customerName = document.getElementById('customer_name').value;
            const roomNumber = parseInt(document.getElementById('room_select').value);
            const checkIn = document.getElementById('check_in').value;
            const checkOut = document.getElementById('check_out').value;
            
            const booking = hotel.createBooking(customerName, roomNumber, checkIn, checkOut);
            
            if (booking) {
                showAlert(`Booking successful! Your Booking ID is: ${booking.bookingId}`, 'success');
                e.target.reset();
                document.getElementById('price-preview').innerHTML = '';
                loadBookingForm();
            } else {
                showAlert('Booking failed! Please check room availability and dates.', 'error');
            }
        });
    }
    
    const checkinForm = document.getElementById('checkin-form');
    if (checkinForm) {
        checkinForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const bookingId = parseInt(document.getElementById('checkin_booking_id').value);
            
            if (hotel.checkIn(bookingId)) {
                showAlert(`Check-in successful for Booking ID: ${bookingId}`, 'success');
                e.target.reset();
            } else {
                showAlert('Check-in failed! Please verify booking ID.', 'error');
            }
        });
    }
    
    const paymentForm = document.getElementById('payment-form');
    if (paymentForm) {
        paymentForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const bookingId = parseInt(document.getElementById('payment_booking_id').value);
            const amountPaid = parseFloat(document.getElementById('amount_paid').value);
            
            const booking = hotel.findBooking(bookingId);
            
            if (booking && hotel.processPayment(bookingId, amountPaid)) {
                const change = amountPaid - booking.totalAmount;
                let message = `Payment successful for Booking ID: ${bookingId}`;
                if (change > 0) {
                    message += ` | Change: $${change.toFixed(2)}`;
                }
                showAlert(message, 'success');
                e.target.reset();
            } else {
                showAlert('Payment failed! Please check booking ID and amount.', 'error');
            }
        });
    }
    
    const checkoutForm = document.getElementById('checkout-form');
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const bookingId = parseInt(document.getElementById('checkout_booking_id').value);
            const result = hotel.checkOut(bookingId);
            
            if (result.success) {
                showAlert(result.message, 'success');
                e.target.reset();
            } else {
                showAlert(result.message, 'error');
            }
        });
    }
    
    displayRooms();
    displayBookings();
    loadBookingForm();
});
