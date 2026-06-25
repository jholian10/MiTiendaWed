async function sendMessage() {
    let input = document.getElementById("user-input");
    let chat = document.getElementById("chat-messages");
    let msg = input.value;

    if(msg.trim() === "") return;


    chat.innerHTML += `<div class="message user">${msg}</div>`;
    input.value = "";
    chat.scrollTop = chat.scrollHeight;


    try {
        const response = await fetch('/support/api', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({mensaje: msg})
        });

        const data = await response.json();

        if (data.respuesta) {
            chat.innerHTML += `<div class="message bot">${data.respuesta}</div>`;
            chat.scrollTop = chat.scrollHeight;
        }
    } catch (error) {
        console.error("Error enviando mensaje:", error);
    }
}


document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") sendMessage();
});
