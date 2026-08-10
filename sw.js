const CACHE = "metal-terminal-v2-1";
const CORE = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./data/latest.json",
  "./icons/icon-192.png",
  "./icons/icon-512.png"
];

self.addEventListener("install", event => {
  event.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)));
  self.skipWaiting();
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", event => {
  const req = event.request;
  if (req.method !== "GET") return;

  // JSON: network first, cache fallback
  if (req.url.includes("/data/latest.json")) {
    event.respondWith(
      fetch(req).then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put("./data/latest.json", copy));
        return res;
      }).catch(() => caches.match("./data/latest.json"))
    );
    return;
  }

  // App shell: cache first, network fallback
  event.respondWith(
    caches.match(req).then(cached => cached || fetch(req).then(res => {
      const copy = res.clone();
      caches.open(CACHE).then(c => c.put(req, copy));
      return res;
    }).catch(() => caches.match("./index.html")))
  );
});