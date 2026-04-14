import os
import re

def clean_text(text):
    # Remove linhas que são apenas espaços em branco ou que contêm elementos de navegação
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        # Regex para remover URLs, mantendo o texto do link se houver
        line = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', line)
        # Remove markdown de imagens e links soltos
        if line.strip() and not re.search(r'(javascript:void\(0\)|#|imovel|assets/img|!\\[.*\\]\(.*\))', line):
            cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)

def unify_markdown_files(directory, output_file):
    all_content = ""
    files_to_process = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith(".md")]

    for filename in sorted(files_to_process):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            cleaned_content = clean_text(content)
            if cleaned_content.strip(): # Apenas adiciona se houver conteúdo após a limpeza
                all_content += f"# Conteúdo de: {filename}\n\n"
                all_content += cleaned_content + '\n\n---\n\n'

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(all_content)

if __name__ == "__main__":
    unify_markdown_files("data/raw/markdown", "data/processed/full_content.md")
