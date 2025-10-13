// Lógica para alternância de tema (light/dark)
const themeToggle = document.getElementById('theme-toggle');

const applyTheme = (theme) => {
    if (theme === 'dark') {
        document.documentElement.classList.add('dark');
        document.documentElement.classList.remove('light');
    } else {
        document.documentElement.classList.remove('dark');
        document.documentElement.classList.add('light');
    }
};

themeToggle.addEventListener('click', () => {
    const isDark = document.documentElement.classList.contains('dark');
    const newTheme = isDark ? 'light' : 'dark';
    localStorage.setItem('theme', newTheme);
    applyTheme(newTheme);
});

// Aplica o tema salvo ou o do sistema ao carregar a página
const savedTheme = localStorage.getItem('theme');
const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
applyTheme(savedTheme || (systemPrefersDark ? 'dark' : 'light'));


// Lógica para a barra de progresso de leitura
const readingProgress = document.getElementById('reading-progress');
const chapterContent = document.getElementById('chapter-content');

if (readingProgress && chapterContent) {
    window.addEventListener('scroll', () => {
        const contentRect = chapterContent.getBoundingClientRect();
        const viewportHeight = window.innerHeight;
        
        // Distância do topo do conteúdo até o topo da viewport
        const top = contentRect.top;
        // Altura total do conteúdo
        const height = contentRect.height;

        // Quanto do conteúdo já passou pela viewport
        let scrolled = Math.max(0, viewportHeight - top);
        
        // Percentual de progresso
        let progress = Math.min(1, scrolled / (height + viewportHeight));

        readingProgress.style.transform = `scaleX(${progress})`;
    });
}

// Lógica para gerar o Sumário Lateral (TOC) dinamicamente
const tocList = document.getElementById('toc-list');
if (tocList && chapterContent) {
    const sections = chapterContent.querySelectorAll('section[data-toc-section]');
    
    if (sections.length > 0) {
        tocList.innerHTML = ''; // Limpa o "Carregando..."
        
        sections.forEach((section, index) => {
            const heading = section.querySelector('h2, h3');
            if (heading) {
                const id = heading.id || `section-${index}`;
                heading.id = id;

                const listItem = document.createElement('li');
                const link = document.createElement('a');
                link.href = `#${id}`;
                link.textContent = heading.textContent;
                link.dataset.targetId = id;
                listItem.appendChild(link);
                tocList.appendChild(listItem);
            }
        });
    } else {
        tocList.innerHTML = '<li>Nenhuma seção encontrada.</li>';
    }

    // Lógica para destacar o item ativo no TOC ao rolar
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            const link = tocList.querySelector(`a[data-target-id="${entry.target.id}"]`);
            if (link) {
                if (entry.isIntersecting && entry.intersectionRatio > 0.1) {
                    tocList.querySelectorAll('a').forEach(a => a.classList.remove('active'));
                    link.classList.add('active');
                } else {
                    link.classList.remove('active');
                }
            }
        });
    }, { rootMargin: "-50% 0px -50% 0px", threshold: 0.1 });

    sections.forEach(section => {
        const heading = section.querySelector('h2, h3');
        if (heading) observer.observe(heading);
    });
}

