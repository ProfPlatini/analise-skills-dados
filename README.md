# Análise de Dados com Skills no Antigravity

Repositório desenvolvido em aula prática utilizando **Python**, **Regras de Projeto (`AGENTS.md`)** e **Skills personalizadas (`.agents/skills/`)** para análise de dados, matriz de decisão, visualização gráfica e auditoria de qualidade de arquivos CSV.

---

## Estrutura do Projeto

```text
├── .agents/skills/          # Skills do projeto
│   ├── chart-image/         # Criação de gráficos com qualidade de publicação e revisão visual
│   ├── conferir-csv/        # Auditoria de estrutura e qualidade de bases CSV
│   └── decision-matrix/     # Matriz de decisão ponderada e análise de sensibilidade
├── dados/                   # Dados brutos originais (intactos)
│   ├── fornecedores.csv
│   └── fornecedores_erro.csv
├── resultados/              # Gráficos, relatórios e bases tratadas gerados pelos scripts
│   ├── analise_fornecedores.png
│   ├── custo_vs_qualidade_fornecedores.png
│   ├── fornecedores_tratado.csv
│   ├── grafico_termometro.png
│   ├── metricas_originais_fornecedores.png
│   ├── qualidade.md
│   ├── relatorio_fornecedores.md
│   └── sensibilidade_cenarios_fornecedores.png
├── AGENTS.md                # Combinados e regras de trabalho do agente
├── termometro.py            # Equação linear (y = ax + b), alertas de faixa (4–20 mA / 0–100 °C) e gráfico
├── forncedores.py           # Matriz de decisão dos 4 fornecedores e geração de 4 gráficos analíticos
└── conferir_csv.py          # Auditoria de qualidade de CSV e preenchimento de dados ausentes
```

---

## Etapas Desenvolvidas

### 1. Calibração de Termômetro (`termometro.py`)
- Cálculo dos coeficientes $a = 0,16$ e $b = 4,0$ da equação da reta ($y = ax + b$) a partir dos pontos $(0, 4)$ e $(100, 20)$.
- Cálculo da corrente elétrica para $x = 50\text{ °C}$ ($y = 12,0\text{ mA}$).
- Avisos automáticos para valores fora da escala de $0\text{ a }100\text{ °C}$ ou $4\text{ a }20\text{ mA}$ e classificação de temperatura (`Baixa`, `Média`, `Alta`).
- Geração do gráfico em `resultados/grafico_termometro.png`.

### 2. Matriz de Decisão de Fornecedores (`forncedores.py`)
- Uso da skill **`decision-matrix`** sobre a base `dados/fornecedores.csv` para comparar os fornecedores **Alfa**, **Beta**, **Gama** e **Delta**.
- Critérios ponderados: Preço Unitário (30%), Qualidade/Defeitos (30%), Prazo de Entrega (20%) e Suporte Técnico (20%).
- **Fornecedor Vencedor:** **Delta** com pontuação **9,22 / 10** (liderando também em todos os cenários da análise de sensibilidade).
- Relatório completo salvo em `resultados/relatorio_fornecedores.md`.

### 3. Visualização Avançada (`chart-image`)
- Uso da skill **`chart-image`** para criar e refinar 4 visualizações em `resultados/`:
  - `analise_fornecedores.png` (pontuação ponderada empilhada e notas por critério)
  - `metricas_originais_fornecedores.png` (indicadores originais em R$, %, dias e nota)
  - `custo_vs_qualidade_fornecedores.png` (análise de *trade-off* custo vs. benefício)
  - `sensibilidade_cenarios_fornecedores.png` (simulação em 4 cenários de pesos)

### 4. Qualidade e Tratamento de Dados (`conferir_csv.py`)
- Uso da skill **`conferir-csv`** na base `dados/fornecedores_erro.csv`.
- Identificação de 2 valores ausentes (`suporte_nota` na linha do fornecedor **Beta** e `preco_unitario` na linha do fornecedor **Delta**).
- Preenchimento dos valores faltantes com a média dos valores anteriores na coluna, gerando `resultados/fornecedores_tratado.csv` e documentando tudo em `resultados/qualidade.md` sem alterar o arquivo original.

---

## Como Executar

1. Crie o ambiente virtual e instale as dependências:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\pip install matplotlib numpy
   ```
2. Execute os scripts utilizando o Python da `.venv`:
   ```powershell
   .\.venv\Scripts\python termometro.py
   .\.venv\Scripts\python forncedores.py
   .\.venv\Scripts\python conferir_csv.py
   ```
