function addToCart(item) {
    alert(item + ' ได้ถูกเพิ่มลงในตะกร้าแล้ว!');
}

document.getElementById('contact-form').addEventListener('submit', function(event) {
    event.preventDefault(); // ป้องกันการส่งฟอร์ม
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    alert('ขอบคุณ ' + name + ' สำหรับการติดต่อ!');
    this.reset(); // รีเซ็ตฟอร์มหลังจากส่ง
});