import streamlit as st
import plotly.express as px
from core.utils import render_help

def render(df, stats_analyzer, game_type):
    st.header("Análise Estatística Profunda")
    render_help("analytics")
    
    col1, col2, col3 = st.columns(3)
    
    freqs = stats_analyzer.calculate_frequencies()
    delays = stats_analyzer.calculate_delays()
    
    with col1:
        st.subheader("Números Mais Quentes")
        st.dataframe(freqs.head(10).rename("Frequência"), width="stretch")
    
    with col2:
        st.subheader("Números Mais Frios")
        st.dataframe(freqs.tail(10).sort_values().rename("Frequência"), width="stretch")
        
    with col3:
        st.subheader("Mais Atrasados")
        st.dataframe(delays.head(10).rename("Atraso (Jogos)"), width="stretch")

    st.divider()
    
    # Visualizations
    st.subheader("Distribuição de Frequência")
    fig_freq = px.bar(x=freqs.index, y=freqs.values, labels={'x': 'Número', 'y': 'Frequência'}, title="Frequência Geral")
    st.plotly_chart(fig_freq, width="stretch")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Distribuição de Paridade (Pares/Ímpares)")
        parity_counts = df['pares'].value_counts().sort_index()
        fig_par = px.pie(values=parity_counts.values, names=parity_counts.index, title="Qtd. Números Pares por Sorteio")
        st.plotly_chart(fig_par, width="stretch")
        
    with col_b:
        st.subheader("Distribuição da Soma")
        fig_sum = px.histogram(df['soma'], title="Soma das Dezenas (Histórico)")
        st.plotly_chart(fig_sum, width="stretch")
