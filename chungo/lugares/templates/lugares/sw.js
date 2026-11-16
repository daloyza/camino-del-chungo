// Service Worker: muestra los avisos de cercanía y abre el lugar al tocarlos.
// Se sirve desde /sw.js (ver views.service_worker) para tener alcance en toda la app.

self.addEventListener("install", function () {
    self.skipWaiting();
});

self.addEventListener("activate", function (evento) {
    evento.waitUntil(self.clients.claim());
});

// Al tocar el aviso: abre el lugar (o "cerca de ti") en una pestaña de la app
self.addEventListener("notificationclick", function (evento) {
    evento.notification.close();
    const url = (evento.notification.data && evento.notification.data.url) || "{% url 'cerca' %}";

    evento.waitUntil(
        self.clients.matchAll({ type: "window", includeUncontrolled: true }).then(function (pestanas) {
            for (const pestana of pestanas) {
                if ("navigate" in pestana) {
                    return pestana.navigate(url).then(p => (p || pestana).focus());
                }
            }
            return self.clients.openWindow(url);
        })
    );
});
