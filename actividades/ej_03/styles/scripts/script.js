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

    // SETPOINT
    const setpointRange = document.getElementById('setpointRange');
    const setpointValue = document.getElementById('setpointValue');
    if(setpointRange && setpointValue) {
        setpointRange.addEventListener('input', function() {
            setpointValue.textContent = setpointRange.value;
        });

        setpointRange.addEventListener('change', function() {
            fetch(`/setpoint/${setpointRange.value}`, { method: 'POST' });
        });
    }

    // Actualiza Temperatura y el Buzzer.
    function refreshTempAndBuzzer() {
        fetch('/sensor/temperature')
            .then(res => res.json())
            .then(data => {
                const tempEl = document.getElementById('sensorTemp');
                if(tempEl) tempEl.textContent = data.temperature?.toFixed(1) ?? '--';
            });

        fetch('/buzzer/status')
            .then(res => res.json())
            .then(data => {
                const buzzEl = document.getElementById('buzzerStatus');
                if(buzzEl) buzzEl.textContent = data.status === 'on' ? 'Encendido' : 'Apagado';
            });
    }

    setInterval(refreshTempAndBuzzer, 2000);
    refreshTempAndBuzzer();
});

function controlador_tira_led() {
    const rojo = document.getElementById('redSlider').value;
    const verde = document.getElementById('greenSlider').value;
    const azul = document.getElementById('blueSlider').value;
    fetch(`/rgbled/global/${rojo}/${verde}/${azul}`);
}

