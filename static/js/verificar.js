document.addEventListener("DOMContentLoaded", () => {
    const codeInput = document.getElementById("code-input");

    if (codeInput) {
        codeInput.addEventListener("input", (e) => {
            const currentVal = e.target.value;
            // Remueve de inmediato cualquier caracter que no sea un número
            const cleanVal = currentVal.replace(/[^0-9]/g, ""); 
            if (currentVal !== cleanVal) {
                e.target.value = cleanVal;
            }
        });
    }
});
