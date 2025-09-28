document.addEventListener('DOMContentLoaded', function() {
    const orderButtons = document.querySelectorAll('.orderBtn');
    const orderList = document.getElementById('orderList');
    const totalPrice = document.getElementById('totalPrice');
    let total = 0;

    orderButtons.forEach(button => {
        button.addEventListener('click', function() {
            const coffeeName = this.getAttribute('data-coffee');
            const price = parseInt(this.getAttribute('data-price'));
            total += price;
            const listItem = document.createElement('li');
            listItem.textContent = coffeeName + ' - ' + price + ' บาท';
            orderList.appendChild(listItem);
            document.getElementById('order-summary').style.display = 'block';
            totalPrice.textContent = 'รวม: ' + total + ' บาท';
        });
    });

    document.getElementById('checkoutBtn').addEventListener('click', function() {
        alert('ชำระเงินเรียบร้อยแล้ว!');
        orderList.innerHTML = '';
        total = 0;
        totalPrice.textContent = '';
        document.getElementById('order-summary').style.display = 'none';
    });
});