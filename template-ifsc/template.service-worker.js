'use strict';

const CACHE_VERSION = 'geoprocessamento-2-v2026.1.1';
const CORE_ASSETS = [
  './',
  './index.html',
  './capitulo-01.html',
  './capitulo-01-quiz.html',
  './capitulo-02.html',
  './capitulo-03.html',
  './capitulo-04.html',
  './capitulo-05.html',
  './capitulo-06.html',
  './capitulo-07.html',
  './capitulo-08.html',
  './offline.html',
  './manifest.webmanifest',
  './estilos.css',
  './estilos-pico.css',
  './estilos.v2.css',
  './main.js',
  './main.v2.js',
  './scripts/pico.min.css',
  './scripts/sql-playground.js',
  './scripts/sql.js-wasm',
  './scripts/svg-interactions.js',
  './dados/banco_exemplo.sqlite'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_VERSION)
      .then((cache) => cache.addAll(CORE_ASSETS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.filter((key) => key !== CACHE_VERSION).map((key) => caches.delete(key))
      )
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') {
    return;
  }

  const { request } = event;

  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((response) => {
          const copy = response.clone();
          caches.open(CACHE_VERSION).then((cache) => cache.put(request, copy));
          return response;
        })
        .catch(() => caches.match(request).then((cached) => cached || caches.match('./offline.html')))
    );
    return;
  }

  event.respondWith(
    caches.match(request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }

      return fetch(request)
        .then((networkResponse) => {
          if (
            !networkResponse ||
            networkResponse.status !== 200 ||
            networkResponse.type === 'opaque'
          ) {
            return networkResponse;
          }

          const responseClone = networkResponse.clone();
          caches.open(CACHE_VERSION).then((cache) => cache.put(request, responseClone));
          return networkResponse;
        })
        .catch(() => caches.match('./offline.html'));
    })
  );
});
