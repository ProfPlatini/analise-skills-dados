import csv
import os
import matplotlib.pyplot as plt
import numpy as np

# Configuração global de estilo para qualidade de publicação (skill chart-image)
plt.rcParams.update({
    "font.sans-serif": "DejaVu Sans",
    "axes.edgecolor": "#333333",
    "axes.linewidth": 0.8,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.labelsize": 10,
    "xtick.labelsize": 9.5,
    "ytick.labelsize": 9.5,
    "legend.fontsize": 9,
    "figure.titlesize": 14,
})

# Paleta de cores com alto contraste e amigável para daltonismo (Okabe-Ito adaptada)
CORES_CRITERIOS = {
    "preco": "#0072B2",      # Azul escuro
    "qualidade": "#009E73",  # Verde azulado
    "prazo": "#D55E00",      # Laranja avermelhado
    "suporte": "#CC79A7",    # Roxo/Rosa
}

CORES_FORNECEDORES = {
    "Delta": "#009E73",  # Destaque para o 1º colocado
    "Beta": "#0072B2",
    "Alfa": "#E69F00",
    "Gama": "#7F7F7F",
}

FONTE_RODAPE = (
    "Fonte: dados/fornecedores.csv | Escala normalizada 1–10 (linha de base = 0) | "
    "Pesos base: Preço (30%), Qualidade/Defeitos (30%), Prazo (20%), Suporte (20%)"
)

# 1. Lendo os dados originais de dados/fornecedores.csv (sem alterar o arquivo original)
caminho_dados = os.path.join("dados", "fornecedores.csv")
fornecedores = []

with open(caminho_dados, mode="r", encoding="utf-8") as f:
    leitor = csv.DictReader(f)
    for linha in leitor:
        fornecedores.append({
            "fornecedor": linha["fornecedor"],
            "preco_unitario": float(linha["preco_unitario"]),
            "prazo_dias": float(linha["prazo_dias"]),
            "defeitos_pct": float(linha["defeitos_pct"]),
            "suporte_nota": float(linha["suporte_nota"]),
        })

# 2. Definindo pesos dos critérios (somando 100% = 1.0) conforme a skill decision-matrix
pesos = {
    "preco": 0.30,      # 30% - Preço Unitário (menor é melhor)
    "qualidade": 0.30,  # 30% - Taxa de Defeitos % (menor é melhor)
    "prazo": 0.20,      # 20% - Prazo em Dias (menor é melhor)
    "suporte": 0.20,    # 20% - Nota do Suporte (maior é melhor, já está em escala 1-10)
}

melhor_preco = min(f["preco_unitario"] for f in fornecedores)
melhor_prazo = min(f["prazo_dias"] for f in fornecedores)
melhor_defeito = min(f["defeitos_pct"] for f in fornecedores)

# 3. Calculando as notas (escala 1-10) e a nota final ponderada de cada fornecedor
for f in fornecedores:
    f["nota_preco"] = 10.0 * (melhor_preco / f["preco_unitario"])
    f["nota_prazo"] = 10.0 * (melhor_prazo / f["prazo_dias"])
    f["nota_qualidade"] = 10.0 * (melhor_defeito / f["defeitos_pct"])
    f["nota_suporte"] = f["suporte_nota"]

    f["pond_preco"] = f["nota_preco"] * pesos["preco"]
    f["pond_qualidade"] = f["nota_qualidade"] * pesos["qualidade"]
    f["pond_prazo"] = f["nota_prazo"] * pesos["prazo"]
    f["pond_suporte"] = f["nota_suporte"] * pesos["suporte"]

    f["nota_total"] = (
        f["pond_preco"]
        + f["pond_qualidade"]
        + f["pond_prazo"]
        + f["pond_suporte"]
    )

