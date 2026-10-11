---
marp: true
theme: default
paginate: true
backgroundColor: white
footer: 'Despliegue de Aplicaciones Web (0614) · UD2: Arquitecturas Web'
layout: default
title: "Arquitecturas Web — Bloque 2.2: Servidores y despliegue (Prácticas)"
permalink: /web/semana-2/practicas/
---

<!-- _class: lead -->
# arquitecturas web
## Prácticas — bloque 2.2: servidores web, de aplicaciones y despliegue

---

## Antes de empezar

- Hoy usamos **Docker** (ya lo conoces de la UD1), pero solo de forma ligera: lanzar contenedores ya construidos, sin tocar su configuración interna.
- La configuración real de Apache/Nginx (ficheros de configuración, hosts virtuales...) se hace en la **UD3**: hoy nos quedamos en el nivel conceptual de "qué sirve cada tipo de servidor".
- Hacemos los **Ejercicios 1 a 4** (miércoles) y seguimos con el resto el **viernes**, antes del cuestionario.

---

<!-- _class: lead -->
# Ejercicios guiados

---

## Ejercicio 1 — Un servidor web sirviendo contenido estático

1. Crea una carpeta local con un `index.html` sencillo escrito por ti (con algo de texto e imágenes si quieres).
2. Ejecuta `docker run -d --name web-estatico -p 8080:80 -v "$(pwd):/usr/share/nginx/html:ro" nginx:1.25`.
3. Abre `http://localhost:8080` (o la URL equivalente en tu entorno) y comprueba que ves tu `index.html`.

**Resultado esperado**: ves tu propio HTML servido por Nginx, sin que Nginx haya ejecutado ningún código, solo leído el fichero.

---

## Ejercicio 2 — Un servidor de aplicaciones sirviendo contenido dinámico

1. Ejecuta `docker run -d --name app-dinamica -p 8081:80 python:3.12-slim sh -c "echo 'from http.server import BaseHTTPRequestHandler, HTTPServer; import datetime; HTTPServer((\"0.0.0.0\",80), type(\"H\",(BaseHTTPRequestHandler,),{\"do_GET\": lambda self: (self.send_response(200), self.end_headers(), self.wfile.write(str(datetime.datetime.now()).encode()))})).serve_forever()' > /app.py && python /app.py"`.
2. Abre `http://localhost:8081` varias veces, recargando.

**Resultado esperado**: la hora mostrada cambia en cada recarga, porque el servidor **ejecuta código** en cada petición (a diferencia del Ejercicio 1).

---

## Ejercicio 3 — Compara ambos con las herramientas de desarrollador

1. Con los dos contenedores de los Ejercicios 1 y 2 en marcha, abre las herramientas de desarrollador (F12) → pestaña Red.
2. Recarga ambas páginas y compara los tiempos de respuesta.
3. Fíjate en la cabecera `Content-Type` de cada una: ¿qué diferencia ves?

**Resultado esperado**: razonas con tus palabras por qué el contenido estático suele responder algo más rápido.

---

## Ejercicio 4 — Dos servidores web "delante" de contenido distinto

1. Levanta un segundo servidor estático en otro puerto: `docker run -d --name web-estatico-2 -p 8090:80 nginx:1.25` (con la imagen oficial, sin volumen esta vez).
2. Compara el `index.html` por defecto de nginx en `http://localhost:8090` con el tuyo del Ejercicio 1.
3. Para ambos contenedores con `docker stop` cuando termines.

**Resultado esperado**: entiendes que un servidor web sirve lo que encuentre en su carpeta de contenido, sea el tuyo o el que trae la imagen por defecto.

---

## Ejercicio 5 — Simula un "servidor web + servidor de aplicaciones" con dos contenedores

1. Deja en marcha tu `app-dinamica` del Ejercicio 2 (puerto 8081).
2. En otra pestaña del navegador abre a la vez `web-estatico` (8080) y `app-dinamica` (8081).

**Resultado esperado**: tienes, a pequeña escala y sin proxy real todavía, la idea de "una parte estática, otra dinámica" que en la UD3 aprenderás a unificar detrás de un único servidor web con proxy inverso.

---

## Ejercicio 6 — Limpieza

1. Lista todos los contenedores de hoy con `docker ps -a`.
2. Párralos y elimínalos con los comandos que ya conoces de la UD1.

**Resultado esperado**: tu entorno Docker queda limpio, sin contenedores de esta práctica.

---

<!-- _class: lead -->
# Retos

*Aquí no hay pasos: piensa qué necesitas hacer.*

---

## Reto 1 — Clasifica una web real

**Objetivo**: elige una página web cualquiera, ábrela con las herramientas de desarrollador y, mirando los recursos que carga (pestaña Red), clasifica al menos 5 peticiones distintas como "previsiblemente estático" o "previsiblemente dinámico", justificando tu respuesta con lo visto en teoría.

---

## Reto 2 — Diseña un despliegue sobre papel

**Objetivo**: para una aplicación sencilla que tú elijas (p. ej. un blog personal), dibuja un esquema con: el dominio, el DNS, el servidor web, el servidor de aplicaciones (si hace falta) y la base de datos, indicando qué partes serían estáticas y cuáles dinámicas.

---

## Reto 3 — Investiga un proveedor de hosting

*Por qué este reto*: antes de desplegar algo de verdad conviene saber qué opciones existen y por qué cuestan lo que cuestan.

**Objetivo**: busca información de un proveedor real (hosting compartido, VPS o cloud) y explica, con tus palabras, en qué categoría de las vistas en teoría encaja su oferta y qué nivel de control te da sobre el servidor.

---

<!-- _class: lead -->
# Autoevaluación

---

## ¿Te ves capaz de...?

- [ ] Explicar la diferencia entre contenido estático y dinámico con un ejemplo propio.
- [ ] Explicar la diferencia entre un servidor web y un servidor de aplicaciones.
- [ ] Dibujar el esquema de una petición que combina ambos tipos de servidor.
- [ ] Explicar qué papel juegan el dominio, el DNS y el hosting en un despliegue.
- [ ] Diferenciar hosting compartido, VPS, servidor dedicado y cloud.
- [ ] Explicar por qué Docker facilita el despliegue, conectándolo con lo aprendido en la UD1.
