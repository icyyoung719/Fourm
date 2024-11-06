localStorage.getItem("forum-dark-mode") === "true" ? document.body.classList.add("dark-mode") : document.body.classList.remove("dark-mode");
function toggle_theme() {
    document.body.classList.toggle("dark-mode");
    localStorage.setItem("forum-dark-mode", document.body.classList.contains("dark-mode"));
}