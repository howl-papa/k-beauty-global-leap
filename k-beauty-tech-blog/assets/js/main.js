document.addEventListener('DOMContentLoaded', () => {
  const newsletterForm = document.querySelector('.newsletter-form');

  if (newsletterForm) {
    newsletterForm.addEventListener('submit', (event) => {
      event.preventDefault();
      const emailInput = newsletterForm.querySelector('input[type="email"]');
      if (emailInput && emailInput.value) {
        alert('구독해 주셔서 감사합니다! 뉴스레터는 곧 준비될 예정입니다.');
        emailInput.value = '';
      }
    });
  }
});
