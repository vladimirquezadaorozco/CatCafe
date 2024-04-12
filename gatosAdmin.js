
// Cuando haces clic en el botón de cerrar
document.querySelector('.close-btn').addEventListener('click', function() {
    document.getElementById('popup-container').style.display = 'none';
});


document.addEventListener('DOMContentLoaded', () => {
    fetchGatos();
});


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


// FUNCION PARA OBTENER LOS DATOS DE CIERTO GATO CON SU ID
function fetchCatInfo(catId) {
    fetch(`http://127.0.0.1:5000/gatos/${catId}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        // Crear el contenido del pop-up con la información del gato
        const popupText = `
            <h2>${data.name}</h2>
            <p>Raza: ${data.race}</p>
            <p>Edad: ${data.age} años</p>
            <p>Info: ${data.info}</p>
        `;
        document.getElementById('popup-container').style.display = 'block';
        document.getElementById('popup-text').innerHTML = popupText; // Usa innerHTML para establecer el contenido
    })
    .catch(error => {
        console.error('Error fetching cat info:', error);
    });
}


// Función para verificar nuevas solicitudes y mostrarlas
function verificarNuevasSolicitudes() {
    fetch('http://127.0.0.1:5000/obtener_notificaciones') 
      .then(response => response.json())
      .then(solicitudes => {
        const notificacionesDiv = document.getElementById('notificaciones');
        notificacionesDiv.innerHTML = ''; // Limpia las notificaciones anteriores
        solicitudes.forEach(solicitud => {
          mostrarNotificacion(solicitud);
        });
      })
      .catch(error => console.error('Error al obtener solicitudes:', error));
  }
  
  // Ejecuta la función al cargar la página y luego cada 30 segundos
  document.addEventListener('DOMContentLoaded', verificarNuevasSolicitudes);
  setInterval(verificarNuevasSolicitudes, 30000);
  

  function mostrarNotificacion(solicitud) {
    // Crear la estructura HTML para la notificación
    const notificacionHTML = `
      <div class="notificacion">
        <p>Nueva solicitud de adopción:</p>
        <p>Nombre del gato: ${solicitud.id_gato}</p>
        <p>Nombre del cliente: ${solicitud.nombre_cliente}</p>
        <p>Email del cliente: ${solicitud.email_cliente}</p>
        <button onclick="cerrarNotificacion(this)">Cerrar</button>
      </div>
    `;
  
    // Añadir la notificación al contenedor de notificaciones
    const notificacionesDiv = document.getElementById('notificaciones');
    notificacionesDiv.innerHTML += notificacionHTML;
  }
  
  function cerrarNotificacion(btn) {
    // Cerrar la notificación cuando se haga clic en el botón cerrar
    btn.parentElement.style.display = 'none';
  }
  
  