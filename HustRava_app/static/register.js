// Enable the Register button immediately
document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("#register-button").removeAttribute("disabled");
    document.getElementById("warning").remove();
});

function register() {
    document.getElementById("submit").click();
}
