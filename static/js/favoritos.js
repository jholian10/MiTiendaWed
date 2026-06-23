const toastElement = document.getElementById('liveToast');
const toast = new bootstrap.Toast(toastElement, { delay: 3000 });

function mostrarNotificacion(mensaje, tipo = 'success') {
    const toastBody = document.getElementById('toastMessage');

    let icon = '';
    if (tipo === 'success') {
        icon = '<i class="bi bi-check-circle-fill"></i>';
    } else if (tipo === 'error') {
        icon = '<i class="bi bi-x-circle-fill"></i>';
    } else {
        icon = '<i class="bi bi-info-circle-fill"></i>';
    }

    toastBody.innerHTML = `${icon} ${mensaje}`;
    toast.show();
}

function removerFavorito(btn, productoId) {
    fetch(`/favoritos/toggle/${productoId}`, { method: 'POST' })
        .then(response => {
            if (response.ok) {
                const cardElement = document.getElementById(`product-card-${productoId}`);
                if (cardElement) {
                    cardElement.style.opacity = '0';
                    setTimeout(() => cardElement.remove(), 300);
                }
                mostrarNotificacion('Removido de favoritos', 'info');


                const fav = document.getElementById('fav-container');
                if (fav.children.length === 1) {
                    document.getElementById('empty-msg').classList.remove('d-none');
                }
            }
        })
        .catch(error => {
            console.error("Error:", error);
            mostrarNotificacion('Error al remover favorito', 'error');
        });
}
