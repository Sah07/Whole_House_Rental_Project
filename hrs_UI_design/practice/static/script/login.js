const checkbox = document.getElementById('show-password');
const passwordInput = document.getElementById('password');

checkbox.addEventListener('change', () => {
    // toggle type without re-render issues

    passwordInput.type = checkbox.checked ? 'text' : 'password';
});