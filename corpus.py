import argparse
import stanza
from nltk import ngrams
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import re
from wordcloud import WordCloud
import os

# Caminho do diretório atual do script
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))

# Criar diretório de saída se não existir
DIRETORIO_OUTPUT = os.path.join(DIRETORIO_ATUAL, "output")
os.makedirs(DIRETORIO_OUTPUT, exist_ok=True)


# CLI: Argumentos
parser = argparse.ArgumentParser(description="Gera n-grams e visualizações para corpus latino")
parser.add_argument("--no-stopwords", action="store_true", help="Remove stopwords latinas")
args = parser.parse_args()

# Texto fonte
with open("de_bello_gallico.txt", "r", encoding="utf-8") as f:
    texto = f.read()

# Limpeza
def pre_processamento(texto):
    texto = re.sub(r"\b[ADFIKLMNOPRUVX]+\.\b", "", texto)
    texto = re.sub(r"[^\w\sāēīōūæœ]", " ", texto)
    texto = re.sub(r"\d+", "", texto)
    texto = re.sub(r"\s{2,}", " ", texto)
    return texto.strip()

texto_limpo = pre_processamento(texto)

# NLP
stanza.download('la')
nlp = stanza.Pipeline(lang='la', processors='tokenize,mwt,pos,lemma', use_gpu=False)
print("⏳ Analisando texto...")
doc = nlp(texto_limpo)
print("✔️ Análise completa.")

# Stopwords
stopwords_latinas = {
    "et", "in", "de", "cum", "ad", "per", "a", "ab", "ex", "sub", "sed", "ut",
    "non", "autem", "nam", "ne", "nec", "vel", "enim", "atque", "quoque",
    "quod", "quia", "si", "quoniam", "dum", "postquam", "antequam", "ubi",
    "ita", "tamen", "ergo", "inter", "contra", "propter", "super", "is", "hic", 
    "ille", "qui", "quae", "quod", "quis", "ut", "an", "aut", "etiam", "tamen", 
    "igitur", "sum", "esse", "fui", "possum", "idem", "ipse", "quidem"
}

# Filtro
def is_token_valido(word):
    return (
        word.lemma and
        word.upos not in {"PUNCT", "SYM", "NUM", "X"} and
        re.match(r"^[a-zA-Zāēīōūæœ]+$", word.lemma) and
        len(word.lemma) > 1
    )

tokens_filtrados = [
    (word.text, word.lemma.lower(), word.upos)
    for sent in doc.sentences
    for word in sent.words
    if is_token_valido(word)
]

if args.no_stopwords:
    tokens_filtrados = [
        (token, lemma, pos)
        for token, lemma, pos in tokens_filtrados
        if lemma not in stopwords_latinas
    ]
    print("🧹 Stopwords e ruídos removidos.")

# Exporta POS
sufixo = "_sem_stopwords" if args.no_stopwords else "_com_stopwords"
df_pos = pd.DataFrame(tokens_filtrados, columns=["Token", "Lema", "POS"])
df_pos.to_csv(os.path.join(DIRETORIO_OUTPUT, f"corpus_lema_pos{sufixo}.csv"), index=False)
print(f"📄 Exportado: corpus_lema_pos{sufixo}.csv")

# n-grams
lemmas = [lemma for (_, lemma, _) in tokens_filtrados]

def gerar_ngrams(lista, n):
    return list(ngrams(lista, n))

bigramas = gerar_ngrams(lemmas, 2)
trigramas = gerar_ngrams(lemmas, 3)

# Frequência
cont_bigramas = Counter(bigramas)
cont_trigramas = Counter(trigramas)

df_bi = pd.DataFrame(cont_bigramas.items(), columns=["Bigrama", "Frequência"])
df_tri = pd.DataFrame(cont_trigramas.items(), columns=["Trigrama", "Frequência"])
df_bi.to_csv(os.path.join(DIRETORIO_OUTPUT, f"bigrama{sufixo}.csv"), index=False)
df_tri.to_csv(os.path.join(DIRETORIO_OUTPUT, f"trigrama{sufixo}.csv"), index=False)
print(f"📦 Exportado: bigrama{sufixo}.csv e trigrama{sufixo}.csv")

# Gráfico Bigramas
top_bi = df_bi.sort_values(by="Frequência", ascending=False).head(30)
plt.figure(figsize=(12, 8))
plt.barh([f"{a[0]} {a[1]}" for a in top_bi["Bigrama"]], top_bi["Frequência"], color="#4c72b0")
plt.xlabel("Frequência")
plt.title("Top 30 Bigrama" + (" (sem stopwords)" if args.no_stopwords else " (com stopwords)"))
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(os.path.join(DIRETORIO_OUTPUT, f"grafico_top30_bigrama{sufixo}.png"))
plt.show()
print(f"📦 Exportado: grafico_top30_bigrama{sufixo}.png")

# Gráfico Trigramas
top_tri = df_tri.sort_values(by="Frequência", ascending=False).head(30)
plt.figure(figsize=(12, 8))
plt.barh([f"{a[0]} {a[1]} {a[2]}" for a in top_tri["Trigrama"]], top_tri["Frequência"], color="#55a868")
plt.xlabel("Frequência")
plt.title("Top 30 Trigrama" + (" (sem stopwords)" if args.no_stopwords else " (com stopwords)"))
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(os.path.join(DIRETORIO_OUTPUT, f"grafico_top30_trigrama{sufixo}.png"))
plt.show()
print(f"📦 Exportado: grafico_top30_trigrama{sufixo}.png")

# Nuvem de palavras
freq_lemas = Counter(lemmas)
wordcloud = WordCloud(width=1000, height=600, background_color="white", colormap="viridis")
wordcloud.generate_from_frequencies(freq_lemas)
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Nuvem de Palavras" + (" (sem stopwords)" if args.no_stopwords else " (com stopwords)"))
plt.tight_layout()
plt.savefig(os.path.join(DIRETORIO_OUTPUT, f"nuvem_palavras{sufixo}.png"))
plt.show()
print(f"📦 Exportado: nuvem_palavras{sufixo}.png")
