import streamlit as st
from backtest.simulator import BacktestSimulator
from backtest.metrics import calculate_metrics
import plotly.express as px
from core.utils import render_help

def render(df, game_type):
    st.header("Simulação Histórica")
    render_help("backtest")
    
    st.markdown("Simule como o modelo de predição teria performado no passado.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        num_sims = st.slider("Qtd. Sorteios para Testar", 5, 50, 20)
        pool_size = st.number_input("Tamanho do Pool", 15, 25, 18)
        
        start_btn = st.button("Iniciar Simulação", type="primary", key="btn_backtest_start")

    ss_key = "backtest_results"
        
    if start_btn:
        with st.spinner("Rodando simulação histórica..."):
            sim = BacktestSimulator(df, game_type)
            # Start index: we need enough history. Let's start at len - num_sims
            start_idx = max(50, len(df) - num_sims) 
            
            results_df = sim.run_simulation(start_idx, num_sims, pool_size=pool_size)
            metrics = calculate_metrics(results_df, game_type)
            
            st.session_state[ss_key] = {
                'df': results_df,
                'metrics': metrics
            }
    
    if ss_key in st.session_state:
        results = st.session_state[ss_key]
        results_df = results['df']
        metrics = results['metrics']
        
        with col2:
            st.subheader("Resumo dos Resultados")
            st.json(metrics)
            
        st.divider()
        st.subheader("Desempenho ao Longo do Tempo")
        if not results_df.empty:
            # Traduzir colunas para exibição
            display_df = results_df.rename(columns={
                'concurso': 'Concurso',
                'target': 'Dezenas Sorteadas',
                'pool': 'Pool Escolhido',
                'games_played': 'Jogos Gerados',
                'best_hit': 'Melhor Acerto',
                'avg_hit': 'Média de Acertos'
            })
            
            fig = px.line(results_df, x='concurso', y='best_hit', title="Melhores Acertos por Sorteio")
            # add baseline hline?
            st.plotly_chart(fig, width="stretch")
            
            st.write("Logs Detalhados")
            st.dataframe(display_df)
            
        if st.button("Limpar Simulação", type="secondary", key="btn_backtest_clear"):
            del st.session_state[ss_key]
            st.rerun()

