# 🧠 Análise de N-grams no Corpus Latino (*De Bello Gallico*)

Este projeto realiza a análise morfossintática e geração de bigramas e trigramas lematizados do texto *De Bello Gallico*, de Júlio César. Utiliza a biblioteca [Stanza](https://stanfordnlp.github.io/stanza/) para processamento de linguagem natural (NLP) em Latim, aplicando filtros para remoção de stopwords, pontuação, ruídos e visualizações estatísticas.

---

## 📦 Requisitos

### 1. Clone o repositório:
```bash
git clone https://github.com/LeoVichi/caesar_corpus
cd caesar_corpus
```

### 2. Crie e ative um ambiente virtual Python:
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências com:

```bash
pip install -r requirements.txt
```

**Dependências**:
- `stanza`
- `nltk`
- `pandas`
- `matplotlib`
- `wordcloud`

### Se estiver em Linux, pode ser necessário instalar:

```bash
sudo apt install libfreetype6-dev libpng-dev
```

---

## 📁 Estrutura esperada

- `de_bello_gallico.txt` — Arquivo de entrada com o corpus original em Latim.
- `corpus_lema_pos_com_stopwords.csv` — Tokens, lemas e POS tag.
- `bigrama_com_stopwords.csv`, `trigrama_com_stopwords.csv` — N-grams gerados.
- `grafico_top30_bigrama_com_stopwords.png`, `grafico_top30_trigrama_com_stopwords.png` — Gráficos de frequência.
- `nuvem_palavras_com_stopwords.png` — Nuvem de palavras.

---


## Como executar

No terminal, dentro da pasta do projeto:

```bash
python3 corpus_final.py
```

### Para remover stopwords e termos irrelevantes:

```bash
python3 corpus_final.py --no-stopwords
```

---

## 📊 Funcionalidades

- 🔠 **Lematização** com POS-tagging (usando Stanza para Latim).
- ✂️ **Limpeza automática** de:
  - Abreviações latinas com ponto
  - Pontuações
  - Números
- 🛑 **Remoção de stopwords latinas**, incluindo pronomes e auxiliares frequentes.
- 🔁 **Geração de n-grams** (bigramas e trigramas) com frequência.
- 📈 **Visualização gráfica** dos 30 n-grams mais frequentes.
- ☁️ **Nuvem de palavras** baseada nos lemas mais frequentes.

---

## 📚 Finalidade

Este script pode ser usado como:

- Ferramenta auxiliar para **pesquisa em filologia computacional**
- Apoio a projetos de **Humanidades Digitais**
- Base para análises estatísticas de estilo, coocorrência e sintaxe
- Material didático em cursos de Latim ou Linguística Computacional

---

## 🧑‍💻 Autor

**Leonardo Vichi**  
Desenvolvido por [Leonardo Vichi](https://github.com/LeoVichi) para atividade de Estágio Pós-Doutoral junto ao Programa de Pós-Graduação em Letras Clássicas da Universidade Federal do Rio de Janeiro - PPGLC/UFRJ.


---

## ⚖️ Licença

Distribuído sob a licença [MIT](https://opensource.org/licenses/MIT).
