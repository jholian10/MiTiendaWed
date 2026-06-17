/* Editar Perfil - Minimal JS */
document.addEventListener("DOMContentLoaded", function() {
    const fileInput = document.querySelector('input[name="foto_perfil"]');
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(event) {
                    const previewImg = document.querySelector('.preview-avatar');
                    if (previewImg) {
                        previewImg.src = event.target.result;
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }
});
