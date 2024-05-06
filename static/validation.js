document.addEventListener('DOMContentLoaded', function () {
    const inputs = document.querySelectorAll('input , textarea');
    inputs.forEach(input => {
        input.addEventListener('input', function () {
            const errorMessage = this.nextElementSibling;
            if (!this.validity.valid) {
                errorMessage.style.display = 'block';
            } else {
                errorMessage.style.display = 'none';
            }
        });
    });
});