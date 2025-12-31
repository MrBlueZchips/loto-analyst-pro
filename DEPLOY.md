# 🚀 Guia de Publicação Online (Streamlit Cloud)

Para que seus amigos possam acessar o **Loto Analyst Pro** de qualquer lugar (celular ou computador), a maneira mais fácil e gratuita é usando a **Streamlit Community Cloud**.

## Pré-requisitos
1.  Uma conta no [GitHub](https://github.com/) (gratuita).
2.  Uma conta na [Streamlit Cloud](https://streamlit.io/cloud) (pode logar com o GitHub).

---

## Passo 1: Preparar os Dados
Como seu software usa arquivos Excel (`.xlsx`) locais, eles precisam subir junto com o código.
*   Certifique-se de que os arquivos `Lotofácil-resultados-....xlsx` e `Mega-Sena-...xlsx` estão na mesma pasta do `app.py`.
*   ⚠️ **Atenção**: Dados públicos de loteria não são sensíveis, então tudo bem colocá-los no GitHub.

## Passo 2: Criar Repositório no GitHub
1.  Acesse [github.com/new](https://github.com/new).
2.  Nomeie como `loto-analyst-pro`.
3.  Deixe como **Public** (para a conta gratuita do Streamlit funcionar fácil).
4.  Clique em **Create repository**.

## Passo 3: Enviar o Código
Se você tem o Git instalado no seu computador, abra o terminal na pasta do projeto e rode:

```bash
git init
git add .
git commit -m "Primeira versão para deploy"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/loto-analyst-pro.git
git push -u origin main
```

*(Substitua `SEU_USUARIO` pelo seu nome de usuário do GitHub)*

> **Opção Simples (Upload Manual)**: Se não quiser usar comandos, na página do repositório criado no GitHub, clique em "Uploading an existing file" e arraste **todos** os arquivos e pastas do projeto para lá. Commit changes.

## Passo 4: Conectar na Streamlit Cloud
1.  Acesse [share.streamlit.io](https://share.streamlit.io/).
2.  Clique em **New app**.
3.  Selecione o repositório `loto-analyst-pro`.
4.  **Main file path**: Digite `app.py`.
5.  Clique em **Deploy!**.

## 🕒 Aguarde...
O Streamlit vai ler o arquivo `requirements.txt`, instalar as bibliotecas (Pandas, Plotly, etc.) e iniciar o servidor. Isso leva uns 2-3 minutos.

Assim que terminar, você receberá um link (ex: `https://loto-analyst-pro.streamlit.app`) para mandar no WhatsApp dos seus amigos! 🎱
