# Padrão Oficial da Série de Livros (IFSC Digital Book)

Este arquivo é a **fonte única de padrão editorial e técnico** para agentes de IA que criarem ou revisarem capítulos desta série.

## 1) Objetivo

Garantir que todos os livros/capítulos mantenham o mesmo layout, comportamento e identidade visual do projeto atual.

## 2) Regra de Ouro para Agentes

Ao criar ou editar capítulos HTML:

1. **Manter a estrutura base obrigatória**:
   - `#reading-progress`
   - `header` institucional com 4 logotipos e `onerror="this.style.display='none'"`
   - `main` com `aside` (`#toc-list`) + `article`
   - `footer` padronizado
2. **Não criar CSS inline** para substituir regras globais.
3. **Usar somente**:
   - `estilos.v2.css`
   - `main.v2.js`
   - Tailwind CDN
   - Prism (tema okaidia)
   - Lucide icons
4. **Todo bloco de código** deve usar `.code-block` ou `.code-container` + classe `language-*`.
5. Toda seção relevante precisa de `data-toc="section"` com `<h2>`/`<h3>` claros e IDs únicos.
6. Navegação entre capítulos deve manter links `Anterior/Próximo` consistentes.
7. Caminhos sempre relativos e compatíveis com uso offline.

## 3) Head Canônico (obrigatório)

Todo capítulo deve conter:

- `<meta charset="UTF-8">`
- `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- `<meta name="color-scheme" content="light dark">`
- `<script src="https://cdn.tailwindcss.com"></script>`
- `<link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-okaidia.min.css" rel="stylesheet">`
- `<link rel="stylesheet" href="estilos.v2.css">`
- script de configuração Tailwind com cores IFSC

## 4) Script Canônico no fim do Body

Incluir nesta ordem:

```html
<script src="https://unpkg.com/lucide@latest"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
<script src="main.v2.js"></script>
<script>
  lucide.createIcons();
</script>
```

## 5) O que pode ficar centralizado em arquivo único

### Seguro centralizar

- `estilos.v2.css` (cores, tipografia, spacing, responsividade, widgets)
- `main.v2.js` (tema, TOC, barra de leitura, cópia de código, PWA)
- `manifest.webmanifest`, `service-worker.js`, `offline.html`

### Não é ideal centralizar sem cuidado

- Todo o HTML de cada capítulo em um único arquivo compartilhado.

Motivo: capítulos possuem conteúdo e hierarquia próprios; forçar injeção total via JS aumenta acoplamento e dificulta manutenção editorial.

## 6) Estratégia recomendada para manutenção em série

1. **Template único de capítulo**: usar `template_base.html` como base de criação.
2. **CSS e JS globais**: alterações visuais/comportamentais sempre em `estilos.v2.css` e `main.v2.js`.
3. **Checklist de consistência** antes de publicar:
   - Head canônico
   - Estrutura body canônica
   - `data-toc="section"` nos blocos principais
   - Blocos de código com classe Prism
   - Links Anterior/Próximo válidos
   - Capítulo listado no `service-worker.js`

## 7) Prompt curto para usar com agentes de IA

Use este prompt quando pedir criação de novo capítulo:

> "Crie/edite este capítulo seguindo estritamente o arquivo `PADRAO-AGENTES-IFSC.md` e o `template_base.html`, mantendo o padrão IFSC Digital Book, sem CSS inline novo, sem componentes extras fora do padrão, com seções `data-toc='section'`, blocos de código compatíveis com Prism e scripts globais `main.v2.js` + `estilos.v2.css`."

## 8) Decisão sobre "um arquivo que altera todos os livros"

**Resposta curta:** sim, parcialmente.

- Para visual e comportamento global: **já é o caminho correto** (CSS/JS únicos).
- Para conteúdo completo de todos os capítulos: **evite centralização total** (risco de manutenção e regressões).

Melhor equilíbrio: **template único + CSS/JS globais**.

## 9) Regra operacional de sincronização entre livros

Quando usar a pasta `template-ifsc` em outro repositório, o agente deve seguir este fluxo obrigatório:

1. Executar pré-visualização:

```powershell
.\template-ifsc\template.apply-to-book.ps1 -TargetBookPath "." -DryRun
```

2. Confirmar que os arquivos mapeados estão corretos.
3. Executar aplicação real:

```powershell
.\template-ifsc\template.apply-to-book.ps1 -TargetBookPath "."
```

4. Validar navegação, tema, TOC, cópia de código e offline.

Nunca aplicar diretamente sem `-DryRun` em livros já publicados.
