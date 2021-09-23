var images=[
    '../static/User/images/1.jpg',
    '../static/User/images/2.jpg',
    '../static/User/images/3.jpg'
];
var text=[
    'Want to become a Seller?',
    'Register and Get your Business going',
    'Best in Class Support 24x7'
]
var i=0;
var e=document.querySelector(".below-right");
var e1=document.querySelector(".cover-right");
setInterval(function(){
    e.style.backgroundImage= "url(" + images[i] + ")";
    e1.innerHTML="<div class='container hello'>\
    <h2 class='center-me'>"+text[i]+"</h2>\
    </div>"
    ;
    i++;
    if(i==images.length){
        i=0;
    }
},2000);

function changeText(){
    var e=document.querySelector(".btn-info");
    var w=document.querySelector(".form-check-input");
    if(w.checked){
        e.innerText='Next';
    }
    else{
        e.innerText='Submit';
    }
}