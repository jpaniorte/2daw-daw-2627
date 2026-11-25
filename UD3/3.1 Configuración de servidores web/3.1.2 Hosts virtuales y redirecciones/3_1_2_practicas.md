---
layout: default
title: "Servidores Web — Bloque 3.1.2: Hosts virtuales y redirecciones (Prácticas)"
permalink: /servidores-web/semana-2/practicas/
---

# Práctica 3.1.2 — Una cocina, varias marcas

**Módulo:** Despliegue de Aplicaciones Web (0614) · 2º DAW · UD3: Administración de servidores web

## Objetivos

- Alojar **varias webs en un mismo Nginx** con **hosts virtuales** por nombre.
- Declarar el **servidor por defecto** y ver qué pasa cuando el `Host` no coincide con nadie.
- Servir **una aplicación distinta en cada ruta** (`/hola`, `/test`, `/mundo`) con `location`, `root` y `alias`.
- Entender **cuál de varias `location` gana** y detectar cuándo una expresión regular «roba» una ruta.
- Configurar **redirecciones** (301, 302, `www`, `rewrite`) y diagnosticar un **bucle**.
- Dar una **página de error propia** y leer el log para encontrar el fallo.

## Cómo funciona esta práctica

- **Se hace en clase**, en tu VM (`ssh daw`) o en tu ordenador con Docker. **Todo se prueba en `localhost`** con `curl`: no hace falta dominio ni navegador.
- Hay **puntos de control 🧑‍🏫**: cuando llegues a uno, **avisa al profesor**, que lo revisará contigo en tu pantalla antes de que sigas.
- **Además, se entrega**: un documento con la **respuesta a cada pregunta ❓** (P1, P2…) y **cada evidencia 📸** (E1, E2…). En cada respuesta, incluye el comando que has usado y **solo el fragmento relevante** de la salida.
- Después de **cada cambio** en `conf.d/`, comprueba y recarga:

```bash
docker compose exec web nginx -t && docker compose exec web nginx -s reload
```

| Parte | Tiempo aprox. |
|-------|---------------|
| 0. Preparación | 5 min |
| 1. Hosts virtuales | 15 min |
| 2. Una aplicación por ruta | 20 min |
| 3. Redirecciones | 15 min |
| 4. Página de error propia | 5 min |

---

## 0. Preparación (5 min)

Si estás en la VM:

```bash
ssh daw
```

Ya dentro, libera el puerto 80 (si dejaste en marcha el Nginx de la práctica anterior) y crea la carpeta de hoy:

```bash
docker ps                                  # ¿qué hay usando el puerto 80?
(cd ~/daw/3.1.1 && docker compose down)    # para el Nginx de 3.1.1, si lo tienes
mkdir -p ~/daw/3.1.2 && cd ~/daw/3.1.2
mkdir -p conf.d sitios/principal/hola sitios/principal/test sitios/tienda sitios/docs sitios/errores
```

Crea las webs. Cada una dice quién es, para saber siempre qué sitio ha respondido:

```bash
echo "<h1>Web principal</h1>"   > sitios/principal/index.html
echo "<h1>App hola</h1>"        > sitios/principal/hola/index.html
echo "<h1>App test</h1>"        > sitios/principal/test/index.html
echo "<h1>Nuevo</h1>"           > sitios/principal/nuevo.html
echo "<h1>Tienda</h1>"          > sitios/tienda/index.html
echo "<h1>Documentacion</h1>"   > sitios/docs/index.html
echo "<h1>404 propia</h1>"      > sitios/errores/404.html
```

Y el `compose.yaml`:

```bash
cat > compose.yaml <<'EOF'
services:
  web:
    image: nginx:1.30
    ports:
      - "80:80"
    volumes:
      - ./conf.d:/etc/nginx/conf.d:ro
      - ./sitios:/usr/share/nginx/sitios:ro
    restart: unless-stopped
EOF
```

