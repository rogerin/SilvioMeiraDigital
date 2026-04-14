import os
import re
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from markdownify import markdownify as md
import yt_dlp
import subprocess
from playwright.async_api import async_playwright

# Configurações
visited_links = set()
youtube_links = []
spotify_links = []
markdown_sections = []

ROOT_DOMAIN = ""
OUTPUT_DIR = "data/raw/markdown"
TRANSCRIPT_DIR = os.path.join(OUTPUT_DIR, "transcripts")
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

def is_internal(url):
    return ROOT_DOMAIN in urlparse(url).netloc

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

async def fetch_and_parse(page, url):
    try:
        print(f"🔗 Visitando: {url}")
        await page.goto(url, wait_until="networkidle")
        content = await page.content()
        return BeautifulSoup(content, "html.parser"), content
    except Exception as e:
        print(f"⚠️ Erro ao acessar {url}: {e}")
        return None, ""

def save_html_as_md(url, html):
    title = urlparse(url).path.replace("/", "_") or "index"
    filename = sanitize_filename(title.strip("_")) + ".md"
    markdown = md(html)
    with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
        f.write(f"# Página: {url}\n\n")
        f.write(markdown)
    markdown_sections.append(f"## Conteúdo de `{url}`\n\n{markdown}\n\n")

async def scrape_site(page, url):
    if url in visited_links:
        return
    visited_links.add(url)
    
    soup, raw_html = await fetch_and_parse(page, url)
    if not soup:
        return

    save_html_as_md(url, raw_html)

    for link in soup.find_all("a", href=True):
        full_url = urljoin(url, link['href'])
        if "youtube.com" in full_url or "youtu.be" in full_url:
            if full_url not in youtube_links:
                youtube_links.append(full_url)
        elif "spotify.com" in full_url:
            if full_url not in spotify_links:
                spotify_links.append(full_url)
        elif is_internal(full_url):
            await scrape_site(page, full_url)

def download_youtube_video(url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'quiet': True,
        'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def transcribe_with_ollama(audio_path):
    try:
        print(f"🧠 Transcrevendo com ollama: {audio_path}")
        cmd = [
            "ollama", "run", "llama3",
            f"Transcreva este áudio e devolva em formato markdown bem formatado, com títulos e parágrafos. O áudio está aqui: {audio_path}"
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
        return result.stdout
    except Exception as e:
        print(f"❌ Falha na transcrição: {e}")
        return ""

def process_youtube_links():
    for link in youtube_links:
        print(f"🎥 Processando vídeo: {link}")
        video_id = link.split("v=")[-1] if "v=" in link else link.split("/")[-1]
        audio_path = os.path.join(TRANSCRIPT_DIR, f"{sanitize_filename(video_id)}.mp3")
        try:
            download_youtube_video(link, audio_path)
            md_text = transcribe_with_ollama(audio_path)
            markdown_sections.append(f"\n## 🎧 Transcrição do vídeo `{link}`\n\n{md_text}\n")
        except Exception as e:
            print(f"⚠️ Erro com vídeo {link}: {e}")

def save_final_markdown():
    print("📦 Salvando markdown final...")
    final_md = "# 📚 Conteúdo Consolidado do Site\n\n"

    final_md += "### 🎵 Links do Spotify encontrados:\n"
    for s in spotify_links:
        final_md += f"- {s}\n"

    final_md += "\n### 📺 Links do YouTube encontrados:\n"
    for y in youtube_links:
        final_md += f"- {y}\n"

    final_md += "\n---\n\n".join(markdown_sections)

    with open(os.path.join(OUTPUT_DIR, "conteudo_completo.md"), "w", encoding="utf-8") as f:
        f.write(final_md)

async def main(site_url):
    global ROOT_DOMAIN
    ROOT_DOMAIN = urlparse(site_url).netloc

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await scrape_site(page, site_url)
        await browser.close()

    # process_youtube_links()
    save_final_markdown()
    print(f"✅ Finalizado! Markdown salvo em `{OUTPUT_DIR}/conteudo_completo.md`")

if __name__ == "__main__":
    # Exemplo:
    asyncio.run(main("https://www.imobiliariamariadejesus.com.br/venda/imoveis/todas-as-cidades/todos-os-bairros/0-quartos/0-suite-ou-mais/0-vaga/0-banheiro-ou-mais/todos-os-condominios?valorminimo=0&valormaximo=0&pagina=1"))
