document.addEventListener("DOMContentLoaded", () => {

    // 1. Manejo de cantidad (Botones + y -)
    const inputCantidad = document.getElementById("input-cantidad");
    const btnMas = document.getElementById("btn-mas");
    const btnMenos = document.getElementById("btn-menos");
    const maxStock = inputCantidad ? parseInt(inputCantidad.max) : 0;

    if (btnMenos && inputCantidad) {
        btnMenos.addEventListener("click", () => {
            let actual = parseInt(inputCantidad.value);
            if (actual > 1) inputCantidad.value = actual - 1;
        });
    }

    if (btnMas && inputCantidad) {
        btnMas.addEventListener("click", () => {
            let actual = parseInt(inputCantidad.value);
            if (actual < maxStock) inputCantidad.value = actual + 1;
        });
    }

    // 2. Sistema de Valoración por Estrellas
    const estrellas = document.querySelectorAll(".star-panel-item");
    const inputCalificacion = document.getElementById("input-calificacion");
    const labelRating = document.getElementById("label-rating");

    const textos = {
        "1": "Insatisfactorio (1/5)",
        "2": "Deficiente (2/5)",
        "3": "Regular (3/5)",
        "4": "Muy Bueno (4/5)",
        "5": "Excelente (5/5)"
    };

    if(estrellas.length > 0) {
        let valorFijado = 5;
        marcarEstrellas(valorFijado);

        estrellas.forEach(est => {
            est.addEventListener("click", () => {
                valorFijado = est.getAttribute("data-value");
                if (inputCalificacion) inputCalificacion.value = valorFijado;
                if (labelRating) labelRating.innerText = textos[valorFijado];
                marcarEstrellas(valorFijado);
            });

            est.addEventListener("mouseover", () => {
                marcarEstrellas(est.getAttribute("data-value"));
            });

            est.addEventListener("mouseout", () => {
                marcarEstrellas(valorFijado);
            });
        });
    }

    function marcarEstrellas(valor) {
        estrellas.forEach(est => {
            const estVal = parseInt(est.getAttribute("data-value"));
            if (estVal <= parseInt(valor)) {
                est.classList.add("selected");
            } else {
                est.classList.remove("selected");
            }
        });
    }

    // 3. INTERCEPTAR EL FORMULARIO DE "AÑADIR AL CARRITO" (Para actualizar el Navbar en tiempo real)
    // Buscamos cualquier formulario cuyo action vaya hacia el carrito/agregar/
    const formCarrito = document.querySelector("form[action*='/carrito/agregar/']");
    if (formCarrito) {
        formCarrito.addEventListener("submit", async (e) => {
            // Detenemos el envío normal de HTML que recarga la página de golpe
            e.preventDefault();

            const actionUrl = formCarrito.getAttribute("action");
            const formData = new FormData(formCarrito);

            try {
                // Hacemos la petición AJAX enviando la cabecera X-Requested-With que tu Flask espera
                const response = await fetch(actionUrl, {
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-Requested-With": "XMLHttpRequest"
                    }
                });

                const data = await response.json();

                if (response.status === 401 || data.status === 'login_required') {
                    window.location.href = "/auth/login";
                    return;
                }

                if (data.status === "success") {
                    actualizarContadores();
                    
                } else {
                    alert(data.message || "Error al añadir el producto.");
                }

            } catch (error) {
                console.error("Error al enviar al carrito:", error);
            }
        });
    }

    // Cargamos contadores iniciales al abrir la página
    actualizarContadores();
});

// 4. Función de actualización con las URLs correctas del backend de Flask
async function actualizarContadores() {
    try {
        // CORRECCIÓN DE RUTAS: Se cambió de '/carrito/cantidad-api' a '/carrito/api/cantidad'
        const resCart = await fetch("/carrito/api/cantidad");
        if (resCart.ok) {
            const data = await resCart.json();
            const elCart = document.getElementById('cart-count');
            if (elCart) elCart.innerText = data.cantidad;
        }
        
        // CORRECCIÓN DE RUTAS: Se cambió de '/favoritos/cantidad-api' a '/favoritos/api/cantidad'
        const resFav = await fetch("/favoritos/api/cantidad");
        if (resFav.ok) {
            const data = await resFav.json();
            const elFav = document.getElementById('fav-count');
            if (elFav) elFav.innerText = data.cantidad;
        }
    } catch (e) {
        console.error("Error actualizando contadores del navbar:", e);
    }
}

async function toggleFavoritoDetalle(btn, productoId) {
    try {
        btn.disabled = true;
        const response = await fetch(`/favoritos/toggle/${productoId}`, { method: 'POST' });
        if (response.status === 401) {
            window.location.href = "/auth/login";
            return;
        }
        if (response.ok) {
            actualizarContadores();
            btn.classList.toggle('is-active');
            const icon = btn.querySelector('i');
            if (icon) {
                icon.classList.toggle('bi-heart');
                icon.classList.toggle('bi-heart-fill');
            }
        }
    } catch (error) {
        console.error("Error favoritos:", error);
    } finally {
        btn.disabled = false;
    }
}