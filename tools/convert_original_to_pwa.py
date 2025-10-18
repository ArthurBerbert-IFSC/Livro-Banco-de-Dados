"""
Converter: Original Word HTML -> PWA Chapters (Python)

- Splits by top-level <h1> (chapters)
- Preserves inner HTML (tables, images, inline styles)
- Copies images from Original/..._arquivos to geoprocessamento-2/imagens/capitulos/capitulo-XX/
- Rewrites <img src> to new relative paths

Usage (from repo root):
  python tools/convert_original_to_pwa.py
"""
from __future__ import annotations
import os
import re
import shutil
from html import escape
import unicodedata

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ORIGINAL_HTML = os.path.join(REPO_ROOT, 'Original', 'Apostila Geoprocessamento 2 vs2.3.htm')
ORIGINAL_ASSETS_DIR = os.path.join(REPO_ROOT, 'Original', 'Apostila Geoprocessamento 2 vs2.3_arquivos')
OUTPUT_DIR = os.path.join(REPO_ROOT, 'geoprocessamento-2')
OUTPUT_IMG_BASE = os.path.join(OUTPUT_DIR, 'imagens', 'capitulos')


def ensure_dir(p: str) -> None:
    os.makedirs(p, exist_ok=True)


def read_original_html() -> str:
    data = open(ORIGINAL_HTML, 'rb').read()
    for enc in ('cp1252', 'latin1', 'utf-8', 'utf-8-sig'):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    # Fallback binary decode
    return data.decode('latin1', errors='ignore')


def strip_tags(html: str) -> str:
    return re.sub(r'<[^>]*>', '', html).strip()


def extract_chapters(full_html: str):
    chapters = []
    h1_iter = list(re.finditer(r'<h1[^>]*>([\s\S]*?)</h1>', full_html, flags=re.I))
    if not h1_iter:
        raise RuntimeError('Nenhum <h1> encontrado no arquivo original.')
    for i, m in enumerate(h1_iter):
        start = m.start()
        end = m.end()
        next_start = h1_iter[i + 1].start() if i + 1 < len(h1_iter) else len(full_html)
        h1_inner = m.group(1)
        content = full_html[end:next_start]
        chapters.append({
            'h1_inner': h1_inner,
            'content': content,
        })
    return chapters


def parse_chapter_meta(h1_inner: str):
    raw = strip_tags(h1_inner)
    # Normalize NBSP and HTML entities to spaces
    raw = raw.replace('\xa0', ' ').replace('&nbsp;', ' ')
    raw = re.sub(r'\s+', ' ', raw).strip()
    m = re.match(r'^(\d+)\s+(.*)$', raw)
    if m:
        return int(m.group(1)), m.group(2).strip()
    return None, raw


def copy_and_rewrite_images(html: str, chapter_num: int) -> str:
    chapter_id = f"{chapter_num:02d}"
    out_dir = os.path.join(OUTPUT_IMG_BASE, f"capitulo-{chapter_id}")
    ensure_dir(out_dir)

    def repl(m):
        prefix, quote, src = m.group(1), m.group(2), m.group(3)
        if src.lower().startswith('data:') or src.lower().startswith('http:') or src.lower().startswith('https:'):
            return m.group(0)
        decoded = src
        try:
            decoded = os.path.basename(bytes(src, 'utf-8').decode('utf-8'))
        except Exception:
            decoded = os.path.basename(src)
        file_name = os.path.basename(decoded)
        orig_path = os.path.join(ORIGINAL_ASSETS_DIR, file_name)
        dest_path = os.path.join(out_dir, file_name)
        try:
            if os.path.exists(orig_path):
                shutil.copy2(orig_path, dest_path)
            else:
                alt_path = os.path.join(REPO_ROOT, 'Original', src)
                if os.path.exists(alt_path):
                    shutil.copy2(alt_path, dest_path)
                else:
                    print(f"[aviso] Imagem não encontrada: {src}")
        except Exception as e:
            print(f"[aviso] Falha ao copiar imagem: {src} -> {dest_path}: {e}")
        rel_new = f"imagens/capitulos/capitulo-{chapter_id}/{file_name}"
        return f"{prefix}{quote}{rel_new}{quote}"

    return re.sub(r'(<img[^>]*?\s+src=)(["\'])([^"\']+)(["\'])', repl, html, flags=re.I)


