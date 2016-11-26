document.addEventListener("DOMContentLoaded", function() {
    var els = document.getElementsByClassName("img-link");
    for(var i = 0; i < els.length; i++) {
        els[i].addEventListener("click", imgLinkHandler);
    }
});

function imgLinkHandler(ev) {
    ev.preventDefault();
    var thumb = this.children[0];
    var mainImg = document.getElementById("img-main");

    var thumbNum = thumb.getAttribute("data-num");
    var mainNum = mainImg.getAttribute("data-num");

    thumb.setAttribute("data-num", mainNum);
    thumb.src = "images/devices/GoAmateur/thumb" + mainNum + ".png";

    mainImg.setAttribute("data-num", thumbNum);
    mainImg.src = "images/devices/GoAmateur/img" + thumbNum + ".png";
}
