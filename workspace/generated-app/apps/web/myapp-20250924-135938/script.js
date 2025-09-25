
document.querySelectorAll('[data-scroll]').forEach(el=>{
  el.addEventListener('click',e=>{
    e.preventDefault();
    document.querySelector(el.getAttribute('href'))?.scrollIntoView({behavior:'smooth'});
  });
});
