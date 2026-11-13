---
layout: default
title: "Servidores Web — Bloque 3.1.1: Nginx (Taller en directo)"
permalink: /servidores-web/semana-1/taller/
---

# Taller 3.1.1 — Nginx en directo

**Módulo:** Despliegue de Aplicaciones Web (0614) · 2º DAW · UD3: Administración de servidores web

> Guion para el docente: lo que se hace en directo, compartiendo pantalla, después de la presentación. El alumnado **solo mira** (y pregunta); luego repetirá todo esto, y más, en la práctica.

**Duración:** 15–20 min · **Dónde:** en tu VM de Azure (`ssh daw`), con tu dominio (en este guion, `tunombre.me`).

| # | Paso | Tiempo | Qué se ve |
|---|------|--------|-----------|
| 1 | Primer Nginx | 2 min | Un comando y ya hay web en `http://tunombre.me` |
| 2 | Dentro del contenedor | 3 min | Dónde está la configuración y quién ejecuta qué |
| 3 | Logs en directo | 2 min | Cada recarga del navegador es una línea |
| 4 | Mi web y mi configuración | 3 min | *Bind mounts*, `nginx -t` y `reload` |
| 5 | Romperlo a propósito | 3 min | `reload` aguanta; `restart` tumba la web |
| 6 | Módulos: miniaturas al vuelo | 4 min | `unknown directive`, `load_module` y la foto en el navegador |
| 7 | 403 y la cabecera `Server` | 2 min | Permisos, log de errores y `server_tokens off` |

---

## Antes de clase (10 min, una sola vez)

- [ ] La VM encendida y `ssh daw` funcionando. **Nada escuchando en el puerto 80** (`docker ps`; si queda el `prueba` del dosier 1: `docker rm -f prueba`).
- [ ] `dig +short tunombre.me` devuelve la IP de la VM.
- [ ] Imagen ya descargada, para no esperar en clase: `ssh daw 'docker pull nginx:1.30'`.
- [ ] **Copiar la carpeta del taller a la VM.** Está en el repositorio, junto a este guion, en `handson/taller/`: la web (`html/index.html`), una foto de prueba de 1600 × 1000 (`html/img/foto.jpg`) y las carpetas `nginx/conf.d/` y `nginx/njs/` **vacías**, porque esos ficheros se crean en directo en los pasos 4 y 6. Desde **tu ordenador**, en la carpeta de este guion:
  ```bash
  cd "UD3/3.1 Configuración de servidores web/3.1.1 Apache y Nginx/handson"
  ssh daw 'rm -rf ~/taller'          # por si quedó de otra vez
  scp -r taller daw:~/
  ssh daw 'ls -R ~/taller'
  ```
  > Si `~/taller` ya existe, `scp -r` crearía `~/taller/taller`: por eso se borra antes.
  >
  > Si prefieres una foto tuya, sustitúyela: `scp mifoto.jpg daw:~/taller/html/img/foto.jpg`.
  >
  > La imagen del `index.html` aparecerá rota hasta el paso 6 (todavía no hay `/miniatura/`). Es una buena pregunta para la clase: «¿por qué no se ve?».
- [ ] **Plan B en directo:** en `handson/solucion/` están `compose.yaml` y `nginx/` tal como quedan al final del paso 6 (cambia `tunombre.me` por tu dominio en `nginx/conf.d/default.conf`). Si una edición se tuerce: `scp -r solucion/compose.yaml solucion/nginx daw:~/taller/` y `ssh daw 'cd ~/taller && docker compose up -d --build'`.
- [ ] **Pantalla:** letra grande en el terminal. Dos terminales abiertos con `ssh daw` (uno para comandos y otro para `docker logs -f`) y el navegador con `http://tunombre.me` (en una ventana privada, para que no use caché).

