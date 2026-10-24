import os
import matplotlib.pyplot as plt

# Pontos conhecidos: (x1, y1) = (0, 4) e (x2, y2) = (100, 20)
x1, y1 = 0, 4
x2, y2 = 100, 20

# Calculando o coeficiente 'a' (inclinação da reta)
a = (y2 - y1) / (x2 - x1)

# Calculando o coeficiente 'b' (valor de y quando x é 0)
b = y1 - (a * x1)

# Calculando o valor de y (corrente em mA) para x = 50 graus
x = 50
y = (a * x) + b

print(f"Valor de A: {a}")
print(f"Valor de B: {b}")
print(f"Para a temperatura x = {x} °C, a corrente y é: {y} mA")

# 1. Avisos de limites (temperatura fora de 0-100 °C e corrente fora de 4-20 mA)
if x < 0 or x > 100:
    print("AVISO: A temperatura está fora da faixa de 0 a 100 °C!")

if y < 4 or y > 20:
    print("AVISO: A corrente elétrica está fora da faixa de 4 a 20 mA!")

# 2. Classificação da temperatura
if x <= 30:
    classificacao = "Baixa"
elif x <= 60:
    classificacao = "Média"
else:
    classificacao = "Alta"

print(f"Classificação da temperatura: {classificacao}")

# 3. Gráfico com Matplotlib (Temperatura no eixo X e Corrente no eixo Y)
os.makedirs("resultados", exist_ok=True)
caminho_grafico = os.path.join("resultados", "grafico_termometro.png")

temperaturas = [x1, x, x2]
correntes = [y1, y, y2]

plt.figure(figsize=(8, 5))
plt.plot([x1, x2], [y1, y2], label="Reta (y = ax + b)", color="blue")
plt.scatter([x], [y], color="red", zorder=5, label=f"Ponto ({x} °C, {y} mA)")

plt.title("Termômetro: Temperatura vs Corrente Elétrica")
plt.xlabel("Temperatura (°C)")
plt.ylabel("Corrente Elétrica (mA)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()

# Salvando na pasta resultados/ conforme os combinados
plt.savefig(caminho_grafico)
plt.close()

print(f"Gráfico salvo em: {caminho_grafico}")

