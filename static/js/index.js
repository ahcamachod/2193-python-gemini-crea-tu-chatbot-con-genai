let chat = document.querySelector('#chat');
let input = document.querySelector('#input');
let botonEnviar = document.querySelector('#boton-enviar');

async function enviarMensaje() {
    if(input.value == "" || input.value == null) return;
    let mensaje = input.value;
    input.value = "";

    let nuevaBurbuja = creaBurbujaUsuario();
    nuevaBurbuja.innerHTML = mensaje;
    chat.appendChild(nuevaBurbuja);

    let nuevaBurbujaBot = creaBurbujaBot();
    chat.appendChild(nuevaBurbujaBot);
    irParaFinalDelChat();
    nuevaBurbujaBot.innerHTML = "Analizando ..."
    
    // Enviar la solicitud con el mensaje para la API del ChatBot
    const respuesta = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
        "Content-Type": "application/json",
        },
        body: JSON.stringify({'msg':mensaje}),
    });
    const textoDeRespuesta = await respuesta.text();
    console.log(textoDeRespuesta);
    nuevaBurbujaBot.innerHTML = textoDeRespuesta.replace(/\n/g, '<br>');
    irParaFinalDelChat();
}

function creaBurbujaUsuario() {
    let burbuja = document.createElement('p');
    burbuja.classList = 'chat__burbuja chat__burbuja--usuario';
    return burbuja;
}

function creaBurbujaBot() {
    let burbuja = document.createElement('p');
    burbuja.classList = 'chat__burbuja chat__burbuja--bot';
    return burbuja;
}

function irParaFinalDelChat() {
    chat.scrollTop = chat.scrollHeight;
}

botonEnviar.addEventListener('click', enviarMensaje);
input.addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.keyCode === 13) {
        botonEnviar.click();
    }
});