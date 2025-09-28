let cart = [];

// ฟังก์ชันสำหรับเพิ่มสินค้าลงในตะกร้า
function addToCart(item) {
    cart.push(item);
    displayCart();
    alert(item + ' ถูกเพิ่มลงในตะกร้า!');
}

// ฟังก์ชันสำหรับแสดงสินค้าที่อยู่ในตะกร้า
function displayCart() {
    const cartItems = document.getElementById('cart-items');
    cartItems.innerHTML = '';
    cart.forEach(item => {
        const li = document.createElement('li');
        li.textContent = item;
        cartItems.appendChild(li);
    });
}

// ฟังก์ชันสำหรับชำระเงิน
function checkout() {
    if (cart.length === 0) {
        alert('ตะกร้าสินค้าเปล่า!');
    } else {
        alert('ขอบคุณที่ช้อปปิ้งกับเรา!');
        cart = [];
        displayCart();
    }
}