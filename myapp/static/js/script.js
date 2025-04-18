document.addEventListener('DOMContentLoaded', function () {
    const logo = document.querySelector('.refresh-logo');
    if (logo) {
        logo.addEventListener('click', function () {
            window.location.reload();
        });
    }
});

let index = 0;
  setInterval(() => {
    const slides = document.querySelectorAll('.slide');
    slides.forEach(s => s.classList.remove('active'));
    index = (index + 1) % slides.length;
    slides[index].classList.add('active');
  }, 3000);

  // Примерный JS-счётчик
  document.addEventListener('DOMContentLoaded', () => {
    // Эти значения можно подгружать по Ajax
    document.getElementById('client-count').innerText = '152'; // взять из бэкенда
    document.getElementById('account-count').innerText = '47';  // взять из бэкенда
  });