

from time import sleep
from pyfirmata2 import *

def myCallback(data):
    global pin_led_r, pin_led_y, pin_led_g
    print(data)
    pin_led_r.write(data)
    pin_led_y.write(data)
    pin_led_g.write(data)
    pass

placa = Arduino('COM4')
# -> iniciar a leitura analógica
# -> deve-se informar o período de amostragem em ms
F = 100  # frequência de amostragem em Hz
placa.samplingOn(1000 // F)
sleep(3)  # atraso necessário para estabilidade da leitura
pin = placa.get_pin('a:0:i')  # analógico: pino A0: entrada
pin_led_r = placa.get_pin('d:9:p')
pin_led_y = placa.get_pin('d:10:p')
pin_led_g = placa.get_pin('d:11:p')

# -> é necessário registrar uma função de callback, ou seja,
# -> uma função que será chamada automaticamente a cada intervalo de tempo
# -> definido anteriormente pelo método samplingOn
pin.register_callback(myCallback)
pin.enable_reporting()

# -> loop para execução do programa
while True:
    sleep(0.1)



