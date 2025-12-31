import streamlit as st
from desdobramento.engine import Unfolder
from core.utils import render_help

def render(game_type):
    st.header("Desdobramento Combinatório")
    render_help("unfolding")
    
    st.info("Gere jogos garantindo a cobertura de números específicos.")
    
    col1, col2 = st.columns(2)
    
    max_nums = 25 if game_type == 'lotofacil' else 60
    
    with col1:
        st.subheader("Seleção")
        selected = st.multiselect("Selecione Números para Desdobrar", range(1, max_nums + 1))
        fixed = st.multiselect("Selecione Números Fixos", range(1, max_nums + 1))
        
        limit_games = st.number_input("Máx. de Jogos para Gerar", min_value=1, max_value=1000, value=10)
        
    with col2:
        gen_btn = st.button("Gerar Jogos", key="btn_unf_generate")
        
    ss_key = "unfold_games"
    
    if gen_btn:
        if not selected:
            st.error("Por favor, selecione números para desdobrar.")
        else:
            unf = Unfolder(game_type)
            try:
                # Combine selected + fixed for the pool logic
                full_pool = list(set(selected) | set(fixed))
            
                games = unf.unfold(full_pool, fixed_numbers=fixed, limit=limit_games)
                
                st.session_state[ss_key] = games
                
            except Exception as e:
                st.error(f"Erro: {e}")
                
    if ss_key in st.session_state:
        games = st.session_state[ss_key]
        st.success(f"Gerados {len(games)} jogos.")
        for i, g in enumerate(games):
            st.text(f"{i+1}: {g}")
            
        # CSV Download
        import pandas as pd
        df_export = pd.DataFrame(games)
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.download_button("💾 Baixar CSV", df_export.to_csv(index=False), "jogos.csv", key="down_csv_unfold")
        with col_d2:
            from core.utils import convert_to_txt
            st.download_button("💾 Baixar TXT", convert_to_txt(games), "jogos.txt", key="down_txt_unfold")
            
        if st.button("Limpar", key="btn_unf_clear"):
            del st.session_state[ss_key]
            st.rerun()
