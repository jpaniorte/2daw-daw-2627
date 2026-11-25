---
layout: default
title: "Servidores Web — Bloque 3.1.2: Hosts virtuales y redirecciones (Teoría)"
permalink: /servidores-web/semana-2/teoria/
---

# Bloque 3.1.2 — Hosts virtuales y redirecciones

**Módulo:** Despliegue de Aplicaciones Web (0614) · 2º DAW · UD3: Administración de servidores web

> En el bloque 3.1.1 pusimos en marcha **un** Nginx que servía **una** web. Pero un servidor real no atiende una sola cosa: aloja varias webs, cada una en su nombre y con sus rutas, y a veces tiene que decirle al cliente «esto se ha mudado». Hoy aprendemos a **configurarlo**: **hosts virtuales** (varias webs en un servidor), **`location`** (qué hacer con cada ruta: `/hola` para una aplicación, `/test` para otra, `/mundo` para otra) y **redirecciones**.

Todo el bloque se practica en **`localhost`**: no hace falta dominio, DNS ni máquina remota. Lo que aprendas aquí es exactamente lo que aplicarás después a `tunombre.me` en la VM.

## Planificación orientativa

| # | Sección |
|---|---------|
| 1 | Un servidor, muchas webs: la cabecera `Host` |
| 2 | Hosts virtuales en Nginx |
| 3 | El servidor por defecto |
| 4 | `location`: cada ruta, su aplicación |
| 5 | `root` frente a `alias`, y `try_files` |
| 6 | Redirecciones |
| 7 | Páginas de error propias |
| 8 | Y en Apache… |
| 9 | Todo junto: una cocina, varias marcas |

## 1. Un servidor, muchas webs: la cabecera `Host`

Un servidor tiene **una** IP y escucha en el puerto 80. Sin embargo, `miweb.com` y `tienda.com` pueden apuntar a esa misma IP. ¿Cómo sabe Nginx cuál de las dos quieres? Por la **cabecera `Host`** que el navegador envía en cada petición (la vimos en el bloque 2.1):

```
GET / HTTP/1.1
Host: tienda.localhost
```

Con eso, un mismo servidor puede alojar tantas webs como quiera. Cada una es un **host virtual** (en Nginx, un bloque `server`). Hay tres maneras de distinguirlos:

| Tipo | Qué decide la web | Cuándo se usa |
|------|-------------------|---------------|
| **Por nombre** | La cabecera `Host` | **Casi siempre.** Una IP, muchas webs |
| **Por IP** | La IP a la que llega la petición | Un servidor con varias IP, una por web (hoy raro) |
| **Por puerto** | El puerto (`:8080`, `:8081`) | Pruebas y servicios internos |

En este bloque trabajamos con los hosts **por nombre**.

> **Una analogía:** el edificio es el servidor (una dirección, una puerta). Dentro hay varios restaurantes. El **`Host`** es el nombre del restaurante que dices al entrar; el portero (Nginx) te lleva al comedor correcto.

## 2. Hosts virtuales en Nginx

### 2.1 Un bloque `server` por web

En la imagen oficial, los sitios van en `/etc/nginx/conf.d/*.conf`. Cada web es un `server`:

```nginx
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
```

Los dos escuchan en el **mismo puerto**. Lo que los distingue es `server_name`.

### 2.2 Cómo elige Nginx el `server`

Nginx decide en dos pasos:

1. **Por `listen`**: se queda con los `server` que escuchan en la IP y el puerto a los que ha llegado la petición.
2. **Por `server_name`**: entre ellos, elige el que coincide con la cabecera `Host`. Si ninguno coincide, responde el **servidor por defecto** (sección 3).

`server_name` admite varios nombres y comodines:

```nginx
server_name tienda.localhost www.tienda.localhost;   # dos nombres para la misma web
server_name *.localhost;                              # cualquier subdominio
```

### 2.3 Probarlo sin tocar el DNS

Los nombres que acaban en **`.localhost`** se resuelven siempre a `127.0.0.1`, sin configurar nada. Basta con:

```bash
curl http://localhost/              # → <h1>Web principal</h1>
curl http://tienda.localhost/       # → <h1>Tienda</h1>
```

