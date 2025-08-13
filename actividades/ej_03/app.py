import asyncio
from microdot import Microdot
from microdot import send_file
from machine import Pin
import machine, neopixel
import onewire, ds18x20
import time

app = Microdot()

led1 = machine.Pin(32, Pin.OUT, value=0)
led2 = machine.Pin(33, Pin.OUT, value=0)
led3 = machine.Pin(25, Pin.OUT, value=0)
np = neopixel.NeoPixel(machine.Pin(27), 4)

np[0] = (0, 0, 0) 
np[1] = (0, 0, 0) 
np[2] = (0, 0, 0) 
np[3] = (0, 0, 0) 

setpoint = 23

ds_pin = machine.Pin(19) 
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
roms = ds_sensor.scan()
print("ROMs encontrados:", roms)

def read_temp_sensor():
    ds_sensor.convert_temp()
    time.sleep_ms(750)
    if roms:
        temp = ds_sensor.read_temp(roms[0])
        print("Temp leída:", temp)
        if temp is not None:
            return temp
    print("No se pudo leer temperatura")
    return None

buzzer_pin = Pin(14, Pin.OUT, value=0)
buzzer_status = False

@app.get('/')
async def index(request):
    return send_file('index.html')

@app.get('styles/base.css')
async def index(request):
    return send_file('styles/base.css')

@app.get('scripts/script.js')
async def index(request):
    return send_file('scripts/script.js')

@app.get('scripts/base.js')
async def index(request):
    return send_file('scripts/base.js')

@app.route('/led/toggle/<string:led>')
async def led_toggle(request, led):
    global led1, led2, led3
    
    print(led)

    if led == "1":
        led1.value(not led1.value())
    elif led == "2":
        led2.value(not led2.value())
    elif led == "3":
        led3.value(not led3.value())
        
    return {"status": "ok"}

@app.route('/rgbled/global/<int:rojo>/<int:verde>/<int:azul>')
async def rgbled_global(request, rojo, verde, azul):
    global np
    
    for pixel in range(4):
        np[pixel] = (rojo, verde, azul)
    np.write()
    return {"status": "ok"}

@app.route('/setpoint/<int:value>', methods=['POST'])
async def set_setpoint(request, value):
    global setpoint
    setpoint = value
    print(f"Nuevo setpoint: {setpoint}")
    return {"status": "ok"}

@app.route('/sensor/temperature')
async def sensor_temperature(request):
    temp = read_temp_sensor()
    global setpoint, buzzer_pin, buzzer_status
    if temp is not None:
        if temp > setpoint:
            buzzer_pin.value(1)
            buzzer_status = True
        else:
            buzzer_pin.value(0)
            buzzer_status = False
        return {"temperature": temp}
    else:
        # Si no hay lectura, apaga el buzzer y devuelve None
        buzzer_pin.value(0)
        buzzer_status = False
        return {"temperature": None}

@app.route('/buzzer/status')
async def buzzer_status_api(request):
    global buzzer_status
    return {"status": "on" if buzzer_status else "off"}

app.run()
# Aplicacion del servidor
