document.querySelectorAll('.image-button').forEach(button => {
    button.addEventListener('click', function() {
        var catDescription = '';
        switch (this.id) {
            case 'Gato1':
                catDescription = 'Luis Miguel es un gato cariñoso de 1 año en busca de un hogar. Es juguetón y afectuoso, ideal para un hogar sin otros animales. Está esterilizado/castrado, vacunado y desparasitado. Se lleva bien con niños y disfruta tanto de interiores como exteriores. ¿Listo para darle a Luis Miguel un hogar amoroso?';
                break;
            case 'Gato2':
                catDescription = 'Juan es un gatito curioso de 2 años en busca de un hogar. Es independiente y explorador, perfecto para un hogar tranquilo. Está esterilizado, vacunado y desparasitado. Se adapta bien a otros animales y disfruta de largas siestas al sol. ¿Listo para darle a Juan un hogar lleno de aventuras?';
                break;
            case 'Gato3':
                catDescription = 'Jose Jose es un gato noble de 3 años en busca de un hogar cariñoso. Es tranquilo y reservado, ideal para un hogar sereno. Está esterilizado, vacunado y desparasitado. Se lleva bien con niños y disfruta de la compañía humana. ¿Listo para darle a Jose Jose un hogar lleno de amor?';
                break;
            case 'Gato4':
                catDescription = 'Juan Gabriel es un gato enérgico de 1 año en busca de un hogar activo. Es juguetón y divertido, perfecto para un hogar con niños. Está esterilizado, vacunado y desparasitado. Se lleva bien con otros animales y disfruta de largas sesiones de juego. ¿Listo para darle a Juan Gabriel un hogar lleno de diversión?';
                break;
            case 'Gato5':
                catDescription = '  Ferrrnando es un gato misterioso de 4 años en busca de un hogar tranquilo. Es observador y cauteloso, ideal para un hogar sin mucho bullicio. Está esterilizado, vacunado y desparasitado. Se adapta bien a otros animales y disfruta de largos paseos nocturnos. ¿Listo para darle a Ferrrnando un hogar lleno de paz?';
                break;
            case 'Gato6':
                catDescription = 'Tigre es un gatito carismático de 2 años en busca de un hogar amoroso. Es cariñoso y sociable, perfecto para un hogar con muchos mimos. Está esterilizado, vacunado y desparasitado. Se lleva bien con niños y otros animales, y disfruta de largas conversaciones con sus humanos. ¿Listo para darle a Tigre un hogar lleno de alegría?';
                break;
        }
        document.getElementById('popup-container').style.display = 'block';
        document.getElementById('popup-text').textContent = catDescription;
    });
});

document.querySelector('.close-btn').addEventListener('click', function() {
    document.getElementById('popup-container').style.display = 'none';
});


