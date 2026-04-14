<p align="center">
  <img src="assets/banner.png" alt="Silvio Meira Digital" width="600">
</p>

# Silvio Meira Digital - Content Pipeline

Este projeto é uma ferramenta de engenharia de dados projetada para extrair, processar e organizar todo o acervo digital de Silvio Meira (blog, vídeos e artigos) em um formato otimizado para treinamento e consumo por Inteligências Artificiais.

## 🚀 Tecnologias

- **Python 3.10+**
- **Playwright**: Extração de conteúdo dinâmico.
- **BeautifulSoup4**: Parsing de HTML.
- **YT-DLP**: Download de áudio de vídeos do YouTube.
- **Ollama (Llama 3)**: Transcrição e formatação de áudio via LLM.
- **FFmpeg**: Processamento de mídia.

## 📂 Estrutura do Projeto

```text
SilvioMeiraDigital/
├── data/                       # Todos os dados gerados
│   ├── raw/                    # Backups brutos do site (Markdown original)
│   ├── processed/              # Conteúdo limpo e unificado
│   └── output/                 # Partes segmentadas prontas para consumo (IA)
├── src/                        # Código fonte
│   ├── scrapers/               # Scripts de extração (Site, YouTube)
│   ├── processors/             # Limpeza, unificação e segmentação de texto
│   └── utils/                  # Helpers (em desenvolvimento)
├── assets/                     # Imagens e arquivos estáticos
├── scripts/                    # Scripts de automação ou setup
├── requirements.txt            # Dependências do projeto
└── README.md                   # Documentação principal
```

## 🛠️ Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/usuario/SilvioMeiraDigital.git
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Instale os navegadores do Playwright:
   ```bash
   playwright install chromium
   ```

4. Certifique-se de ter o **FFmpeg** instalado no sistema e o **Ollama** rodando localmente com o modelo `llama3`.

## ⚙️ Como Executar

### 1. Extração (Scraping)
Captura o conteúdo do site e salva em `data/raw/markdown`.
```bash
python src/scrapers/web_scraper.py
```

### 2. Unificação e Limpeza
Consolida todos os arquivos extraídos em um único arquivo Markdown limpo em `data/processed/full_content.md`.
```bash
python src/processors/unifier.py
```

### 3. Segmentação (Splitting)
Divide o conteúdo unificado em partes menores em `data/output/parts/` para facilitar o processamento por IAs.
```bash
python src/processors/splitter.py
```

## 📝 Convenções

- Novos scripts devem ser adicionados em `src/`.
- Dados gerados não devem ser versionados (conforme `.gitignore`).
- Formato de saída padrão: Markdown UTF-8.

## ⚠️ Observações Importantes

- O processo de transcrição via Ollama é intensivo em hardware (GPU recomendada).
- Respeite o `robots.txt` do site durante a extração.
