function led_toggle(led){
    fetch(`/led/toggle/${led}`);
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll(".led-button").forEach(button => {
        button.addEventListener("click", (e) => {
            led_toggle(e.target.dataset.ledId);
        });
    });
        
    const applyBtn = document.getElementById('applyColorButton');
    if (applyBtn) {
        applyBtn.addEventListener('click', controlador_tira_led);
    }

});

function controlador_tira_led() {
    const rojo = document.getElementById('redSlider').value;
    const verde = document.getElementById('greenSlider').value;
    const azul = document.getElementById('blueSlider').value;
    fetch(`/rgbled/global/${rojo}/${verde}/${azul}`);
}
