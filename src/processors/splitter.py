import os
import re
from bs4 import BeautifulSoup

DIRETORIO = "data/raw/markdown"
ARQUIVO_SAIDA_BASE = "data/output/parts/parte_"
LIMITE_TAMANHO = 5_000_000  # 5MB por parte

def limpar_markdown(conteudo):
    # Remove espaços em branco excessivos e cabeçalhos repetidos
    conteudo = re.sub(r'\n{3,}', '\n\n', conteudo)
    linhas = conteudo.splitlines()
    resultado = []
    ultimo_header = ""
    for linha in linhas:
        if linha.startswith("#") and linha.strip() == ultimo_header:
            continue
        if linha.startswith("#"):
            ultimo_header = linha.strip()
        resultado.append(linha)
    return "\n".join(resultado).strip()

def ler_arquivos_markdown():
    arquivos = sorted([
        os.path.join(DIRETORIO, f)
        for f in os.listdir(DIRETORIO)
        if f.endswith(".md") and not f.startswith("parte_")
    ])
    conteudo_total = ""
    for caminho in arquivos:
        with open(caminho, "r", encoding="utf-8") as f:
            texto = f.read()
            texto_limpo = limpar_markdown(texto)
            conteudo_total += f"\n\n---\n\n## 📄 {os.path.basename(caminho)}\n\n" + texto_limpo
    return conteudo_total

def dividir_em_partes(conteudo, limite=LIMITE_TAMANHO):
    partes = [conteudo[i:i+limite] for i in range(0, len(conteudo), limite)]
    for idx, parte in enumerate(partes, 1):
        with open(f"{ARQUIVO_SAIDA_BASE}{idx}.md", "w", encoding="utf-8") as f:
            f.write(parte)
        print(f"✅ Parte {idx} salva: {ARQUIVO_SAIDA_BASE}{idx}.md")

# Execução
if __name__ == "__main__":
    print("📦 Limpando e unindo arquivos markdown...")
    conteudo = ler_arquivos_markdown()
    dividir_em_partes(conteudo)
    print("🎉 Finalizado!")