def build_chapter_html(chapter_num: int, chapter_title: str, body_html: str, chapter_description: str = '') -> str:
    # This legacy signature is replaced below; kept temporarily for compatibility.
    return build_chapter_html_with_layout(
        chapter_num=chapter_num,
        chapter_title=chapter_title,
        body_html=body_html,
        chapter_description=chapter_description,
        toc_items=[],
        prev_link=None,
        next_link=None,
        total_chapters=None,
    )


def slugify(text: str) -> str:
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s\-]', ' ', text)
    text = re.sub(r'\s+', '-', text).strip('-')
    return text or 'secao'


def sanitize_and_build_toc(html: str):
    # Remove Word styles and classes (handle single, double, and unquoted)
    cleaned = re.sub(r'\s+style=("[^"]*"|\'[^\']*\'|[^\s>]+)', '', html, flags=re.I)
    cleaned = re.sub(r'\s+class=("[^"]*"|\'[^\']*\'|[^\s>]+)', '', cleaned, flags=re.I)
    # Remove empty spans
    cleaned = re.sub(r'<span[^>]*>\s*</span>', '', cleaned, flags=re.I)
    # Simplify spans to text
    cleaned = re.sub(r'<span[^>]*>', '', cleaned, flags=re.I)
    cleaned = cleaned.replace('</span>', '')

    # Remove empty paragraphs (&nbsp; only)
    cleaned = re.sub(r'<p[^>]*>\s*(?:&nbsp;|\u00A0|\s)*</p>', '', cleaned, flags=re.I)

    # Normalize tables
    cleaned = re.sub(r'<table[^>]*>', '<table class="min-w-full border border-slate-300 my-6">', cleaned, flags=re.I)
    cleaned = re.sub(r'<thead[^>]*>', '<thead>', cleaned, flags=re.I)
    cleaned = re.sub(r'<tbody[^>]*>', '<tbody>', cleaned, flags=re.I)
    cleaned = re.sub(r'<tr[^>]*>', '<tr>', cleaned, flags=re.I)
    cleaned = re.sub(r'<th[^>]*>', '<th class="border border-slate-300 p-2 bg-slate-50">', cleaned, flags=re.I)
    cleaned = re.sub(r'<td[^>]*>', '<td class="border border-slate-300 p-2">', cleaned, flags=re.I)

    # Normalize images: keep src, add responsive classes, map align
    def img_repl(m):
        full = m.group(0)
        attrs = m.group(1)
        # extract src
        src_m = re.search(r'src=(["\'])([^"\']+)\1', attrs, flags=re.I)
        src_attr = src_m.group(0) if src_m else ''
        # detect align
        align_m = re.search(r'\salign=([a-z]+)', attrs, flags=re.I)
        align = align_m.group(1).lower() if align_m else ''
        # build class
        classes = ['my-4', 'rounded-lg', 'shadow-sm', 'max-w-full', 'h-auto']
        if align == 'left':
            classes += ['float-left', 'mr-4']
        elif align == 'right':
            classes += ['float-right', 'ml-4']
        class_attr = f'class="{' '.join(classes)}"'
        return f'<img {src_attr} {class_attr} />'

    cleaned = re.sub(r'<img([^>]*)>', img_repl, cleaned, flags=re.I)

    # Headings: add id anchors and classes; collect TOC from h2 and h3
    toc = []

    def parse_heading(inner_html: str):
        """Return (num, title) where num can be like '1.2.3' or None, title is cleaned text.
        Also collapses any excessive spaces/newlines and NBSP.
        """
        text = strip_tags(inner_html)
        # normalize NBSP and whitespace/newlines
        text = text.replace('\xa0', ' ').replace('&nbsp;', ' ')
        text = re.sub(r'\s+', ' ', text).strip()
        # capture optional numbering at start (e.g., 1, 1.2, 1.2.3) and optional trailing dot
        m = re.match(r'^(\d+(?:\.\d+)*)(?:\.)?\s+(.*)$', text)
        if m:
            return m.group(1), m.group(2).strip()
        return None, text

    def h2_repl(m):
        inner = m.group(1)
        num, title = parse_heading(inner)
        base_text = title  # used for TOC and id
        sid = slugify(base_text)
        toc.append({'level': 2, 'text': base_text, 'id': sid})
        display_text = f"{num} {title}" if num else title
        display = escape(display_text)
        return f'<h2 id="{sid}" class="mt-10 scroll-mt-24 text-2xl font-semibold text-ifsc-green dark:text-emerald-300">{display}</h2>'

    def h3_repl(m):
        inner = m.group(1)
        num, title = parse_heading(inner)
        base_text = title
        sid = slugify(base_text)
        toc.append({'level': 3, 'text': base_text, 'id': sid})
        display_text = f"{num} {title}" if num else title
        display = escape(display_text)
        return f'<h3 id="{sid}" class="mt-8 scroll-mt-24 text-xl font-semibold">{display}</h3>'

    cleaned = re.sub(r'<h2[^>]*>([\s\S]*?)</h2>', h2_repl, cleaned, flags=re.I)
    cleaned = re.sub(r'<h3[^>]*>([\s\S]*?)</h3>', h3_repl, cleaned, flags=re.I)

    return cleaned, toc


