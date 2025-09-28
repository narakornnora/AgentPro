let cart = [];

// ฟังก์ชันเพิ่มสินค้าไปยังตะกร้า
function addToCart(product) {
    cart.push(product);
    updateCartCount();
    updateCartDisplay();
}

// ฟังก์ชันอัปเดตจำนวนสินค้าในตะกร้า
function updateCartCount() {
    document.getElementById('cart-count').innerText = cart.length;
}

// ฟังก์ชันอัปเดตการแสดงผลของตะกร้า
function updateCartDisplay() {
    const cartItems = document.getElementById('cart-items');
    cartItems.innerHTML = '';
    let totalPrice = 0;
    cart.forEach(item => {
        const li = document.createElement('li');
        li.innerText = `${item.name} - ${item.price} บาท`;
        cartItems.appendChild(li);
        totalPrice += item.price;
    });
    document.getElementById('total-price').innerText = `รวม: ${totalPrice} บาท`;
}

// ฟังก์ชันที่ทำงานเมื่อคลิกปุ่มเพิ่มไปยังตะกร้า
document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', function() {
        const productElement = this.parentElement;
        const product = {
            id: productElement.getAttribute('data-id'),
            name: productElement.getAttribute('data-name'),
            price: parseFloat(productElement.getAttribute('data-price'))
        };
        addToCart(product);
    });
});

// ฟังก์ชันที่ทำงานเมื่อคลิกปุ่มตะกร้า
document.getElementById('cart-button').addEventListener('click', function() {
    const cartSection = document.getElementById('cart');
    cartSection.style.display = cartSection.style.display === 'none' ? 'block' : 'none';
});

// ฟังก์ชันที่ทำงานเมื่อคลิกปุ่มสั่งซื้อ
document.getElementById('checkout').addEventListener('click', function() {
    alert('ขอบคุณสำหรับการสั่งซื้อ!');
    cart = [];
    updateCartCount();
    updateCartDisplay();
    document.getElementById('cart').style.display = 'none';
});