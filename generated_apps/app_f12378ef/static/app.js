// API base URL
const API_BASE_URL = 'https://your-api-url.com/api';

// Function to fetch users
async function fetchUsers() {
    const response = await fetch(`${API_BASE_URL}/users`);
    const users = await response.json();
    return users;
}

// Function to create a new user
async function createUser(userData) {
    const response = await fetch(`${API_BASE_URL}/users`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    });
    const newUser = await response.json();
    return newUser;
}

// Function to fetch reservations
async function fetchReservations() {
    const response = await fetch(`${API_BASE_URL}/reservations`);
    const reservations = await response.json();
    return reservations;
}

// Function to create a new reservation
async function createReservation(reservationData) {
    const response = await fetch(`${API_BASE_URL}/reservations`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(reservationData)
    });
    const newReservation = await response.json();
    return newReservation;
}

// Function to fetch menu
async function fetchMenu() {
    const response = await fetch(`${API_BASE_URL}/menu`);
    const menu = await response.json();
    return menu;
}

// UI Interaction
document.addEventListener('DOMContentLoaded', async () => {
    const usersList = document.getElementById('users-list');
    const reservationsList = document.getElementById('reservations-list');
    const menuList = document.getElementById('menu-list');

    // Fetch and display users
    const users = await fetchUsers();
    users.forEach(user => {
        const li = document.createElement('li');
        li.textContent = user.name;
        usersList.appendChild(li);
    });

    // Fetch and display reservations
    const reservations = await fetchReservations();
    reservations.forEach(reservation => {
        const li = document.createElement('li');
        li.textContent = `${reservation.user} - ${reservation.date}`;
        reservationsList.appendChild(li);
    });

    // Fetch and display menu
    const menu = await fetchMenu();
    menu.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.name} - ${item.price}`;
        menuList.appendChild(li);
    });

    // Handle new user creation
    document.getElementById('create-user-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const userName = event.target.elements['username'].value;
        const newUser = await createUser({ name: userName });
        const li = document.createElement('li');
        li.textContent = newUser.name;
        usersList.appendChild(li);
        event.target.reset();
    });

    // Handle new reservation creation
    document.getElementById('create-reservation-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const reservationUser = event.target.elements['reservation-user'].value;
        const reservationDate = event.target.elements['reservation-date'].value;
        const newReservation = await createReservation({ user: reservationUser, date: reservationDate });
        const li = document.createElement('li');
        li.textContent = `${newReservation.user} - ${newReservation.date}`;
        reservationsList.appendChild(li);
        event.target.reset();
    });
});
```

### หมายเหตุ:
- คุณต้องแทนที่ `https://your-api-url.com/api` ด้วย URL ของ API ของคุณ
- คุณต้องมี HTML ที่เหมาะสมเพื่อให้ JavaScript ทำงานได้ เช่น:
  - `<ul id="users-list"></ul>`
  - `<ul id="reservations-list"></ul>`
  - `<ul id="menu-list"></ul>`
  - ฟอร์มสำหรับสร้างผู้ใช้และการจอง
- ตรวจสอบให้แน่ใจว่า API ของคุณรองรับ CORS หากคุณเรียกจากโดเมนที่แตกต่าง