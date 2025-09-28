const books = [
    { title: 'หนังสือ A', price: 300 },
    { title: 'หนังสือ B', price: 250 },
    { title: 'หนังสือ C', price: 400 }
];

let cartCount = 0;

function displayBooks() {
    const gallery = document.getElementById('gallery');
    books.forEach((book, index) => {
        const bookDiv = document.createElement('div');
        bookDiv.classList.add('book');
        bookDiv.innerHTML = `<h2>${book.title}</h2><p>ราคา: ${book.price} บาท</p><button onclick='addToCart(${index})'>เพิ่มไปยังรถเข็น</button>`;
        gallery.appendChild(bookDiv);
    });
}

function addToCart(index) {
    cartCount++;
    document.getElementById('cart-count').innerText = cartCount;
    alert(books[index].title + ' ถูกเพิ่มไปยังรถเข็น');
}

document.getElementById('search').addEventListener('input', function() {
    const searchTerm = this.value.toLowerCase();
    const filteredBooks = books.filter(book => book.title.toLowerCase().includes(searchTerm));
    document.getElementById('gallery').innerHTML = '';
    filteredBooks.forEach((book, index) => {
        const bookDiv = document.createElement('div');
        bookDiv.classList.add('book');
        bookDiv.innerHTML = `<h2>${book.title}</h2><p>ราคา: ${book.price} บาท</p><button onclick='addToCart(${index})'>เพิ่มไปยังรถเข็น</button>`;
        document.getElementById('gallery').appendChild(bookDiv);
    });
});

displayBooks();