# Ordenando do maior para o menor score
ranking = sorted(fornecedores, key=lambda x: x["nota_total"], reverse=True)
vencedor = ranking[0]
segundo = ranking[1]
margem_pct = ((vencedor["nota_total"] - segundo["nota_total"]) / segundo["nota_total"]) * 100

# Cenários de sensibilidade
cenarios = {
    "Base Equilibrado\n(30/30/20/20)": (0.30, 0.30, 0.20, 0.20),
    "Foco em Custo\n(50/20/15/15)": (0.50, 0.20, 0.15, 0.15),
    "Foco em Qualidade\ne Prazo (15/40/30/15)": (0.15, 0.40, 0.30, 0.15),
    "Pesos Iguais\n(25/25/25/25)": (0.25, 0.25, 0.25, 0.25),
}

os.makedirs("resultados", exist_ok=True)

# ==============================================================================
# GRÁFICO 1 (MELHORADO): analise_fornecedores.png
# Pontuação Ponderada Empilhada + Notas Individuais por Critério (com rótulos e QA)
# ==============================================================================
caminho_grafico_1 = os.path.join("resultados", "analise_fornecedores.png")

nomes = [f["fornecedor"] for f in ranking]
p_preco = np.array([f["pond_preco"] for f in ranking])
p_qual = np.array([f["pond_qualidade"] for f in ranking])
p_prazo = np.array([f["pond_prazo"] for f in ranking])
p_sup = np.array([f["pond_suporte"] for f in ranking])
totais = np.array([f["nota_total"] for f in ranking])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.8))
fig.subplots_adjust(top=0.84, bottom=0.14, wspace=0.22)

x = np.arange(len(nomes))

# Subplot 1: Barras empilhadas com valores internos e total no topo
ax1.bar(x, p_preco, width=0.55, label="Preço Unitário (peso 30%)", color=CORES_CRITERIOS["preco"])
ax1.bar(x, p_qual, width=0.55, bottom=p_preco, label="Qualidade / Baixo Defeito (peso 30%)", color=CORES_CRITERIOS["qualidade"])
ax1.bar(x, p_prazo, width=0.55, bottom=p_preco + p_qual, label="Prazo de Entrega (peso 20%)", color=CORES_CRITERIOS["prazo"])
ax1.bar(x, p_sup, width=0.55, bottom=p_preco + p_qual + p_prazo, label="Suporte Técnico (peso 20%)", color=CORES_CRITERIOS["suporte"])

acumulados = [
    (p_preco, np.zeros_like(p_preco)),
    (p_qual, p_preco),
    (p_prazo, p_preco + p_qual),
    (p_sup, p_preco + p_qual + p_prazo),
]
for valores, base in acumulados:
    for i, (val, b) in enumerate(zip(valores, base)):
        if val >= 0.55:
            ax1.text(
                i, b + val / 2, f"{val:.2f}",
                ha="center", va="center", color="white", fontsize=8.5, fontweight="bold"
            )

for i, total in enumerate(totais):
    destaque = " ★ 1º" if i == 0 else f" ({i+1}º)"
    ax1.text(
        i, total + 0.22, f"{total:.2f}{destaque}",
        ha="center", va="bottom", fontweight="bold", fontsize=10, color="#111111"
    )

media_total = float(np.mean(totais))
ax1.axhline(media_total, color="#444444", linestyle="--", linewidth=1.1, label=f"Média geral ({media_total:.2f} pts)")

ax1.set_title("A) Pontuação Final Ponderada (Escala 0–10 pontos)")
ax1.set_xticks(x)
ax1.set_xticklabels([f"Fornecedor {n}" for n in nomes])
ax1.set_ylabel("Pontuação Ponderada Total (pontos)")
ax1.set_ylim(0, 11.4)
ax1.grid(axis="y", linestyle=":", alpha=0.6)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.legend(loc="upper right", frameon=True, facecolor="white", framealpha=0.95)

