let cart = [];

// ฟังก์ชันสำหรับเพิ่มสินค้าในตะกร้า
function addToCart(item, price) {
    cart.push({ item, price });
    displayCart();
    alert(item + ' ถูกเพิ่มในตะกร้า');
}

// ฟังก์ชันสำหรับแสดงรายการในตะกร้า
function displayCart() {
    const cartItems = document.getElementById('cart-items');
    cartItems.innerHTML = '';
    cart.forEach((product, index) => {
        cartItems.innerHTML += `<p>${product.item} - ${product.price} บาท</p>`;
    });
}

// ฟังก์ชันสำหรับการชำระเงิน
function checkout() {
    if (cart.length === 0) {
        alert('ตะกร้าว่าง!');
    } else {
        alert('ขอบคุณที่ช้อปปิ้งกับเรา!');
        cart = [];
        displayCart();
    }
}