function cambiarCantidad(detalleId, cambio) {
    const inputQty = document.getElementById(`qty-${detalleId}`);
    const subtotalSpan = document.getElementById(`subtotal-${detalleId}`);
    const precioUnitario = parseFloat(document.getElementById(`precio-${detalleId}`).innerText);
    
    let cantidadActual = parseInt(inputQty.value);
    
    // Evaluar el límite inferior solicitado
    if (cantidadActual === 1 && cambio === -1) {
        mostrarAlertaMinimal();
        return; 
    }

    let nuevaCantidad = cantidadActual + cambio;
    
    // 1. Cambiar visualmente de inmediato (Optimistic UI)
    inputQty.value = nuevaCantidad;
    let nuevoSubtotal = precioUnitario * nuevaCantidad;
    subtotalSpan.innerText = nuevoSubtotal.toFixed(2);
    
    recalcularTotalesGlobales();

    // 2. Enviar actualización asíncrona mediante FormData
    const formData = new FormData();
    formData.append('cantidad', cambio); 

    fetch(`/carrito/agregar/${detalleId.replace(/\D/g, '') || 1}`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("No se pudo sincronizar con la base de datos.");
        }
        return response.json();
    })
    .catch(error => {
        console.error("Error en persistencia:", error);
        // Revertimos visualmente por seguridad si falla la red
        inputQty.value = cantidadActual;
        subtotalSpan.innerText = (precioUnitario * cantidadActual).toFixed(2);
        recalcularTotalesGlobales();
    });
}

function recalcularTotalesGlobales() {
    let totalAcumulado = 0;
    
    document.querySelectorAll('[id^="subtotal-"]').forEach(span => {
        totalAcumulado += parseFloat(span.innerText);
    });
    
    document.getElementById('summary-subtotal').innerText = totalAcumulado.toFixed(2);
    document.getElementById('summary-total').innerText = totalAcumulado.toFixed(2);
}

function mostrarAlertaMinimal() {
    const toast = document.getElementById('custom-toast');
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3500);
}