# Subplot 2: Notas brutas normalizadas (1 a 10) por critério
largura = 0.19
deslocamentos = [-1.5 * largura, -0.5 * largura, 0.5 * largura, 1.5 * largura]
series_notas = [
    ([f["nota_preco"] for f in ranking], "Preço (1–10)", CORES_CRITERIOS["preco"]),
    ([f["nota_qualidade"] for f in ranking], "Qualidade (1–10)", CORES_CRITERIOS["qualidade"]),
    ([f["nota_prazo"] for f in ranking], "Prazo (1–10)", CORES_CRITERIOS["prazo"]),
    ([f["nota_suporte"] for f in ranking], "Suporte (1–10)", CORES_CRITERIOS["suporte"]),
]

for desl, (valores_nota, rotulo, cor) in zip(deslocamentos, series_notas):
    barras = ax2.bar(x + desl, valores_nota, width=largura, label=rotulo, color=cor)
    for barra in barras:
        altura = barra.get_height()
        ax2.text(
            barra.get_x() + barra.get_width() / 2,
            altura + 0.15,
            f"{altura:.1f}",
            ha="center", va="bottom", fontsize=7.5, color="#222222"
        )

ax2.set_title("B) Notas Padronizadas por Critério (Escala 0–10)")
ax2.set_xticks(x)
ax2.set_xticklabels([f"Fornecedor {n}" for n in nomes])
ax2.set_ylabel("Nota Padronizada (10 = melhor desempenho)")
ax2.set_ylim(0, 12.2)
ax2.grid(axis="y", linestyle=":", alpha=0.6)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.legend(loc="upper right", ncol=2, frameon=True, facecolor="white", framealpha=0.95)

fig.suptitle(
    "Matriz de Decisão: Desempenho Global e por Critério dos 4 Fornecedores",
    fontsize=14, fontweight="bold", y=0.96
)
fig.text(0.5, 0.91, "Delta lidera com 9,22 pontos (+23,7% acima do 2º colocado Beta), vencendo em Qualidade, Prazo e Suporte", ha="center", fontsize=10.5, color="#333333")
fig.text(0.5, 0.02, FONTE_RODAPE, ha="center", fontsize=8.5, color="#555555", style="italic")

plt.savefig(caminho_grafico_1, dpi=200)
plt.close()

# ==============================================================================
# GRÁFICO 2 (NOVO): metricas_originais_fornecedores.png
# Painel 2x2 com os dados originais e suas unidades reais (R$, dias, %, nota)
# ==============================================================================
caminho_grafico_2 = os.path.join("resultados", "metricas_originais_fornecedores.png")

fig, eixos = plt.subplots(2, 2, figsize=(13.5, 8.5))
fig.subplots_adjust(top=0.85, bottom=0.10, hspace=0.38, wspace=0.25)

painel_cfg = [
    (eixos[0, 0], "preco_unitario", "1. Preço Unitário (R\\$) — Menor é melhor", "Preço (R\\$ / unidade)", "R\\$ {:.2f}", min, 130),
    (eixos[0, 1], "defeitos_pct", "2. Taxa de Defeitos (%) — Menor é melhor", "Defeitos (% dos lotes)", "{:.1f}%", min, 4.8),
    (eixos[1, 0], "prazo_dias", "3. Prazo de Entrega (dias) — Menor é melhor", "Tempo de Entrega (dias)", "{:.0f} dias", min, 14.5),
    (eixos[1, 1], "suporte_nota", "4. Avaliação do Suporte (0–10) — Maior é melhor", "Nota de Suporte (pontos)", "{:.1f} / 10", max, 11.5),
]

