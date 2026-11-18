---
layout: default
title: "Servidores Web — Bloque 3.1.1: Nginx (Taller en directo)"
permalink: /servidores-web/semana-1/taller/
---

# Taller 3.1.1 — Nginx en directo

**Módulo:** Despliegue de Aplicaciones Web (0614) · 2º DAW · UD3: Administración de servidores web

> Guion para el docente: lo que se hace en directo, compartiendo pantalla, después de la presentación. El alumnado **solo mira** (y pregunta); luego repetirá todo esto, y más, en la práctica.

**Duración:** 15–20 min · **Dónde:** en tu ordenador, con Docker Desktop. Todo se sirve en **`http://localhost:8080`**.

| # | Paso | Tiempo | Qué se ve |
|---|------|--------|-----------|
| 1 | Primer Nginx | 2 min | Un comando y ya hay web en `http://localhost:8080` |
| 2 | Dentro del contenedor | 3 min | Dónde está la configuración y quién ejecuta qué |
| 3 | Logs en directo | 2 min | Cada recarga del navegador es una línea |
| 4 | Mi web y mi configuración | 3 min | *Bind mounts*, `nginx -t` y `reload` |
| 5 | Romperlo a propósito | 3 min | `reload` aguanta; `restart` tumba la web |
| 6 | Módulos: miniaturas al vuelo | 4 min | `unknown directive`, `load_module` y la foto en el navegador |
| 7 | 403 y la cabecera `Server` | 2 min | Log de errores y `server_tokens off` |

---

## Antes de clase (5 min, una sola vez)

- [ ] Docker Desktop arrancado (`docker version` responde) y **nada escuchando en el puerto 8080** (`docker ps`).
- [ ] Imagen ya descargada, para no esperar en clase: `docker pull nginx:1.30`.
- [ ] **Copiar la carpeta del taller a `~/taller`.** Está en el repositorio, junto a este guion, en `handson/taller/`: la web (`html/index.html`), una foto de prueba de 1600 × 1000 (`html/img/foto.jpg`) y las carpetas `nginx/conf.d/` y `nginx/njs/` **vacías**, porque esos ficheros se crean en directo en los pasos 4 y 6. Desde la carpeta de este guion:
  ```bash
  rm -rf ~/taller                    # por si quedó de otra vez
  cp -R handson/taller ~/taller
  ls -R ~/taller
  ```
  > Si `~/taller` ya existe, `cp -R` crearía `~/taller/taller`: por eso se borra antes.
  >
  > Sin el repositorio a mano, todo esto (`taller/` y `solucion/`) está también en **`3_1_1_handson.zip`**: `unzip 3_1_1_handson.zip && cp -R 3_1_1_handson/taller ~/taller`.
  >
  > Si prefieres una foto tuya, sustitúyela: `cp mifoto.jpg ~/taller/html/img/foto.jpg`.
  >
  > La imagen del `index.html` aparecerá rota hasta el paso 6 (todavía no hay `/miniatura/`). Es una buena pregunta para la clase: «¿por qué no se ve?».
- [ ] **Plan B en directo:** en `handson/solucion/` están `compose.yaml` y `nginx/` tal como quedan al final del paso 6. Si una edición se tuerce: `cp -R handson/solucion/compose.yaml handson/solucion/nginx ~/taller/` y `cd ~/taller && docker compose up -d --build`.
- [ ] **Pantalla:** letra grande en el terminal. Dos terminales abiertos (uno para comandos y otro para `docker logs -f`), el editor con `~/taller` abierto y el navegador con `http://localhost:8080` (en una ventana privada, para que no use caché).

> **zsh** (el terminal por defecto del Mac): las URLs con `?` van **entre comillas** en `curl`, o zsh responde `no matches found`.

---

## Paso 1 — Primer Nginx (2 min)

```bash
docker run -d --name web -p 8080:80 nginx:1.30
curl -I http://localhost:8080
```

Abre `http://localhost:8080` en el navegador: **Welcome to nginx!**

🗣️ **Qué contar:**
- Un comando y hay un servidor web funcionando. `-p 8080:80` = puerto 8080 de mi ordenador → puerto 80 del contenedor. Dentro, Nginx escucha en el 80 de siempre.
- Señala en `curl -I` la cabecera **`Server: nginx/1.30.6`**: la volveremos a mirar en el paso 7.

## Paso 2 — Dentro del contenedor (3 min)

```bash
docker top web
```

```
UID    PID   ...  CMD
root   676   ...  nginx: master process nginx -g daemon off;
statd  723   ...  nginx: worker process
statd  724   ...  nginx: worker process
```

