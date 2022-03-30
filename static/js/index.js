const togglebtn = document.querySelector('.navbar-toggle')
const category = document.querySelector('.category')


togglebtn.addEventListener('click',()=>{
    category.classList.toggle('active');
});