for ax, chave, titulo, ylabel, formato, func_melhor, limite_y in painel_cfg:
    valores = [f[chave] for f in ranking]
    melhor_val = func_melhor(valores)
    cores_barras = ["#009E73" if v == melhor_val else "#8C969E" for v in valores]

    barras = ax.bar(nomes, valores, width=0.5, color=cores_barras, edgecolor="#222222", linewidth=0.7)
    for barra, val in zip(barras, valores):
        destaque_txt = " (Melhor)" if val == melhor_val else ""
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            val + (limite_y * 0.025),
            formato.format(val) + destaque_txt,
            ha="center", va="bottom", fontsize=9,
            fontweight="bold" if val == melhor_val else "normal",
            color="#006644" if val == melhor_val else "#222222",
        )

    ax.set_title(titulo)
    ax.set_ylabel(ylabel)
    ax.set_ylim(0, limite_y)
    ax.grid(axis="y", linestyle=":", alpha=0.6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

fig.suptitle(
    "Indicadores Originais dos Fornecedores (Unidades Físicas e Financeiras Reais)",
    fontsize=14, fontweight="bold", y=0.96
)
fig.text(
    0.5, 0.91,
    "Barras em verde indicam o melhor desempenho em cada métrica bruta (Gama tem menor preço; Delta lidera nos demais)",
    ha="center", fontsize=10.5, color="#333333"
)
fig.text(
    0.5, 0.02,
    "Fonte: dados/fornecedores.csv | Eixos quantitativos iniciados na linha de base zero (0) sem truncamento.",
    ha="center", fontsize=8.5, color="#555555", style="italic"
)

plt.savefig(caminho_grafico_2, dpi=200)
plt.close()

# ==============================================================================
# GRÁFICO 3 (NOVO): custo_vs_qualidade_fornecedores.png
# Análise de Trade-off: Preço Unitário (R$) vs Pontuação Total (0–10)
# ==============================================================================
caminho_grafico_3 = os.path.join("resultados", "custo_vs_qualidade_fornecedores.png")

fig, ax = plt.subplots(figsize=(10.5, 6.5))
fig.subplots_adjust(top=0.83, bottom=0.15, left=0.10, right=0.95)

offsets_anotacao = {
    "Delta": (0, 0.85),
    "Beta": (0, 0.85),
    "Alfa": (0, 0.85),
    "Gama": (0, -0.95),
}

for f in ranking:
    nome = f["fornecedor"]
    preco = f["preco_unitario"]
    score = f["nota_total"]
    cor = CORES_FORNECEDORES[nome]
    tamanho = f["suporte_nota"] * 50

    ax.scatter(
        preco, score, s=tamanho, color=cor, alpha=0.9,
        edgecolors="#111111", linewidth=1.5, zorder=4,
        label=f"{nome}: R\\$ {preco:.0f} | Score {score:.2f} | Defeitos {f['defeitos_pct']}%"
    )

    dx, dy = offsets_anotacao[nome]
    ax.annotate(
        f"{nome} ({score:.2f} pts)\nPrazo: {int(f['prazo_dias'])}d | Defeitos: {f['defeitos_pct']}% | Suporte: {f['suporte_nota']}",
        xy=(preco, score),
        xytext=(preco + dx, score + dy),
        ha="center", va="center",
        fontsize=8.5, fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=cor, lw=1.0, shrinkA=0, shrinkB=6),
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=cor, alpha=0.95),
        zorder=5
    )

ax.set_title("Trade-off Custo vs. Desempenho Global (Preço em R\\$ vs. Pontuação Ponderada)")
ax.set_xlabel("Preço Unitário (R\\$ / unidade) — Valores menores à esquerda são mais econômicos")
ax.set_ylabel("Pontuação Final Ponderada (Escala 0 a 10 pontos)")
ax.set_xlim(78, 118)
ax.set_ylim(0, 11.2)
ax.grid(True, linestyle=":", alpha=0.6)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(
    loc="lower right", title="Resumo por Fornecedor (tamanho = Suporte)",
    frameon=True, facecolor="white", markerscale=0.45, labelspacing=0.6
)

