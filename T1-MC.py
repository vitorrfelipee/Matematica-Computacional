import numpy as np
import matplotlib.pyplot as plt

# Passo 2: Função que calcula a parte inteira e a parte fracionária de x
def calcula_e_f(x):
    e = int(np.floor(np.log2(x)))
    f = x / (2**e) - 1
    return e, f

# Passo 3: Função que calcula a raiz quadrada de 2^e baseada no valor de e
def sqrt_2e(e):
    if e == 0:
        return 1
    elif e == 1:
        return np.sqrt(2)
    elif e % 2 == 0:  # e é par
        return 2**(e//2)
    else:  # e é ímpar
        return 2**((e-1)//2) * np.sqrt(2)

# Passo 3: Função da raiz quadrada calculada
def raiz_calculada(x):
    e, f = calcula_e_f(x)
    sqrt_2e_val = sqrt_2e(e)
    # Usamos a série de Taylor para a raiz quadrada em torno de 1 para a parte f
    # Como f é a parte fracionária, é pequena, e podemos assumir f ≈ sqrt(1+f)
    return sqrt_2e_val * (1 + f / 2)

# Função para calcular e^x usando o método de Bailey
def bailey_e_x(x):
    n = np.ceil((x - (np.log(2)/2)) / np.log(2))
    r = (x - n * np.log(2)) / 256
    return (2**n) * (np.exp(r))**256

# Define o intervalo de valores de x para a raiz quadrada
x_valores_sqrt = np.arange(0.05, 5.05, 0.05)
# Define o intervalo de valores de x para o método de Bailey
x_valores_bailey = np.arange(0.05, 10.05, 0.05)

# Inicializa vetores para armazenar os erros
erros_sqrt = []
erros_bailey_abs = []

# Calcula o erro para a raiz quadrada
for x in x_valores_sqrt:
    calculo_sqrt = raiz_calculada(x)
    real_sqrt = np.sqrt(x)
    erro_sqrt = calculo_sqrt - real_sqrt
    erros_sqrt.append(erro_sqrt)

# Calcula o erro para o método de Bailey
for x in x_valores_bailey:
    calculo_bailey = bailey_e_x(x)
    real_e_x = np.exp(x)
    erro_bailey = abs(calculo_bailey - real_e_x)
    erros_bailey_abs.append(erro_bailey)

# Gráfico para o erro da raiz quadrada
plt.figure(figsize=(12, 6))
plt.plot(x_valores_sqrt, erros_sqrt, label='Erro Raiz Quadrada', color='blue')
plt.title('Erro entre a Raiz Quadrada Calculada e a Real')
plt.xlabel('x')
plt.ylabel('Erro')
plt.grid(True)
plt.legend()
plt.show()

# Gráfico para o erro do método de Bailey
plt.figure(figsize=(12, 6))
plt.plot(x_valores_bailey, erros_bailey_abs, label='Erro Método Bailey (Absoluto)', color='green')
plt.title('Erro Absoluto entre o Método Bailey e o Cálculo Padrão de e^x')
plt.xlabel('x')
plt.ylabel('Erro')
plt.grid(True)
plt.legend()
plt.show()