Y si quieres probar **cualquier** nombre sin que exista, envía tú la cabecera con `-H`:

```bash
curl -H "Host: tienda.localhost" http://localhost/
```

> **Es la herramienta de depuración clave de este bloque.** Con `curl -H "Host: …"` compruebas qué `server` responde a cada nombre, aunque el DNS no exista todavía.

### 2.4 Un `root` y unos logs por sitio

Cada host virtual tiene su propia carpeta (`root`) y puede tener sus propios logs:

```nginx
server {
    listen      80;
    server_name tienda.localhost;
    root        /usr/share/nginx/sitios/tienda;
    access_log  /var/log/nginx/tienda.access.log;
    error_log   /var/log/nginx/tienda.error.log;
}
```

Así, cuando algo falla en la tienda, miras el log de la tienda y no una mezcla de todas las webs (recuerda `docker logs` del bloque 3.1.1: lo que va a `/dev/stdout` se ve ahí; los ficheros propios se leen con `docker exec web tail /var/log/nginx/tienda.access.log`).

## 3. El servidor por defecto

¿Qué pasa si llega una petición con un `Host` que no coincide con ningún `server_name`? Por ejemplo, alguien entra por la **IP** en vez de por el nombre, o un bot prueba `Host: cualquiercosa.com`.

- Si no has dicho nada, responde **el primer `server` definido** para ese puerto. Es un error muy típico: la web de un cliente se ve con el nombre de otro.
- Lo correcto es **declarar tú el servidor por defecto** con `default_server`:

```nginx
server {
    listen 80 default_server;
    server_name _;            # un nombre que no existe: no coincide con nada
    return 444;               # Nginx cierra la conexión sin responder
}
```

Resultado:

```bash
curl -H "Host: otro.com" http://localhost/
# curl: (52) Empty reply from server
```

`444` es un código **propio de Nginx** (no existe en HTTP): corta la conexión sin enviar nada. Otra opción es `return 404;` si prefieres responder algo.

> En Apache pasa lo mismo: responde el primer `<VirtualHost>` (por eso el fichero por defecto se llama `000-default.conf`, para que se cargue el primero).

## 4. `location`: cada ruta, su aplicación

Dentro de un `server`, los bloques **`location`** deciden qué hacer según la **ruta** de la URL. Es lo que permite que `/hola` sea una aplicación, `/test` otra y `/mundo` otra, **dentro del mismo host**.

### 4.1 Un ejemplo con tres rutas

```nginx
server {
    listen      80;
    server_name localhost;
    root        /usr/share/nginx/sitios/principal;

    location / { index index.html; }                 # la web principal

    location /hola/  { }                             # carpeta principal/hola/
    location = /test { return 200 "Solo /test\n"; }  # solo esa URL exacta
    location /mundo/ { alias /usr/share/nginx/sitios/docs/; }   # otra carpeta
}
```

```bash
curl http://localhost/hola/      # → <h1>App hola</h1>
curl http://localhost/test       # → Solo /test
curl http://localhost/mundo/     # → <h1>Documentacion</h1>
```

Cada `location` puede tener su propia carpeta, su propia respuesta, sus propias redirecciones o, más adelante (bloque 3.2.2), enviar la petición a **otra aplicación** con `proxy_pass`.

### 4.2 Cómo elige Nginx la `location`

Varias `location` pueden coincidir con la misma URL. Nginx aplica **este orden**:

| Orden | Forma | Significado |
|-------|-------|-------------|
| 1.º | `location = /ruta` | **Exacta**: solo esa URL. Si coincide, gana y se acaba |
| 2.º | `location ^~ /ruta` | **Prefijo preferente**: si es el prefijo más largo, gana y **no se miran las expresiones regulares** |
| 3.º | `location ~ regex` | **Expresión regular** (distingue mayúsculas; `~*` no las distingue). Gana la **primera que coincida en el fichero** |
| 4.º | `location /ruta` | **Prefijo normal**: si no ha ganado nada antes, se usa el prefijo **más largo** |

Ejemplo comprobado:

```nginx
location = /test      { return 200 "exacta\n"; }
location ^~ /img/     { return 200 "prefijo ^~\n"; }
location ~ \.(png|jpg)$ { return 200 "regex\n"; }
location /            { index index.html; }
```

