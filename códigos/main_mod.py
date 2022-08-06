
from pyfirmata2 import *
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

def apaga_leds():
    global pin_led_r, pin_led_y, pin_led_g
    pin_led_r.write(False)
    pin_led_y.write(False)
    pin_led_g.write(False)
    pass

def loop_leitura():
    global pin_entrada, tempo_atual, tempo_leitura, carga, periodo_amostragem
    tempo_atual = 0
    if carga:
        pin_entrada.write(1)
    else:
        pin_entrada.write(0)
    while tempo_atual < tempo_leitura:
        sleep(periodo_amostragem / 10)
    pass

def desliga_circuito():
    global placa, pin_entrada
    placa.samplingOff()
    pin_entrada.write(0)
    apaga_leds()
    sleep(3)
    placa.exit()
    pass

def callback(data):
    global tempo_atual, periodo_amostragem, carga
    global t_data_c, y_data_c, t_data_d, y_data_d
    global pin_led_r, pin_led_y, pin_led_g

    tempo_atual = tempo_atual + periodo_amostragem

    if carga:
        y_data_c = np.append(y_data_c, data)
        t_data_c = np.append(t_data_c, tempo_atual)
    else:
        y_data_d = np.append(y_data_d, data)
        t_data_d = np.append(t_data_d, tempo_atual)

    print('tempo: {:.4} --- leitura: {:.4}'.format(tempo_atual, data))

    if 0 <= data < 0.35:
        pin_led_r.write(True); pin_led_y.write(False); pin_led_g.write(False)
    if 0.35 <= data <= 0.9:
        pin_led_r.write(False); pin_led_y.write(True); pin_led_g.write(False)
    if data > 0.9:
        pin_led_r.write(False); pin_led_y.write(False); pin_led_g.write(True)
    pass

def plot_curvas():
    global t_data_c, y_data_c, t_data_d, y_data_d, periodo_amostragem
    # plt.style.use("dark_background")
    plt.figure()
    plt.subplot(211)
    plt.plot(t_data_c, y_data_c, color='red', label='carga', drawstyle="steps-post")
    plt.title('Circuito RC')
    plt.ylabel('tensão no capacitor (V)')
    plt.legend()
    plt.grid()
    plt.xlim(0, t_data_c[-1] + periodo_amostragem)
    plt.ylim(0, 1.01)

    plt.subplot(212)
    plt.plot(t_data_d, y_data_d, color='blue', label='descarga', drawstyle="steps-post")
    plt.ylabel('tensão no capacitor (V)')
    plt.xlabel('tempo (s)')
    plt.legend()
    plt.grid()
    plt.xlim(0, t_data_d[-1] + periodo_amostragem)
    plt.ylim(0, 1.01)

    plt.show()
    pass


t_data_c = np.array([])  # tempo na carga
y_data_c = np.array([])  # tensão no capacitor durante a carga
t_data_d = np.array([])  # tempo na descarga
y_data_d = np.array([])  # tensão no capacitor durante a descarga
tempo_leitura = 90  # (s)
freq_amostragem = 100  # (Hz)
periodo_amostragem = 1 / freq_amostragem  # (s)
tempo_atual = 0
carga = True
placa = Arduino('COM3')
pin_saida = placa.get_pin('a:1:i')  # saída (tensão no capacitor)
pin_entrada = placa.get_pin('d:5:p')  # entrada (tensão aplicada no circuito)
pin_entrada.write(0)
pin_led_r = placa.get_pin('d:9:o')
pin_led_y = placa.get_pin('d:10:o')
pin_led_g = placa.get_pin('d:11:o')
apaga_leds()
placa.samplingOn(1000 // freq_amostragem)
sleep(3)
pin_saida.register_callback(callback)
pin_saida.enable_reporting()
carga = True
loop_leitura()
carga = False
loop_leitura()
desliga_circuito()
plot_curvas()