> **Plan B** si la VM falla: Docker Desktop en tu portátil, con `localhost` en lugar de `tunombre.me`. Todo funciona igual **salvo el 403 por permisos del paso 7**, que con Docker Desktop no aparece (se puede enseñar creando el fichero dentro del contenedor: `docker exec web sh -c 'echo x > /usr/share/nginx/html/s.html; chmod 600 /usr/share/nginx/html/s.html'`).

---

## Paso 1 — Primer Nginx (2 min)

```bash
docker run -d --name web -p 80:80 nginx:1.30
curl -I http://localhost
```

Abre `http://tunombre.me` en el navegador: **Welcome to nginx!**

🗣️ **Qué contar:**
- Un comando y hay un servidor web en Internet. `-p 80:80` = puerto 80 de la VM → puerto 80 del contenedor; el NSG de Azure ya tenía el 80 abierto (dosier 1).
- Señala en `curl -I` la cabecera **`Server: nginx/1.30.6`**: la volveremos a mirar en el paso 7.

## Paso 2 — Dentro del contenedor (3 min)

```bash
docker top web
```

```
UID    PID   ...  CMD
root   2459  ...  nginx: master process nginx -g daemon off;
101    2502  ...  nginx: worker process
101    2503  ...  nginx: worker process
```

🗣️ El **maestro** corre como `root` y es el **proceso principal** del contenedor (`daemon off`). Los **workers** corren con el UID 101, que dentro del contenedor es el usuario `nginx` (en la VM puede salir otro nombre para ese UID). Hay un *worker* por núcleo (`worker_processes auto`).

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

Recarga varias veces `http://tunombre.me` en el navegador y pide una página que no existe (`http://tunombre.me/noexiste`).

🗣️ **Qué contar:**
- Cada recarga es **una línea**. Señala la IP (la del centro), la petición, el **200** y el **404** y el *user-agent* del navegador.
- El 404 aparece **dos veces**: una línea en el log de acceso y otra en el de errores (`open() … failed (2: No such file or directory)`).
- Si aparece alguna línea que no es vuestra (`/wp-login.php`, `/.env`…), **aprovéchala**: son bots que ya han encontrado la VM.

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
.:
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

🗣️ **Qué contar:** de momento solo tenemos **la web** (`html/`), que copié antes de clase. Las carpetas `nginx/conf.d/` y `nginx/njs/` están **vacías**. Ahora vamos a escribir, aquí en el disco de la VM (no dentro del contenedor), los dos ficheros que faltan para que Nginx sirva esta web:

1. **`nginx/conf.d/default.conf`**: la configuración del sitio (qué dominio, qué carpeta, qué fichero por defecto).
2. **`compose.yaml`**: cómo arrancar el contenedor y qué carpetas de la VM se montan dentro.

Como están en la VM y no en el contenedor, **si borramos el contenedor no se pierden**.

**El sitio**, `nginx/conf.d/default.conf` (cambia `tunombre.me` por tu dominio):

```bash
cat > nginx/conf.d/default.conf <<'EOF'
server {
    listen 80;
    server_name tunombre.me www.tunombre.me;

    root  /usr/share/nginx/html;
    index index.html;
}
EOF
```

🗣️ Lo mínimo: puerto, nombre del sitio, carpeta publicada y fichero por defecto. Es lo mismo que el `default.conf` que acabamos de ver dentro del contenedor, pero ahora es **nuestro**.

**El `compose.yaml`:**

```bash
cat > compose.yaml <<'EOF'
services:
  web:
    image: nginx:1.30
    ports:
      - "80:80"
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

Recarga `http://tunombre.me`: ahora sale **tu** web.

