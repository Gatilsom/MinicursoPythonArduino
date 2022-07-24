
from time import sleep
from pyfirmata2 import *

placa = Arduino('COM3')

pin_led_r = placa.get_pin('d:9:p')
pin_led_y = placa.get_pin('d:10:p')
pin_led_g = placa.get_pin('d:11:p')

nivel = 0
passo = 0.01
crescente = True

while True:
    pin_led_r.write(nivel)
    pin_led_y.write(nivel)
    pin_led_g.write(nivel)
    sleep(0.1)  # atraso de 100 ms
    if crescente:
        if nivel < 1:
            nivel = nivel + passo
        if nivel >= 1:
            nivel = 1
            crescente = False
    else:
        if nivel > 0:
            nivel = nivel - passo
        if nivel <= 0:
            nivel = 0
            crescente = True



