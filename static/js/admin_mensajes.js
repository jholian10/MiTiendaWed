/* Admin Mensajes - JS para interactividad */
document.addEventListener("DOMContentLoaded", function() {
    const userItems = document.querySelectorAll('.user-item');
    
    userItems.forEach(item => {
        item.addEventListener('click', function() {
            userItems.forEach(u => u.classList.remove('active'));
            this.classList.add('active');
        });
    });
});
