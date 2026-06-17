function actualizarContadoresNavbar() {
    // Actualizar Carrito
    fetch('/carrito/api/cantidad')
        .then(res => res.json())
        .then(data => {
            const el = document.getElementById('contador-carrito');
            if(el) el.innerText = data.cantidad;
        });

    // Actualizar Favoritos
    fetch('/favoritos/api/cantidad')
        .then(res => res.json())
        .then(data => {
            const el = document.getElementById('contador-favoritos');
            if(el) el.innerText = data.cantidad;
        });
}