document.getElementById('formCambiarPassword').addEventListener('submit', function(event) {
    const nuevaPass = document.getElementById('nueva_password').value;
    const confirmarPass = document.getElementById('confirmar_password').value;
    const errorDiv = document.getElementById('error_password');
    
    // Verificamos longitud y coincidencia
    if (nuevaPass.length < 6 || nuevaPass !== confirmarPass) {
        // Evitamos que el formulario se envíe
        event.preventDefault(); 
        // Mostramos el error
        errorDiv.classList.remove('d-none');
    } else {
        // Ocultamos el error por si estaba visible
        errorDiv.classList.add('d-none');
    }
});
