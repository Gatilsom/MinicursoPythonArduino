
from time import sleep
from pyfirmata2 import *

def callback(data):
    global click, pin_led_r, pin_led_y, pin_led_g
    if click == 0:
        pin_led_r.write(False); pin_led_y.write(False); pin_led_g.write(False)
    if click == 1:
        pin_led_r.write(True); pin_led_y.write(False); pin_led_g.write(False)
    if click == 2:
        pin_led_r.write(True); pin_led_y.write(True); pin_led_g.write(False)
    if click == 3:
        pin_led_r.write(True); pin_led_y.write(True); pin_led_g.write(True)
    pass

placa = Arduino('COM4')
placa.samplingOn(10)  # inicia amostragem com intervalo de 10 ms
sleep(3)  # atraso necessário para estabilidade da leitura
pin_led_r = placa.get_pin('d:9:o')
pin_led_y = placa.get_pin('d:10:o')
pin_led_g = placa.get_pin('d:11:o')
pin_bot = placa.get_pin('d:2:i')  # pino da saída do botão em pull-up
pin_bot.register_callback(callback)
pin_bot.enable_reporting()
aux = 0  # variável auxiliar para debounce
click = 0  # número de clicks

while True:
    if pin_bot.read():  # primeira leitura (borda de descida)
        if aux:
            sleep(0.05)  # atraso de 50 ms
            if pin_bot.read():  # segunda leitura (borda de descida)
                click += 1
                if click > 3:
                    click = 0
                aux = 0
    else:
        aux = 1


