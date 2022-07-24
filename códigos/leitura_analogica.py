

from time import sleep
from pyfirmata2 import *

def myCallback(data):
    print(data)

placa = Arduino('COM3')
# -> iniciar a leitura analógica
# -> deve-se informar o período de amostragem em ms
F = 100  # frequência de amostragem em Hz
placa.samplingOn(1000 // F)
sleep(3)  # atraso necessário para estabilidade da leitura
pin = placa.get_pin('a:0:i')  # analógico: pino A0: entrada

# -> é necessário registrar uma função de callback, ou seja,
# -> uma função que será chamada automaticamente a cada intervalo de tempo
# -> definido anteriormente pelo método samplingOn
pin.register_callback(myCallback)
pin.enable_reporting()

# -> loop para execução do programa
while True:
    sleep(0.1)



