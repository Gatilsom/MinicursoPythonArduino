
"""
import numpy as np
import matplotlib.pyplot as plt
from pyfirmata2 import *
from time import sleep, time
from serial import SerialException, SerialTimeoutException, PortNotOpenError

"""

# -> do pacote pyfirmta2 importe tudo (*)
from pyfirmata2 import *

# -> instanciar um objeto que representa a placa do arduino
# -> é nessesário informar em qual porta serial a placa está conectada
placa = Arduino('COM3')

# -> as portas do arduino são definidas a partir do método get_pin
# -> este método recebe como parâmetro uma string que descreve a porta a ser utilizada
# -> formato da string: 'digital/analógica: número do pino: tipo de entrada/saída'

# 'i' para entrada (digital ou analógica)
# 'u' para entrada com pullup (digital)
# 'o' para saída (digital)
# 'p' para saída pwm (digital)

pin = placa.get_pin('d:3:o')  # digital: pino 3: saída

# -> escrita e leitura digital:
pin.write(True)  # ou pin.write(False)
pin.read()

