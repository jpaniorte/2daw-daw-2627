---
layout: default
title: "Arquitecturas Web — Bloque 2.2: Servidores web y de aplicaciones (Prácticas)"
permalink: /web/semana-2/practicas/
---

# Práctica 2.2 — Un servidor web delante, servidores de aplicaciones detrás

**Módulo:** Despliegue de Aplicaciones Web (0614) · 2º DAW · UD2: Arquitecturas web

## Objetivos

- Distinguir en la práctica el contenido **estático** del **dinámico**, y el renderizado en el **cliente** (CSR) del renderizado en el **servidor** (SSR).
- Comprobar lo que hace un **servidor web** sin tocar el código de la aplicación: compresión y caché.
- Ver a Nginx funcionando como **proxy inverso** y **balanceador** delante de dos servidores de aplicaciones, y provocar los errores **502** y **504**.
- Entender por qué una petición funciona con curl y **falla desde el navegador** (CORS).
- **Desplegar** un artefacto versionado, hacer una actualización **rolling** y un **rollback**.

## Qué hay que entregar

Un documento con la **respuesta a cada pregunta marcada con ❓** (P1, P2…). En cada una, incluye el comando que has usado y **solo el fragmento relevante** de la salida (no hace falta pegar respuestas enteras).

---

## 0. Preparación (5 min)

### El entorno

Descarga y descomprime [`web_2_practica_entorno.zip`]({{ '/UD2/2.2%20Servidores%20web%20y%20de%20aplicaciones/web_2_practica_entorno.zip' | relative_url }}). Contiene cuatro servicios de Docker Compose:

| Servicio | URL | Qué es |
|----------|-----|--------|
| **web** | `http://localhost:8080` | **Nginx** (servidor web): sirve lo estático y reenvía todo lo que empieza por `/api/` a los backends. |
| **app1** y **app2** | sin puerto publicado | Dos instancias de la misma aplicación **Node.js** (servidor de aplicaciones), creadas a partir de la imagen `miapp`. |
| **otro-origen** | `http://localhost:9090` | Otra web distinta que intenta usar nuestra API desde el navegador. |

```
navegador / curl → web (Nginx, :8080)
                     ├── /, /csr.html, /assets/*  → responde Nginx directamente (estático)
                     └── /api/*                   → reenvía a app1 o app2 (Node.js, dinámico)
```

```bash
cd web_2_practica_entorno
docker compose up -d --build   # --build: construye la imagen miapp la primera vez
docker compose ps              # los cuatro servicios deben aparecer en estado "running"
curl localhost:8080/api/info   # debe devolver un JSON
```

Echa un vistazo a los ficheros antes de empezar. Vas a usarlos durante la práctica: `docker-compose.yml`, `.env`, `nginx/default.conf` y `app/server.js`.

> **Windows:** usa **Git Bash**. Todos los comandos están escritos para bash.

> **Si la API responde `502` al arrancar o después de parar un backend:** espera unos 10 segundos y repite. Lo entenderás en la parte 3.

> **Si Docker no funciona:** sigue el plan B del `README.md` de la carpeta del entorno (solo cubre una parte de la práctica).

### Opciones de curl nuevas

Además de las de la práctica 2.1 (`-v`, `-i`, `-I`, `-s`, `-H`, `-X`…):

| Opción | Qué hace |
|--------|----------|
| `-o /dev/null` | Descarta el cuerpo de la respuesta. |
| `-w "%{size_download}\n"` | Al terminar, imprime los bytes del cuerpo que se han descargado. |
| `-w "%{time_total}\n"` | Al terminar, imprime cuánto ha tardado la petición, en segundos. |

---

## 1. Estático vs. dinámico, CSR vs. SSR (12 min)

### 1.1 Mismo fichero, misma respuesta

```bash
curl -i localhost:8080/
curl -i localhost:8080/
```

### 1.2 Misma ruta, respuesta distinta

```bash
curl localhost:8080/api/info
curl localhost:8080/api/info
curl localhost:8080/api/info
```

❓ **P1.** Compara las dos respuestas de 1.1 entre sí, y las de 1.2 entre sí. ¿Qué cambia y qué no? ¿Cuál es contenido **estático** y cuál **dinámico**? En las cabeceras de 1.1 aparecen `Last-Modified` y `Content-Length`: ¿por qué tiene sentido que Nginx pueda dar esos datos de un fichero estático sin ejecutar nada?

### 1.3 Lo que ve un buscador

Estas dos páginas muestran **la misma lista de productos** cuando las abres en el navegador. Ábrelas primero en el navegador (`http://localhost:8080/csr.html` y `http://localhost:8080/api/ssr`) y luego pídelas con curl, que **no ejecuta JavaScript** (como algunos rastreadores):