def apply_didactic_boxes(html: str) -> str:
    label_map = {
        'dica:': {
            'icon': 'lightbulb',
            'classes': 'border-l-4 border-emerald-500 bg-emerald-50/60 dark:border-emerald-500/80 dark:bg-emerald-900/20',
            'title': 'Dica'
        },
        'atenção:': {
            'icon': 'alert-triangle',
            'classes': 'border-l-4 border-amber-500 bg-amber-50/60 dark:border-amber-500/80 dark:bg-amber-900/20',
            'title': 'Atenção'
        },
        'conceito:': {
            'icon': 'book-open-text',
            'classes': 'border-l-4 border-indigo-500 bg-indigo-50/60 dark:border-indigo-500/80 dark:bg-indigo-900/20',
            'title': 'Conceito'
        },
        'observação:': {
            'icon': 'info',
            'classes': 'border-l-4 border-sky-500 bg-sky-50/60 dark:border-sky-500/80 dark:bg-sky-900/20',
            'title': 'Observação'
        },
        'nota:': {
            'icon': 'sticky-note',
            'classes': 'border-l-4 border-slate-400 bg-slate-50/60 dark:border-slate-500/70 dark:bg-slate-800/30',
            'title': 'Nota'
        },
        'importante:': {
            'icon': 'alert-octagon',
            'classes': 'border-l-4 border-red-500 bg-red-50/60 dark:border-red-500/80 dark:bg-red-900/20',
            'title': 'Importante'
        },
        'consulta sql:': {
            'icon': 'file-code',
            'classes': 'border rounded-xl border-sky-300 dark:border-sky-700 bg-sky-50 dark:bg-sky-900/40',
            'title': 'Consulta SQL'
        },
    }

    def para_repl(m):
        inner = m.group(1)
        text = strip_tags(inner).strip()
        low = text.lower()
        for key, spec in label_map.items():
            if low.startswith(key):
                content_html = inner[len(key):] if inner.lower().startswith(key) else inner
                return (
                    f'<div class="not-prose my-4 {spec["classes"]} rounded-r-xl p-4">'
                    f'  <div class="flex items-start gap-3">'
                    f'    <i data-lucide="{spec["icon"]}" class="mt-0.5 text-slate-700 dark:text-slate-300"></i>'
                    f'    <div>'
                    f'      <p class="m-0 text-sm font-semibold text-slate-700 dark:text-slate-200">{spec["title"]}</p>'
                    f'      <div class="mt-1 text-slate-700 dark:text-slate-300">{content_html}</div>'
                    f'    </div>'
                    f'  </div>'
                    f'</div>'
                )
        return m.group(0)

    return re.sub(r'<p[^>]*>([\s\S]*?)</p>', para_repl, html, flags=re.I)


