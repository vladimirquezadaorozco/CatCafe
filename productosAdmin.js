document.getElementById('addProductForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Previene el envío tradicional del formulario

    const productName = document.getElementById('productName').value;
    const productPrice = document.getElementById('productPrice').value;
    const productStock = document.getElementById('productStock').value;

    const productData = {
        name: productName,
        disponibles: parseInt(productStock)
    };

    fetch('http://127.0.0.1:5000/comprar_producto', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(productData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Producto agregado con éxito:', data);
        // Aquí puedes limpiar el formulario o actualizar la UI para mostrar el nuevo producto
    })
    .catch(error => console.error('Error al agregar el producto:', error));
});