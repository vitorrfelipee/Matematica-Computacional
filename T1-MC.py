import numpy as np
import matplotlib.pyplot as plt

ln2 = 0.69314718055994530941723212145818
sqrt2 = 1.4142135623730950488016887242097
euler = np.e


#Função que calcula a parte inteira e a parte fracionária de x
def calcula_e_f(x):
    e = log_base_2(x)  # Usando a função log_base_2 personalizada
    f = x / pow(2, e) - 1
    return e, f

#Função que calcula a raiz quadrada de 2^e baseada no valor de e
def sqrt_2e(e):
    if e == 0:
        return 1
    elif e == 1:
        return sqrt2  # Usando a constante sqrt2
    elif e % 2 == 0:  # e é par
        return pow(2, e // 2)
    else:  # e é ímpar
        return pow(2, (e - 1) // 2) * sqrt2

#Função da raiz quadrada calculada
def raiz_calculada(x):
    e, f = calcula_e_f(x)
    sqrt_2e_val = sqrt_2e(e)
    # Aproximação linear para a raiz quadrada de 1+f
    return sqrt_2e_val * (1 + f / 2)

#Função para exponenciação 
def pow(x: float, y: int):
    if y == 0:
        return 1
    elif y == 1:
        return x
    elif y < 0:
        return 1 / pow(x, -y)
    elif y % 2 == 0:
        half_pow = pow(x, y // 2)
        return half_pow * half_pow
    else:
        return x * pow(x, y - 1)

#Função para calcular logaritmo base 2 
def log_base_2(x):
    exponent = 0
    if x >= 1:
        while x >= 2:
            x /= 2
            exponent += 1
    else:
        while x < 1:
            x *= 2
            exponent -= 1
    return exponent

#Método de Horner para exponenciação fracionária
def horner(x):
    result = 1
    for i in range(10, 0, -1):
        result = 1 + x * result / i
    return result

# Função para calcular e^x usando o método de Bailey com o Método de Horner
def bailey_e_x(x):
    # Arredondar n para cima para o próximo inteiro
    n = np.ceil((x - ln2 / 2) / ln2)
    r = (x - n * ln2) / 256

    # Calcule e^r usando o Método de Horner
    e_elevado_r = horner(r)

    #Agora calcule 2^n e (e^r)^256 usando pow
    return pow(2, n) * pow(e_elevado_r, 256)

# Criar a LUT para e^k
def criar_LUT():
    lut = {2**(-i): np.exp(2**(-i)) for i in range(53)} #53 é o máximo de precisão alcançada
    return lut

lut = criar_LUT()

# Função para calcular e^x usando o método de Nice Number
def calculo_ex_usando_lut(x, lut):
    y = 1 
    
    while x > 0:
        # Encontrar o maior valor k na LUT tal que x - k >= 0
        keys = [k for k in lut.keys() if k <= x]
        if keys:
            max_k = max(keys)
            x -= max_k  # Atualiza x
            y *= lut[max_k]  # Atualiza y
        else:
            break

    # A correção (1 + x) é aplicada apenas se x for menor que o menor valor da LUT
    if x < min(lut.keys()):
        y *= (1 + x)  # Corrige o resultado com o resíduo de x

    return y


# Define o intervalo de valores de x para a raiz quadrada
x_valores_sqrt = np.arange(0.05, 5.05, 0.05)
# Define o intervalo de valores de x para o método de Bailey
x_valores_bailey = np.arange(0.05, 10.05, 0.05)
# Define o intervalo de valores de x para o método de Nice Number
x_valores_lut = np.arange(0.05, 10.05, 0.05)

# Inicializa vetores para armazenar os erros
erros_sqrt = []
erros_bailey_abs = []
erros_lut = []

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
    
# Calcula o erro para o método de Nice Number
for x in x_valores_lut:
    calculo_lut = calculo_ex_usando_lut(x, lut)
    real_exp = np.exp(x)
    erro_lut = abs(calculo_lut - real_exp)
    erros_lut.append(erro_lut)

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

# Gráfico para o erro do método de Nice Number
plt.figure(figsize=(12, 6))
plt.plot(x_valores_lut, erros_lut, label='Erro Método Nice Number', color='orange')
plt.title('Erro Absoluto entre o Método Nice Numbers e o Cálculo Padrão de e^x')
plt.xlabel('x')
plt.ylabel('Erro')
plt.grid(True)
plt.legend()
plt.show()