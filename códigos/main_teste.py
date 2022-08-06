
from pyfirmata2 import *
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

def callback_capacitor(data):
    global tempo_atual, periodo_amostragem, carga, valor_pot
    global t_data_c, y_data_c, t_data_d, y_data_d
    global pin_led_r, pin_led_y, pin_led_g

    tempo_atual = tempo_atual + periodo_amostragem

    if carga:
        y_data_c = np.append(y_data_c, data)
        t_data_c = np.append(t_data_c, tempo_atual)
    else:
        y_data_d = np.append(y_data_d, data)
        t_data_d = np.append(t_data_d, tempo_atual)

    print('{:.4} --- {:.4} --- {:.4}'.format(tempo_atual,valor_pot, data))

    if 0 <= data < 0.35:
        pin_led_r.write(True)
        pin_led_y.write(False)
        pin_led_g.write(False)
    if 0.35 <= data <= 0.9:
        pin_led_r.write(False)
        pin_led_y.write(True)
        pin_led_g.write(False)
    if data > 0.9:
        pin_led_r.write(False)
        pin_led_y.write(False)
        pin_led_g.write(True)
    pass


def callback_potenciometro(data):
    global pin_entrada, modo_manual, valor_pot
    if modo_manual:
        valor_pot = data
        pin_entrada.write(valor_pot)
    else:
        if carga:
            pin_entrada.write(1)
        else:
            pin_entrada.write(0)
    pass

def callback_botao(data):
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
modo_manual = True
valor_pot = 0

placa = Arduino('COM4')
pin_pot = placa.get_pin('a:0:i')  # sinal do potenciômetro
pin_saida = placa.get_pin('a:1:i')  # saída (tensão no capacitor)
pin_entrada = placa.get_pin('d:5:p')  # entrada (tensão aplicada no circuito)
pin_entrada.write(0)
pin_led_r = placa.get_pin('d:9:o')
pin_led_y = placa.get_pin('d:10:o')
pin_led_g = placa.get_pin('d:11:o')
pin_led_r.write(False)
pin_led_y.write(False)
pin_led_g.write(False)
pin_bot = placa.get_pin('d:2:i')  # pino da saída do botão em pull-up
aux_bot = 0  # variável auxiliar para debounce

placa.samplingOn(1000 // freq_amostragem)
sleep(3)
pin_saida.register_callback(callback_capacitor)
pin_pot.register_callback(callback_potenciometro)
pin_bot.register_callback(callback_botao)
pin_saida.enable_reporting()
pin_pot.enable_reporting()
pin_bot.enable_reporting()


if carga:
    pin_entrada.write(1)
else:
    pin_entrada.write(0)
while tempo_atual < tempo_leitura:
    if pin_bot.read():  # primeira leitura (borda de descida)
        if aux_bot:
            sleep(0.15)  # atraso de 150 ms
            if pin_bot.read():  # segunda leitura (borda de descida)
                modo_manual = not modo_manual
                aux_bot = 0
    else:
        aux_bot = 1
    sleep(periodo_amostragem / 10)



tempo_atual = 0
carga = False
if carga:
    pin_entrada.write(1)
else:
    pin_entrada.write(0)
while tempo_atual < tempo_leitura:
    if pin_bot.read():  # primeira leitura (borda de descida)
        if aux_bot:
            sleep(0.15)  # atraso de 150 ms
            if pin_bot.read():  # segunda leitura (borda de descida)
                modo_manual = not modo_manual
                aux_bot = 0
    else:
        aux_bot = 1
    sleep(periodo_amostragem / 10)


placa.samplingOff()
pin_entrada.write(0)
pin_led_r.write(False)
pin_led_y.write(False)
pin_led_g.write(False)
sleep(3)
placa.exit()



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