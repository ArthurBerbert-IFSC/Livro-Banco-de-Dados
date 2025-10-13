Guia Mestre do Agente: Livro Digital de Geoprocessamento 2 (PWA)
1. Objetivo Principal e Visão Geral
Atuar como desenvolvedor web especialista em conteúdo educacional para criar o livro digital da disciplina GE2014902 - GEOPROCESSAMENTO 2 - T01.
O projeto final será uma Progressive Web App (PWA) offline-first, composta por um conjunto de páginas HTML estáticas. O objetivo é criar um material de estudo interativo, responsivo e 100% funcional sem conexão à internet após o primeiro carregamento, seguindo o padrão de design institucional do IFSC.
Características Principais:
 * Disciplina: Geoprocessamento 2 (GE2014902)
 * Professor Responsável: Arthur Berbert
 * Versão: 2026.1
 * Identidade Visual: Padrão IFSC (logotipos, paleta de cores verde).
 * Tecnologia: PWA com Service Worker para cache de todos os recursos.
2. Princípios Inegociáveis
 * PWA Offline-First: O aplicativo deve ser instalável e todo o conteúdo, incluindo recursos interativos, deve funcionar perfeitamente offline.
 * Estrutura Multi-Arquivo Limpa: Cada capítulo em seu próprio arquivo HTML (capitulo-01.html, etc.), com caminhos relativos.
 * Responsividade: Layout impecável em celulares, tablets e desktops.
 * Clareza e Legibilidade: Design limpo e focado na experiência de leitura.
 * Semântica HTML5: Uso correto das tags estruturais.
 * Identidade Visual IFSC: Consistência com a marca da instituição.
3. Estrutura de Arquivos Sugerida
A estrutura deve acomodar os recursos da PWA e os componentes interativos offline.
/geoprocessamento-2/
│-- index.html
│-- capitulo-01.html
│-- capitulo-02.html
│-- ...
│
│-- estilos.css
│-- main.js
│
│-- /scripts/
│   └── sql.js-wasm            # Arquivo WebAssembly para o SQL.js
│
│-- /dados/
│   └── banco_exemplo.sqlite   # Pequeno banco de dados para o playground SQL
│
│-- /imagens/
│   ├── /logotipos/
│   └── /capitulos/
│
│-- manifest.webmanifest       # Manifesto da PWA
│-- service-worker.js          # Lógica de cache offline
│-- /icons/
    └── ... (ícones da PWA em vários tamanhos)

4. Layout Canônico da Página HTML
Cada capítulo deve seguir esta estrutura base.
4.1. Bloco <head>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="manifest" href="manifest.webmanifest">
    <title>{{Título do Capítulo}} — Geoprocessamento 2</title>

    <!-- Scripts e Estilos (CDN com fallback local, cacheados pelo Service Worker) -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-okaidia.min.css" rel="stylesheet">
    <link rel="stylesheet" href="estilos.css">

    <!-- Configuração do Tailwind (pode ser movida para um arquivo JS) -->
    <script>
      tailwind.config = { /* ... mesma configuração do IFSC ... */ }
    </script>
</head>

4.2. Estrutura do <body>
A estrutura do corpo permanece a mesma, garantindo consistência: barra de progresso, header, main (com aside para o sumário e article para o conteúdo) e footer. O conteúdo do cabeçalho e rodapé deve ser atualizado:
 * Cabeçalho: O título principal deve ser "Geoprocessamento 2" ou "Bancos de Dados Espaciais".
 * Rodapé: O código da disciplina deve ser "GE2014902", e a versão "2026.1".
5. Componentes Didáticos e Estilo
Os blocos didáticos podem variar, mas aqui estão sugestões temáticas e flexíveis.
5.1. Ícones Temáticos (Lucide)
| Função do Ícone | Sugestão (Lucide) |
|---|---|
| Conceito de Banco de Dados | database, archive |
| Dados Espaciais / Vetoriais | map-pin, move-3d |
| Dados Matriciais / Raster | layers, grid-2x2 |
| Consulta SQL | file-code, terminal-square |
| Análise / Workflow | workflow, line-chart |
| Topologia / Relações | link, git-merge |
5.2. Blocos Didáticos Sugeridos
Além dos blocos padrão (Dica, Atenção, Conceito), adicione estes:
| Tipo | Classes Tailwind Sugeridas | Ícone Lucide | Observação |
|---|---|---|---|
| Caixa de Consulta | border border-sky-300 dark:border-sky-700 bg-sky-50 dark:bg-sky-900/40 rounded-xl | file-code | Um contêiner para apresentar exemplos de código SQL. |
| Resultado da Consulta | font-mono text-xs bg-slate-100 dark:bg-slate-800 p-4 rounded-lg overflow-x-auto | table-2 | Ideal para mostrar o output de uma query em formato de tabela ou texto. |
Flexibilidade dos Blocos: Lembre-se que estes são pontos de partida. Você pode combinar estilos (ex: uma "Dica" com um exemplo de "Consulta" dentro) ou criar novas variações conforme o conteúdo exigir. O importante é manter a consistência visual.
6. Recursos Interativos (Offline-First)
A abordagem PWA permite interatividade rica, desde que todos os recursos sejam cacheados pelo service-worker.js.
6.1. SQL Playground Offline com sql.js
Incorpore um ambiente interativo para executar consultas SQL diretamente no navegador.
 * Como funciona:
   * Use a biblioteca sql.js (um port do SQLite para WebAssembly).
   * No primeiro acesso, o service-worker.js cacheia a biblioteca e um arquivo de banco de dados de exemplo (banco_exemplo.sqlite).
   * A página do capítulo carrega o banco de dados em memória.
   * O aluno digita uma consulta SQL em um <textarea>.
   * O sql.js executa a consulta no navegador, sem precisar de um servidor.
   * O resultado é exibido dinamicamente em uma tabela HTML no bloco "Resultado da Consulta".
 * Benefício: Aprendizado prático e imediato, totalmente offline.
6.2. Mapas Vetoriais Interativos com SVG
Para visualizações geoespaciais sem depender de serviços de mapa online (como Google Maps ou OpenStreetMap), use SVG.
 * Como funciona:
   * Exporte uma camada de dados simples (ex: limites de bairros, localização de pontos) como um arquivo SVG.
   * Incorpore o SVG diretamente no HTML. Cada polígono ou ponto no SVG pode ter um id.
   * Use JavaScript para adicionar interatividade:
     * Mudar a cor de uma feição ao passar o mouse (mouseover).
     * Exibir uma "tooltip" com informações ao clicar em uma feição (click).
     * Filtrar ou destacar feições com base em controles na página.
 * Benefício: Visualizações geográficas leves, personalizáveis e 100% offline.
7. Lógica da PWA (service-worker.js)
O service-worker.js é o coração da funcionalidade offline. Ele deve ser configurado para:
 * Pré-cache na Instalação: Armazenar todos os arquivos essenciais (.html, .css, .js, imagens, ícones, manifest.webmanifest, o arquivo .sqlite e o sql.js-wasm) quando o usuário visita o site pela primeira vez.
 * Estratégia de Cache: Usar uma estratégia "Cache First" para o conteúdo do livro, garantindo que ele sempre carregue da versão local.
 * Atualização em Segundo Plano: Verificar se há uma nova versão do livro e atualizá-la silenciosamente, notificando o usuário de que uma nova versão está pronta para ser ativada.
Este guia fornece uma base sólida e moderna para o seu novo livro digital. Ele não apenas padroniza o visual, mas também eleva a experiência de aprendizado com interatividade real e funcionalidade offline robusta.
