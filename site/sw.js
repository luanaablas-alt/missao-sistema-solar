/* Guarda o jogo no aparelho para abrir rápido e funcionar sem internet. */
var CACHE="mss-9954855ffb",FILES=["/", "/index.html", "/privacidade", "/termos", "/manifest.webmanifest", "/vendor/three-r128.min.js", "/fonts/atkinson-hyperlegible-latin-400-normal.woff2", "/fonts/atkinson-hyperlegible-latin-700-normal.woff2", "/fonts/fredoka-latin-500-normal.woff2", "/fonts/fredoka-latin-600-normal.woff2", "/fonts/fredoka-latin-700-normal.woff2", "/tex/earth.jpg", "/tex/jupiter.jpg", "/tex/mars.jpg", "/tex/mercury.jpg", "/tex/moon.jpg", "/tex/neptune.jpg", "/tex/saturn.jpg", "/tex/sun.jpg", "/tex/uranus.jpg", "/tex/venus.jpg", "/icons/apple-touch-icon.png", "/icons/icon-192.png", "/icons/icon-512.png", "/icons/maskable-512.png"];
self.addEventListener("install",function(e){e.waitUntil(caches.open(CACHE).then(function(c){return c.addAll(FILES);}).then(function(){return self.skipWaiting();}));});
self.addEventListener("activate",function(e){e.waitUntil(caches.keys().then(function(ks){return Promise.all(ks.filter(function(k){return k!==CACHE;}).map(function(k){return caches.delete(k);}));}).then(function(){return self.clients.claim();}));});
self.addEventListener("fetch",function(e){
  var r=e.request;if(r.method!=="GET"||new URL(r.url).origin!==location.origin)return;
  if(r.mode==="navigate"){e.respondWith(fetch(r).then(function(res){var cp=res.clone();caches.open(CACHE).then(function(c){c.put(r,cp);});return res;}).catch(function(){return caches.match(r).then(function(m){return m||caches.match("/index.html");});}));return;}
  e.respondWith(caches.match(r).then(function(m){return m||fetch(r);}));
});
