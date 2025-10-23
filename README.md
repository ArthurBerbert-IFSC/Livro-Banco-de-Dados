# README.md

# Geoprocessamento 2 - Livro Digital

Este projeto é um livro digital interativo da disciplina **Geoprocessamento 2 (GE2014902)**, desenvolvido como uma **Progressive Web App (PWA)**. O objetivo é fornecer um material de estudo acessível, responsivo e funcional offline, seguindo as diretrizes de design do IFSC.

## Estrutura do Projeto

O projeto está organizado como uma Progressive Web App (PWA) na raiz do repositório:

```
/
├── index.html                # Página principal com o sumário
├── capitulo-01.html         # Capítulo 1: Fundamentos de Bancos de Dados
├── capitulo-02.html         # Capítulo 2: Modelagem de Dados
├── capitulo-03.html         # Capítulo 3: Bancos de Dados GeoPackage
├── capitulo-04.html         # Capítulo 4: Fundamentos do SQL
├── capitulo-05.html         # Capítulo 5: Banco de Dados com PostGIS
├── capitulo-06.html         # Capítulo 6: Padronizar Campos
├── capitulo-07.html         # Capítulo 7: PostGIS Avançado
├── estilos.css               # Estilos CSS customizados
├── main.js                   # JavaScript principal (tema, scrollspy)
├── service-worker.js         # Service Worker para cache offline
├── manifest.webmanifest      # Manifesto da PWA
├── imagens/                  # Recursos visuais
│   ├── logotipos/           # Logos IFSC e da disciplina
│   └── capitulos/           # Imagens organizadas por capítulo
├── scripts/                  # Scripts adicionais
│   ├── sql.js-wasm          # WebAssembly para SQL.js
│   ├── sql-playground.js     # Playground SQL interativo
│   └── svg-interactions.js   # Interatividade com mapas SVG
├── dados/                    # Bancos de dados de exemplo
│   └── banco_exemplo.sqlite
├── icons/                    # Ícones da PWA (vários tamanhos)
├── _dev/                     # Arquivos de desenvolvimento
│   ├── Original/            # Arquivo-fonte Word exportado
│   └── tools/               # Scripts de conversão (Python)
├── AGENTS.md                 # Documentação para desenvolvimento
└── README.md                 # Este arquivo
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
   cd Livro-Banco-de-Dados
   ```

2. **Abra o arquivo `index.html`** diretamente no navegador ou use um servidor local:
   ```bash
   # Python 3
   python -m http.server 8000
   
   # Ou com Node.js
   npx serve
   ```

3. **Acesse no navegador**: 
   - Diretamente: `file:///caminho/para/index.html`
   - Com servidor: `http://localhost:8000`

4. **Instale como PWA** (opcional): 
   - No Chrome/Edge, clique no ícone de instalação na barra de endereços
   - A aplicação ficará disponível offline após a primeira visita

## Para Desenvolvedores

### Regenerar Capítulos

Se você precisar regenerar os capítulos a partir do arquivo-fonte:

```bash
# Ative o ambiente virtual Python (se necessário)
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Execute o conversor
python _dev/tools/convert_original_to_pwa.py
```

O script irá:
- Ler o arquivo `_dev/Original/Apostila Geoprocessamento 2 vs2.3.htm`
- Dividir por capítulos (tags `<h1>`)
- Copiar e otimizar imagens para `imagens/capitulos/`
- Gerar os arquivos `capitulo-XX.html` na raiz com layout PWA completo

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