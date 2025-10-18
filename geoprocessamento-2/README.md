# README.md

# Geoprocessamento 2 - Livro Digital

Este projeto é um livro digital interativo da disciplina **Geoprocessamento 2 (GE2014902)**, desenvolvido como uma **Progressive Web App (PWA)**. O objetivo é fornecer um material de estudo acessível, responsivo e funcional offline, seguindo as diretrizes de design do IFSC.

## Estrutura do Projeto

O projeto é organizado da seguinte forma:

```
geoprocessamento-2
├── index.html                # Página principal com o sumário do livro
├── capitulo-01.html         # Conteúdo do Capítulo 1
├── capitulo-02.html         # Conteúdo do Capítulo 2
├── capitulo-03.html         # Conteúdo do Capítulo 3
├── capitulo-04.html         # Conteúdo do Capítulo 4
├── capitulo-05.html         # Conteúdo do Capítulo 5
├── estilos.css               # Estilos CSS para o PWA
├── main.js                   # Lógica principal do JavaScript
├── scripts                   # Scripts adicionais
│   ├── sql.js-wasm          # WebAssembly para SQL.js
│   ├── sql-playground.js     # Lógica do playground SQL
│   └── svg-interactions.js   # Interatividade de elementos SVG
├── dados                     # Dados utilizados no projeto
│   └── banco_exemplo.sqlite   # Banco de dados SQLite de exemplo
├── imagens                   # Imagens utilizadas no projeto
│   ├── logotipos             # Logotipos da instituição
│   └── capitulos             # Imagens dos capítulos
├── manifest.webmanifest      # Manifesto da PWA
├── service-worker.js         # Lógica de cache para funcionalidade offline
├── icons                     # Ícones da PWA
│   └── .gitkeep              # Placeholder para controle de versão
└── Original                  # Diretório com os arquivos originais
```

## Funcionalidades

- **Acessibilidade Offline**: Todo o conteúdo é acessível mesmo sem conexão à internet após o primeiro carregamento.
- **Interatividade**: Inclui um playground SQL para execução de consultas diretamente no navegador e visualizações geoespaciais interativas usando SVG.
- **Responsividade**: O design é otimizado para funcionar em dispositivos móveis, tablets e desktops.
- **Identidade Visual**: O projeto segue as diretrizes de identidade visual do IFSC, garantindo uma apresentação consistente.

## Como Usar

1. **Clone o repositório**:
   ```bash
   git clone <URL do repositório>
   cd geoprocessamento-2
   ```

2. **Abra o arquivo `index.html` em um navegador** para acessar o sumário e navegar pelos capítulos.

3. **Instale como PWA**: O aplicativo pode ser instalado em dispositivos móveis e desktops para acesso rápido.

## Converter o arquivo original (Word/HTML) em capítulos

Para transformar `Original/Apostila Geoprocessamento 2 vs2.3.htm` no conjunto de páginas da PWA:

1) Pré-requisito: Python 3.x (um ambiente virtual já está configurado no VS Code).

2) Execute o conversor (Windows PowerShell):

```
& "D:/GitHub/Livro Banco de Dados/.venv/Scripts/python.exe" "d:\GitHub\Livro Banco de Dados\tools\convert_original_to_pwa.py"
```

O que o script faz:
- Divide o HTML original por `<h1>` (capítulos);
- Copia imagens de `Original/*_arquivos` para `geoprocessamento-2/imagens/capitulos/capitulo-XX/`;
- Reescreve os caminhos das imagens;
- Gera arquivos `capitulo-0N.html` com o template da PWA.

Se renomear o arquivo original, ajuste os caminhos no script `tools/convert_original_to_pwa.py`.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).