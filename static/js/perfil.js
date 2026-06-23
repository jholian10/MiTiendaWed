document.getElementById('formCambiarPassword').addEventListener('submit', function(event) {
    const nuevaPass = document.getElementById('nueva_password').value;
    const confirmarPass = document.getElementById('confirmar_password').value;
    const errorDiv = document.getElementById('error_password');


    if (nuevaPass.length < 6 || nuevaPass !== confirmarPass) {

        event.preventDefault();

        errorDiv.classList.remove('d-none');
    } else {

        errorDiv.classList.add('d-none');
    }
});
