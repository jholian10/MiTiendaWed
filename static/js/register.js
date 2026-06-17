document.addEventListener("DOMContentLoaded", () => {
    const passwordInput = document.getElementById("register-password-field");
    const toggleButton = document.getElementById("register-password-toggle");
    const nameField = document.getElementById("name-field");
    const registrationForm = document.getElementById("registration-form");
    
    // Elementos del indicador de contraseña
    const statusMsg = document.getElementById("password-status-msg");
    const statusIcon = document.getElementById("status-icon");

    // Control de visualización de contraseña (Ojo)
    if (toggleButton && passwordInput) {
        toggleButton.addEventListener("click", () => {
            const isInputPassword = passwordInput.type === "password";
            passwordInput.type = isInputPassword ? "text" : "password";
            
            const iconElement = toggleButton.querySelector("i");
            if (isInputPassword) {
                iconElement.classList.replace("bi-eye", "bi-eye-slash");
            } else {
                iconElement.classList.replace("bi-eye-slash", "bi-eye");
            }
        });
    }

    // Bloqueo de números en tiempo real en el campo de Nombre
    if (nameField) {
        nameField.addEventListener("input", (e) => {
            const originalValue = e.target.value;
            const cleanedValue = originalValue.replace(/[0-9]/g, "");
            if (originalValue !== cleanedValue) {
                e.target.value = cleanedValue;
            }
        });
    }

    // Validación en tiempo real de longitud mínima de la contraseña (mínimo 6 caracteres)
    if (passwordInput) {
        passwordInput.addEventListener("input", () => {
            if (passwordInput.value.length >= 6) {
                statusMsg.classList.remove("requirement-invalid");
                statusMsg.classList.add("requirement-valid");
                statusIcon.classList.remove("bi-x-lg");
                statusIcon.classList.add("bi-check-lg");
            } else {
                statusMsg.classList.remove("requirement-valid");
                statusMsg.classList.add("requirement-invalid");
                statusIcon.classList.remove("bi-check-lg");
                statusIcon.classList.add("bi-x-lg");
            }
        });
    }

    // Evitar el envío si no cumple el mínimo de caracteres al hacer submit
    if (registrationForm) {
        registrationForm.addEventListener("submit", (e) => {
            if (passwordInput.value.length < 6) {
                e.preventDefault();
                passwordInput.focus();
            }
        });
    }
});
