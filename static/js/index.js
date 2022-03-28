const togglebtn = document.querySelector('#list')
const menu = document.querySelector('.m-nav-menu')
const logo = document.querySelector('.logo')

togglebtn.addEventListener('click',()=>{
    menu.classList.toggle('active');
    logo.classList.toggle('active')
});