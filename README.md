# projeto_cpi_economy
# 🌍 A Geografia da Honestidade: Análise Global de Corrupção

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Status](https://img.shields.io/badge/Status-Concluído-success)

> "O dinheiro compra honestidade? Ou a liberdade de imprensa é o verdadeiro antídoto contra a corrupção?"

## 📌 Sobre o Projeto

Este projeto de Ciência de Dados investiga a relação entre fatores socioeconômicos (PIB, IDH) e políticos (Liberdade de Imprensa) com o **Índice de Percepção da Corrupção (CPI)** em mais de 180 países.

O objetivo foi ir além da análise descritiva, criando um **Pipeline de Dados (ETL)**, aplicando **Machine Learning (K-Means)** para segmentação de países e disponibilizando tudo em um **Dashboard Interativo**.

## 🚀 Funcionalidades e Features

* **ETL Automatizado:** Tratamento de dados de múltiplas fontes (CSV, APIs), limpeza de nulos e padronização de nomes de países.
* **Análise Exploratória (EDA):** Correlações entre riqueza e honestidade, e o impacto da mídia na transparência.
* **Machine Learning (Clustering):** Algoritmo **K-Means** para agrupar países em "clubes" (ex: *Zona de Risco*, *Em Transição*, *Elite Global*) sem viés humano.
* **Análise Temporal:** Acompanhamento da evolução histórica do Brasil e comparativo com a média global.
* **Dashboard Web:** Aplicação interativa construída com **Streamlit**.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.12
* **Gerenciador de Pacotes:** [uv](https://github.com/astral-sh/uv) (para alta performance)
* **Análise de Dados:** Pandas, NumPy
* **Visualização:** Plotly Express, Plotly Graph Objects
* **Machine Learning:** Scikit-learn (K-Means, StandardScaler)
* **Web App:** Streamlit

## 📊 Principais Insights & Storytelling

A análise revelou que a corrupção não é um problema isolado, mas sistêmico. Abaixo, os 5 principais achados baseados nos dados:

### 1. O "Paradoxo da Riqueza" (Correlação GDP vs CPI)
Existe uma correlação positiva forte (**Pearson > 0.7**) entre PIB per Capita e Honestidade.
* **A Regra:** Países ricos tendem a ser mais transparentes devido a instituições mais fortes.
* **A Exceção (Outliers):** Identificamos países com alta renda (ex: petroleiros ou paraísos fiscais) que mantêm índices de corrupção elevados, provando que **riqueza econômica sem accountability não gera transparência**.

### 2. O Quarto Poder: A Influência da Mídia
A variável *Freedom of Press* demonstrou ser um dos preditores mais confiáveis para a corrupção.
* **Insight:** Não existem países no "Quadrante de Ouro" (Baixa Corrupção) que não tenham também uma Imprensa Livre. Isso sugere que a fiscalização jornalística é um pré-requisito obrigatório para a integridade pública.

### 3. Clustering: Os "Três Mundos" da Corrupção
O algoritmo **K-Means** (não-supervisionado) identificou automaticamente 3 clusters globais distintos, sem intervenção humana:
* 🔴 **Zona de Risco:** Baixa renda, alta censura e corrupção sistêmica (Majoritariamente África Subsaariana e zonas de conflito).
* 🟡 **A Armadilha da Renda Média (Cluster do Brasil):** Países em desenvolvimento, democracias imperfeitas e estagnação nos índices de transparência.
* 🔵 **A Elite Institucional:** Alta renda, plena liberdade de imprensa e baixíssima tolerância à corrupção (Escandinávia, Nova Zelândia, Cingapura).

### 4. A Geografia da Honestidade
A análise geoespacial revelou um forte componente de "contágio regional".
* Vizinhos tendem a ter notas similares, sugerindo que a corrupção (ou a integridade) transcende fronteiras nacionais e se torna cultural/regional. A América do Sul, por exemplo, apresenta uma média inferior à Europa Ocidental, mas superior a outras regiões em desenvolvimento.

### 5. O Caso Brasil 🇧🇷
* **Posição Relativa:** O Brasil encontra-se no cluster de "Transição".
* **Análise de Resíduos:** Ao cruzar PIB vs CPI, o Brasil apresenta uma performance ligeiramente abaixo do esperado para o tamanho de sua economia. Isso indica que nossas instituições entregam menos transparência do que nossa riqueza teórica permitiria.

## 📂 Estrutura do Projeto

```text
├── app.py                 # O Dashboard interativo (Streamlit)
├── notebooks/             # Jupyter Notebooks com as análises passo-a-passo
│   ├── 01_extracao.ipynb
│   ├── ...
│   └── 08_analise_temporal.ipynb
├── datasets/              # Arquivos CSV processados e prontos para uso
├── requirements.txt       # Lista de dependências do projeto
└── README.md              # Documentação


