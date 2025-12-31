# 🚀 Guia de Publicação Online (Conta Hobby)

Este guia foi personalizado para sua configuração SSH `github.com-hobby`.

## Passo 1: Criar o Repositório no GitHub
1.  Faça login na sua conta **mrbluezchips** (ou a conta do email hobby).
2.  Acesse [github.com/new](https://github.com/new).
3.  Nomeie o repositório exatamente como: `loto-analyst-pro`.
4.  Deixe como **Public**.
5.  **NÃO** marque "Add a README file" (pois já temos o código aqui).
6.  Clique em **Create repository**.

## Passo 2: Enviar o Código (Já configurado!)
Eu já inicializei o git e fiz o commit inicial para você. Agora basta rodar estes comandos no terminal para conectar e enviar:

```bash
# Adiciona o link remoto usando SEU alias SSH específico
git remote add origin git@github.com-hobby:mrbluezchips/loto-analyst-pro.git

# Envia os arquivos
git push -u origin main
```

> **Nota**: Se o seu usuário no GitHub não for `mrbluezchips`, altere o comando acima para o nome correto.

## Passo 3: Conectar na Streamlit Cloud
1.  Acesse [share.streamlit.io](https://share.streamlit.io/).
2.  Faça login com a sua conta do GitHub.
3.  Clique em **New app**.
4.  Selecione o repositório `loto-analyst-pro`.
5.  **Main file path**: `app.py`.
6.  Clique em **Deploy!**.

Pronto! Em minutos seu app estará no ar.
