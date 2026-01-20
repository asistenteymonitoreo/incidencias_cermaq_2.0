const CACHE_NAME = 'cermaq-v1';
const ASSETS = [
    '/',
    '/static/css/formulario.css',
    '/static/imagenes/logo-pestaña.png'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(ASSETS);
        })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});
