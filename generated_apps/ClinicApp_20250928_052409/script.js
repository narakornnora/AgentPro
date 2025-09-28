document.getElementById('appointment-form').addEventListener('submit', function(event) {
    event.preventDefault(); // ป้องกันการรีเฟรชหน้า
    const patientName = document.getElementById('patient-name').value;
    const doctorName = document.getElementById('doctor-name').value;
    const appointmentDate = document.getElementById('appointment-date').value;
    const confirmationMessage = `นัดหมายของคุณ ${patientName} กับ ${doctorName} วันที่ ${appointmentDate} สำเร็จแล้ว!`;
    document.getElementById('confirmation-message').innerText = confirmationMessage;
    this.reset(); // รีเซ็ตฟอร์มหลังจากส่ง
});