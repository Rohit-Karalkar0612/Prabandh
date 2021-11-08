function bg(input){
    console.log(input.target.files[0].name);
    $(".imagecover").hide();
    $(".product").hide();
    $(".inactive").show();
    $(".removeb").removeClass("d-none");
    document.querySelector(".drag").style.color="blue";
    var ou=document.querySelector("#o");
    ou.src=URL.createObjectURL(input.target.files[0]);
    ou.onload = function() {
        URL.revokeObjectURL(ou.src)
    }
    console.log("lkk");
}

function remove(event){
    event.preventDefault();
    $(".inactive").hide();
    $(".removeb").addClass("d-none");
    $(".imagecover").show();
    $(".product").show();
}