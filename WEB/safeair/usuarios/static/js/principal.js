var modal1 = document.getElementById('id01');
var modal2 = document.getElementById('id02');

window.onclick = function (event) {
    if (event.target == modal1) {
        modal1.style.display = "none";
    } else if (event.target == modal2) {
        modal2.style.display = "none";
    }
};

function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
}

function previewAvatar(event) {
    var input = event.target;
    var reader = new FileReader();

    reader.onload = function () {
        var imgElement = document.getElementById('avatar-preview');
        imgElement.src = reader.result;
    };

    reader.readAsDataURL(input.files[0]);
}
