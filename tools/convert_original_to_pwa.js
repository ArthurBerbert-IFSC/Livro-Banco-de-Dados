/*
  Converter: Original Word HTML -> PWA Chapters
  - Splits by top-level <h1> (chapters)
  - Preserves inner HTML (tables, images, inline styles)
  - Copies images from Original/..._arquivos to geoprocessamento-2/imagens/capitulos/capitulo-XX/
  - Rewrites <img src> to new relative paths
  - Wraps content into the standardized PWA chapter template

  Usage (from repo root):
    node tools/convert_original_to_pwa.js
*/

const fs = require('fs');
const path = require('path');

const REPO_ROOT = path.resolve(__dirname, '..');
const ORIGINAL_HTML = path.join(REPO_ROOT, 'Original', 'Apostila Geoprocessamento 2 vs2.3.htm');
const ORIGINAL_ASSETS_DIR = path.join(REPO_ROOT, 'Original', 'Apostila Geoprocessamento 2 vs2.3_arquivos');
const OUTPUT_DIR = path.join(REPO_ROOT, 'geoprocessamento-2');
const OUTPUT_IMG_BASE = path.join(OUTPUT_DIR, 'imagens', 'capitulos');

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

function readOriginalHtml() {
  // Attempt windows-1252 decode; fallback to latin1; final fallback to utf8
  const bytes = fs.readFileSync(ORIGINAL_HTML);
  let text;
  try {
    const { TextDecoder } = require('util');
    // Some Node versions support 'windows-1252' alias
    try {
      text = new TextDecoder('windows-1252').decode(bytes);
    } catch (e) {
      text = new TextDecoder('latin1').decode(bytes);
    }
  } catch (e) {
    // Very old Node: use Buffer decoding
    try {
      text = Buffer.from(bytes).toString('latin1');
    } catch (e2) {
      text = bytes.toString('utf8');
    }
  }
  return text;
}

function stripTags(html) {
  return html.replace(/<[^>]*>/g, '').replace(/\s+/g, ' ').trim();
}

function extractChapters(fullHtml) {
  // Find all <h1 ...> ... </h1> occurrences and slice content per chapter
  const h1Regex = /<h1[^>]*>([\s\S]*?)<\/h1>/gi;
  const indices = [];
  let match;
  while ((match = h1Regex.exec(fullHtml)) !== null) {
    indices.push({ start: match.index, end: h1Regex.lastIndex, inner: match[1] });
  }
  if (indices.length === 0) {
    throw new Error('Nenhum <h1> encontrado no arquivo original.');
  }
  const chapters = [];
  for (let i = 0; i < indices.length; i++) {
    const startIdx = indices[i].start;
    const endIdx = i + 1 < indices.length ? indices[i + 1].start : fullHtml.length;
    const h1Inner = indices[i].inner;
    const content = fullHtml.slice(indices[i].end, endIdx);
    const fullH1Html = fullHtml.slice(indices[i].start, indices[i].end);
    chapters.push({ h1Inner, fullH1Html, content });
  }
  return chapters;
}

function parseChapterMeta(h1Inner) {
  const raw = stripTags(h1Inner);
  // Expected: "1 Fundamentos de Bancos de Dados"
  const m = raw.match(/^(\d+)\s+(.*)$/);
  if (m) {
    return { num: parseInt(m[1], 10), title: m[2].trim() };
  }
  // Fallback: no number detected
  return { num: NaN, title: raw };
}

