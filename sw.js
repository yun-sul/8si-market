/* 8시마켓 시제품 — PWA 최소 서비스 워커
   캐시는 하지 않고 네트워크 응답을 그대로 사용합니다. (항상 최신 시제품이 보이도록) */
self.addEventListener('install', function(){ self.skipWaiting(); });
self.addEventListener('activate', function(e){ e.waitUntil(self.clients.claim()); });
self.addEventListener('fetch', function(){});