```bash
curl localhost:8080/csr.html
curl localhost:8080/api/ssr
```

❓ **P2.** ¿En cuál de las dos respuestas de curl aparecen los nombres de los productos? En la otra, ¿qué hay en su lugar y quién acaba construyendo la lista? (Mira el fichero `estatico/assets/app.7d21e4.js`.) ¿Cuál es **CSR** y cuál **SSR**?

❓ **P3.** ¿Cuál de las dos es mejor para el **SEO** y por qué? Fíjate en quién sirve cada una: ¿cuál necesitaría un **servidor de aplicaciones** en producción y cuál podría servirse solo con Nginx o desde una CDN?

---

## 2. Lo que hace el servidor web sin tocar la aplicación (10 min)

### 2.1 Compresión

```bash
curl -s -o /dev/null -w "%{size_download}\n" localhost:8080/assets/estilos.a3f9c1.css
curl -s -o /dev/null -w "%{size_download}\n" -H "Accept-Encoding: gzip" localhost:8080/assets/estilos.a3f9c1.css
curl -sI -H "Accept-Encoding: gzip" localhost:8080/assets/estilos.a3f9c1.css
```

❓ **P4.** ¿Cuántos bytes se descargan en cada caso? ¿Qué cabecera de la respuesta indica que el cuerpo viene comprimido? Busca en `nginx/default.conf` la parte que lo activa: ¿has tenido que tocar `server.js` para conseguirlo? (Nota: este CSS es muy repetitivo y comprime mucho más que uno real.)

### 2.2 Caché y *cache busting*

```bash
curl -sI localhost:8080/ | grep -i cache-control
curl -sI localhost:8080/assets/estilos.a3f9c1.css | grep -i cache-control
```

❓ **P5.** ¿Qué `Cache-Control` tiene cada uno? El CSS se puede guardar en caché **un año** (`max-age=31536000`) y `index.html` no. Si mañana cambias los estilos, ¿cómo se entera el navegador de que hay un CSS nuevo si tiene guardado el antiguo durante un año? (Pista: el nombre del fichero y quién lo referencia.)

### 2.3 Revalidar: el 304

`no-cache` **no** significa "no guardar": significa "guárdalo, pero pregúntame antes de usarlo". Copia el `ETag` de `index.html` y úsalo para preguntar si ha cambiado:

```bash
curl -sI localhost:8080/ | grep -i etag
curl -i -H 'If-None-Match: "PEGA_AQUÍ_EL_ETAG_SIN_COMILLAS"' localhost:8080/
```

❓ **P6.** ¿Qué código devuelve la segunda petición y cuántos bytes de cuerpo trae? Explica con tus palabras qué gana el servidor con esto en una web con miles de visitas.

---

## 3. Proxy inverso, balanceo y health checks (18 min)

### 3.1 ¿Quién me atiende?

Lanza varias peticiones seguidas y mira qué backend responde. Nginx añade la cabecera `X-Backend` con la IP:puerto del backend al que ha reenviado la petición:

```bash
for i in 1 2 3 4 5 6; do curl -si localhost:8080/api/info | grep -iE 'x-backend|"servidor"|visitas'; done
```

❓ **P7.** ¿Qué patrón sigue el reparto entre `app1` y `app2`? ¿Cómo se llama esa estrategia y dónde está configurada (`nginx/default.conf`)? ¿Qué servicio de Docker Compose tiene el puerto `8080` publicado y cuáles no tienen ninguno? ¿Puedes llegar a `app1` directamente desde tu máquina?

❓ **P8.** Fíjate en el campo `visitas_en_esta_instancia`. ¿Es un contador global de la aplicación? Si la aplicación guardara así la **sesión** de un usuario (en la memoria de la instancia), ¿qué le pasaría al usuario con este reparto? ¿Qué estrategia de balanceo de la teoría lo "arreglaría" y qué solución es mejor?

### 3.2 Se cae un backend

```bash
docker compose stop app1
for i in 1 2 3 4; do curl -si localhost:8080/api/info | grep -iE '^HTTP|x-backend|"servidor"'; done
```

❓ **P9.** ¿Algún usuario ha recibido un error? En la **primera** petición, la cabecera `X-Backend` lleva **dos** direcciones: ¿qué ha hecho Nginx? ¿Y en las siguientes? Busca en `nginx/default.conf` las opciones `max_fails`, `fail_timeout` y `proxy_next_upstream` y explica qué hace cada una. (Esto es un health check **pasivo**: Nginx descubre que un backend está caído cuando le falla una petición real.)

### 3.3 Se caen todos: 502

