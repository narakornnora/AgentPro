document.addEventListener('DOMContentLoaded', () => {
    const cartItems = document.querySelector('.cart-items');
    const addToCartButtons = document.querySelectorAll('.add-to-cart');

    // ฟังก์ชันเพิ่มสินค้าในตะกร้า
    addToCartButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const product = e.target.parentElement;
            const productName = product.querySelector('h3').innerText;
            const productPrice = product.querySelector('p').innerText;

            const cartItem = document.createElement('div');
            cartItem.classList.add('cart-item');
            cartItem.innerHTML = `<p>${productName} - ${productPrice}</p>`;

            cartItems.appendChild(cartItem);
        });
    });

    // ฟังก์ชันจำลองการล็อกอิน
    const loginForm = document.getElementById('login-form');
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        alert('Logged in successfully!');
    });
});