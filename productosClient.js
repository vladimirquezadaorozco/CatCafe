document.querySelector('.close-btn').addEventListener('click', function() {
    document.getElementById('popup-container').style.display = 'none';
});

document.addEventListener('DOMContentLoaded', () => {
    fetchProductos();
});

function fetchProductos() {
    fetch('http://127.0.0.1:5000/productos')
    .then(response => response.json())
    .then(productos => {
        const mainContainer = document.getElementById('product-container');
        mainContainer.innerHTML = '';
        productos.forEach(producto => {
            const productoElement = document.createElement('div');
            productoElement.className = 'product-container';
            productoElement.innerHTML = `
                <h2>${producto.name}</h2>
                <button class="product-button" data-id="${producto.id_producto}">
                    <img src="./images/${encodeURIComponent(producto.name)}.png" alt="Image of ${producto.name}">
                </button>
            `;
            mainContainer.appendChild(productoElement);
        });

        attachClickEventToProductButtons();
    })
    .catch(error => {
        console.error('Error fetching productos:', error);
    });
}

function attachClickEventToProductButtons() {
    const productos = document.querySelectorAll('.product-container');
    productos.forEach(producto => {
        producto.addEventListener('click', () => {
            const popupContainer = document.getElementById('popup-container');
            const popupText = document.getElementById('popup-text');
            popupText.textContent = 'Información de ' + producto.querySelector('h2').textContent;
            popupContainer.style.display = 'flex';
        });
    });
}

function hidePopup() {
    document.getElementById('popup-container').style.display = 'none';
}


function fetchProductos() {     
    fetch('http://127.0.0.1:5000/productos')
    .then(response => response.json())
    .then(productos => {
        const mainContainer = document.getElementById('product-container');
        mainContainer.innerHTML = ''; // Limpiar el contenedor para los nuevos gatos

        productos.forEach(producto => {
            const productoElement = document.createElement('div');
            productoElement.className = 'product-container';
            productoElement.innerHTML = `
                <h2>${producto.name}</h2>
                <p>Disponibles: ${producto.disponibles}</p>
                <button class="product-button" data-id="${producto.id_producto}">
                    <img src="./images/${encodeURIComponent(producto.name)}.png" alt="Image of ${producto.name}">
                </button>
            `;
            mainContainer.appendChild(productoElement);
        });

        attachClickEventToButtons();
    })
    .catch(error => {
        console.error('Error fetching productos:', error);
    });
}

function attachClickEventToButtons() {
    document.querySelectorAll('.product-button').forEach(button => {
        button.addEventListener('click', function() {
            const productID = this.dataset.id; // Aquí capturamos el id_gato del data-id del botón
            if (productID) {
                fetchProductInfo(productID); // Llamamos a fetchCatInfo con el id_gato correcto
            } else {
                console.error('El ID del producto no está definido.');
            }
        });
    });
}

// Funcion para crear el pop up
function fetchProductInfo(productID) {
    fetch(`http://127.0.0.1:5000/productos/${productID}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {  // Adjuntamos los datos del gato dentro del pop up
        const popupText = `
        <h2>${data.name}</h2>
        <p class="costo">Costo: ${data.precio}</p>
        <p class="disponibles">Disponibles: ${data.disponibles} años</p>

        <div>
            <input type="number" id="cantidad" placeholder="Cantidad" min="1" max="${data.disponibilidad}" />
            <button onclick="comprarProducto(${productID})">Comprar</button>
        </div>
        `;
        document.getElementById('popup-container').style.display = 'block';
        document.getElementById('popup-text').innerHTML = popupText;
    })
    .catch(error => {
        console.error('Error fetching producto info:', error);
    });
}

function comprarProducto(productId) {
    const cantidad = document.getElementById('cantidad').value;

    
    const compraInfo = {
        productId: productId,
        cantidadComprada: cantidad
    };

    fetch('http://127.0.0.1:5000/comprar_producto', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(compraInfo)  // Envía toda la información del gato en el cuerpo de la solicitud
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        console.log('Compra realizada con exito:', data);
        hidePopup(); // Cierra el pop-up después de enviar la solicitud
    })
    .catch(error => {
        console.error('Error al realizar la compra:', error);
    });
}

