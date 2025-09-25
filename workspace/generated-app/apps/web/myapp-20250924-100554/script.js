document.addEventListener('submit', e=>{
  if(e.target.matches('form')){ e.preventDefault(); alert('ส่งข้อความเรียบร้อย'); }
});