```bash
docker compose stop app2
curl -i localhost:8080/api/info
curl -s -o /dev/null -w "%{http_code}\n" localhost:8080/
```

❓ **P10.** ¿Qué código devuelve la API y quién genera esa respuesta (mira la cabecera `Server` y el cuerpo)? ¿Por qué la página principal sigue respondiendo `200`? Relaciónalo con la separación entre servidor web y servidor de aplicaciones.

Vuelve a arrancarlos y **espera unos 10 segundos** antes de seguir:

```bash
docker compose start app1 app2
```

### 3.4 Un backend demasiado lento: 504

La ruta `/api/lento?s=N` tarda N segundos en contestar.

```bash
curl -s -w "\n%{http_code} en %{time_total}s\n" "localhost:8080/api/lento?s=2"
curl -si -w "\n%{http_code} en %{time_total}s\n" "localhost:8080/api/lento?s=5" | grep -iE '^HTTP|x-backend|en [0-9]'
```

❓ **P11.** ¿Qué código obtienes con 2 s y con 5 s? ¿Qué directiva de `nginx/default.conf` marca el límite? La petición de 5 s ha tardado unos **6 segundos** y `X-Backend` vuelve a mostrar dos direcciones: explica por qué. ¿Qué diferencia hay entre un **502** y un **504**?

> Espera otra vez 10 segundos antes de seguir: los dos backends han quedado "en cuarentena" un momento por no responder a tiempo.

---

## 4. CORS: funciona con curl, falla en el navegador (10 min)

### 4.1 Desde otra web

Abre en el navegador `http://localhost:9090` con las **DevTools** abiertas (F12 → pestaña *Consola*). Esa página intenta leer `http://localhost:8080/api/info` con `fetch`.

❓ **P12.** ¿Qué muestra la página? Copia el error de la consola. `localhost:9090` y `localhost:8080` están en la misma máquina: ¿por qué son **orígenes distintos**? Mira ahora en la pestaña *Red* (*Network*) la petición a `/api/info`: ¿ha llegado al servidor? ¿Qué código ha devuelto?

### 4.2 La misma petición con curl

```bash
curl -si -H "Origin: http://localhost:9090" localhost:8080/api/info | head -8
curl -si -X OPTIONS -H "Origin: http://localhost:9090" -H "Access-Control-Request-Method: DELETE" localhost:8080/api/info | head -8
```

La segunda simula la petición de comprobación (*preflight*) que hace el navegador antes de un `DELETE`.

❓ **P13.** Con curl obtienes los datos sin problema. ¿Qué cabecera falta en la respuesta para que el navegador la acepte? ¿Quién aplica CORS: el servidor o el navegador? ¿Protege CORS a la API de alguien que use curl?

### 4.3 Autorizar el otro origen

Edita `.env` y pon `CORS_ORIGIN=http://localhost:9090`. Después recrea los backends (Compose detecta que ha cambiado su configuración):

```bash
docker compose up -d
```

Espera unos segundos, repite los dos comandos de 4.2 y recarga `http://localhost:9090` en el navegador.

❓ **P14.** ¿Qué cabeceras `Access-Control-Allow-*` aparecen ahora en cada respuesta? ¿Qué código devuelve el preflight? ¿Funciona la página de `localhost:9090`? ¿Has cambiado el código de la aplicación o solo su **configuración**?

---

## 5. Desplegar un artefacto versionado (15 min)

### 5.1 El artefacto

```bash
docker images miapp
docker compose exec app1 env | grep APP_VERSION
```

Abre `app/Dockerfile` y `docker-compose.yml`: la versión se graba **dentro** de la imagen al construirla, y la imagen se etiqueta con esa misma versión (`miapp:${VERSION}`).

### 5.2 Construir la versión 1.1.0

1. En `app/server.js`, cambia el mensaje: `const MENSAJE = "¡Rebajas de otoño!";`
2. En `.env`, pon `VERSION=1.1.0`.
3. Construye la nueva imagen **sin desplegarla todavía**:

```bash
docker compose build
docker images miapp
```

❓ **P15.** ¿Cuántas imágenes `miapp` hay ahora y con qué etiquetas? ¿Ha cambiado algo de lo que responde la API (`curl localhost:8080/api/info`)? ¿Por qué? Según **SemVer**, ¿es correcto que este cambio sea un `MINOR` (1.0.0 → 1.1.0)? ¿Qué número subirías si hubieras cambiado el formato del JSON de forma incompatible?

### 5.3 Despliegue *rolling*

Abre **otra terminal** en la misma carpeta y deja este bucle en marcha (una petición por segundo; `Ctrl+C` para pararlo):

