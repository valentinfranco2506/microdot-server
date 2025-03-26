import machine
i2c = machine.I2C(sda=machine.Pin(21), scl=machine.Pin(22))


from ssd1306 import SSD1306_I2C
oled = SSD1306_I2C(128, 32, i2c)

def connect_to(ssid : str, passwd : str) -> None:
    """Conecta el microcontrolador a la red indicada.

    Parameters
    ----------
    ssid : str
        Nombre de la red a conectarse
    passwd : str
        Contraseña de la red
    """
    
    import network
    from time import sleep
    
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(ssid, passwd)
        while not sta_if.isconnected():
            sleep(.05)
            
    return sta_if.ifconfig()[0]

oled.fill(0)
oled.show()

oled.text("Ip Mirta:",0,0)
oled.text(connect_to("Cooperadora Alumnos", ""), 0, 10)
oled.show()


   