---

## 1. Hosts virtuales (15 min)

### 1.1 Dos webs en un mismo servidor

Crea `conf.d/sitios.conf` con dos sitios:

```bash
cat > conf.d/sitios.conf <<'EOF'
server {
    listen      80;
    server_name localhost;
    root        /usr/share/nginx/sitios/principal;
}

server {
    listen      80;
    server_name tienda.localhost;
    root        /usr/share/nginx/sitios/tienda;
}
EOF
```

Arranca y pide cada web **por su nombre**:

```bash
docker compose up -d
docker compose exec web nginx -t
curl http://localhost/
curl http://tienda.localhost/
```

📸 **E1.** Salida de los dos `curl`: cada nombre devuelve una web distinta.

❓ **P1.** Las dos webs están en la **misma IP y el mismo puerto**. ¿Qué dato de la petición usa Nginx para decidir cuál servir? ¿Qué directiva de cada `server` lo compara?

### 1.2 Sin DNS: la cabecera `Host`

```bash
curl -H "Host: tienda.localhost" http://localhost/
curl -H "Host: otro.com" http://localhost/
```

❓ **P2.** La segunda petición lleva un `Host` que **no existe** en tu configuración. ¿Qué web responde? ¿Por qué? ¿Qué problema puede suponer en un servidor con webs de varios clientes?

### 1.3 El servidor por defecto

Añade al final de `conf.d/sitios.conf` un servidor que recoja lo que no coincida con nada:

```nginx
server {
    listen 80 default_server;
    server_name _;
    return 444;
}
```

Comprueba, recarga y repite las pruebas:

```bash
curl -H "Host: otro.com" http://localhost/
echo "código de salida: $?"
curl http://localhost/
curl http://tienda.localhost/
```

❓ **P3.** ¿Qué respuesta da ahora `otro.com`? ¿Qué significa el código `444` y en qué se diferencia de un `404`? Comprueba que las dos webs siguen funcionando.

### 1.4 Un log por sitio

Añade dentro de cada `server` (`localhost` y `tienda.localhost`) su propio registro de accesos:

```nginx
    access_log  /var/log/nginx/principal.access.log;     # en localhost
    access_log  /var/log/nginx/tienda.access.log;        # en tienda.localhost
```

Recarga, haz dos peticiones a cada sitio y lee los logs:

```bash
docker compose exec web cat /var/log/nginx/tienda.access.log
docker compose exec web cat /var/log/nginx/principal.access.log
```

📸 **E2.** Salida de los dos logs: cada uno solo contiene las peticiones de su web.

❓ **P4.** ¿Por qué estos logs no salen con `docker logs`, pero el `access.log` normal sí? (Pista: `ls -l /var/log/nginx` dentro del contenedor.) ¿Qué ventaja tiene separar los logs por sitio?

🧑‍🏫 **Punto de control 1:** enseña al profesor los dos hosts virtuales respondiendo por su nombre, el servidor por defecto (`curl: (52) Empty reply from server`) y los dos logs separados.

---

## 2. Una aplicación por ruta (20 min)

Dentro de `localhost`, cada ruta va a servir un contenido distinto: `/hola` una app, `/test` otra y `/mundo` una tercera. Añade estas `location` **dentro del `server` de `localhost`**:

```nginx
    location /hola/  { }                                  # carpeta principal/hola/
    location = /test { return 200 "Solo /test\n"; }       # solo esa URL exacta
    location /mundo/ { alias /usr/share/nginx/sitios/docs/; }   # otra carpeta
```

```bash
curl http://localhost/hola/
curl http://localhost/test
curl http://localhost/mundo/
```

📸 **E3.** Salida de los tres `curl`.

❓ **P5.** Pide ahora `curl -I http://localhost/hola` (**sin** barra final). ¿Qué código devuelve y a dónde te manda? ¿Quién ha decidido esa redirección, si tú no la has escrito?