def build_chapter_html_with_layout(
    *,
    chapter_num: int,
    chapter_title: str,
    body_html: str,
    chapter_description: str,
    toc_items: list[dict],
    prev_link: tuple[str, str] | None,
    next_link: tuple[str, str] | None,
    total_chapters: int | None,
):
    page_title = f"{chapter_title} — Geoprocessamento 2"
    header_h1 = f"Capítulo {chapter_num}: {chapter_title}"
    desc_block = f'<p class="text-lg text-slate-600 dark:text-slate-400">{escape(chapter_description)}</p>' if chapter_description else ''
    # Build sidebar TOC
    toc_html_parts = [
        '<nav class="text-sm">',
        '<p class="text-xs uppercase tracking-wide text-slate-500 dark:text-slate-400 mb-2">Neste capítulo</p>',
        '<ul class="space-y-1">'
    ]
    for item in toc_items:
        indent = 'ml-0' if item['level'] == 2 else 'ml-4'
        toc_html_parts.append(
            f'<li class="{indent}"><a href="#{item["id"]}" class="hover:text-ifsc-green dark:hover:text-emerald-300">{escape(item["text"])}</a></li>'
        )
    toc_html_parts.append('</ul></nav>')
    toc_html = '\n'.join(toc_html_parts)

    # Chapter navigation
    nav_links = []
    nav_links.append('<a href="index.html" class="text-sm hover:underline">← Sumário</a>')
    if prev_link:
        prev_href, prev_label = prev_link
        nav_links.append(f'<a href="{prev_href}" class="text-sm hover:underline">← Cap. anterior: {escape(prev_label)}</a>')
    if next_link:
        next_href, next_label = next_link
        nav_links.append(f'<a href="{next_href}" class="text-sm hover:underline">Próx. capítulo: {escape(next_label)} →</a>')
    nav_top = ' · '.join(nav_links)

    return f"""<!DOCTYPE html>
<html lang="pt-BR" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="manifest" href="manifest.webmanifest">
    <title>{escape(page_title)}</title>

    <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-okaidia.min.css" rel="stylesheet">
    <link rel="stylesheet" href="estilos.css">

    <script>
      tailwind.config = {{
        darkMode: 'class',
        theme: {{
          extend: {{
            fontFamily: {{ sans: ['Inter', 'sans-serif'] }},
            colors: {{ 'ifsc-green': '#1B5E20', 'ifsc-soft': '#E6F4EA', 'ifsc-gray': '#374151' }}
          }}
        }}
      }}
    </script>
</head>
<body class="bg-slate-50 dark:bg-slate-950 text-ifsc-gray dark:text-slate-300 antialiased">
    <header class="bg-white/95 backdrop-blur shadow-sm sticky top-0 z-40 dark:bg-slate-900/90">
        <div class="border-b border-slate-200/60 dark:border-slate-700/60">
            <div class="container mx-auto px-6 py-4 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                <div class="flex flex-wrap items-center justify-center gap-4 md:justify-start">
                    <img src="imagens/logotipos/Logo_Disciplina_5.png" alt="Logo da Disciplina" class="h-16 md:h-18 lg:h-20 w-auto opacity-100 drop-shadow-sm" onerror="this.style.display='none'">
                    <img src="imagens/logotipos/florianopolis_horizontal_marca2015_PNG.png" alt="IFSC Florianópolis" class="h-10 w-auto opacity-80" onerror="this.style.display='none'">
                </div>
                <div class="flex items-center gap-3 justify-center md:justify-end">
                    <div class="text-center md:text-right">
                        <p class="text-lg font-semibold text-ifsc-green dark:text-emerald-300">GE2014902 - Geoprocessamento 2</p>
                        <p class="text-xs text-gray-500 dark:text-slate-300/80">Versão 2026.1</p>
                    </div>
                    <button id="theme-toggle" type="button" class="theme-toggle" aria-label="Alternar tema">
                        <i data-lucide="sun" class="sun-icon"></i>
                        <i data-lucide="moon" class="moon-icon"></i>
                    </button>
                </div>
            </div>
        </div>
    </header>

    <main class="container mx-auto px-6 py-8">
        <div class="mb-6 text-slate-500 dark:text-slate-400">{nav_top}</div>
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
            <aside class="lg:col-span-3 hidden lg:block">
                <div class="sticky top-24 p-4 border border-slate-200 dark:border-slate-700 rounded-xl bg-white/60 dark:bg-slate-900/40">
                    {toc_html}
                </div>
            </aside>
            <article class="lg:col-span-9">
                <header class="mb-8">
                    <h1 class="text-4xl font-bold text-ifsc-green dark:text-emerald-300 mb-2">{escape(header_h1)}</h1>
                    {desc_block}
                </header>
                <div class="prose prose-lg max-w-none prose-slate dark:prose-invert prose-justificado prose-indent">
                {body_html}
                </div>
                <div class="mt-10 pt-6 border-t border-slate-200 dark:border-slate-700 flex flex-wrap items-center justify-between gap-3">
                    <a href="index.html" class="text-slate-500 hover:underline">Sumário</a>
                    <div class="flex gap-3">
                        {f'<a href="{prev_link[0]}" class="inline-flex items-center gap-2 rounded-lg border border-slate-300 dark:border-slate-600 px-3 py-2 hover:bg-slate-50 dark:hover:bg-slate-800">← {escape(prev_link[1])}</a>' if prev_link else ''}
                        {f'<a href="{next_link[0]}" class="inline-flex items-center gap-2 rounded-lg border border-slate-300 dark:border-slate-600 px-3 py-2 hover:bg-slate-50 dark:hover:bg-slate-800">{escape(next_link[1])} →</a>' if next_link else ''}
                    </div>
                </div>
            </article>
        </div>
    </main>

    <footer class="mt-8 bg-white shadow-inner dark:bg-slate-900/90">
        <div class="container mx-auto px-6 py-8 text-center text-slate-600 dark:text-slate-400">
            <p class="text-base font-semibold text-ifsc-green">GE2014902 - GEOPROCESSAMENTO 2 - T01</p>
            <p class="text-sm">Curso Técnico em Geoprocessamento · DACC - IFSC Florianópolis</p>
            <p class="text-sm">Professor responsável: Arthur Berbert</p>
            <p class="text-xs text-slate-400 mt-2">Versão 2026.1</p>
        </div>
    </footer>

    <script src="https://unpkg.com/lucide@latest"></script>
    <script src="main.js"></script>
    <script>lucide.createIcons();</script>
</body>
</html>
"""


