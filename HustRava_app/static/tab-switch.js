// JavaScript for tab switching
const tabLinks = document.querySelectorAll(".tab-link");
const contentSections = document.querySelectorAll(".content-section");

tabLinks.forEach(link => {
    link.addEventListener("click", function () {
        event.preventDefault(); // 阻止默认跳转

        // Remove 'active' class from all links and sections
        tabLinks.forEach(link => link.classList.remove("active"));
        contentSections.forEach(section => section.classList.remove("active"));

        // Add 'active' class to the clicked link and corresponding section
        this.classList.add("active");
        const target = document.getElementById(this.getAttribute("data-target"));
        target.classList.add("active");
    });
});
