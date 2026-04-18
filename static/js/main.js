// Bitfarma - Main JS

document.addEventListener('DOMContentLoaded', function () {

  // Auto-dismiss flash alerts after 5 seconds
  const alerts = document.querySelectorAll('.alert.alert-dismissible');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 5000);
  });

  // Confirm dangerous form submissions
  document.querySelectorAll('form[data-confirm]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      const msg = form.getAttribute('data-confirm');
      if (!confirm(msg)) {
        e.preventDefault();
      }
    });
  });

  // Tooltip initialization
  const tooltipEls = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltipEls.forEach(function (el) {
    new bootstrap.Tooltip(el);
  });

  // Highlight active table rows on click (pharmacist dashboard)
  document.querySelectorAll('.table tbody tr').forEach(function (row) {
    row.style.cursor = 'default';
  });

});
