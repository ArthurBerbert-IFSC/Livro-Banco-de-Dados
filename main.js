// main.js
document.addEventListener('DOMContentLoaded', () => {
    // Theme toggle functionality
    const themeToggleButton = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme') || 'light';

    if (currentTheme === 'dark') {
        document.documentElement.classList.add('dark');
    }

    themeToggleButton.addEventListener('click', () => {
        document.documentElement.classList.toggle('dark');
        const newTheme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
        localStorage.setItem('theme', newTheme);
    });

    // Scrollspy for chapter sidebar TOC
    const toc = document.querySelector('aside nav');
    if (toc) {
        const links = Array.from(toc.querySelectorAll('a[href^="#"]'));
        const sections = links
            .map((a) => {
                try {
                    const id = decodeURIComponent(a.getAttribute('href').slice(1));
                    const el = document.getElementById(id);
                    return el ? { id, el, link: a } : null;
                } catch {
                    return null;
                }
            })
            .filter(Boolean);

        const clearActive = () => {
            links.forEach((a) => a.classList.remove('text-ifsc-green', 'dark:text-emerald-300', 'font-semibold'));
        };

        const activate = (id) => {
            clearActive();
            const target = sections.find((s) => s.id === id);
            if (target) {
                target.link.classList.add('text-ifsc-green', 'dark:text-emerald-300', 'font-semibold');
            }
        };

        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        activate(entry.target.id);
                    }
                });
            },
            {
                root: null,
                rootMargin: '0px 0px -70% 0px',
                threshold: 0.1,
            }
        );

        sections.forEach((s) => observer.observe(s.el));

        // Smooth scroll on TOC click
        links.forEach((a) => {
            a.addEventListener('click', (e) => {
                const href = a.getAttribute('href');
                if (href && href.startsWith('#')) {
                    e.preventDefault();
                    const id = href.slice(1);
                    const el = document.getElementById(id);
                    if (el) {
                        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        history.replaceState(null, '', `#${id}`);
                    }
                }
            });
        });
    }

    // Additional interactive functionalities can be added here
});