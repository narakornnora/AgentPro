let cartCount = 0;
const cartButton = document.getElementById('cart-button');
const cartCountDisplay = document.getElementById('cart-count');
const addToCartButtons = document.querySelectorAll('.add-to-cart');

// ฟังก์ชันสำหรับเพิ่มหนังสือลงในตะกร้า
addToCartButtons.forEach(button => {
    button.addEventListener('click', () => {
        cartCount++;
        cartCountDisplay.textContent = cartCount;
        alert('เพิ่มหนังสือในตะกร้าแล้ว!'); // แจ้งเตือนเมื่อเพิ่มหนังสือ
    });
});

// ฟังก์ชันค้นหาหนังสือ
const searchInput = document.getElementById('search');
searchInput.addEventListener('input', () => {
    const filter = searchInput.value.toLowerCase();
    const books = document.querySelectorAll('.book');
    books.forEach(book => {
        const title = book.querySelector('h3').textContent.toLowerCase();
        if (title.includes(filter)) {
            book.style.display = '';
        } else {
            book.style.display = 'none';
        }
    });
});