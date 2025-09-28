function addToCart(item) {
    alert(item + ' ได้ถูกเพิ่มลงในตะกร้าแล้ว!');
}

document.getElementById('contact-form').addEventListener('submit', function(event) {
    event.preventDefault(); // ป้องกันการรีเฟรชหน้า
    const name = document.getElementById('name').value;
    const message = document.getElementById('message').value;
    alert('ขอบคุณ ' + name + ' สำหรับข้อความของคุณ!');
    // ล้างฟอร์มหลังจากส่ง
    document.getElementById('contact-form').reset();
});