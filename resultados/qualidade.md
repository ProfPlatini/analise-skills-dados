# Relatório de Qualidade e Tratamento dos Dados (`conferir-csv`)

## 1. Identificação do Arquivo e Finalidade
- **Arquivo original analisado:** `dados\fornecedores_erro.csv` (mantido intacto, sem alterações).
- **Arquivo tratado gerado:** `resultados\fornecedores_tratado.csv`.
- **Finalidade da análise:** Avaliação comparativa de fornecedores.
- **O que cada linha representa:** Cada linha representa um fornecedor avaliado (`Alfa`, `Beta`, `Gama`, `Delta`).
- **Separador identificado:** Vírgula (`,`).

## 2. Estrutura Geral (Calculada via Código)
- **Quantidade de linhas de dados:** 4 linhas (além de 1 linha de cabeçalho).
- **Quantidade de colunas:** 5 colunas.
- **Linhas duplicadas:** 0.
- **Total de valores ausentes encontrados no original:** 2.
- **Total de valores inválidos/fora de sentido:** 0.

## 3. Regra de Tratamento Aplicada (Média dos Anteriores)
Conforme solicitado, os valores ausentes foram preenchidos em um novo arquivo (`resultados/fornecedores_tratado.csv`) usando a **média aritmética das linhas anteriores** daquela mesma coluna:

| Linha | Fornecedor | Coluna Preenchida | Valores Anteriores na Coluna | Média dos Anteriores (Valor Aplicado) | Média de Toda a Coluna (Referência) |
|-------|------------|-------------------|------------------------------|---------------------------------------|-------------------------------------|
| 5 | **Delta** | `preco_unitario` | `90.0, 100.0, 85.0` | **91.67** | 91.67 |
| 3 | **Beta** | `suporte_nota` | `8.0` | **8.00** | 7.83 |

## 4. Tabela Final Tratada (`resultados/fornecedores_tratado.csv`)
| fornecedor | preco_unitario | prazo_dias | defeitos_pct | suporte_nota |
|------------|----------------|------------|--------------|--------------|
| Alfa | 90 | 8 | 2 | 8 |
| Beta | 100 | 5 | 1 | 8 |
| Gama | 85 | 12 | 4 | 6 |
| Delta | 91.67 | 4 | 0.5 | 9.5 |
