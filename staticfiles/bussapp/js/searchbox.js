
document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    form.addEventListener('submit', function () {
        // Clear the search and date inputs after submission
        form.querySelector('input[name="q"]').value = '';
        form.querySelector('input[name="start_date"]').value = '';
        form.querySelector('input[name="end_date"]').value = '';
    });
});

