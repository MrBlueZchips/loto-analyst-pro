#!/bin/bash
# Script utilitário para rodar o Loto Analyst corretamente

# Caminho para o executável do Streamlit no venv do usuário
STREAMLIT_PATH="/home/bluezchips/hobby/.venv/bin/streamlit"
APP_PATH="/home/bluezchips/hobby/loto_analyst/app.py"

echo "🎱 Iniciando Loto Analyst..."
echo "Executando: $STREAMLIT_PATH run $APP_PATH"

# Executa o comando correto
"$STREAMLIT_PATH" run "$APP_PATH"
