document.addEventListener('DOMContentLoaded', () => {//Asi nos aseguramos de que el script se ejecuta despues de que el HTML se carga completamente
    const loginForm = document.getElementById('loginForm');  // Obtenemos el formulario por el ID
  
    loginForm.addEventListener('submit', function(event) {   // Añadir un manejador de evento 'submit' al formulario
      event.preventDefault(); // Prevenir el comportamiento predeterminado del formulario
  
      const username = document.getElementById('username').value; // Obtener el valor ingresado en el input de usuario
      const password = document.getElementById('password').value;  // Obtener el valor ingresado en el input de contraseña
        
      // Crear un objeto con los datos de usuario y contraseña
      const loginData = {
        username: username, // clave 'username' se asigna al valor de la variable username
        password: password , // clave 'password' se asigna al valor de la variable password
      };
  
      fetch('http://127.0.0.1:5000/login', {  // Usar 'fetch' para enviar una solicitud POST al servidor
        method: 'POST', // Método HTTP para enviar datos
        headers: {
          'Content-Type': 'application/json', // Indicar que el tipo de contenido es JSON
        },
        body: JSON.stringify(loginData), // Convertir el objeto loginData a una cadena JSON
      })
      .then(response => {
        // Revisa si la respuesta del servidor es satisfactoria
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        } else {
          return response.json(); // Si quieres procesar la respuesta como JSON
        }
      })
      .then(data => {
        // Aquí puedes manejar la respuesta. En este caso, solamente despliega un mensaje de exito en la consola
        console.log('Success:', data);
      })
      .catch(error => {
        // Si ocurre un error en la solicitud o en la respuesta, lo capturas aquí
        console.error('Error during fetch:', error);
      });
    });
  });