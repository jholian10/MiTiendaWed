document.addEventListener("DOMContentLoaded", () => {
    inicializarEstados();
    inicializarAnimaciones();
});

function mostrarNotificacion(mensaje, tipo = 'success', titulo = '') {
    const container = document.getElementById('toastContainer');
    const template = document.getElementById('toastTemplate');
    const clone = template.content.cloneNode(true);

    const toastEl = clone.querySelector('.toast');
    const iconEl = clone.querySelector('.toast-icon');
    const titleEl = clone.querySelector('.toast-title');
    const msgEl = clone.querySelector('.toast-message');

    toastEl.classList.add(`toast-${tipo}`);

    if (tipo === 'success') {
        iconEl.classList.add('bi-check-circle-fill');
        titleEl.textContent = titulo || '¡Operación Exitosa!';
    } else if (tipo === 'warning') {
        iconEl.classList.add('bi-exclamation-triangle-fill');
        titleEl.textContent = titulo || 'Aviso';
    } else {
        iconEl.classList.add('bi-x-circle-fill');
        titleEl.textContent = titulo || 'Error';
    }

    msgEl.textContent = mensaje;

    container.appendChild(toastEl);
    const bsToast = new bootstrap.Toast(toastEl);
    bsToast.show();

    toastEl.addEventListener('hidden.bs.toast', () => {
        toastEl.remove();
    });
}

async function inicializarEstados() {
    try {
        const resCart = await fetch("/carrito/api/cantidad");
        if (resCart.ok) {
            const dataCart = await resCart.json();
            actualizarBadge('cart-count', dataCart.cantidad);
        }

        const resFav = await fetch("/favoritos/api/cantidad");
        if (resFav.ok) {
            const dataFav = await resFav.json();
            actualizarBadge('fav-count', dataFav.cantidad || 0);

            const favoritosIds = dataFav.ids || [];
            document.querySelectorAll('.btn-fav-float').forEach(boton => {
                const productoId = parseInt(boton.getAttribute('data-id'));
                if (favoritosIds.includes(productoId)) {
                    boton.classList.add('active');
                }
            });
        }
    } catch (error) {
        console.error("Error al sincronizar datos con el servidor:", error);
    }
}

function actualizarBadge(id, cantidad) {
    const badge = document.getElementById(id);
    if (badge && parseInt(badge.innerText) !== cantidad) {
        badge.innerText = cantidad;
        badge.style.transform = 'scale(1.3)';
        setTimeout(() => { badge.style.transform = 'scale(1)'; }, 200);
    }
}

async function agregarAlCarritoAsincrono(button, productoId) {
    const originalHtml = button.innerHTML;
    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Procesando...';
    button.disabled = true;

    try {
        const formData = new FormData();
        formData.append('cantidad', 1);

        const url = `/carrito/agregar/${productoId}`;
        const response = await fetch(url, {
            method: 'POST',
            body: formData,
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });

        if (response.status === 401) {
            mostrarNotificacion("Debes iniciar sesión para realizar compras.", "warning", "Acceso Requerido");
            setTimeout(() => window.location.href = "/auth/login", 2000);
            return;
        }

        if (response.ok) {
            const data = await response.json();
            mostrarNotificacion(data.message || "Producto añadido a tu pedido.", "success");

            const resCart = await fetch("/carrito/api/cantidad");
            if (resCart.ok) {
                const dataCart = await resCart.json();
                actualizarBadge('cart-count', dataCart.cantidad);
            }
        } else {
            mostrarNotificacion("No pudimos procesar tu solicitud.", "error");
        }
    } catch (error) {
        mostrarNotificacion("Error de conexión al agregar al carrito.", "error");
    } finally {
        button.innerHTML = originalHtml;
        button.disabled = false;
    }
}

async function toggleFavorito(button, productoId) {
    if(button.classList.contains('processing')) return;
    button.classList.add('processing');

    try {
        const url = `/favoritos/toggle/${productoId}`;
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 401) {
            mostrarNotificacion("Inicia sesión para guardar tus favoritos.", "warning");
            setTimeout(() => window.location.href = "/auth/login", 1500);
            return;
        }

        if (response.ok) {
            const data = await response.json();

            if(data.agregado) {
                button.classList.add('active');
                mostrarNotificacion(data.message || "Guardado en tus favoritos", "success", "Favorito Añadido");
            } else {
                button.classList.remove('active');
                mostrarNotificacion(data.message || "Eliminado de tus favoritos", "success", "Favorito Removido");
            }

            const resFav = await fetch("/favoritos/api/cantidad");
            if (resFav.ok) {
                const dataFav = await resFav.json();
                actualizarBadge('fav-count', dataFav.cantidad || 0);
            }
        }
    } catch (error) {
        mostrarNotificacion("Error al conectar con la base de datos.", "error", "Fallo de conexión");
    } finally {
        button.classList.remove('processing');
    }
}

function inicializarAnimaciones() {
    const cards = document.querySelectorAll('.product-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';

        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';

            setTimeout(() => {
                card.style.transition = 'all 0.4s cubic-bezier(0.16, 1, 0.3, 1)';
            }, 500);
        }, 100 * (index % 10));
    });
}
