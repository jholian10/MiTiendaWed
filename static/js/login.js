document.addEventListener("DOMContentLoaded", () => {
    const passwordInput = document.getElementById("main-password-field");
    const toggleButton = document.getElementById("main-password-toggle");

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
});
