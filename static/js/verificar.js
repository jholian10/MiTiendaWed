document.addEventListener("DOMContentLoaded", () => {
    const codeInput = document.getElementById("code-input");

    if (codeInput) {
        codeInput.addEventListener("input", (e) => {
            const currentVal = e.target.value;

            const cleanVal = currentVal.replace(/[^0-9]/g, "");
            if (currentVal !== cleanVal) {
                e.target.value = cleanVal;
            }
        });
    }
});
