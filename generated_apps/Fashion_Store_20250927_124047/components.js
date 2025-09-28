// ไฟล์นี้สามารถใช้สำหรับแยก component ต่าง ๆ ในอนาคต
// ตัวอย่างการสร้าง component
function createProductComponent(name, price, imageUrl) {
    const product = document.createElement('div');
    product.classList.add('product');
    product.innerHTML = `
        <img src="${imageUrl}" alt="${name}">
        <h3>${name}</h3>
        <p>${price}</p>
        <button class="add-to-cart">Add to Cart</button>
    `;
    return product;
}

// การใช้งาน component
// const newProduct = createProductComponent('New Product', '$30.00', 'https://via.placeholder.com/150');
// document.querySelector('.product-list').appendChild(newProduct);
