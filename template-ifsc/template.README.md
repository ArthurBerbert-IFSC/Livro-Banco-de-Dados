# Template IFSC para Série de Livros

Este diretório concentra os arquivos que definem o padrão visual e técnico dos livros.

## Arquivos centrais (fonte única)

- template.estilos.v2.css
- template.main.v2.js
- template.manifest.webmanifest
- template.service-worker.js
- template.offline.html
- template.chapter.html
- template.agentes-ifsc.md

## Como gerenciar em um único lugar

## Regra obrigatória de execução (para agentes e humanos)

Sempre executar em 2 etapas:

1. **Prévia sem alteração** (`-DryRun`)
2. **Aplicação real** (sem `-DryRun`)

Fluxo padrão no repositório de destino:

```powershell
.\template-ifsc\template.apply-to-book.ps1 -TargetBookPath "." -DryRun
.\template-ifsc\template.apply-to-book.ps1 -TargetBookPath "."
```

### Opção recomendada (mais simples)

1. Escolha **um repositório mestre** com a pasta `template-ifsc`.
2. Em cada livro novo, copie a pasta `template-ifsc`.
3. Rode o script `template.apply-to-book.ps1` para atualizar os arquivos globais do livro.

Exemplo:

```powershell
.\template-ifsc\template.apply-to-book.ps1 -TargetBookPath "D:\GitHub\OutroLivro"
```

Pré-visualização sem alterar arquivos:

```powershell
.\template-ifsc\template.apply-to-book.ps1 -TargetBookPath "D:\GitHub\OutroLivro" -DryRun
```

### Opção avançada (vários livros em paralelo)

Use a pasta `template-ifsc` como submódulo Git ou subtree em cada projeto de livro. Assim, você versiona o padrão e aplica updates controlados.

## Estratégia de manutenção segura

- Centralize somente o que é global: CSS, JS, PWA e template de capítulo.
- Mantenha conteúdo dos capítulos separado por livro.
- Sempre execute `-DryRun` antes de atualizar um livro já em produção.
- Se mudar `template.service-worker.js`, revise lista de assets de cada livro.

## Fluxo sugerido

1. Ajuste padrão no repositório mestre em `template-ifsc`.
2. Versione (Git).
3. Em cada livro, atualize a pasta `template-ifsc`.
4. Execute primeiro em `-DryRun`, depois execute sem `-DryRun`.
5. Valide navegação, tema, TOC e offline.
