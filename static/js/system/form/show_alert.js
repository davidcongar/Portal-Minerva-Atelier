function showAlert(message) {
  window.dispatchEvent(new CustomEvent('show-info', { detail: message }));
  infoAlert.style.display = 'flex';
  infoAlert.style.opacity = '1';

  setTimeout(() => {
    infoAlert.style.opacity = '0';
    setTimeout(() => infoAlert.style.display = 'none', 1000);
  }, 3000);
}
