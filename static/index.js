var first_c = document.querySelector('.mini_c');
var second_c = document.getElementById('c2');
var third_c = document.getElementById('c3');
var forth_c = document.getElementById('c4');


function moveDiv(){
    first_c.style.left = '-100px';
    first_c.style.top = '-50px';

    second_c.style.left = '-100px';
    second_c.style.top = '50px';

    third_c.style.left = '100px'; 
    third_c.style.top = '-50px'; 
    
    forth_c.style.left = '100px';
    forth_c.style.top = '50px';
}


setTimeout(moveDiv, 1000);
