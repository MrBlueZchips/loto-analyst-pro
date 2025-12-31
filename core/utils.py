import streamlit as st
import os

def render_help(module_name):
    """
    Renders a help expander reading from docs/{module_name}.md.
    """
    # Assuming standard structure: root -> core -> utils.py
    # docs are in root -> docs
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'docs', f'{module_name}.md')
    
    if os.path.exists(file_path):
        with st.expander(f"📘 Guia do Módulo: {module_name.capitalize().replace('_', ' ')}"):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            st.markdown(content)
    else:
        # Silently fail or log if dev
        pass

def convert_to_txt(games):
    """Converts a list of games to a TXT string."""
    txt_output = ""
    for i, game in enumerate(games):
        txt_output += f"Jogo {i+1}: " + " ".join([str(n).zfill(2) for n in game]) + "\n"
    return txt_output