❓ **P6.** Pide `curl http://localhost/test/` (**con** barra). ¿Qué responde y por qué no es lo mismo que `/test`? ¿Qué `location` ha atendido esa petición?

### 2.1 Cuando una expresión regular «roba» una ruta

Añade una regla que ponga una cabecera a todos los `.html` (debajo de `location /hola/`):

```nginx
    location ~ \.html$ { add_header X-Regla regex-html; }
```

```bash
curl -sI http://localhost/hola/index.html | grep -i -E "HTTP|x-regla"
```

Aparece `X-Regla`: la petición `/hola/index.html` **la ha atendido la regex**, no la `location /hola/`. Las expresiones regulares se evalúan **después** de los prefijos normales y, si coinciden, ganan.

Arregla la ruta cambiando `location /hola/` por la forma **preferente**:

```nginx
    location ^~ /hola/ { }
```

Recarga y repite el `curl -sI`.

📸 **E4.** `curl -I` de `/hola/index.html` **antes** (con `X-Regla`) y **después** (sin ella).

❓ **P7.** ¿Qué hace `^~` y por qué soluciona el problema? ¿Qué cuatro tipos de `location` hay, ordenados de mayor a menor prioridad? ¿Qué pasa con `/nuevo.html`: sigue con `X-Regla`? ¿Por qué?

### 2.2 `root` o `alias`: la trampa de la barra

Añade este `location` **mal escrito** (sin barra final en el `alias`):

```nginx
    location /malo/ { alias /usr/share/nginx/sitios/docs; }
```

```bash
curl -i http://localhost/malo/
curl -i http://localhost/malo/index.html
docker compose logs --tail 20 web | grep -E "malo|docs"
```

📸 **E5.** Los dos códigos de estado y las líneas del log de errores.

❓ **P8.** ¿Qué códigos de estado aparecen? En el log, ¿qué ruta de fichero ha buscado Nginx en el segundo caso? ¿Qué le falta al `alias` para que funcione? Corrígelo (con `/` al final) y comprueba que `/malo/index.html` da 200. Después explica con un ejemplo la diferencia entre `root` y `alias`.

> Borra el `location /malo/` al terminar: es solo para el ejercicio.

🧑‍🏫 **Punto de control 2:** enseña al profesor `/hola/`, `/test` y `/mundo/` respondiendo cada uno con su contenido, `/hola/index.html` **sin** `X-Regla`, y el error de `/malo/` en el log.

---

## 3. Redirecciones (15 min)

Añade estas reglas **dentro del `server` de `localhost`**:

```nginx
    location = /viejo { return 301 /nuevo.html; }                      # permanente
    location /tmp     { return 302 /nuevo.html; }                      # temporal
    location /reglas  { rewrite ^/reglas/(.*)$ /$1 permanent; }        # reescribe con regex
```

```bash
curl -I http://localhost/viejo
curl -I http://localhost/tmp
curl -I http://localhost/reglas/nuevo.html
curl -L http://localhost/viejo
```

📸 **E6.** Salida de los tres `curl -I` y del `curl -L`.

❓ **P9.** ¿Qué diferencia hay entre el 301 y el 302? ¿Cuál usarías al **probar** una redirección y por qué? ¿Y cuál para una web que ha cambiado de dirección para siempre?

❓ **P10.** Explica con tus palabras qué hace `rewrite ^/reglas/(.*)$ /$1 permanent;`. ¿Qué es `(.*)` y qué es `$1`? ¿Por qué aquí se usa `rewrite` en lugar de `return`?

### 3.1 De `www` a sin `www`

Añade un servidor cuya única misión es redirigir:

```nginx
server {
    listen      80;
    server_name www.localhost;
    return 301  http://localhost$request_uri;
}
```

```bash
curl -I -H "Host: www.localhost" http://localhost/hola/
```

❓ **P11.** ¿A dónde te manda? ¿Qué pasaría con la ruta `/hola/` si pusieras `return 301 http://localhost/;` en vez de `$request_uri`?

