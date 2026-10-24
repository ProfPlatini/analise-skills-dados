# Matriz de Decisão: Escolha do Melhor Fornecedor

## 1. Contexto da Decisão
- **Decisão:** Selecionar o melhor fornecedor entre as 4 opções analisadas (`Alfa`, `Beta`, `Gama`, `Delta`) com base nos dados de `dados/fornecedores.csv`.
- **Alternativas avaliadas:** Alfa, Beta, Gama e Delta.

## 2. Critérios de Avaliação e Pesos
| # | Critério | Coluna de Origem | Tipo | Peso | Como é Medido (Escala 1-10) |
|---|----------|------------------|------|------|-----------------------------|
| 1 | Preço Unitário | `preco_unitario` | Menor é melhor | 30% | `10 * (Menor Preço / Preço do Fornecedor)` |
| 2 | Qualidade (Baixo Defeito) | `defeitos_pct` | Menor é melhor | 30% | `10 * (Menor Defeito / Defeito do Fornecedor)` |
| 3 | Prazo de Entrega | `prazo_dias` | Menor é melhor | 20% | `10 * (Menor Prazo / Prazo do Fornecedor)` |
| 4 | Suporte Técnico | `suporte_nota` | Maior é melhor | 20% | Nota direta da base (escala de 1 a 10) |

## 3. Dados Originais dos Fornecedores
| Fornecedor | Preço Unitário (R$) | Prazo (dias) | Defeitos (%) | Nota de Suporte |
|------------|---------------------|--------------|--------------|-----------------|
| Alfa | 90.00 | 8 | 2.0% | 8.0 |
| Beta | 100.00 | 5 | 1.0% | 9.0 |
| Gama | 85.00 | 12 | 4.0% | 6.0 |
| Delta | 110.00 | 4 | 0.5% | 9.5 |

## 4. Resultados da Matriz de Decisão (Notas 1-10 e Pontuação Ponderada)
| Posição | Fornecedor | Preço (30%) | Qualidade (30%) | Prazo (20%) | Suporte (20%) | **Total Ponderado** |
|---------|------------|-------------|-----------------|-------------|---------------|---------------------|
| 1º | **Delta** **(Vencedor)** | 7.73 (2.32) | 10.00 (3.00) | 10.00 (2.00) | 9.50 (1.90) | **9.22** |
| 2º | **Beta** | 8.50 (2.55) | 5.00 (1.50) | 8.00 (1.60) | 9.00 (1.80) | **7.45** |
| 3º | **Alfa** | 9.44 (2.83) | 2.50 (0.75) | 5.00 (1.00) | 8.00 (1.60) | **6.18** |
| 4º | **Gama** | 10.00 (3.00) | 1.25 (0.38) | 3.33 (0.67) | 6.00 (1.20) | **5.24** |

## 5. Análise de Sensibilidade
- **Margem de vitória:** O fornecedor **Delta** venceu o 2º colocado (**Beta**) com **9.22** contra **7.45** (diferença de **23.7%**).
- **Teste em diferentes cenários de prioridade:**
  - *Base (Equilibrado: 30% Preço, 30% Qualidade, 20% Prazo, 20% Suporte):* Vencedor = **Delta** (Nota: 9.22)
  - *Foco em Custo (50% Preço, 20% Qualidade, 15% Prazo, 15% Suporte):* Vencedor = **Delta** (Nota: 8.79)
  - *Foco em Qualidade e Prazo (15% Preço, 40% Qualidade, 30% Prazo, 15% Suporte):* Vencedor = **Delta** (Nota: 9.58)
  - *Pesos Iguais (25% para cada critério):* Vencedor = **Delta** (Nota: 9.31)

## 6. Recomendação Final
- **Fornecedor Recomendado:** **Delta** (Pontuação Total: **9.22 / 10**).
- **Justificativa:** O fornecedor **Delta** apresenta o menor prazo de entrega (4 dias), a menor taxa de defeitos (0.5%) e o melhor suporte (9.5), compensando com folga o preço unitário de R$ 110.00.
- **Trade-offs (Trocas):** Caso o orçamento seja extremamente restrito e o preço represente 50% ou mais da decisão sozinho, a disputa fica mais próxima, mas no cenário equilibrado e técnico o **Delta** é a escolha mais segura e robusta.
