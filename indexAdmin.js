
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

function fetchCatInfo(catId) {
    fetch(`http://127.0.0.1:5000/gatos/${catId}`)
    .then(response => response.json())
    .then(data => {
        document.getElementById('popup-container').style.display = 'block';
        document.getElementById('popup-text').textContent = data.info; // Asegúrate de que el servidor envíe un campo 'info'
    })
    .catch(error => {
        console.error('Error fetching cat info:', error);
    });
}