def main() -> None:
    ensure_dir(OUTPUT_IMG_BASE)
    full = read_original_html()
    chapters = extract_chapters(full)
    print(f"Capítulos encontrados: {len(chapters)}")

    # Prepare metadata for prev/next nav
    meta_list = []
    for idx, ch in enumerate(chapters):
        num, title = parse_chapter_meta(ch['h1_inner'])
        if not num:
            num = idx + 1
        if not title:
            title = f"Capítulo {num}"
        meta_list.append((num, title))

    # Generate each chapter with TOC and navigation
    total = len(meta_list)
    for idx, ch in enumerate(chapters):
        num, title = parse_chapter_meta(ch['h1_inner'])
        if not num:
            num = idx + 1
        if not title:
            title = f"Capítulo {num}"

        body_raw = ch['content']
        body_imgs = copy_and_rewrite_images(body_raw, num)
        body_clean, toc = sanitize_and_build_toc(body_imgs)

        prev_link = None
        next_link = None
        if idx > 0:
            pnum, ptitle = meta_list[idx - 1]
            prev_link = (f"capitulo-{pnum:02d}.html", ptitle)
        if idx + 1 < total:
            nnum, ntitle = meta_list[idx + 1]
            next_link = (f"capitulo-{nnum:02d}.html", ntitle)

        html_out = build_chapter_html_with_layout(
            chapter_num=num,
            chapter_title=title,
            body_html=body_clean,
            chapter_description='',
            toc_items=toc,
            prev_link=prev_link,
            next_link=next_link,
            total_chapters=total,
        )

        out_name = f"capitulo-{num:02d}.html"
        out_path = os.path.join(OUTPUT_DIR, out_name)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html_out)
        print(f"Gerado: {os.path.relpath(out_path, REPO_ROOT)}")


if __name__ == '__main__':
    main()