🗣️ El **maestro** corre como `root` y es el **proceso principal** del contenedor (`daemon off`). Los **workers** corren con el UID 101, que dentro del contenedor es el usuario `nginx`. Fuera sale otro nombre (`statd` en Docker Desktop) porque `docker top` traduce el UID con los usuarios de la máquina donde corre Docker, no con los del contenedor. Hay un *worker* por núcleo (`worker_processes auto`).

```bash
docker exec web ls /etc/nginx /etc/nginx/conf.d
docker exec web cat /etc/nginx/conf.d/default.conf
```

🗣️ Señala en `default.conf` el bloque `server`, el `location /`, y las directivas `listen`, `root` e `index`, **cada una con su `;`**. Si da tiempo:

```bash
docker exec web nginx -T | head -40
```

🗣️ `nginx -T` = **toda** la configuración efectiva, con los `include` ya resueltos.

## Paso 3 — Logs en directo (2 min)

En el **segundo terminal**:

```bash
docker logs -f web
```

Recarga varias veces `http://localhost:8080` en el navegador y pide una página que no existe (`http://localhost:8080/noexiste`).

🗣️ **Qué contar:**
- Cada recarga es **una línea**. Señala la IP del cliente, la petición, el **200** y el **404** y el *user-agent* del navegador.
- La IP no es `127.0.0.1` sino la de la pasarela de Docker (`192.168.65.1` en Docker Desktop): para Nginx, la petición llega desde fuera del contenedor.
- El 404 aparece **dos veces**: una línea en el log de acceso y otra en el de errores (`open() … failed (2: No such file or directory)`).

Deja este terminal así durante todo el taller.

---

## Paso 4 — Mi web y mi configuración (3–4 min)

Primero, fuera el contenedor de los pasos anteriores, y a la carpeta del taller:

```bash
docker rm -f web
cd ~/taller
ls -R
```

Salida esperada:

```
html  nginx

./html:
img  index.html

./html/img:
foto.jpg

./nginx:
conf.d  njs

./nginx/conf.d:

./nginx/njs:
```

🗣️ **Qué contar:** de momento solo tenemos **la web** (`html/`), que copié antes de clase. Las carpetas `nginx/conf.d/` y `nginx/njs/` están **vacías**. Ahora vamos a escribir, aquí en el disco de mi ordenador (no dentro del contenedor), los dos ficheros que faltan para que Nginx sirva esta web:

1. **`nginx/conf.d/default.conf`**: la configuración del sitio (qué nombre, qué carpeta, qué fichero por defecto).
2. **`compose.yaml`**: cómo arrancar el contenedor y qué carpetas de mi ordenador se montan dentro.

Como están en mi ordenador y no en el contenedor, **si borramos el contenedor no se pierden**.

**El sitio**, `nginx/conf.d/default.conf`:

```bash
cat > nginx/conf.d/default.conf <<'EOF'
server {
    listen 80;
    server_name localhost;

    root  /usr/share/nginx/html;
    index index.html;
}
EOF
```

🗣️ Lo mínimo: puerto, nombre del sitio, carpeta publicada y fichero por defecto. Es lo mismo que el `default.conf` que acabamos de ver dentro del contenedor, pero ahora es **nuestro**. El `listen` es el **80**: es el puerto de dentro del contenedor; el 8080 solo existe en mi ordenador.

**El `compose.yaml`:**

```bash
cat > compose.yaml <<'EOF'
services:
  web:
    image: nginx:1.30
    ports:
      - "8080:80"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./html:/usr/share/nginx/html:ro
    restart: unless-stopped
EOF
```

🗣️ Las dos líneas de `volumes` **sustituyen** la carpeta `conf.d` y la web de la imagen por las nuestras. `:ro` = solo lectura.

```bash
docker compose up -d
docker compose ps
```

(En el segundo terminal, corta el `docker logs -f web` con Ctrl+C y cambia a `cd ~/taller && docker compose logs -f`).

Recarga `http://localhost:8080`: ahora sale **tu** web.

🗣️ **Qué contar:**
- La web (`html/`) y los sitios (`nginx/conf.d/`) están en **mi ordenador** y se **montan** en el contenedor (`:ro`, solo lectura). Si borro el contenedor, no se pierde nada.
- Edita `html/index.html` en el editor (cambia una palabra) y recarga el navegador: **no hace falta recargar Nginx** para cambiar la web.
- Cambiar la **configuración**, en cambio, sí requiere recargar. Siempre así:

```bash
docker compose exec web nginx -t
docker compose exec web nginx -s reload
```

## Paso 5 — Romperlo a propósito (3 min)

Edita `nginx/conf.d/default.conf` y **quita el `;`** de la línea `index index.html;`.