🗣️ **Qué contar:**
- La web (`html/`) y los sitios (`nginx/conf.d/`) están en la **VM** y se **montan** en el contenedor (`:ro`, solo lectura). Si borro el contenedor, no se pierde nada.
- Edita `html/index.html` (cambia una palabra) y recarga el navegador: **no hace falta recargar Nginx** para cambiar la web.
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
nginx: [emerg] directive "index" is not terminated by ";" in /etc/nginx/conf.d/default.conf:6
nginx: configuration file /etc/nginx/nginx.conf test failed
```

🗣️ Te dice **qué**, **en qué fichero** y **en qué línea**. Ahora, «me da igual, recargo»:

```bash
docker compose exec web nginx -s reload     # da el mismo error
curl -s -o /dev/null -w "%{http_code}\n" http://localhost
```

🗣️ **200**: el `reload` **rechaza** la configuración rota y Nginx **sigue funcionando** con la anterior. Parece que no pasa nada… hasta que alguien reinicia:

```bash
docker compose restart web
docker compose ps
```

```
NAME           ...   STATUS
taller-web-1   ...   Restarting (1) 2 seconds ago
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

**6.1 Usar una directiva sin su módulo.** Edita `nginx/conf.d/default.conf` (`nano nginx/conf.d/default.conf`) y añade este bloque dentro del `server`, antes de la `}` final:

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
nano nginx/nginx.conf
```

Haz tres cambios en directo:

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

**6.4 Usar nuestra imagen.** En `compose.yaml` (`nano compose.yaml`), cambia la línea `image: nginx:1.30` por:

```yaml
    build: ./nginx
```

```bash
docker compose up -d --build
docker compose exec web nginx -t
```

🗣️ `nginx.conf` y `njs/` van **dentro de la imagen** (cambian poco); el sitio y la web siguen **montados** (cambian a menudo).

Abre en el navegador:

- `http://tunombre.me/img/foto.jpg` (la original)
- `http://tunombre.me/miniatura/foto.jpg?w=200`
- `http://tunombre.me/miniatura/foto.jpg?w=600`

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
curl http://tunombre.me/hola
```

🗣️ JavaScript ejecutado **dentro de Nginx**. Fíjate en que aquí basta con `reload`: el módulo ya estaba cargado en nuestra imagen y solo hemos cambiado el sitio.

## Paso 7 — 403 y la cabecera `Server` (2 min)

```bash
echo "secreto" > html/secreto.html
chmod 600 html/secreto.html
ls -l html/secreto.html
curl -s -o /dev/null -w "%{http_code}\n" http://localhost/secreto.html
```

🗣️ **403**. El fichero es de `daw` con permisos `600` y el *worker* corre como `nginx`, que no puede leerlo. El segundo terminal muestra el porqué: `open() "…/secreto.html" failed (13: Permission denied)`.

```bash
chmod 644 html/secreto.html
curl -s -o /dev/null -w "%{http_code}\n" http://localhost/secreto.html   # 200
curl -I http://localhost | grep Server
```

🗣️ Ahora sale `Server: nginx`, **sin versión**: el `nginx.conf` de nuestra imagen lleva `server_tokens off;`. Compáralo con el paso 1.

**Y a la práctica**: «Ahora vosotros, en vuestra VM, y con evidencias.»

---

## Limpieza (después de clase)

```bash
ssh daw 'cd ~/taller && docker compose down --rmi local && rm -rf ~/taller'
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
    └── img/foto.jpg        ← antes de clase (handson/taller/)
```

Estos ficheros finales están también en `handson/solucion/`. Si prefieres pegarlos en vez de copiarlos con `scp`, aquí están los dos que más se editan en directo:

`nginx/conf.d/default.conf` (final):

```bash
cat > nginx/conf.d/default.conf <<'EOF'
server {
    listen 80;
    server_name tunombre.me www.tunombre.me;

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

Con `nginx:1.30` (1.30.6): miniaturas de una foto de 1200 × 800 a 300 px (1 678 bytes) y a 100 px (830 bytes), `/hola` con njs, `server_tokens off` → `Server: nginx`, 403 por carpeta sin índice, 404. Con el `;` quitado: `nginx -t` y `reload` dan `directive "index" is not terminated by ";"`, la web sigue respondiendo 200 y, tras `docker compose restart`, el contenedor queda en `Restarting (1)` hasta que se corrige y vuelve solo a `Up`.
