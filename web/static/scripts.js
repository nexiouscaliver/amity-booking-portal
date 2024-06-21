document.addEventListener('DOMContentLoaded', () => {
    let slideIndex = 0;
    const slides = document.querySelector('.slides');
    const totalSlides = slides.querySelectorAll('img').length;

    function showSlide() {
        slides.style.transform = `translateX(-${slideIndex * 100}%)`;
    }

    function prevSlide() {
        slideIndex = (slideIndex > 0) ? slideIndex - 1 : totalSlides - 1;
        showSlide();
    }

    function nextSlide() {
        slideIndex = (slideIndex < totalSlides - 1) ? slideIndex + 1 : 0;
        showSlide();
    }

    document.querySelector('.prev').addEventListener('click', prevSlide);
    document.querySelector('.next').addEventListener('click', nextSlide);

    showSlide(); // Show initial slide
});

document.addEventListener('DOMContentLoaded', () => {
    AOS.init();
});