| Petición | Responde | Por qué |
|----------|----------|---------|
| `/test` | `exacta` | Coincide la exacta |
| `/test/` | la web `principal/test/` | **No** es exacta: cae en `location /` |
| `/img/a.png` | `prefijo ^~` | `^~` impide que se mire la expresión regular de `.png` |
| `/foto.png` | `regex` | No hay prefijo `^~` que lo impida |
| `/otra/cosa` | `location /` | Es el prefijo más largo que coincide |

> **Reglas prácticas:** para una URL concreta, `=`. Para una carpeta, un prefijo (`location /hola/`). Para «todos los ficheros de un tipo», una regex. Y si una regex te «roba» una carpeta, pon `^~` en esa carpeta.

### 4.3 La barra final importa

- `location /hola/ { }` atiende `/hola/…`. Si el cliente pide **`/hola`** (sin barra) y existe la carpeta, Nginx responde con una **redirección 301** a `/hola/`:

```bash
curl -I http://localhost/hola
# HTTP/1.1 301 Moved Permanently
# Location: http://localhost/hola/
```

- Por eso conviene escribir las `location` de carpeta **con barra final**.

## 5. `root` frente a `alias`, y `try_files`

### 5.1 `root` añade la ruta; `alias` la sustituye

Las dos dicen «de qué carpeta saco los ficheros», pero se comportan distinto:

| | Fichero que busca Nginx para `GET /mundo/index.html` |
|--|------|
| `location /mundo/ { root /datos; }` | `/datos`**`/mundo/`**`index.html` (la ruta **se añade**) |
| `location /mundo/ { alias /datos/; }` | `/datos/index.html` (la parte `/mundo/` **se sustituye**) |

Con `root`, la carpeta se tiene que llamar como la URL. Con `alias`, puedes servir **cualquier carpeta** bajo la ruta que quieras (un `/docs` que está fuera del `root` del sitio, por ejemplo).

Comprobado: este `root` busca el fichero donde no está.

```nginx
location /ro/ { root /usr/share/nginx/sitios/docs; }
# GET /ro/index.html → 404
# error.log: open() "/usr/share/nginx/sitios/docs/ro/index.html" failed (2: No such file or directory)
```

### 5.2 La trampa de la barra en `alias`

Si la `location` termina en `/`, el `alias` **también** debe terminar en `/`. Si no, las rutas salen mal:

```nginx
location /malo/  { alias /usr/share/nginx/sitios/docs;  }   # sin barra final
location /bueno/ { alias /usr/share/nginx/sitios/docs/; }   # correcto
```

```bash
curl -i http://localhost/malo/              # 403 Forbidden
curl -i http://localhost/malo/index.html    # 404 Not Found
curl -i http://localhost/bueno/index.html   # 200 OK
```

En el log de errores se ve qué ha pasado: Nginx **pega** lo que sobra de la URL a la ruta del `alias`:

```
open() "/usr/share/nginx/sitios/docsindex.html" failed (2: No such file or directory)
```

> **`docsindex.html`**: falta una barra. Si ves un nombre de fichero «pegado» en el log, mira la barra final de tu `alias`.

### 5.3 `try_files`: probar varias opciones

`try_files` busca, en orden, un fichero o carpeta y, si no existe ninguno, usa la **última opción** (una ruta o un código):

```nginx
location /app/ {
    try_files $uri /nuevo.html;     # el fichero pedido; si no existe, /nuevo.html
}
```

```bash
curl http://localhost/app/loquesea    # → <h1>Nuevo</h1>
```

Se usa mucho para aplicaciones de una sola página (siempre devolver `index.html`) y para «si existe el fichero, sírvelo; si no, haz otra cosa».

## 6. Redirecciones

Una **redirección** le dice al cliente: «lo que buscas está en **otra URL**; pídelo allí». El servidor responde con un código `3xx` y una cabecera `Location`.

### 6.1 Qué código usar

