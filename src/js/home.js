let prevScrollPos = window.pageYOffset;

window.onscroll = function() {
    let currentScrollPos = window.pageYOffset;

    // Ocultar o mostrar la navbar dependiendo del scroll
    if (prevScrollPos > currentScrollPos) {
        // El usuario está haciendo scroll hacia arriba, muestra la navbar
        document.querySelector('.navbar').style.top = '0';
    } else {
        // El usuario está haciendo scroll hacia abajo, oculta la navbar
        document.querySelector('.navbar').style.top = '-60px'; // Asegúrate de que esta altura coincida con la altura de tu navbar
    }

    prevScrollPos = currentScrollPos; // Actualiza la posición del scroll
};
