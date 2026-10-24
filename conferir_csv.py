import csv
import os

caminho_arquivo = os.path.join("dados", "fornecedores_erro.csv")

# 1. Descobrir separador e ler todas as linhas brutas (sem alterar o arquivo original)
with open(caminho_arquivo, mode="r", encoding="utf-8") as f:
    conteudo = f.read()
    linhas_brutas = [linha for linha in conteudo.splitlines() if linha.strip() != ""]

cabecalho_bruto = linhas_brutas[0]
separador = "," if "," in cabecalho_bruto else ";"

with open(caminho_arquivo, mode="r", encoding="utf-8") as f:
    leitor = csv.reader(f, delimiter=separador)
    todas_linhas = list(leitor)

colunas = todas_linhas[0]
dados = [ list(linha) for linha in todas_linhas[1:] ]

qtd_linhas = len(dados)
qtd_colunas = len(colunas)

# 2. Verificar linhas duplicadas
tuplas_dados = [tuple(linha) for linha in dados]
qtd_duplicadas = len(tuplas_dados) - len(set(tuplas_dados))

# 3. Verificar tipos, valores ausentes e preparar preenchimento com a média dos anteriores
colunas_numericas_esperadas = {
    "preco_unitario": {"min": 0.01, "max": None, "descricao": "Preço unitário em R$ (deve ser > 0)"},
    "prazo_dias": {"min": 1, "max": None, "descricao": "Prazo em dias (deve ser > 0)"},
    "defeitos_pct": {"min": 0.0, "max": 100.0, "descricao": "Percentual de defeitos (0% a 100%)"},
    "suporte_nota": {"min": 0.0, "max": 10.0, "descricao": "Nota de suporte (0 a 10)"},
}

ausentes_por_coluna = {col: [] for col in colunas}
problemas_tipo_ou_faixa = {col: [] for col in colunas}
tipos_detectados = {}

# Cópia dos dados para gerar o arquivo tratado em resultados/ sem tocar no original
dados_tratados = [list(linha) for linha in dados]
registro_preenchimentos = []

for idx_col, col in enumerate(colunas):
    valores_anteriores = []
    # Coletar também todos os valores válidos da coluna para referência
    todos_validos_coluna = [
        float(linha[idx_col])
        for linha in dados
        if idx_col < len(linha) and linha[idx_col].strip() != "" and col in colunas_numericas_esperadas
    ]

    for idx_pos, linha in enumerate(dados):
        idx_linha_csv = idx_pos + 2  # Linha 2 em diante no arquivo CSV
        valor = linha[idx_col] if idx_col < len(linha) else ""
        fornecedor_linha = linha[0] if len(linha) > 0 else f"Linha {idx_linha_csv}"

        if valor.strip() == "":
            ausentes_por_coluna[col].append((idx_linha_csv, fornecedor_linha))
            # Regra: Preencher com a média dos valores anteriores na coluna
            if col in colunas_numericas_esperadas and len(valores_anteriores) > 0:
                media_anteriores = sum(valores_anteriores) / len(valores_anteriores)
                media_todos = sum(todos_validos_coluna) / len(todos_validos_coluna)
                dados_tratados[idx_pos][idx_col] = f"{media_anteriores:.2f}".rstrip("0").rstrip(".")
                registro_preenchimentos.append({
                    "linha": idx_linha_csv,
                    "fornecedor": fornecedor_linha,
                    "coluna": col,
                    "valores_anteriores": list(valores_anteriores),
                    "media_anteriores": media_anteriores,
                    "media_todos_coluna": media_todos,
                })
            continue

        if col in colunas_numericas_esperadas:
            try:
                num = float(valor)
                valores_anteriores.append(num)
                regras = colunas_numericas_esperadas[col]
                if regras["min"] is not None and num < regras["min"]:
                    problemas_tipo_ou_faixa[col].append(
                        f"Linha {idx_linha_csv} ({fornecedor_linha}): valor {num} abaixo do mínimo ({regras['min']})"
                    )
                if regras["max"] is not None and num > regras["max"]:
                    problemas_tipo_ou_faixa[col].append(
                        f"Linha {idx_linha_csv} ({fornecedor_linha}): valor {num} acima do máximo ({regras['max']})"
                    )
            except ValueError:
                problemas_tipo_ou_faixa[col].append(
                    f"Linha {idx_linha_csv} ({fornecedor_linha}): texto '{valor}' encontrado onde deveria ser número"
                )

    if col in colunas_numericas_esperadas:
        tipos_detectados[col] = "Numérico (float/int)"
    else:
        tipos_detectados[col] = "Texto (string - identificador/categoria)"