```bash
while true; do curl -s localhost:8080/api/info | grep -E '"servidor"|"version"' | tr -d '\n'; echo; sleep 1; done
```

En la primera terminal, actualiza **los backends de uno en uno**:

```bash
docker compose up -d --no-deps app1
# espera unos 15 segundos mirando el bucle
docker compose up -d --no-deps app2
```

❓ **P16.** Copia un fragmento del bucle **entre** los dos comandos. ¿Qué versiones convivían en ese momento? ¿Ha habido algún momento sin servicio (alguna línea vacía o error)? ¿Por qué se llama **rolling** a esta estrategia? ¿Qué problema tendría si la versión nueva cambiara el esquema de la base de datos?

### 5.4 Rollback

Imagina que la 1.1.0 tiene un error grave. **Sin tocar `server.js`** (deja el mensaje nuevo en el código), vuelve a la versión anterior:

```bash
# en .env: VERSION=1.0.0
docker compose up -d
docker compose ps
curl -s localhost:8080/api/info
```

❓ **P17.** ¿Qué versión y qué mensaje responde ahora la API, aunque `server.js` tenga el mensaje nuevo? ¿Se ha vuelto a construir algo (mira la salida de `docker compose up -d`)? Explica qué ventaja tiene desplegar un **artefacto inmutable y versionado** frente a "volver a compilar el código antiguo" o "hacer `git pull` en el servidor".

❓ **P18.** En este entorno, `CORS_ORIGIN` llega al contenedor como **variable de entorno** y la versión va **grabada en la imagen**. ¿Por qué tiene sentido que sea así y no al revés? Si la aplicación necesitara la contraseña de la base de datos, ¿dónde la pondrías y dónde **nunca**?

---

## ¿Y si no quiero usar curl?

Puedes hacer la práctica con otra herramienta siempre que puedas **ver las cabeceras de la respuesta**:

| Herramienta | Notas |
|-------------|-------|
| **DevTools del navegador** (F12 → Red / *Network*) | Sirve para casi todo. Ojo: el navegador **cachea** y **descomprime** solo. Marca *Disable cache* para las partes 2 y 3, y mira la columna *Size* (transferido) frente a *Content* (descomprimido). |
| **Postman / Bruno / Insomnia** | Válidos para las partes 1, 2, 3 y 5. En la parte 4 **no** verás el error de CORS: no son navegadores y no aplican la política del mismo origen (es justo lo que pregunta la P13). |
| **HTTPie** (`http -v …`) | Equivalente a curl con una sintaxis más amigable. |

En el documento de entrega indica qué herramienta has usado.

---

## Ampliación (si terminas antes)

1. **El *event loop* de Node se bloquea.** La ruta `/api/calcular` hace un cálculo de 2 s que **bloquea** el único hilo de Node. Para un backend, espera 15 s y lanza a la vez un cálculo y una petición normal:

   ```bash
   docker compose stop app2
   # espera 15 segundos
   curl -s localhost:8080/api/calcular > /dev/null &
   sleep 0.3; curl -s -o /dev/null -w "info tardó %{time_total}s\n" localhost:8080/api/info
   docker compose start app2
   ```

   ¿Cuánto ha tardado `/api/info`, que normalmente responde en milisegundos? Compáralo con `/api/lento?s=2`, que también tarda 2 s pero **no** bloquea: ¿por qué uno afecta al resto de peticiones y el otro no?

2. **Cambiar la estrategia de balanceo.** En `nginx/default.conf`, añade `ip_hash;` en la línea siguiente a `zone backends 64k;`. Después:

   ```bash
   docker compose exec web nginx -t          # comprueba la sintaxis
   docker compose exec web nginx -s reload   # aplica sin parar el servidor
   ```

   Espera 10 segundos y repite el bucle de 3.1. ¿Qué ha cambiado y por qué? (Todas tus peticiones llegan a Nginx desde la misma IP.) Prueba también con `least_conn;`. Al terminar, quita la línea y recarga.

3. **El build de un frontend no es un servidor.** Si tienes Node.js instalado, crea una app de Vue (`npm create vue@latest`), ejecuta `npm run build -- --base=/vue/` (para que sus rutas empiecen por `/vue/`) y copia el contenido de `dist/` en `estatico/vue/`. Ábrela en `http://localhost:8080/vue/`. ¿Qué proceso la está sirviendo? ¿Hace falta Node.js en el servidor?

---

## Al terminar

```bash
docker compose down
docker rmi miapp:1.0.0 miapp:1.1.0
```

Deja `.env` como estaba (`VERSION=1.0.0` y `CORS_ORIGIN=` vacío) si vas a reutilizar el entorno.
