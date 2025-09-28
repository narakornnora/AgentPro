// Thai Restaurant Booking JavaScript

const apiBaseUrl = 'https://your-api-url.com/api'; // เปลี่ยนเป็น URL ของ API ของคุณ

// ฟังก์ชันสำหรับดึงรายการผู้ใช้
async function fetchUsers() {
    try {
        const response = await fetch(`${apiBaseUrl}/users`);
        const users = await response.json();
        console.log(users);
        // แสดงผู้ใช้ใน UI
        displayUsers(users);
    } catch (error) {
        console.error('Error fetching users:', error);
    }
}

// ฟังก์ชันสำหรับสร้างการจองโต๊ะ
async function createReservation(reservationData) {
    try {
        const response = await fetch(`${apiBaseUrl}/reservations`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(reservationData),
        });
        const result = await response.json();
        console.log(result);
        // แสดงผลการจองใน UI
        alert('Reservation created successfully!');
    } catch (error) {
        console.error('Error creating reservation:', error);
    }
}

// ฟังก์ชันสำหรับดึงรายการโปรโมชั่น
async function fetchPromotions() {
    try {
        const response = await fetch(`${apiBaseUrl}/promotions`);
        const promotions = await response.json();
        console.log(promotions);
        // แสดงโปรโมชั่นใน UI
        displayPromotions(promotions);
    } catch (error) {
        console.error('Error fetching promotions:', error);
    }
}

// ฟังก์ชันสำหรับดึงข้อมูลร้านอาหาร
async function fetchRestaurantInfo() {
    try {
        const response = await fetch(`${apiBaseUrl}/restaurant_info`);
        const restaurantInfo = await response.json();
        console.log(restaurantInfo);
        // แสดงข้อมูลร้านอาหารใน UI
        displayRestaurantInfo(restaurantInfo);
    } catch (error) {
        console.error('Error fetching restaurant info:', error);
    }
}

// ฟังก์ชันสำหรับแสดงผู้ใช้ใน UI
function displayUsers(users) {
    const userContainer = document.getElementById('user-list');
    userContainer.innerHTML = '';
    users.forEach(user => {
        const userElement = document.createElement('div');
        userElement.textContent = `${user.name} (${user.email})`;
        userContainer.appendChild(userElement);
    });
}

// ฟังก์ชันสำหรับแสดงโปรโมชั่นใน UI
function displayPromotions(promotions) {
    const promotionContainer = document.getElementById('promotion-list');
    promotionContainer.innerHTML = '';
    promotions.forEach(promotion => {
        const promoElement = document.createElement('div');
        promoElement.textContent = promotion.description;
        promotionContainer.appendChild(promoElement);
    });
}

// ฟังก์ชันสำหรับแสดงข้อมูลร้านอาหารใน UI
function displayRestaurantInfo(info) {
    const infoContainer = document.getElementById('restaurant-info');
    infoContainer.innerHTML = `
        <h2>${info.name}</h2>
        <p>${info.description}</p>
        <p>Address: ${info.address}</p>
        <p>Phone: ${info.phone}</p>
    `;
}

// ตัวอย่างการใช้งาน
document.addEventListener('DOMContentLoaded', () => {
    fetchUsers();
    fetchPromotions();
    fetchRestaurantInfo();

    document.getElementById('reservation-form').addEventListener('submit', (event) => {
        event.preventDefault();
        const reservationData = {
            name: event.target.name.value,
            date: event.target.date.value,
            time: event.target.time.value,
            guests: event.target.guests.value,
        };
        createReservation(reservationData);
    });
});
```

**หมายเหตุ:** 
- อย่าลืมเปลี่ยน `https://your-api-url.com/api` เป็น URL ของ API ของคุณ
- คุณต้องมี HTML ที่มี `user-list`, `promotion-list`, `restaurant-info`, และ `reservation-form` เพื่อให้โค้ดทำงานได้อย่างถูกต