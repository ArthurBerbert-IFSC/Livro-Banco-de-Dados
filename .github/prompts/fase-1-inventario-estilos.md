# Fase 1 — Inventário de Estilos (Piloto)

## 1) Componentes mapeados no piloto

### Estrutura base
- Shell de página: html/body + tema dark via classe no elemento raiz.
- Header institucional com logotipos, identificação da disciplina e botão de tema.
- Conteúdo principal com container central.
- Footer institucional padronizado.

### Home (sumário)
- Grid de cartões de capítulos com classes customizadas:
  - chapter-card
  - chapter-number
  - chapter-title
  - chapter-description
- Ícones Lucide em setas e toggle de tema.

### Capítulo 01
- Layout em duas colunas no desktop: sumário lateral + artigo.
- Tipografia de conteúdo com Tailwind Typography + extensões custom:
  - prose-justificado
  - prose-indent
- Conteúdo rico com tabelas e imagens oriundas da conversão.

## 2) Achados críticos (priorizados)

### P0 — Dependência externa sem garantia offline total
- Páginas dependem de CDN para Tailwind, Prism e Lucide.
- Esses assets não estão no precache explícito do service worker.
- Impacto: risco de quebra visual/funcional offline após limpeza de cache/primeira carga incompleta.

Referências:
- [index.html](../../index.html#L9-L13)
- [capitulo-01.html](../../capitulo-01.html#L9-L10)
- [capitulo-01.html](../../capitulo-01.html#L1380-L1382)
- [service-worker.js](../../service-worker.js#L1-L24)

### P0 — Arquitetura CSS monolítica com seletores globais
- O CSS central mistura base, layout, componentes e tipografia editorial no mesmo arquivo.
- Uso de seletores globais (body/header/container/footer) aumenta risco de conflito com utilitários Tailwind.

Referências:
- [estilos.css](../../estilos.css#L1-L76)
- [estilos.css](../../estilos.css#L79-L159)

### P1 — Classes usadas sem definição no CSS local
- Classes usadas no HTML e sem estilo local identificado:
  - theme-toggle, sun-icon, moon-icon, chapter-arrow
- Classe tooltip é criada por JS e também sem estilo local identificado.

Referências:
- [index.html](../../index.html#L47-L49)
- [index.html](../../index.html#L70)
- [scripts/svg-interactions.js](../../scripts/svg-interactions.js#L9-L14)

### P1 — Duplicação estrutural entre capítulos
- Configuração de Tailwind repetida em todos os capítulos e também no index.
- Estruturas de header/footer e bootstrap visual repetidas em múltiplos HTML.

Referências:
- [index.html](../../index.html#L16-L30)
- [capitulo-01.html](../../capitulo-01.html#L14-L22)
- [capitulo-02.html](../../capitulo-02.html#L14)
- [capitulo-03.html](../../capitulo-03.html#L14)
- [capitulo-04.html](../../capitulo-04.html#L14)
- [capitulo-05.html](../../capitulo-05.html#L14)
- [capitulo-06.html](../../capitulo-06.html#L14)
- [capitulo-07.html](../../capitulo-07.html#L14)
- [capitulo-08.html](../../capitulo-08.html#L14)

## 3) Conflitos e fragilidades observadas
- Tema híbrido: background/text no body definidos ao mesmo tempo por utilitários Tailwind no HTML e por CSS global.
- Regras dark em seletores globais (.dark body, .dark header) podem disputar precedência com classes utilitárias no markup.
- Conteúdo convertido traz elementos com marcação legada (ex.: br clear=all), o que dificulta previsibilidade visual em capítulos longos.

Referências:
- [estilos.css](../../estilos.css#L1-L8)
- [estilos.css](../../estilos.css#L61-L76)
- [capitulo-01.html](../../capitulo-01.html#L1350-L1360)

## 4) Decisões de arquitetura recomendadas para Fase 2
- Separar estilos por camadas no CSS:
  - base/tokens
  - layout
  - componentes
  - tema/estados
  - tipografia de conteúdo
- Reduzir regras globais em favor de classes de escopo.
- Definir contrato visual para componentes do piloto antes de replicar.
- Padronizar origem de template no conversor Python.

Referências:
- [_dev/tools/convert_original_to_pwa.py](../../_dev/tools/convert_original_to_pwa.py#L289-L420)

## 5) Pronto para iniciar Fase 2
Entrada validada para implementação:
- Inventário de componentes fechado para index + capítulo 01.
- Principais riscos e duplicações mapeados.
- Prioridades técnicas (P0/P1) definidas para começar refatoração com baixo risco.
