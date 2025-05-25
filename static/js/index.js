let chat = document.querySelector('#chat');
let input = document.querySelector('#input');
let botonEnviar = document.querySelector('#boton-enviar');
let imagenSeleccionada;
let botonAdjunto = document.querySelector('#mas_archivo'); // Buscamos el botón con su ID
let miniaturaImagen;

async function tomarImagen(){
    let fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'image/*';
    fileInput.onchange = async e=>{
        //garantizar que tomamos la imagen que cargamos
        if(miniaturaImagen){
            miniaturaImagen.remove();
        }
        imagenSeleccionada = e.target.files[0];

        miniaturaImagen = document.createElement('img');
        miniaturaImagen.src = URL.createObjectURL(imagenSeleccionada);
        miniaturaImagen.style.maxWidth = '3rem'; //16 pixeles x 3
        miniaturaImagen.style.maxHeight = '3rem';
        miniaturaImagen.style.margin = '0.5rem'; 

        document.querySelector('.entrada__container').insertBefore(miniaturaImagen, input);  

        let formData = new FormData();
        formData.append('imagen', imagenSeleccionada);

        const response = await fetch('http://127.0.0.1:5000/cargar_imagen', {
            method: 'POST',
            body: formData
        });

        const respuesta = await response.text();
        console.log(respuesta);
        console.log(imagenSeleccionada);
    }
    fileInput.click();
}

async function enviarMensaje() {
    if(input.value == "" || input.value == null) return;
    let mensaje = input.value;
    input.value = "";

    if(miniaturaImagen){
        miniaturaImagen.remove();
    }

    let nuevaBurbuja = creaBurbujaUsuario();
    nuevaBurbuja.innerHTML = mensaje;
    chat.appendChild(nuevaBurbuja);

    let nuevaBurbujaBot = creaBurbujaBot();
    chat.appendChild(nuevaBurbujaBot);
    irParaFinalDelChat();
    nuevaBurbujaBot.innerHTML = "Analizando"

    let estados = ['Analizando .','Analizando ..','Analizando ...','Analizando .'] //Añadimos una animación
    let indiceEstado = 0;

    let intervaloAnimacion = setInterval(() => {
        nuevaBurbujaBot.innerHTML = estados[indiceEstado];
        indiceEstado = (indiceEstado + 1) % estados.length;
    },500);
    
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

    clearInterval(intervaloAnimacion);

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

botonAdjunto.addEventListener('click',tomarImagen);