| Código | Nombre | Es… | El método |
|--------|--------|-----|-----------|
| **301** | Moved Permanently | **Permanente** | Los navegadores pueden cambiar `POST` por `GET` |
| **302** | Found | **Temporal** | Igual |
| **307** | Temporary Redirect | Temporal | **Se mantiene** (`POST` sigue siendo `POST`) |
| **308** | Permanent Redirect | Permanente | **Se mantiene** |

La regla del día a día: **301 si el cambio es para siempre, 302 si es temporal** (por ejemplo, una página en mantenimiento).

Además:

- **Buscadores:** un 301 les dice que transfieran su posición a la URL nueva; un 302 no.
- **Cachés:** los navegadores **recuerdan** un 301. Si te equivocas, tendrás que limpiar la caché o probar en una ventana privada (aunque corrijas el servidor, tu navegador seguirá yendo al sitio equivocado). **Mientras pruebas, usa 302** y cámbialo a 301 cuando funcione.

### 6.2 `return`: la forma más simple y clara

```nginx
location = /viejo { return 301 /nuevo.html; }        # permanente
location /tmp      { return 302 /nuevo.html; }       # temporal
```

```bash
curl -I http://localhost/viejo
# HTTP/1.1 301 Moved Permanently
# Location: http://localhost/nuevo.html

curl -I http://localhost/tmp
# HTTP/1.1 302 Moved Temporarily
# Location: http://localhost/nuevo.html
```

Para seguirla hasta el final, `curl -L`:

```bash
curl -L http://localhost/viejo       # → <h1>Nuevo</h1>
```

### 6.3 Caso típico: de `www` a sin `www`

Un `server` aparte cuya única misión es redirigir, **conservando la ruta y los parámetros** con `$request_uri`:

```nginx
server {
    listen      80;
    server_name www.localhost;
    return 301  http://localhost$request_uri;
}
```

```bash
curl -I -H "Host: www.localhost" http://localhost/hola/
# HTTP/1.1 301 Moved Permanently
# Location: http://localhost/hola/
```

(Al revés es igual: redirigir `localhost` a `www.localhost`. Lo importante es **elegir una forma y mantenerla**, para no tener la misma web duplicada.)

### 6.4 `rewrite`: cambiar la URL con una expresión regular

Cuando hay que transformar la ruta, no solo sustituirla entera, se usa `rewrite`:

```nginx
location /reglas {
    rewrite ^/reglas/(.*)$ /$1 permanent;     # /reglas/x → /x, con 301
}
```

```bash
curl -I http://localhost/reglas/nuevo.html
# HTTP/1.1 301 Moved Permanently
# Location: http://localhost/nuevo.html
```

- `rewrite regex destino [flag];`. Con `permanent` responde 301 y con `redirect`, 302. Sin flag, **reescribe la URL internamente** y el cliente no se entera.
- `(.*)` captura lo que sigue, y `$1` lo reutiliza en el destino.

**¿`return` o `rewrite`?** Si basta con una URL fija o con `$request_uri`, **`return`**: es más claro y más rápido. Usa `rewrite` solo cuando necesites capturar partes de la URL.

### 6.5 Casos de uso

| Situación | Solución |
|-----------|----------|
| Una página ha cambiado de sitio | `location = /viejo { return 301 /nuevo; }` |
| Cambia la estructura de URL (`/blog/2026/x` → `/articulos/x`) | `rewrite` con 301 |
| Quitar o poner `www` | Un `server` solo para redirigir (6.3) |
| Mantenimiento temporal | `return 302 /mantenimiento.html;` |
| Pasar de HTTP a HTTPS | `return 301 https://$host$request_uri;` (lo hacemos en el bloque 3.2.1) |

### 6.6 El peligro: los bucles de redirección

Una redirección que apunta a sí misma, o dos que se apuntan entre sí, no termina nunca:

```nginx
location /bucle { return 301 /bucle; }
```

```bash
curl -L http://localhost/bucle
# curl: (47) Maximum (50) redirects followed
```

`curl` se rinde a las 50; un navegador muestra **«ERR_TOO_MANY_REDIRECTS»**. Casi siempre aparece al combinar dos reglas (por ejemplo, HTTP→HTTPS y `www`→sin `www` mal escritas). Cuando falles, **mira las cabeceras de cada salto** con `curl -IL`.

## 7. Páginas de error propias

