document.addEventListener('DOMContentLoaded', () => { 
  const loginButton = document.getElementById('loginB'); // Botón de login
  const registerButton = document.getElementById('registerB'); // Botón de registro
  
  // Función para manejar el registro
  function handleRegister(event) {
    event.preventDefault(); // Prevenir el comportamiento predeterminado

    // Recoger los datos de los campos del formulario
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    // Crear el objeto con los datos
    const registerData = {
      username: username,
      password: password,
    };

    // Enviar los datos al servidor para el registro
    fetch('http://127.0.0.1:5000/register', { 
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(registerData),
    })
    .then(response => response.json())
    .then(data => {
      console.log('Registration Success:', data);
      // Manejar el éxito del registro, por ejemplo, mostrando un mensaje al usuario
    })
    .catch(error => {
      console.error('Registration Error:', error);
      // Manejar el error de registro
    });
  }


  // Función para manejar el login
  function handleLogin(event) {
    event.preventDefault(); // Prevenir el comportamiento predeterminado

    // Recoger los datos de los campos del formulario
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    // Crear el objeto con los datos
    const loginData = {
      username: username,
      password: password,
    };

    // Enviar los datos al servidor para el login
    fetch('http://127.0.0.1:5000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(loginData),
    })
    .then(response => response.json())
    .then(data => {
      console.log(data.message);
      // Redireccionando al usuario a otra página
      if (data.message === "Login successful") {
        // Si el login es exitoso, redirige al usuario a "indexAdmin.html"
        window.location.href = 'indexAdmin.html';
      } else {
        // Si el login no es exitoso, muestra un mensaje de error
        // Aquí podrás colocar el código para mostrar el mensaje de error en la UI
        // Esto lo ajustaremos después de ver tu código HTML para el login
        console.error('Login Failed:', data.message);
        // Por ahora, podrías por ejemplo cambiar el contenido de un elemento de mensaje de error en tu HTML así:
        // document.getElementById('error-message').textContent = data.message;
      }



    })
    .catch(error => {
      console.error('Login Error:', error);
      // Manejar el error de login
    });
  }

  // Añadir manejadores de evento a los botones
  registerButton.addEventListener('click', handleRegister);
  loginButton.addEventListener('click', handleLogin);
});
