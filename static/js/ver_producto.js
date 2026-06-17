document.addEventListener("DOMContentLoaded", () => {
    // Controles de cantidad
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

    // Estrellas Interactivas
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
                inputCalificacion.value = valorFijado;
                labelRating.innerText = textos[valorFijado];
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

    actualizarContadores();
});

async function actualizarContadores() {
    try {
        const resCart = await fetch("/carrito/cantidad-api");
        if (resCart.ok) {
            const data = await resCart.json();
            document.getElementById('cart-count').innerText = data.cantidad;
        }
        const resFav = await fetch("/favoritos/cantidad-api");
        if (resFav.ok) {
            const data = await resFav.json();
            document.getElementById('fav-count').innerText = data.cantidad;
        }
    } catch (e) { 
        console.error("Error contadores:", e); 
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
            icon.classList.toggle('bi-heart');
            icon.classList.toggle('bi-heart-fill');
        }
    } catch (error) {
        console.error("Error favoritos:", error);
    } finally {
        btn.disabled = false;
    }
}
