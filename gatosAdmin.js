
// CARGAMOS LA INFORMACION DE LOS GATOS Y PRODUCTOS
window.onload = function() {
    cargarGatos();
    cargarProductos();
  };

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



// Cargar gatos y productos al cargar la página PARA QUE SE MUESTREN EN EL SELECCIONADOR
  
  function cargarGatos() {
    // Realizar una solicitud GET para obtener gatos
    fetch('http://127.0.0.1:5000/gatos')
      .then(response => response.json())
      .then(data => {
        const selector = document.getElementById('gato-selector');
        data.forEach(gato => {
          let option = new Option(gato.name, gato.id_gato);
          selector.add(option);
        });
      });
  }
  
  function cargarProductos() {
    // Realizar una solicitud GET para obtener productos
    fetch('http://127.0.0.1:5000/productos')
      .then(response => response.json())
      .then(data => {
        const selector = document.getElementById('producto-selector');
        data.forEach(producto => {
          let option = new Option(producto.nombre, producto.id_producto);
          selector.add(option);
        });
      });
  }


// EDITAMOS LOS GATOS CONFORMWE LA INFORMACION QUE SE ESCRIBE EN LOS TEXT BOXS
function editarGato() {
    const idGato = document.getElementById('gato-selector').value;
    const nombre = document.getElementById('gato-name').value;
    const edad = document.getElementById('gato-age').value;
    const raza = document.getElementById('gato-race').value;
    const info = document.getElementById('gato-info').value;
  
    // Realizar una solicitud PUT para actualizar el gato
    fetch('http://127.0.0.1:5000/gatos/' + idGato, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: nombre,
        age: edad,
        race: raza,
        info: info
      })
    })
    .then(response => response.json())
    .then(data => {
      alert(data.message); // Muestra un mensaje con la respuesta del servidor
      cargarGatos(); // Recargar la lista de gatos
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Ocurrió un error al actualizar el gato');
    });
  }
  

  // EDITAMOS LOS PRODUCTOS CONFORMWE LA INFORMACION QUE SE ESCRIBE EN LOS TEXT BOXS
  function editarProducto() {
    const idProducto = document.getElementById('producto-selector').value;
    const nombre = document.getElementById('producto-nombre').value;
    const disponibilidad = document.getElementById('producto-disponibilidad').value;
    const precio = document.getElementById('producto-precio').value;
  
    // Realizar una solicitud PUT para actualizar el producto
    fetch('http://127.0.0.1:5000/productos/' + idProducto, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        nombre: nombre,
        disponibilidad: disponibilidad,
        precio: precio
      })
    })
    .then(response => response.json())
    .then(data => {
      alert(data.message); // Muestra un mensaje con la respuesta del servidor
      cargarProductos(); // Recargar la lista de productos
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Ocurrió un error al actualizar el producto');
    });
  }
  

  // FUNCION PARA AGREGAR UN GATO CON LOS DATOS QUE SE LE ESCRIBEN EN EL TEXT BOX
  function agregarGato() {
    const nombre = document.getElementById('nuevo-gato-nombre').value;
    const edad = document.getElementById('nuevo-gato-edad').value;
    const raza = document.getElementById('nuevo-gato-raza').value;
    const info = document.getElementById('nuevo-gato-info').value;
  
    fetch('http://127.0.0.1:5000/gatos', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name: nombre, age: edad, race: raza, info: info })
    })
    .then(response => response.json())
    .then(data => {
      alert(data.message); // Muestra un mensaje con la respuesta del servidor
      cargarGatos(); // Recargar la lista de gatos
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Ocurrió un error al agregar el gato');
    });
  }
  

  // FUNCION PARA AGREGAR UN PRODUCTO CON LOS DATOS QUE SE LE ESCRIBEN EN EL TEXT BOX
  function agregarProducto() {
    const nombre = document.getElementById('nuevo-producto-nombre').value;
    const disponibilidad = document.getElementById('nuevo-producto-disponibilidad').value;
    const precio = document.getElementById('nuevo-producto-precio').value;
  
    fetch('http://127.0.0.1:5000/productos', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ nombre: nombre, disponibilidad: disponibilidad, precio: precio })
    })
    .then(response => response.json())
    .then(data => {
      alert(data.message); // Muestra un mensaje con la respuesta del servidor
      cargarProductos(); // Recargar la lista de productos
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Ocurrió un error al agregar el producto');
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
  setInterval(verificarNuevasSolicitudes, 30000); // verifica las solicutudes cada 30 segundos
  

  function mostrarNotificacion(solicitud) {
    // Crear la estructura HTML para la notificación
    const notificacionHTML = `
      <div class="notificacion">
        <h3>Nueva solicitud de adopción:</h3>
        <p>Quieren adoptar al gato con ID: ${solicitud.id_gato}</p>
        <h3>Datos del solicitante:</h3>
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
  
  