total_ausentes = sum(len(lista) for lista in ausentes_por_coluna.values())
total_problemas_faixa = sum(len(lista) for lista in problemas_tipo_ou_faixa.values())

# 4. Salvar o novo CSV preenchido em resultados/fornecedores_tratado.csv
os.makedirs("resultados", exist_ok=True)
caminho_csv_tratado = os.path.join("resultados", "fornecedores_tratado.csv")

with open(caminho_csv_tratado, mode="w", encoding="utf-8", newline="") as f:
    escritor = csv.writer(f, delimiter=separador)
    escritor.writerow(colunas)
    escritor.writerows(dados_tratados)

# 5. Exibir resultados e cálculos no terminal
print("=== PREENCHIMENTO DE VALORES FALTANTES (MÉDIA DOS ANTERIORES) ===")
for item in registro_preenchimentos:
    print(
        f"- Fornecedor {item['fornecedor']} (Linha {item['linha']}), coluna '{item['coluna']}':\n"
        f"  Valores anteriores usados: {item['valores_anteriores']}\n"
        f"  Média dos anteriores aplicada: {item['media_anteriores']:.2f} "
        f"(Ref. média de toda a coluna: {item['media_todos_coluna']:.2f})"
    )
print(f"\nArquivo tratado salvo em: {caminho_csv_tratado}")

# 6. Atualizar o resumo em resultados/qualidade.md
caminho_relatorio = os.path.join("resultados", "qualidade.md")

linhas_md = [
    "# Relatório de Qualidade e Tratamento dos Dados (`conferir-csv`)",
    "",
    "## 1. Identificação do Arquivo e Finalidade",
    f"- **Arquivo original analisado:** `{caminho_arquivo}` (mantido intacto, sem alterações).",
    f"- **Arquivo tratado gerado:** `{caminho_csv_tratado}`.",
    "- **Finalidade da análise:** Avaliação comparativa de fornecedores.",
    "- **O que cada linha representa:** Cada linha representa um fornecedor avaliado (`Alfa`, `Beta`, `Gama`, `Delta`).",
    f"- **Separador identificado:** Vírgula (`{separador}`).",
    "",
    "## 2. Estrutura Geral (Calculada via Código)",
    f"- **Quantidade de linhas de dados:** {qtd_linhas} linhas (além de 1 linha de cabeçalho).",
    f"- **Quantidade de colunas:** {qtd_colunas} colunas.",
    f"- **Linhas duplicadas:** {qtd_duplicadas}.",
    f"- **Total de valores ausentes encontrados no original:** {total_ausentes}.",
    f"- **Total de valores inválidos/fora de sentido:** {total_problemas_faixa}.",
    "",
    "## 3. Regra de Tratamento Aplicada (Média dos Anteriores)",
    "Conforme solicitado, os valores ausentes foram preenchidos em um novo arquivo (`resultados/fornecedores_tratado.csv`) usando a **média aritmética das linhas anteriores** daquela mesma coluna:",
    "",
    "| Linha | Fornecedor | Coluna Preenchida | Valores Anteriores na Coluna | Média dos Anteriores (Valor Aplicado) | Média de Toda a Coluna (Referência) |",
    "|-------|------------|-------------------|------------------------------|---------------------------------------|-------------------------------------|",
]

for item in registro_preenchimentos:
    vals_str = ", ".join(str(v) for v in item["valores_anteriores"])
    linhas_md.append(
        f"| {item['linha']} | **{item['fornecedor']}** | `{item['coluna']}` | `{vals_str}` | **{item['media_anteriores']:.2f}** | {item['media_todos_coluna']:.2f} |"
    )

linhas_md.extend([
    "",
    "## 4. Tabela Final Tratada (`resultados/fornecedores_tratado.csv`)",
    "| fornecedor | preco_unitario | prazo_dias | defeitos_pct | suporte_nota |",
    "|------------|----------------|------------|--------------|--------------|",
])

for linha in dados_tratados:
    linhas_md.append(f"| {linha[0]} | {linha[1]} | {linha[2]} | {linha[3]} | {linha[4]} |")

with open(caminho_relatorio, mode="w", encoding="utf-8") as f:
    f.write("\n".join(linhas_md) + "\n")

print(f"Relatório atualizado em: {caminho_relatorio}")