Por defecto, un 404 muestra la página gris de Nginx. Con `error_page` la cambias por una tuya:

```nginx
server {
    ...
    error_page 404 /errores/404.html;

    location /errores/ {
        alias    /usr/share/nginx/sitios/errores/;
        internal;                                  # solo accesible desde Nginx
    }
}
```

```bash
curl -i http://localhost/nada
# HTTP/1.1 404 Not Found
# <h1>Esta pagina no existe (404 propia)</h1>
```

- El **código sigue siendo 404** (la página cambia, no el código): es lo correcto para los buscadores.
- `internal;` hace que la página solo se pueda usar como respuesta de error; si alguien pide directamente `/errores/404.html` sin que haya error, recibe también 404.
- Se pueden agrupar varios códigos: `error_page 500 502 503 504 /50x.html;`.

## 8. Y en Apache…

Las ideas son las mismas; cambia la sintaxis. Equivalencias de lo que hemos visto (comprobado `Redirect` y `RewriteRule` con `httpd:2.4`):

| Idea | Nginx | Apache |
|------|-------|--------|
| Host virtual | `server { … }` | `<VirtualHost *:80> … </VirtualHost>` |
| Nombre del sitio | `server_name a b;` | `ServerName a` + `ServerAlias b` |
| Carpeta de la web | `root` | `DocumentRoot` |
| Servidor por defecto | `listen 80 default_server;` | El **primer** `<VirtualHost>` cargado |
| Carpeta fuera del `root` | `location /docs/ { alias …; }` | `Alias /docs/ /ruta/` |
| Redirección simple | `return 301 /nuevo;` | `Redirect 301 /viejo /nuevo` |
| Redirección con patrón | `rewrite ^/a/(.*)$ /b/$1 permanent;` | `RedirectMatch 301 ^/a/(.*)$ /b/$1` o `RewriteRule` |
| Reescritura avanzada | `rewrite`, `if`, `map` | `mod_rewrite`: `RewriteEngine On`, `RewriteCond`, `RewriteRule` |
| Página de error | `error_page 404 /404.html;` | `ErrorDocument 404 /404.html` |
| Logs por sitio | `access_log` / `error_log` | `CustomLog` / `ErrorLog` |
| Configuración por carpeta | **No existe** | **`.htaccess`** |

```apache
<VirtualHost *:80>
    ServerName   localhost
    DocumentRoot /var/www/principal
    Redirect 301 /viejo /nuevo.html
    RewriteEngine On
    RewriteRule ^/reglas/(.*)$ /$1 [R=301,L]
</VirtualHost>
```

### `.htaccess`: la configuración que cada carpeta lleva consigo

En Apache, un fichero `.htaccess` dentro de una carpeta cambia la configuración **solo para esa carpeta**, sin tocar la configuración del servidor ni reiniciarlo. Es cómodo (lo usan los alojamientos compartidos y WordPress), pero:

- Apache tiene que **buscar y leer** `.htaccess` en cada carpeta de la ruta, **en cada petición**: es más lento.
- Solo funciona si el servidor lo permite con **`AllowOverride`**. Con `AllowOverride None` se ignora.
- Cualquiera con acceso a la carpeta puede cambiar el comportamiento del servidor.

**Nginx no tiene nada parecido**: toda la configuración está en los ficheros del servidor. Es una de las razones de su rendimiento, y por eso, si vienes de Apache, tus reglas de `.htaccess` se convierten en `location`, `return` y `rewrite`.

## 9. Todo junto: una cocina, varias marcas

Una carpeta con todo lo de hoy, en tu máquina (con Docker):

```
servidor/
├── compose.yaml
├── conf.d/
│   └── sitios.conf         ← los hosts virtuales, las location y las redirecciones
└── sitios/
    ├── principal/          ← localhost (index.html, nuevo.html, hola/, test/)
    ├── tienda/             ← tienda.localhost
    ├── docs/               ← lo que sirve /mundo/
    └── errores/404.html
```

```yaml
services:
  web:
    image: nginx:1.30
    ports:
      - "80:80"
    volumes:
      - ./conf.d:/etc/nginx/conf.d:ro
      - ./sitios:/usr/share/nginx/sitios:ro
    restart: unless-stopped
```

