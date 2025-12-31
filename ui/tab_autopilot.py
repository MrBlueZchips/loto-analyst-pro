import streamlit as st
import pandas as pd
from prediction.scoring import Scorer
from prediction.generator import Generator
from desdobramento.engine import Unfolder
from core.utils import render_help

def render(df, stats_analyzer, game_type):
    st.header("🤖 Piloto Automático")
    render_help("autopilot")
    st.markdown("Deixe a IA pilotar. Defina seus objetivos e nós cuidamos da matemática.")

    col1, col2 = st.columns([1, 2])

    max_nums = 25 if game_type == 'lotofacil' else 60

    with col1:
        st.subheader("Configuração")
        
        # Strategy Selection
        strategy = st.selectbox(
            "Perfil de Estratégia", 
            ["⚖️ Balanceada (Recomendada)", "🌊 Surfista de Tendência", "🐢 Contrarian (Do Contra)"],
            index=0,
            key="auto_strategy_select"
        )
        
        # Number of games
        n_games = st.number_input(
            "Quantos jogos gerar?", 
            min_value=1, 
            max_value=50, 
            value=5,
            key="auto_ngames_input"
        )
        
        # Optional: Fixed numbers
        all_numbers = list(range(1, 26)) if game_type == 'lotofacil' else list(range(1, 61))
        fixed_numbers = st.multiselect(
            "Números Fixos (Opcional)", 
            all_numbers,
            key="auto_fixed_multiselect"
        )
        
        if len(fixed_numbers) > (15 if game_type == 'lotofacil' else 6):
             st.warning("Muitos números fixos!")

        run_btn = st.button("🚀 Rodar Piloto Automático", type="primary", key="btn_auto_run")

    # Key for session state
    ss_key = "autopilot_games"

    if run_btn:
        try:
            with st.spinner("Analisando padrões e gerando jogos..."):
                # 1. Define Weights based on Strategy
                if "Tendência" in strategy: # Matches "Surfista de Tendência"
                    w_freq, w_delay, w_trend = 0.6, 0.1, 0.3
                    # st.toast("Estratégia Aplicada: Surfista de Tendência 🌊")
                elif "Contrarian" in strategy:
                    w_freq, w_delay, w_trend = 0.2, 0.7, 0.1
                    # st.toast("Estratégia Aplicada: Contrarian 🐢")
                else: # Balanced
                    w_freq, w_delay, w_trend = 0.4, 0.4, 0.2
                    # st.toast("Estratégia Aplicada: Balanceada ⚖️")

                # 2. Score and Candidate Generation
                scorer = Scorer(stats_analyzer)
                
                scores = scorer.calculate_hybrid_score(w_freq=w_freq, w_delay=w_delay, w_trend=w_trend)
                
                # Pass scores to generator
                gen = Generator(scorer)
                gen.scores = scores 
                
                # Pool Size
                pool_size = 19 if game_type == 'lotofacil' else 12 
                
                pool = gen.generate_candidate_pool(pool_size=pool_size)
                
                # 3. Unfolding with Random Injection
                # We generate games with -1 size, then inject 1 random number
                
                std_draw_size = 15 if game_type == 'lotofacil' else 6
                target_unfold_size = std_draw_size - 1
                
                # Check if we have enough numbers to unfold (Pool + Fixed)
                # If fixed >= target, we might have issues, but let's assume valid
                
                unfolder = Unfolder(game_type)
                
                # Generate base games (size N-1)
                base_games = unfolder.unfold(
                    pool, 
                    fixed_numbers=fixed_numbers, 
                    limit=n_games, 
                    override_draw_size=target_unfold_size
                )
                
                # Inject Random Number
                import random
                max_num = 25 if game_type == 'lotofacil' else 60
                all_possible = set(range(1, max_num + 1))
                
                final_games = []
                for game in base_games:
                    current_set = set(game)
                    remaining = list(all_possible - current_set)
                    
                    if remaining:
                        random_addition = random.choice(remaining)
                        new_game = sorted(game + [random_addition])
                        final_games.append(new_game)
                    else:
                        # Should not happen in lottery context
                        final_games.append(game)
                
                games = final_games
                
                # SAVE TO SESSION STATE
                st.session_state[ss_key] = {
                    'games': games,
                    'strategy': strategy,
                    'pool_size': pool_size,
                    'fixed_count': len(fixed_numbers)
                }
        except Exception as e:
            st.error(f"Ocorreu um erro durante a execução: {e}")
            st.code(f"Detalhes do erro: {type(e).__name__}", language="text")

    # RENDER RESULTS FROM STATE
    if ss_key in st.session_state:
        results = st.session_state[ss_key]
        games = results['games']
        
        with col2:
            st.success(f"Sucesso! {len(games)} jogos gerados (Memória).")
            
            st.markdown("### 📋 Jogos Gerados")
            for i, g in enumerate(games):
                st.code(f"Jogo {i+1}: {g}", language="text")
                
            # Metrics / Rationale
            strat_name = results['strategy'].split(' ')[0]
            st.info(f"**Racional da IA**: Selecionados as top {results['pool_size']} candidatas com base em fatores da estratégia **{strat_name}**. Fixadas {results['fixed_count']} dezenas.")
            
            # Download
            df_export = pd.DataFrame(games)
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.download_button("💾 Baixar CSV", df_export.to_csv(index=False), "jogos_autopilot.csv", key="down_csv_auto")
            with col_d2:
                from core.utils import convert_to_txt
                st.download_button("💾 Baixar TXT", convert_to_txt(games), "jogos_autopilot.txt", key="down_txt_auto")
                
            if st.button("Limpar Resultados", type="secondary", key="btn_auto_clear"):
                del st.session_state[ss_key]
                st.rerun()
