import streamlit as st
import pandas as pd
import sys
import os
from core.data_loader import DataLoader
from core.features import FeatureExtractor
from analytics.stats import StatsAnalyzer
from ui import tab_stats, tab_prediction, tab_desdobramento, tab_backtest, tab_autopilot

def main():
    st.set_page_config(page_title="Loto Analyst Pro", layout="wide", page_icon="🎱")

    # --- Custom CSS for aesthetic look ---
    st.markdown("""
    <style>
        .reportview-container {
            background: #0e1117;
        }
        .main {
            background-color: #0e1117;
        }
        h1, h2, h3 {
            color: #00ffcc !important;
            font-family: 'Roboto', sans-serif;
        }
        .stButton>button {
            color: #ffffff;
            background-color: #00cc88;
            border-radius: 10px;
        }
        .stat-card {
            background-color: #1f2937;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #374151;
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("🎱 Agente Loto Analyst")
    st.markdown("**Sistema Avançado de Análise de Loterias** | Desenvolvido com Streamlit & Python | **por Robson Pimentel**")

    # Global Manual
    with st.expander("📘 Manual Completo e Treinamento"):
        try:
            manual_path = os.path.join(os.path.dirname(__file__), "manual.md")
            with open(manual_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())
        except FileNotFoundError:
            st.warning(f"Manual não encontrado em: {manual_path}")

    # --- Game Selection Logic (Synced) ---
    
    # Initialize state
    if "selected_game_type" not in st.session_state:
        st.session_state["selected_game_type"] = "lotofacil"
        
    def  update_game_from_sidebar():
        st.session_state["selected_game_type"] = st.session_state.game_type_sidebar
        
    def update_game_from_main():
        st.session_state["selected_game_type"] = st.session_state.game_type_main

    GAME_OPTIONS = ["lotofacil", "megasena"]
    GAME_LABELS = {"lotofacil": "Lotofácil", "megasena": "Mega-Sena"}
    
    current_index = GAME_OPTIONS.index(st.session_state["selected_game_type"])

    # 1. Main Area Selector (Visible on Mobile/Desktop Top)
    col_sel1, col_sel2 = st.columns([2, 1])
    with col_sel1:
        st.selectbox(
            "Selecione o Jogo (Principal)", 
            GAME_OPTIONS,
            index=current_index,
            format_func=lambda x: GAME_LABELS[x],
            key="game_type_main",
            on_change=update_game_from_main,
            label_visibility="collapsed"
        )
    
    # 2. Sidebar Selector (Synced)
    st.sidebar.header("Configuração")
    st.sidebar.selectbox(
        "Selecione o Jogo", 
        GAME_OPTIONS,
        index=current_index,
        format_func=lambda x: GAME_LABELS[x],
        key="game_type_sidebar",
        on_change=update_game_from_sidebar
    )
    
    # Use state for loading
    game_type = st.session_state["selected_game_type"]

    # Load Data
    @st.cache_data
    def load_data(game_type):
        dl = DataLoader(game_type=game_type)
        df = dl.load_data()
        fe = FeatureExtractor(df, game_type=game_type)
        df = fe.extract_features()
        return df
 
    with st.spinner(f"Carregando dados de {GAME_LABELS[game_type]}..."):
        df = load_data(game_type)
        
    # Metrics display in main area
    with col_sel2:
        st.metric("Sorteios Carregados", len(df))
        
    st.sidebar.success(f"Carregados {len(df)} sorteios.")

    # Global Stats Analyzer
    stats_analyzer = StatsAnalyzer(df, game_type=game_type)

    # --- Tabs / Navigation ---
    
    # PATCH: Force Tab Selection System
    USE_TAB_PATCH = True
    
    TAB_NAMES = ["📊 Estatísticas", "🔮 Previsão", "🔢 Desdobramento", "🔙 Simulação", "🤖 Palpites Automáticos"]
    
    if USE_TAB_PATCH:
        # Initialize state if not present
        if "active_tab" not in st.session_state:
            st.session_state["active_tab"] = TAB_NAMES[0]

        # Use Sidebar for Navigation (Mobile Friendly standard)
        st.sidebar.divider()
        st.sidebar.header("Navegação")
        
        selected_tab = st.sidebar.radio(
            "Ir para:", 
            TAB_NAMES, 
            index=TAB_NAMES.index(st.session_state["active_tab"]),
            key="nav_radio"
        )
        
        # Sync simple variable with state for logic ensuring
        st.session_state["active_tab"] = selected_tab
        
        # Render the selected content logic remains the same...
        if selected_tab == TAB_NAMES[0]:
            st.header(TAB_NAMES[0]) # Re-add header since tab strip is gone
            tab_stats.render(df, stats_analyzer, game_type)
        elif selected_tab == TAB_NAMES[1]:
            # st.header(TAB_NAMES[1]) # Render function already has header
            tab_prediction.render(df, stats_analyzer, game_type)
        elif selected_tab == TAB_NAMES[2]:
            tab_desdobramento.render(game_type)
        elif selected_tab == TAB_NAMES[3]:
            tab_backtest.render(df, game_type)
        elif selected_tab == TAB_NAMES[4]:
            tab_autopilot.render(df, stats_analyzer, game_type)
            
    else:
        # Original Native Tabs logic (Revertible)
        tab1, tab2, tab3, tab4, tab5 = st.tabs(TAB_NAMES)

        with tab1:
            tab_stats.render(df, stats_analyzer, game_type)
        with tab2:
            tab_prediction.render(df, stats_analyzer, game_type)
        with tab3:
            tab_desdobramento.render(game_type)
        with tab4:
            tab_backtest.render(df, game_type)
        with tab5:
            tab_autopilot.render(df, stats_analyzer, game_type)

if __name__ == "__main__":
    is_streamlit_running = False
    try:
        from streamlit.runtime import exists
        if exists():
            is_streamlit_running = True
    except ImportError:
        # Fallback check for older versions or issues detecting runtime
        pass
    
    if is_streamlit_running:
        main()
    else:
        # Start streamlit
        from streamlit.web import cli as stcli
        sys.argv = ["streamlit", "run", __file__]
        sys.exit(stcli.main())
