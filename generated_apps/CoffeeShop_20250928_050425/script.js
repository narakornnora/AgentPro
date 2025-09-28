function orderCoffee(coffeeName) {
    alert('คุณได้สั่ง ' + coffeeName + ' เรียบร้อยแล้ว!');
}

document.getElementById('contact-form').addEventListener('submit', function(event) {
    event.preventDefault(); // ป้องกันการรีเฟรชหน้า
    alert('ข้อความของคุณถูกส่งแล้ว!');
    this.reset(); // รีเซ็ตฟอร์ม
});