`conf.d/sitios.conf` (resumen de todo lo anterior):

```nginx
# Servidor por defecto: lo que no coincide con ningún nombre
server {
    listen 80 default_server;
    server_name _;
    return 444;
}

# localhost: la web principal con sus rutas
server {
    listen      80;
    server_name localhost;
    root        /usr/share/nginx/sitios/principal;
    access_log  /var/log/nginx/principal.access.log;
    error_page  404 /errores/404.html;

    location /          { index index.html; }
    location /hola/     { }
    location = /test    { return 200 "Solo /test\n"; }
    location /mundo/    { alias /usr/share/nginx/sitios/docs/; }
    location /errores/  { alias /usr/share/nginx/sitios/errores/; internal; }

    location = /viejo   { return 301 /nuevo.html; }
    location /tmp       { return 302 /nuevo.html; }
}

# tienda.localhost: otra web en el mismo servidor
server {
    listen      80;
    server_name tienda.localhost;
    root        /usr/share/nginx/sitios/tienda;
    access_log  /var/log/nginx/tienda.access.log;
}

# www.localhost: solo redirige
server {
    listen      80;
    server_name www.localhost;
    return 301  http://localhost$request_uri;
}
```

Arranque y comprobación:

```bash
docker compose up -d
docker compose exec web nginx -t

curl http://localhost/                      # web principal
curl http://tienda.localhost/               # la tienda
curl http://localhost/hola/                 # App hola
curl http://localhost/test                  # Solo /test
curl http://localhost/mundo/                # Documentación
curl -I http://localhost/viejo              # 301 → /nuevo.html
curl -IL http://localhost/tmp               # 302 y luego 200
curl -I -H "Host: www.localhost" http://localhost/hola/   # 301 a localhost
curl -H "Host: otro.com" http://localhost/  # (52) Empty reply from server
curl -i http://localhost/nada               # 404 con la página propia
```

- Después de editar `conf.d/`: `docker compose exec web nginx -t` y `docker compose exec web nginx -s reload` (bloque 3.1.1).
- Un fallo de configuración: `nginx -t` dice en qué línea; un fichero «pegado» en el log, mira la barra de un `alias`.

### Qué viene en el siguiente bloque

Hoy cada `location` servía **ficheros**. En el bloque 3.2.1 ponemos **HTTPS** (con la redirección de HTTP a HTTPS que acabamos de adelantar) y control de acceso, y en el 3.2.2, con `proxy_pass`, cada `location` enviará la petición a **otra aplicación** en otro contenedor.

---

## Ideas clave del bloque

- Un servidor puede alojar **varias webs**: Nginx elige por la **IP y puerto (`listen`)** y por la cabecera **`Host`** (`server_name`). Cada web es un **host virtual** (un bloque `server`).
- Los nombres `*.localhost` resuelven a `127.0.0.1`. Para probar cualquier nombre: `curl -H "Host: nombre" http://localhost/`.
- El **servidor por defecto** responde cuando el `Host` no coincide con nada. Si no lo declaras (`listen 80 default_server;`), es el primero del fichero. Con `return 444;` cierra la conexión.
- **`location`** decide qué hacer con cada ruta. Orden: **`=`** exacta → **`^~`** prefijo preferente → **`~`** regex (la primera) → **prefijo más largo**.
- **`root`** **añade** la ruta de la URL a la carpeta; **`alias`** la **sustituye**. Con una `location` terminada en `/`, el `alias` también debe terminar en `/` (si no, ficheros «pegados» como `docsindex.html`).
- `try_files` prueba opciones en orden y usa la última si falla ninguna.
- **301** = permanente (los navegadores lo recuerdan, también los buscadores). **302** = temporal. **307/308** mantienen el método. Mientras pruebas, usa 302.
- **`return`** para redirecciones simples (con `$request_uri` conserva la ruta); **`rewrite`** cuando haga falta capturar partes con una expresión regular.
- Un **bucle de redirección** (`curl: (47) Maximum (50) redirects followed`) se depura mirando las cabeceras de cada salto: `curl -IL`.
- **`error_page`** cambia la página de error pero **no el código**; `internal;` impide pedir esa página directamente.
- En **Apache**: `<VirtualHost>`, `ServerName`, `Alias`, `Redirect` / `RewriteRule`, `ErrorDocument` y **`.htaccess`** (controlado por `AllowOverride`). Nginx no tiene `.htaccess`.

