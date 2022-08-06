
import numpy as np
import matplotlib.pyplot as plt

# -> cria um vetor com números entre o intervalo [-5,5)
# -> possuindo espaçamento de 0.01
x = np.arange(-5, 5, 0.01)

# -> cria um vetor contendo o resultado da seguinte equação:
# ->            y = e^(-x) * cos(2πx)
y = np.exp(-x) * np.cos(2 * np.pi * x)

plt.figure()
plt.subplot(111)
plt.plot(x, y, 'r--', label='curva')
plt.title('Exemplo de Plotagem')
plt.xlabel('eixo das abscissas')
plt.ylabel('eixo das ordenadas')
plt.legend()
plt.grid()
plt.show()



