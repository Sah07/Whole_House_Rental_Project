

document.addEventListener('DOMContentLoaded', function () {
    const msg = document.getElementById('flash-msg');
    const container = document.getElementById('message-container');

    if (msg) {
        setTimeout(() => {
            msg.classList.add('fade-out'); // add fade effect
        }, 2000);

        setTimeout(() => {
            container.remove(); // remove the whole container, not just the message
        }, 3000); // adjust to match animation duration
    }
});