```bash
docker compose exec web nginx -t
```

```
nginx: [emerg] unexpected "}" in /etc/nginx/conf.d/default.conf:7
nginx: configuration file /etc/nginx/nginx.conf test failed
```

🗣️ Te dice **qué**, **en qué fichero** y **en qué línea**… aunque la línea es la **siguiente**: sin el `;`, Nginx sigue leyendo la directiva `index` y tropieza con la `}`. Cuando el error señala una línea que parece bien, mira la de **antes**. Ahora, «me da igual, recargo»:

```bash
docker compose exec web nginx -s reload     # da el mismo error
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080
```

🗣️ **200**: el `reload` **rechaza** la configuración rota y Nginx **sigue funcionando** con la anterior. Parece que no pasa nada… hasta que alguien reinicia:

```bash
docker compose restart web
docker compose ps
```

```
NAME           ...   STATUS
taller-web-1   ...   Restarting (1) Less than a second ago
```

Recarga el navegador: **la web está caída**. En el segundo terminal se ve el `[emerg]` repetido cada pocos segundos.

Vuelve a poner el `;` y espera unos segundos: `restart: unless-stopped` vuelve a arrancarlo solo y `docker compose ps` muestra `Up`.

🗣️ **La moraleja:** `nginx -t` **antes** de recargar, siempre. Una configuración rota que nadie comprobó tumba la web en el **siguiente reinicio**, quizá horas después.

---

## Paso 6 — Módulos: miniaturas al vuelo (4 min)

```bash
docker compose exec web ls /etc/nginx/modules
```

🗣️ Estos `.so` son los **módulos dinámicos** que trae la imagen: `image_filter`, `js` (njs), `acme`, `geoip` y `xslt`. Están, pero **no están cargados**.

**6.1 Usar una directiva sin su módulo.** Edita `nginx/conf.d/default.conf` y añade este bloque dentro del `server`, antes de la `}` final:

```nginx
    location /miniatura/ {
        alias /usr/share/nginx/html/img/;
        image_filter resize $arg_w -;
        image_filter_buffer 10M;
    }
```

```bash
docker compose exec web nginx -t
```

```
nginx: [emerg] unknown directive "image_filter" in /etc/nginx/conf.d/default.conf:10
```

(El número de línea depende de dónde hayas pegado el bloque).

🗣️ Nginx no conoce la directiva porque **el módulo no está cargado**. Se carga con `load_module` al principio de `nginx.conf`, que es un fichero de la imagen… así que hacemos **nuestra propia imagen**.

**6.2 Nuestro `nginx.conf`.** Partimos del original de la imagen:

```bash
docker run --rm nginx:1.30 cat /etc/nginx/nginx.conf > nginx/nginx.conf
```

Ábrelo en el editor y haz tres cambios en directo:

- **Al principio del todo**, antes de `user nginx;`:
  ```nginx
  load_module modules/ngx_http_image_filter_module.so;
  load_module modules/ngx_http_js_module.so;
  ```
- **Dentro de `http { }`**, antes de `include /etc/nginx/conf.d/*.conf;`:
  ```nginx
      server_tokens off;

      js_path   /etc/nginx/njs/;
      js_import hola from hola.js;
  ```

🗣️ `load_module` **fuera** de cualquier bloque (contexto `main`); si lo pones dentro de `http`, `nginx -t` dice `"load_module" directive is not allowed here`. `server_tokens off` lo veremos en el paso 7.

**6.3 El JavaScript de njs y el `Dockerfile`:**

```bash
cat > nginx/njs/hola.js <<'EOF'
function saludo(r) {
    r.return(200, `Hola desde njs. Has pedido ${r.uri} con ${r.method}\n`);
}
export default { saludo };
EOF

cat > nginx/Dockerfile <<'EOF'
FROM nginx:1.30
COPY nginx.conf /etc/nginx/nginx.conf
COPY njs/ /etc/nginx/njs/
EOF
```

**6.4 Usar nuestra imagen.** En `compose.yaml`, cambia la línea `image: nginx:1.30` por:

```yaml
    build: ./nginx
```

```bash
docker compose up -d --build
docker compose exec web nginx -t
```

🗣️ `nginx.conf` y `njs/` van **dentro de la imagen** (cambian poco); el sitio y la web siguen **montados** (cambian a menudo).

Abre en el navegador:

- `http://localhost:8080/img/foto.jpg` (la original, 1600 × 1000)
- `http://localhost:8080/miniatura/foto.jpg?w=200`
- `http://localhost:8080/miniatura/foto.jpg?w=600`

Y recarga `http://localhost:8080`: la imagen del `index.html` ya se ve.

