var divElement = document.querySelector('.main');
var id1 = document.getElementById('main2');
var id2 = document.getElementById('main3');
var id3 = document.getElementById('main4');

function moveDiv() {
    divElement.style.left = '-100px';
    divElement.style.top = '-50px';

    id1.style.left = '-100px';
    id1.style.top = '50px';

    id2.style.left = '100px'; 
    id2.style.top = '-50px'; 
    
    id3.style.left = '100px';
    id3.style.top = '50px';  
}

setTimeout(moveDiv, 1000);