// COn esta funcion creamos la vista de los gatos, es decir, todos los div con los nombres de los gatos

document.addEventListener('DOMContentLoaded', () => {
    fetchProductos();
});

function fetchProductos() {     
    fetch('http://127.0.0.1:5000/productos')
    .then(response => response.json())
    .then(productos => {
        const mainContainer = document.getElementById('product-container');
        mainContainer.innerHTML = ''; // Limpiar el contenedor para los nuevos productos

        productos.forEach(producto => {
            const productoElement = document.createElement('div');
            productoElement.className = 'image-container';
            productoElement.innerHTML = `
                <h2>${producto.nombre}</h2>
                <button class="image-button" data-id="${producto.id_producto}">
                    <img src="./imagesFood/${encodeURIComponent(producto.nombre)}.png" alt="Image of ${producto.nombre}">
                </button>
                <h3>${producto.precio}</h3>
            `;
            mainContainer.appendChild(productoElement);
        });

    })
    .catch(error => {
        console.error('Error fetching productos:', error);
    });
}
