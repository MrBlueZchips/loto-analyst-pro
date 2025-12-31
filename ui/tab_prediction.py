import streamlit as st
from prediction.scoring import Scorer
from prediction.generator import Generator
from core.utils import render_help

def render(df, stats_analyzer, game_type):
    st.header("Predição Algorítmica")
    render_help("prediction")
    
    st.markdown("""
    Este módulo utiliza um sistema de pontuação híbrido (Frequência + Atraso + Tendência Recente) para classificar os números.
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Parâmetros")
        pool_size = st.slider("Tamanho do Pool (Candidatas)", 15, 25, 18)
        w_freq = st.slider("Peso: Frequência", 0.0, 1.0, 0.4)
        w_delay = st.slider("Peso: Atraso", 0.0, 1.0, 0.4)
        w_trend = st.slider("Peso: Tendência", 0.0, 1.0, 0.2)
        

        
        generate_btn = st.button("Gerar Previsão", type="primary", key="btn_pred_generate")

    ss_key = "pred_pool"

    if generate_btn:
        scorer = Scorer(stats_analyzer)
        try:
             scores = scorer.calculate_hybrid_score(w_freq=w_freq, w_delay=w_delay, w_trend=w_trend)
        except TypeError:
             scores = scorer.calculate_hybrid_score() # Fallback
             
        gen = Generator(scorer)
        gen.scores = scores 
        
        pool = gen.generate_candidate_pool(pool_size)
        
        st.session_state[ss_key] = pool
        
    if ss_key in st.session_state:
        pool = st.session_state[ss_key]
        
        with col2:
            st.success("Pool de Candidatas Gerado!")
            st.write(f"**Números Selecionados ({len(pool)}):**")
            st.write(sorted(pool))
            
            st.subheader("Sugestão de Jogos (Desdobramento Simples)")
            # Generate a few sample games from this pool using a simple unfold
            from desdobramento.engine import Unfolder
            unf = Unfolder(game_type)
            # Just show top 5 simple combinations or random fill from this pool
            games = unf.unfold(pool, limit=5)
            
            for i, g in enumerate(games):
                st.code(f"Jogo {i+1}: {g}")
            
            if st.button("Limpar Previsão", type="secondary", key="btn_pred_clear"):
                del st.session_state[ss_key]
                st.rerun()
