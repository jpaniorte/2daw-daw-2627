---
marp: true
theme: default
paginate: true
backgroundColor: white
footer: 'Despliegue de Aplicaciones Web (0614) · UD2: Arquitecturas Web'
layout: default
title: "Arquitecturas Web — Bloque 2.1: Fundamentos web (Prácticas)"
permalink: /web/semana-1/practicas/
---

<!-- _class: lead -->
# arquitecturas web
## Prácticas — bloque 2.1: fundamentos web

---

## Antes de empezar

- Hoy no hace falta ningún entorno especial: solo un navegador con **herramientas de desarrollador** (F12) y una terminal con `curl`.
- Hacemos los **Ejercicios 1 a 4** (miércoles) y seguimos con el resto el **viernes**, antes del cuestionario.

---

<!-- _class: lead -->
# Ejercicios guiados

---

## Ejercicio 1 — Inspecciona una petición HTTP real

1. Abre las herramientas de desarrollador del navegador (F12) → pestaña **Red/Network**.
2. Visita cualquier página web y recarga con la pestaña abierta.
3. Abre la primera petición (el documento HTML) y localiza: el **método**, el **código de estado**, las **cabeceras de petición** y las **cabeceras de respuesta**.

**Resultado esperado**: identificas el método (normalmente `GET`), el código `200`, y al menos las cabeceras `Content-Type`, `User-Agent` y `Host`.

---

## Ejercicio 2 — Lo mismo, con `curl`

```bash
curl -i https://example.com
```

1. Ejecuta el comando y localiza la línea de estado (`HTTP/1.1 200 OK` o similar) y las cabeceras de respuesta.
2. Repite con `curl -I https://example.com` (solo cabeceras, sin cuerpo).
3. Compara lo que ves aquí con lo que viste en el navegador en el Ejercicio 1.

**Resultado esperado**: entiendes que el navegador no hace "magia": por debajo es la misma petición HTTP que acabas de ver con `curl`.

---

## Ejercicio 3 — Provoca distintos códigos de estado

Usando `curl -I` (o el navegador) contra varias URLs:

1. Encuentra una URL que devuelva `200`.
2. Encuentra una URL que devuelva `404` (p. ej. una ruta inventada de un sitio real).
3. Encuentra un caso de redirección (`301`/`302`) — muchos sitios redirigen de `http://` a `https://`, o de una URL sin `www.` a una con `www.`.

**Resultado esperado**: tienes capturas o la salida de `curl` con los tres códigos distintos, y sabes explicar qué significa cada uno.

---

## Ejercicio 4 — Cookies y sesión

1. Abre las herramientas de desarrollador → pestaña **Application/Almacenamiento** → **Cookies**.
2. Inicia sesión en algún sitio web (uno de prueba, o uno que ya uses habitualmente) y observa qué cookies aparecen después de autenticarte.
3. Identifica si hay alguna cookie que parezca un identificador de sesión (nombre tipo `sessionid`, `JSESSIONID`, `connect.sid`...).

**Resultado esperado**: localizas al menos una cookie y razonas por qué el servidor la necesita para "recordarte" entre peticiones.

---

## Ejercicio 5 — DNS a mano

```bash
nslookup www.github.com
# o también:
dig www.github.com
```

1. Ejecuta el comando y localiza la dirección IP resuelta.
2. Repite con otro dominio y compara los tiempos de respuesta.
3. Ejecuta el mismo comando dos veces seguidas: ¿cambia algo en la segunda?

**Resultado esperado**: entiendes que detrás de cada nombre de dominio hay (al menos) una IP real, y que la resolución puede quedar cacheada.

---

## Ejercicio 6 — Clasifica arquitecturas reales

Para cada sistema, decide qué estilo de arquitectura (de los vistos en la sección 4 de la teoría) encaja mejor y justifica por qué:

1. Una tienda online pequeña, hecha por un equipo de 3 personas, que se despliega entera de una vez.
2. Una plataforma de streaming con decenas de equipos trabajando en paralelo (reproducción, recomendaciones, pagos, perfiles...).
3. Un sistema que envía un correo automático cada vez que se confirma un pago, sin que el módulo de pagos sepa nada sobre el envío de correos.

**Resultado esperado**: justificas tu elección con al menos un argumento de la tabla comparativa vista en teoría.

---

<!-- _class: lead -->
# Retos

*Aquí no hay pasos: piensa qué necesitas hacer.*

---

## Reto 1 — Diagrama de capas de una app que conozcas

**Objetivo**: elige una aplicación web que uses habitualmente (un gestor de tareas, una tienda online, una red social...) y dibuja un diagrama con sus capas razonables (presentación / negocio / datos), indicando qué crees que hace cada una en ese caso concreto.

---

## Reto 2 — De monolito a microservicios (solo en papel)

**Objetivo**: imagina que la tienda online del Ejercicio 6.1 crece muchísimo y el equipo pasa de 3 a 30 personas. Propón en qué microservicios dividirías el sistema (p. ej. catálogo, carrito, pagos, usuarios...) y qué tendría que comunicarse con qué.

---

## Reto 3 — Caza de cabeceras de seguridad

*Por qué este reto*: ver cabeceras de seguridad reales te prepara para la UD3, donde configurarás servidores de verdad.

**Objetivo**: usando `curl -I` contra 2-3 sitios web reales de empresas conocidas, busca cabeceras relacionadas con seguridad (`Strict-Transport-Security`, `X-Content-Type-Options`, `Content-Security-Policy`...) y anota cuáles aparecen y en cuáles no.

---

<!-- _class: lead -->
# Autoevaluación

---

## ¿Te ves capaz de...?

- [ ] Explicar con tus palabras el viaje completo de una petición web, desde que escribes una URL hasta que se pinta la página.
- [ ] Diferenciar los métodos HTTP más comunes y cuándo se usa cada uno.
- [ ] Distinguir `401` de `403`, y un `4xx` de un `5xx`.
- [ ] Explicar por qué HTTP es "sin estado" y cómo las cookies/sesiones resuelven ese problema.
- [ ] Explicar la diferencia entre una arquitectura en capas y un estilo de arquitectura a gran escala (monolito, microservicios...).
- [ ] Justificar qué arquitectura encaja mejor según el tamaño y las necesidades de un proyecto.
