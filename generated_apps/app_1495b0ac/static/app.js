// API base URL
const API_BASE_URL = 'https://your-api-url.com';

// Function to fetch users
async function fetchUsers() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/users`);
        const data = await response.json();
        console.log('Users:', data);
        // Update UI with users data
    } catch (error) {
        console.error('Error fetching users:', error);
    }
}

// Function to fetch menu
async function fetchMenu() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/menu`);
        const data = await response.json();
        console.log('Menu:', data);
        // Update UI with menu data
    } catch (error) {
        console.error('Error fetching menu:', error);
    }
}

// Function to fetch promotions
async function fetchPromotions() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/promotions`);
        const data = await response.json();
        console.log('Promotions:', data);
        // Update UI with promotions data
    } catch (error) {
        console.error('Error fetching promotions:', error);
    }
}

// Function to create a reservation
async function createReservation(reservationData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/reservations`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(reservationData),
        });
        const data = await response.json();
        console.log('Reservation created:', data);
        // Update UI to reflect reservation success
    } catch (error) {
        console.error('Error creating reservation:', error);
    }
}

// Function to process payment
async function processPayment(paymentData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/payments`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(paymentData),
        });
        const data = await response.json();
        console.log('Payment processed:', data);
        // Update UI to reflect payment success
    } catch (error) {
        console.error('Error processing payment:', error);
    }
}

// UI interactions
document.getElementById('fetch-users-btn').addEventListener('click', fetchUsers);
document.getElementById('fetch-menu-btn').addEventListener('click', fetchMenu);
document.getElementById('fetch-promotions-btn').addEventListener('click', fetchPromotions);

document.getElementById('reservation-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const reservationData = {
        name: this.name.value,
        date: this.date.value,
        time: this.time.value,
        guests: this.guests.value,
    };
    createReservation(reservationData);
});

document.getElementById('payment-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const paymentData = {
        amount: this.amount.value,
        method: this.method.value,
    };
    processPayment(paymentData);
});
```

### หมายเหตุ:
- เปลี่ยน `https://your-api-url.com` เป็น URL ที่แท้จริงของ API ของคุณ
- ตรวจสอบให้แน่ใจว่า HTML ของคุณมีปุ่มและฟอร์มที่มี ID ตรงกับที่ใช้ใน JavaScript เช่น `fetch-users-btn`, `fetch-menu-btn`, `fetch-promotions-btn`, `reservation-form`, และ `payment-fo