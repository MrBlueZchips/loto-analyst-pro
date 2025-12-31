# Documento de Contexto do Projeto: Loto Analyst Pro

**Arquivo:** `IA-trabalhou-assim.md`
**Data:** 30 de Dezembro de 2025
**Projeto:** Lottery Analysis System (Loto Analyst)

---

## 1. Visão Geral e Objetivo
Este documento descreve detalhadamente o desenvolvimento lógico, arquitetural e funcional do software "Loto Analyst". O objetivo do projeto foi criar uma aplicação web interativa utilizando **Streamlit** para análise de dados de loterias brasileiras (**Lotofácil** e **Mega-Sena**).

O software não promete ganhos garantidos, mas fornece ferramentas estatísticas para explorar padrões empíricos, gerar "palpites" (predições) baseados em métricas ponderadas e validar essas estratégias através de backtesting histórico.

## 2. Estrutura Arquitetural
A aplicação foi desenvolvida em **Python** seguindo uma arquitetura modular para separar responsabilidades (UI, Lógica de Dados, Estatística, Predição).

### Organização de Pastas
- `app.py`: Ponto de entrada da aplicação. Gerencia a configuração da página, barra lateral e a renderização das abas.
- `core/`: Utilitários fundamentais.
  - `data_loader.py`: Carregamento e normalização de dados (CSV ou Mock).
  - `features.py`: Engenharia de features (extração de métricas como primos, pares, soma).
- `analytics/`: Lógica de análise descritiva.
  - `stats.py`: Cálculos estatísticos globais (frequência, atraso, distribuições).
- `prediction/`: Lógica de geração de jogos.
  - `scoring.py`: Algoritmo de ranqueamento dos números.
  - `generator.py`: Geração de pools e filtragem de combinações.
- `desdobramento/`: Lógica combinatória.
  - `engine.py`: Criação de jogos completos a partir de pools de números (Unfolding).
- `backtest/`: Validação histórica.
  - `simulator.py`: Motor que simula o passo-a-passo do passado para validar previsões.
- `ui/`: Componentes visuais do Streamlit separados por abas.

## 3. Fluxo de Dados e Lógica Implementada

### 3.1. Carregamento e Processamento de Dados (`core`)
1.  **DataLoader**: O sistema verifica se há um arquivo CSV. Se não houver, gera dados "mock" realistas para análise imediata.
2.  **FeatureExtractor**: Para cada sorteio, o sistema calcula métricas ricas automaticamente:
    -   **Soma**: Soma total das dezenas sorteadas.
    -   **Pares/Ímpares**: Contagem de distribuição.
    -   **Primos**: Contagem baseada em listas pré-definidas de primos para cada jogo.
    -   **Repetidos**: Quantas dezenas se repetiram do sorteio *imediatamente anterior*.
    -   **Amplitude**: Diferença entre a maior e menor dezena.

### 3.2. Análise Estatística (`analytics`)
O módulo `StatsAnalyzer` não apenas conta ocorrências. Ele implementa lógica para:
-   **Frequência Global**: Quantas vezes cada número saiu em todo o histórico.
-   **Atraso (Delay)**: Contagem de sorteios consecutivos que um número *não* sai (importante para estratégias de "números atrasados").
-   **Distribuições**: Análise da curva de somas e paridade para ajudar a filtrar jogos improváveis (ex: jogos com soma muito baixa ou muito alta).

### 3.3. Sistema de Predição (`prediction`)
A "inteligência" do sistema reside na classe `Scorer` e `Generator`.
-   **Scoring Híbrido**: Cada número (1-25 ou 1-60) recebe uma pontuação (`score`) baseada em pesos configuráveis:
    -   `w_freq` (Peso Frequência): Bonifica números que saem muito.
    -   `w_delay` (Peso Atraso): Bonifica números que estão "devendo" uma aparição (assumindo reversão à média).
    -   `w_trend` (Peso Tendência): Bonifica números que saíram muito nos últimos 10 concursos ("estão quentes").
    -   *Fórmula*: `Score = (w_f * NormFreq) + (w_d * NormDelay) + (w_t * NormRecent)`
-   **Geração de Pool**: O sistema seleciona os Top N números com maior score (ex: top 18 para a Lotofácil) para formar um "cercamento".
-   **Filtragem**: Jogos gerados podem ser descartados se não obedecerem regras de Soma Mín/Máx ou Qtd de Ímpares (configurado no `Generator`).

### 3.4. Desdobramento / Unfolding (`desdobramento`)
Transforma o "Pool" de palpites em jogos jogáveis.
-   Usa `itertools.combinations` para gerar todas as combinações matemáticas possíveis dentro do pool selecionado.
-   Suporta **Números Fixos**: Garante que certos números apareçam em 100% dos jogos gerados.
-   Possui limitador (`limit`) para evitar explosão combinatória em pools muito grandes, pegando apenas os primeiros N jogos ou preenchendo o restante aleatoriamente caso solicitado.

### 3.5. Backtesting (`backtest`)
Permite validar "o que teria acontecido".
-   O `BacktestSimulator` percorre uma janela temporal (ex: últimos 100 jogos).
-   Para cada jogo `T`:
    1.  Treina o modelo com dados de `0` até `T-1`.
    2.  Gera palpites usando a lógica do `Scorer`.
    3.  Gera jogos via `Unfolder`.
    4.  Confere os acertos comparando com o resultado real de `T`.
-   Gera métricas de performance (Média de acertos, Melhor acerto).

## 4. Tecnologias e Decisões de Design
-   **Streamlit**: Escolhido pela rapidez de prototipagem de UI de dados e interatividade (widgets, dataframes).
-   **Pandas**: Backbone de todo o processamento de dados e séries temporais.
-   **Modularidade**: O código foi separado em módulos (UI vs Core Logic) para permitir que a IA no futuro possa refatorar a lógica de `Scoring` sem quebrar a interface, ou mudar a interface sem afetar os cálculos matemáticos.
-   **CSS Personalizado**: Injeção de CSS no `app.py` para dar um visual moderno (Dark Theme, fontes Roboto, cores vibrantes), fugindo do padrão básico do Streamlit.

## 5. Como usar este Contexto
Se você é uma IA lendo isso para continuar o trabalho:
1.  Verifique `core/features.py` se precisar adicionar novas métricas (ex: Fibonacci, Moldura).
2.  Ajuste `prediction/scoring.py` para refinar a inteligência de seleção de números (ex: adicionar Machine Learning real ou pesos dinâmicos).
3.  Use os componentes de UI em `ui/` apenas para exibição; mantenha a lógica pesada nos módulos dedicados.

---
*Fim do documento.*