🗣️ **Una sola foto en disco y Nginx genera cada tamaño al vuelo.** `$arg_w` es el parámetro `w` de la URL.

**Si queda tiempo, njs:** añade al `server` de `nginx/conf.d/default.conf`

```nginx
    location = /hola {
        js_content hola.saludo;
    }
```

```bash
docker compose exec web nginx -t
docker compose exec web nginx -s reload
curl http://localhost:8080/hola
```

🗣️ JavaScript ejecutado **dentro de Nginx**. Fíjate en que aquí basta con `reload`: el módulo ya estaba cargado en nuestra imagen y solo hemos cambiado el sitio.

## Paso 7 — 403 y la cabecera `Server` (2 min)

```bash
mkdir html/fotos
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/fotos/
```

🗣️ **403**. La carpeta existe pero no tiene `index.html`, y Nginx **no lista carpetas** si no se le pide (`autoindex off`). El segundo terminal muestra el porqué: `directory index of "/usr/share/nginx/html/fotos/" is forbidden`.

🗣️ La otra causa típica de un 403 son los **permisos**: en un servidor Linux, un fichero con `chmod 600` que el *worker* (`nginx`) no puede leer da `(13: Permission denied)`. Con Docker Desktop no se ve, porque los ficheros montados desde el Mac o Windows se leen siempre; lo veréis en el servidor.

```bash
echo "<h1>Fotos</h1>" > html/fotos/index.html
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/fotos/   # 200
curl -I http://localhost:8080 | grep Server
```

🗣️ Ahora sale `Server: nginx`, **sin versión**: el `nginx.conf` de nuestra imagen lleva `server_tokens off;`. Compáralo con el paso 1.

**Y a la práctica**: «Ahora vosotros, y con evidencias.»

---

## Limpieza (después de clase)

```bash
cd ~/taller && docker compose down --rmi local && cd ~ && rm -rf ~/taller
```

Para repetir el taller con otro grupo, vuelve a copiar `handson/taller/` como en «Antes de clase».

---

## Cómo queda `~/taller` al final

```
~/taller/
├── compose.yaml            ← paso 4 (y build: ./nginx en el paso 6)
├── nginx/
│   ├── Dockerfile          ← paso 6
│   ├── nginx.conf          ← paso 6 (copiado de la imagen y editado)
│   ├── njs/hola.js         ← paso 6
│   └── conf.d/default.conf ← paso 4 (+ /miniatura/ y /hola en el paso 6)
└── html/
    ├── index.html          ← antes de clase (handson/taller/)
    ├── img/foto.jpg        ← antes de clase (handson/taller/)
    └── fotos/index.html    ← paso 7
```

Estos ficheros finales (salvo `html/fotos/`) están también en `handson/solucion/`. Si prefieres pegarlos en vez de copiarlos, aquí están los dos que más se editan en directo:

`nginx/conf.d/default.conf` (final):

```bash
cat > nginx/conf.d/default.conf <<'EOF'
server {
    listen 80;
    server_name localhost;

    root  /usr/share/nginx/html;
    index index.html;

    location /miniatura/ {
        alias /usr/share/nginx/html/img/;
        image_filter resize $arg_w -;
        image_filter_buffer 10M;
    }

    location = /hola {
        js_content hola.saludo;
    }
}
EOF
```

`nginx/nginx.conf` (final):

```bash
cat > nginx/nginx.conf <<'EOF'
load_module modules/ngx_http_image_filter_module.so;
load_module modules/ngx_http_js_module.so;

user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log notice;
pid        /run/nginx.pid;

events {
    worker_connections  1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    keepalive_timeout  65;

    server_tokens off;

    js_path   /etc/nginx/njs/;
    js_import hola from hola.js;

    include /etc/nginx/conf.d/*.conf;
}
EOF
```

### Comprobado

Con Docker Desktop (Docker 29.7) y `nginx:1.30` (1.30.6), en `localhost:8080`: `Server: nginx/1.30.6`; *workers* como `statd` en `docker top`; 404 en los dos logs con cliente `192.168.65.1`. Sin el `;` de `index`: `nginx -t` y `reload` dan `unexpected "}" … default.conf:7`, la web sigue respondiendo 200 y, tras `docker compose restart`, el contenedor queda en `Restarting (1)` hasta que se corrige y vuelve solo a `Up`. Miniaturas de la foto de 1600 × 1000 a 200 × 125 y 600 × 375; `/hola` con njs; `server_tokens off` → `Server: nginx`. 403 por carpeta sin índice (`directory index … is forbidden`); en cambio, un fichero montado con `chmod 600` devuelve 200.
