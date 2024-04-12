
// Cuando haces clic en el botón de cerrar
document.querySelector('.close-btn').addEventListener('click', function() {
    document.getElementById('popup-container').style.display = 'none';
});


document.addEventListener('DOMContentLoaded', () => {
    fetchGatos();
});

document.addEventListener('DOMContentLoaded', () => {
    // Obtener el botón para cerrar el pop-up
    const closeButton = document.querySelector('.close-btn');
    // Obtener el contenedor del pop-up
    const popupContainer = document.getElementById('popup-container');

    // Función para mostrar el pop-up
    function showPopup() {
        popupContainer.style.display = 'flex';
    }

    // Función para ocultar el pop-up
    function hidePopup() {
        popupContainer.style.display = 'none';
    }

    // Evento para cerrar el pop-up
    closeButton.addEventListener('click', hidePopup);

    // Evento para abrir el pop-up al hacer clic en una imagen de gato
    const gatos = document.querySelectorAll('.image-container'); // Asumiendo que tus imágenes de gato tienen esta clase
    gatos.forEach(gato => {
        gato.addEventListener('click', () => {
            showPopup();
            // Aquí puedes añadir la información del gato seleccionado al pop-up
            const popupText = document.getElementById('popup-text');
            popupText.textContent = 'Información de ' + gato.querySelector('h2').textContent;
        });
    });
});



// COn esta funcion creamos la vista de los gatos, es decir, todos los div con los nombres de los gatos
function fetchGatos() {     
    fetch('http://127.0.0.1:5000/gatos')
    .then(response => response.json())
    .then(gatos => {
        const mainContainer = document.getElementById('cat-container');
        mainContainer.innerHTML = ''; // Limpiar el contenedor para los nuevos gatos

        gatos.forEach(gato => {
            const gatoElement = document.createElement('div');
            gatoElement.className = 'image-container';
            gatoElement.innerHTML = `
                <h2>${gato.name}</h2>
                <button class="image-button" data-id="${gato.id_gato}">
                    <img src="./images/${encodeURIComponent(gato.name)}.png" alt="Image of ${gato.name}">
                </button>
            `;
            mainContainer.appendChild(gatoElement);
        });

        attachClickEventToButtons();
    })
    .catch(error => {
        console.error('Error fetching gatos:', error);
    });
}




function attachClickEventToButtons() {
    document.querySelectorAll('.image-button').forEach(button => {
        button.addEventListener('click', function() {
            const catId = this.dataset.id; // Aquí capturamos el id_gato del data-id del botón
            if (catId) {
                fetchCatInfo(catId); // Llamamos a fetchCatInfo con el id_gato correcto
            } else {
                console.error('El ID del gato no está definido.');
            }
        });
    });
}


// Funcion para crear el pop up
function fetchCatInfo(catId) {
    fetch(`http://127.0.0.1:5000/gatos/${catId}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {  // Adjuntamos los datos del gato dentro del pop up
        const popupText = `
        <h2>${data.name}</h2>
        <p class="race">Raza: ${data.race}</p>
        <p class="age">Edad: ${data.age} años</p>
        <p class="info">Info: ${data.info}</p>

        <div>
            <input type="text" id="cliente-nombre" placeholder="Tu nombre" />
            <input type="email" id="cliente-email" placeholder="Tu email" />
        </div>

        <button onclick="enviarSolicitud(${catId})">ENVIAR SOLICITUD</button>
        `;
        document.getElementById('popup-container').style.display = 'block';
        document.getElementById('popup-text').innerHTML = popupText;
    })
    .catch(error => {
        console.error('Error fetching cat info:', error);
    });
}


// AL MOMENTO DE DARLE AL BOTON DE ENVIAR SOLICITUD EN EL POPUP
function enviarSolicitud(catId) {
    const nombre = document.getElementById('cliente-nombre').value;
    const email = document.getElementById('cliente-email').value;
    
    const gatoInfo = {
        catId: catId,
        clienteNombre: nombre,
        clienteEmail: email
    };

    fetch('http://127.0.0.1:5000/enviar_solicitud', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(gatoInfo)  // Envía toda la información del gato en el cuerpo de la solicitud
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        console.log('Solicitud enviada:', data);
        hidePopup(); // Cierra el pop-up después de enviar la solicitud
    })
    .catch(error => {
        console.error('Error al enviar solicitud:', error);
    });
}

// Función para ocultar el pop-up
function hidePopup() {
    document.getElementById('popup-container').style.display = 'none';
}

