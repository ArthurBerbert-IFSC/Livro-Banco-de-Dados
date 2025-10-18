self.addEventListener('install', (event) => {
    const PRECACHE = 'geoprocessamento-v3';
    event.waitUntil(
        caches.open(PRECACHE).then((cache) => {
            return cache.addAll([
                './',
                './index.html',
                './capitulo-01.html',
                './capitulo-02.html',
                './capitulo-03.html',
                './capitulo-04.html',
                './capitulo-05.html',
                './capitulo-06.html',
                './capitulo-07.html',
                './estilos.css',
                './main.js',
                './scripts/sql.js-wasm',
                './dados/banco_exemplo.sqlite',
                './manifest.webmanifest',
                // Logotipos
                './imagens/logotipos/florianopolis_horizontal_marca2015_PNG.png',
                './imagens/logotipos/Logo_Disciplina_5.png',
            ]);
        })
    );
});

self.addEventListener('fetch', (event) => {
    const req = event.request;
    // Cache First para imagens do projeto
    if (req.destination === 'image' || /\/imagens\//.test(req.url)) {
        event.respondWith(
            caches.match(req).then((cached) => cached || fetch(req).then((resp) => {
                const clone = resp.clone();
                caches.open('geoprocessamento-v3').then((c) => c.put(req, clone));
                return resp;
            }))
        );
        return;
    }
    // Default: Cache falling back to network
    event.respondWith(
        caches.match(req).then((resp) => resp || fetch(req))
    );
});

self.addEventListener('activate', (event) => {
    const cacheWhitelist = ['geoprocessamento-v3'];
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheWhitelist.indexOf(cacheName) === -1) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});