---

## Anexo para el docente

### Comprobado en contenedores reales

Todo lo de este documento se ha probado con `nginx:1.30` (1.30.6) en Docker y la parte de Apache con `httpd:2.4` (2.4.71):

- Dos hosts virtuales por nombre (`localhost`, `tienda.localhost`) en el mismo puerto; `curl http://tienda.localhost:PUERTO/` resuelve a 127.0.0.1 sin configurar nada en macOS.
- Servidor por defecto con `return 444;`: `curl -H "Host: otro.com"` → `curl: (52) Empty reply from server`. Sin `default_server` declarado, responde el primer `server` del puerto.
- Orden de las `location`: `= /test` → «exacta», `/test/` cae en `/`; `^~ /img/` gana a la regex `\.(png|jpg)$` para `/img/a.png`; `/foto.png` → regex.
- `location /hola/ { }` con la petición `/hola` → **301** a `/hola/` (también `/mundo` → `/mundo/`).
- `root` frente a `alias`: `open() ".../docs/ro/index.html" failed (2: No such file or directory)` con `root`; con `alias` sin barra final, `/malo/` → 403 (`directory index of ".../docs" is forbidden`) y `/malo/index.html` → 404 (`open() ".../docsindex.html"`).
- `return 301`, `return 302`, `rewrite … permanent` (301), la redirección de `www` conservando la ruta y el bucle `return 301 /bucle;` con `curl -L` → `curl: (47) Maximum (50) redirects followed` (50 redirecciones).
- `error_page 404` con `internal;`: 404 con la página propia; pedir `/errores/404.html` directamente da también 404.
- En Apache, `Redirect 301 /viejo /nuevo.html` y `RewriteRule ^/reglas/(.*)$ /$1 [R=301,L]` dan 301. Sin `Require all granted` en el directorio de la web, la imagen oficial devuelve 403 (`AH01630: client denied by server configuration`).
- **Importante al probar con un puerto distinto del 80** (por ejemplo `-p 8089:80`): `curl -L` sigue el `Location` a `http://localhost/…` (puerto 80) y falla al conectar. Publica el **80** (como en el `compose.yaml`) o añade `absolute_redirect off;` en el `server`.

### Relación con los RA

- **RA2 c)** (sitios virtuales): secciones 1, 2 y 3.
- **RA2** (configuración del servidor para servir distintas aplicaciones): `location`, `alias`, `try_files` y redirecciones (secciones 4-6).
- Apache, `mod_rewrite` y `.htaccess`: sección 8 (RA1 d: describir los principales servidores).

### Para las diapositivas (hilo del restaurante)

**Una cocina, varias marcas.** Un mismo local (el servidor) con una sola puerta (la IP y el puerto 80) y varios restaurantes dentro (los **hosts virtuales**): el portero lee el nombre que dices al entrar (la cabecera `Host`) y te lleva a la sala correcta. Si dices un nombre que no existe, no te deja pasar (**servidor por defecto**). Dentro de cada restaurante, las **`location`** son las secciones de la carta: `/hola`, `/test`, `/mundo`, cada una con su cocina. Las **redirecciones** son el cartel de la puerta: «nos hemos mudado» (301, para siempre) o «hoy cerrado, vuelva mañana» (302, temporal).

### Para la práctica

- Pedir **tres rutas con tres contenidos distintos** (`/hola`, `/test`, `/mundo`) y que expliquen con qué regla se resuelve cada una (`=`, prefijo, `alias`).
- Un segundo host (`tienda.localhost`) con sus propios logs.
- Provocar a propósito: el `alias` sin barra final, una `location` regex que «roba» una carpeta (arreglarla con `^~`) y un bucle de redirección, y diagnosticarlos con `curl -IL` y el log de errores.
- Una redirección 301 de `/viejo` a `/nuevo`, una 302 y la de `www` a sin `www`.
- Que prueben siempre con `curl -I` y `-L` antes de mirar el navegador (la caché de los 301).
