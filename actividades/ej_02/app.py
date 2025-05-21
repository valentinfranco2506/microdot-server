import asyncio
from microdot import Microdot
from microdot import send_file
from machine import Pin
import machine, neopixel

app = Microdot()

led1 = machine.Pin(32, Pin.OUT, value=0)
led2 = machine.Pin(33, Pin.OUT, value=0)
led3 = machine.Pin(25, Pin.OUT, value=0)
np = neopixel.NeoPixel(machine.Pin(27), 4)

np[0] = (255, 0, 0) 
np[1] = (0, 128, 0) 
np[2] = (0, 0, 64) 
np[3] = (255, 255, 255) 

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

app.run()
