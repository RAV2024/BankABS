function animateValue(id, end, duration = 1500) {
  const obj = document.getElementById(id);
  const start = 0;
  const range = end - start;
  if (range <= 0) {
    obj.innerText = end;  // Например, если end = 0 или отрицательное
    return;
  }
  const stepTime = Math.max(Math.floor(duration / range), 20);
  let current = start;
  const timer = setInterval(() => {
    current++;
    obj.innerText = current;
    if (current >= end) {
      clearInterval(timer);
    }
  }, stepTime);
}

document.addEventListener('DOMContentLoaded', () => {
  const clientCount = parseInt(document.getElementById("client-count").dataset.value) || 0;
  const accountCount = parseInt(document.getElementById("account-count").dataset.value) || 0;

  animateValue("client-count", clientCount);
  animateValue("account-count", accountCount);
});

document.addEventListener('DOMContentLoaded', function() {
    new Swiper(".features-swiper", {
      loop: true,
      speed: 600,
      effect: 'fade',
      fadeEffect: {
        crossFade: true
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
    });
  });
