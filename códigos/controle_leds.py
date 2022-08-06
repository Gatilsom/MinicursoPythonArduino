
from time import sleep
from pyfirmata2 import *

placa = Arduino('COM3')

pin_led_r = placa.get_pin('d:9:o')
pin_led_y = placa.get_pin('d:10:o')
pin_led_g = placa.get_pin('d:11:o')

while True:
    pin_led_r.write(True)
    pin_led_y.write(True)
    pin_led_g.write(True)
    sleep(1)  # atraso de 1 segundo
    pin_led_r.write(False)
    pin_led_y.write(False)
    pin_led_g.write(False)
    sleep(1)  # atraso de 1 segundo

