document.addEventListener("DOMContentLoaded", () => {
    const passwordInput = document.getElementById("password-field");
    const toggleButton = document.getElementById("password-toggle");
    const statusMsg = document.getElementById("password-status-msg");
    const statusIcon = document.getElementById("status-icon");
    const resetForm = document.getElementById("reset-password-form");


    if (toggleButton && passwordInput) {
        toggleButton.addEventListener("click", () => {
            const isPassword = passwordInput.type === "password";
            passwordInput.type = isPassword ? "text" : "password";

            const icon = toggleButton.querySelector("i");
            if (isPassword) {
                icon.classList.replace("bi-eye", "bi-eye-slash");
            } else {
                icon.classList.replace("bi-eye-slash", "bi-eye");
            }
        });
    }


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

    if (resetForm) {
        resetForm.addEventListener("submit", (e) => {
            if (passwordInput.value.length < 6) {
                e.preventDefault();
                passwordInput.focus();
            }
        });
    }
});