function copyAndRewriteImages(htmlContent, chapterNum) {
  const chapterId = String(chapterNum).padStart(2, '0');
  const outDir = path.join(OUTPUT_IMG_BASE, `capitulo-${chapterId}`);
  ensureDir(outDir);

  // Replace src paths; capture the attribute value preserving quotes
  return htmlContent.replace(/(<img[^>]*?\s+src=)(["'])([^"']+)(\2)/gi, (full, prefix, quote, src, q2) => {
    // Ignore data URIs and absolute http(s)
    if (/^data:/i.test(src) || /^https?:/i.test(src)) {
      return full; // leave as-is
    }
    // src usually like "Apostila%20Geoprocessamento%202%20vs2.3_arquivos/image002.jpg"
    let decoded = src;
    try { decoded = decodeURIComponent(src); } catch (_) {}
    // If path is not absolute, join with Original directory
    const origPath = path.join(ORIGINAL_ASSETS_DIR, path.basename(decoded));
    const fileName = path.basename(decoded);
    const destPath = path.join(outDir, fileName);
    try {
      // Copy only if source exists; else try resolving relative to ORIGINAL root
      if (fs.existsSync(origPath)) {
        fs.copyFileSync(origPath, destPath);
      } else {
        const altPath = path.join(REPO_ROOT, 'Original', decoded);
        if (fs.existsSync(altPath)) {
          fs.copyFileSync(altPath, destPath);
        } else {
          console.warn(`[aviso] Imagem não encontrada: ${decoded}`);
        }
      }
    } catch (e) {
      console.warn(`[aviso] Falha ao copiar imagem: ${decoded} -> ${destPath}:`, e.message);
    }
    const relNew = path.posix.join('imagens', 'capitulos', `capitulo-${chapterId}`, fileName);
    return `${prefix}${quote}${relNew}${quote}`;
  });
}

function buildChapterHtml({ chapterNum, chapterTitle, chapterDescription, bodyHtml }) {
  const padNum = String(chapterNum).padStart(2, '0');
  const pageTitle = `${chapterTitle} — Geoprocessamento 2`;
  const headerH1 = `Capítulo ${chapterNum}: ${chapterTitle}`;
  return `<!DOCTYPE html>
<html lang="pt-BR" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="manifest" href="manifest.webmanifest">
    <title>${escapeHtml(pageTitle)}</title>

    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-okaidia.min.css" rel="stylesheet">
    <link rel="stylesheet" href="estilos.css">

    <script>
      tailwind.config = {
        darkMode: 'class',
        theme: {
          extend: {
            fontFamily: { sans: ['Inter', 'sans-serif'] },
            colors: { 'ifsc-green': '#1B5E20', 'ifsc-soft': '#E6F4EA', 'ifsc-gray': '#374151' }
          }
        }
      }
    </script>
</head>
<body class="bg-slate-50 dark:bg-slate-950 text-ifsc-gray dark:text-slate-300 antialiased">
    <header class="bg-white/95 backdrop-blur shadow-sm sticky top-0 z-40 dark:bg-slate-900/90">
        <div class="border-b border-slate-200/60 dark:border-slate-700/60">
            <div class="container mx-auto px-6 py-4 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                <div class="flex flex-wrap items-center justify-center gap-4 md:justify-start">
                    <img src="https://placehold.co/100x40/1B5E20/FFFFFF?text=IFSC" alt="Logotipo do IFSC" class="h-10 w-auto opacity-80" onerror="this.style.display='none'">
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

    <main class="container mx-auto px-6 py-12">
        <article>
            <header class="mb-12">
                <h1 class="text-4xl font-bold text-ifsc-green dark:text-emerald-300 mb-2">${escapeHtml(headerH1)}</h1>
                ${chapterDescription ? `<p class="text-lg text-slate-600 dark:text-slate-400">${escapeHtml(chapterDescription)}</p>` : ''}
            </header>
            <div class="prose max-w-none prose-slate dark:prose-invert">
            ${bodyHtml}
            </div>
        </article>
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
</html>`;
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function run() {
  ensureDir(OUTPUT_IMG_BASE);
  const full = readOriginalHtml();
  const chapters = extractChapters(full);
  console.log(`Capítulos encontrados: ${chapters.length}`);

  chapters.forEach((ch, idx) => {
    const meta = parseChapterMeta(ch.h1Inner);
    const num = isNaN(meta.num) ? idx + 1 : meta.num; // fallback sequential
    const title = meta.title || `Capítulo ${num}`;

    // Body HTML: include the original <h1> as first element? We'll remove redundant h1 since we provide header
    let body = ch.content;
    // Copy and rewrite images
    body = copyAndRewriteImages(body, num);

    const htmlOut = buildChapterHtml({
      chapterNum: num,
      chapterTitle: title,
      chapterDescription: '',
      bodyHtml: body
    });

    const outName = `capitulo-${String(num).padStart(2, '0')}.html`;
    const outPath = path.join(OUTPUT_DIR, outName);
    fs.writeFileSync(outPath, htmlOut, 'utf8');
    console.log(`Gerado: ${path.relative(REPO_ROOT, outPath)}`);
  });
}

if (require.main === module) {
  try {
    run();
  } catch (e) {
    console.error('Erro na conversão:', e);
    process.exit(1);
  }
}