### 3.2 Provocar un bucle y diagnosticarlo

Añade un host que redirige a sí mismo en círculo:

```nginx
server {
    listen      80;
    server_name bucle.localhost;
    location /a { return 301 /b; }
    location /b { return 301 /a; }
}
```

```bash
curl -L http://bucle.localhost/a
curl -sIL http://bucle.localhost/a | grep -E "HTTP|Location" | head -4
```

📸 **E7.** El error de `curl -L` y las primeras líneas de las cabeceras.

❓ **P12.** ¿Qué error muestra `curl`? ¿Cuántas redirecciones sigue antes de rendirse? ¿Qué verías en un navegador? Arréglalo (que `/b` sirva algo en vez de redirigir) y quita el host.

🧑‍🏫 **Punto de control 3:** enseña al profesor el 301, el 302, la redirección de `www` con la ruta conservada y el bucle diagnosticado.

---

## 4. Página de error propia (5 min)

Dentro del `server` de `localhost`, añade:

```nginx
    error_page 404 /errores/404.html;

    location ^~ /errores/ {
        alias    /usr/share/nginx/sitios/errores/;
        internal;
    }
```

```bash
curl -i http://localhost/nada
curl -I http://localhost/errores/404.html
```

📸 **E8.** Salida de los dos `curl`.

❓ **P13.** ¿Qué código devuelve `/nada` y qué cuerpo? ¿Por qué es importante que siga siendo 404 y no 200? ¿Qué efecto tiene `internal;` al pedir directamente `/errores/404.html`?

❓ **P14.** Quita el `^~` de `location ^~ /errores/` (déjala como `location /errores/`) y repite `curl -i http://localhost/nada`. ¿Qué cuerpo sale ahora? Pista: ¿qué otra `location` coincide con `/errores/404.html`? Vuelve a poner `^~`.

---

## Ampliación (si terminas antes)

1. **Más hosts.** Añade `api.localhost` con una sola `location = /estado { return 200 "ok\n"; }` y su propio log. Pruébalo con `curl` por nombre y con `-H "Host: …"`.
2. **Capturar con regex.** Haz una `location ~ ^/usuario/(\d+)$` que responda `return 200 "Usuario $1\n";`. Prueba con `/usuario/42` y con `/usuario/abc`.
3. **`try_files`.** Crea `location /app/ { try_files $uri /nuevo.html; }` y comprueba qué pasa con una ruta que no existe dentro de `/app/`.
4. **Adelanto de HTTPS.** Escribe la redirección que enviaría todo `http://` a `https://` conservando host y ruta: `return 301 https://$host$request_uri;`. No la actives aún (no hay certificado): se hará en el bloque 3.2.1.
5. **Varios nombres.** Haz que `tienda.localhost` y `shop.localhost` sirvan la misma web con un único `server_name`.

---

## Al terminar

**No borres nada:** en el siguiente bloque (3.2.1) añadirás HTTPS a estos mismos sitios. Puedes dejar el contenedor en marcha.

Revisa que tu documento tiene:

| Evidencias | Preguntas |
|------------|-----------|
| E1 Las dos webs por su nombre | P1 – P2 (parte 1) |
| E2 Los dos logs separados | P3 – P4 (parte 1) |
| E3 `/hola/`, `/test` y `/mundo/` | P5 – P6 (parte 2) |
| E4 `/hola/index.html` antes y después de `^~` | P7 (parte 2) |
| E5 Errores de `/malo/` en código y en log | P8 (parte 2) |
| E6 301, 302, `rewrite` y `curl -L` | P9 – P10 (parte 3) |
| E7 El bucle de redirecciones | P11 – P12 (parte 3) |
| E8 La página de error propia | P13 – P14 (parte 4) |

Y que los tres **puntos de control 🧑‍🏫** están revisados por el profesor.