fig.suptitle(
    "Análise de Custo-Benefício: Onde cada Fornecedor se Posiciona",
    fontsize=14, fontweight="bold", y=0.96
)
fig.text(
    0.5, 0.90,
    "Nota de integridade visual: Eixo X exibido na faixa de R\\$ 78 a R\\$ 118 para destacar as diferenças de preço; Eixo Y inicia em 0.",
    ha="center", fontsize=9.5, color="#333333"
)
fig.text(0.5, 0.02, FONTE_RODAPE, ha="center", fontsize=8.5, color="#555555", style="italic")

plt.savefig(caminho_grafico_3, dpi=200)
plt.close()

# ==============================================================================
# GRÁFICO 4 (NOVO): sensibilidade_cenarios_fornecedores.png
# Comparação da pontuação de todos os fornecedores em 4 cenários de pesos
# ==============================================================================
caminho_grafico_4 = os.path.join("resultados", "sensibilidade_cenarios_fornecedores.png")

fig, ax = plt.subplots(figsize=(12.5, 6.5))
fig.subplots_adjust(top=0.83, bottom=0.16, left=0.08, right=0.96)

nomes_cenarios = list(cenarios.keys())
x_cen = np.arange(len(nomes_cenarios))
largura_cen = 0.19
desl_cen = [-1.5 * largura_cen, -0.5 * largura_cen, 0.5 * largura_cen, 1.5 * largura_cen]

for desl, f in zip(desl_cen, ranking):
    nome = f["fornecedor"]
    scores_cenario = []
    for _, (p_pr, p_qu, p_pz, p_su) in cenarios.items():
        sc = (
            f["nota_preco"] * p_pr
            + f["nota_qualidade"] * p_qu
            + f["nota_prazo"] * p_pz
            + f["nota_suporte"] * p_su
        )
        scores_cenario.append(sc)

    barras = ax.bar(
        x_cen + desl, scores_cenario, width=largura_cen,
        label=f"Fornecedor {nome}", color=CORES_FORNECEDORES[nome],
        edgecolor="#222222", linewidth=0.6
    )
    for barra in barras:
        alt = barra.get_height()
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            alt + 0.15,
            f"{alt:.2f}",
            ha="center", va="bottom", fontsize=8.5,
            fontweight="bold" if nome == "Delta" else "normal"
        )

ax.set_title("Simulação de Sensibilidade: Pontuação Total sob Diferentes Prioridades de Negócio")
ax.set_xticks(x_cen)
ax.set_xticklabels(nomes_cenarios)
ax.set_ylabel("Pontuação Ponderada Total (Escala 0 a 10)")
ax.set_ylim(0, 11.2)
ax.grid(axis="y", linestyle=":", alpha=0.6)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(loc="upper right", ncol=4, frameon=True, facecolor="white")

fig.suptitle(
    "Análise de Robustez (Sensibilidade): Delta Vence em Todos os Cenários Testados",
    fontsize=14, fontweight="bold", y=0.96
)
fig.text(
    0.5, 0.90,
    "Mesmo quando o peso do Preço sobe para 50% (Foco em Custo), Delta mantém a liderança (8,79 pts contra 7,80 de Beta e 7,17 de Alfa)",
    ha="center", fontsize=10, color="#333333"
)
fig.text(
    0.5, 0.02,
    "Fonte: dados/fornecedores.csv | Pesos entre parênteses indicam (Preço% / Qualidade% / Prazo% / Suporte%). Eixo Y inicia em 0.",
    ha="center", fontsize=8.5, color="#555555", style="italic"
)

plt.savefig(caminho_grafico_4, dpi=200)
plt.close()

print("Gráficos gerados e revisados com sucesso na pasta resultados/:")
print(f"1. {caminho_grafico_1} (melhorado)")
print(f"2. {caminho_grafico_2} (novo)")
print(f"3. {caminho_grafico_3} (novo)")
print(f"4. {caminho_grafico_4} (novo)")
