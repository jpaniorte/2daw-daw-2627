---
layout: default
title: "Servidores Web — Bloque 3.1.1: Instalación y configuración básica de Nginx (Teoría)"
permalink: /servidores-web/semana-1/teoria/
---

# Bloque 3.1.1 — Instalación y configuración básica de Nginx

**Módulo:** Despliegue de Aplicaciones Web (0614) · 2º DAW · UD3: Administración de servidores web

> En la UD2 vimos **qué hace** un servidor web y por qué casi siempre hay uno delante de las aplicaciones. Hoy conocemos a los dos más usados, **Apache y Nginx**, y ponemos en marcha **Nginx** de verdad: en un contenedor, en **tu VM de Azure** y sirviendo **tu dominio**. Aprenderemos dónde está su configuración, cómo ampliarlo con **módulos**, cómo cambiarlo sin romper nada y cómo saber qué está pasando leyendo sus logs.

## Planificación orientativa

| # | Sección |
|---|---------|
| 1 | Apache y Nginx frente a frente |
| 2 | Cómo lo vamos a ejecutar: Docker |
| 3 | Nginx con la imagen oficial |
| 4 | Módulos: ampliar la funcionalidad |
| 5 | Cambiar la configuración sin romper nada |
| 6 | Logs: qué está pasando en el servidor |
| 7 | Permisos y usuario del servicio |
| 8 | Primeras medidas de seguridad |
| 9 | Todo junto: Nginx en la VM |

## 1. Apache y Nginx frente a frente

| | Apache HTTP Server | Nginx |
|--|--------------------|-------|
| Nace | 1995, a partir del servidor NCSA httpd | 2004, creado por Igor Sysoev |
| Por qué nace | Hacía falta un servidor web libre y ampliable para la web que empezaba | Resolver el **problema C10k**: atender 10 000 conexiones simultáneas en una sola máquina |
| Quién lo mantiene | La Apache Software Foundation | F5 (versión libre y versión comercial NGINX Plus) |
| Licencia | Apache 2.0 | BSD de 2 cláusulas |

Los dos son software libre y llevan años entre los servidores web más usados del mundo. Nginx está por delante en número de sitios desde hace tiempo, pero Apache sigue muy presente, sobre todo en alojamiento compartido.

- Es el servidor web **más usado** y el que encontrarás casi siempre **delante de las aplicaciones**, como proxy inverso (3.2.2), que es justo lo que montaremos en la UD4 y la UD5.
- Su **imagen oficial de Docker** es de las más descargadas, está al día y es sencilla.
- Todo lo que pide el módulo (sitios virtuales, autenticación, HTTPS, certificados, rendimiento, módulos) se puede hacer con él. Si mañana trabajas con Apache, las ideas son las mismas: solo cambian los nombres.

## 2. Cómo lo vamos a ejecutar: Docker

### 2.1 Tres formas de instalar un servidor web

| Forma | Ejemplo | Ventajas | Inconvenientes |
|-------|---------|----------|----------------|
| **Paquete del sistema** | `sudo apt install nginx` en Ubuntu/Debian | Es lo «clásico»: el servicio lo gestiona systemd | Lo que instalas se mezcla con el sistema; difícil de repetir igual en otra máquina; la versión es la de la distribución |
| **Imagen oficial de Docker** | `nginx:1.30` | Lista para usar, versión reciente, un comando | Hay que entender cómo organiza esa imagen la configuración |
| **Imagen propia** | `FROM nginx:1.30` + `COPY` de tu configuración en un `Dockerfile` | La imagen oficial **con tu configuración dentro**: reproducible y versionable | Hay que escribir el `Dockerfile` |

En este curso usamos **Docker** (UD1) con la **imagen oficial** de Nginx, y una imagen propia basada en ella cuando queramos llevar la configuración dentro (sección 5).

### 2.2 Sin systemd: el servidor es el proceso principal del contenedor

En una máquina normal, el servicio lo gestiona **systemd** (`systemctl`). En un contenedor **no hay systemd**: el contenedor vive mientras vive su **proceso principal (PID 1)**, como vimos en la UD1. Por eso la imagen oficial arranca Nginx **en primer plano**:

```
nginx -g 'daemon off;'
```

Si el proceso principal termina (por ejemplo, porque la configuración tiene un error), **el contenedor se para**.

Equivalencias para gestionar el servicio:

| Acción | Servidor con systemd | En un contenedor |
|--------|----------------------|------------------|
| Arrancar | `systemctl start nginx` | `docker start web` |
| Parar | `systemctl stop nginx` | `docker stop web` |
| **Reiniciar** | `systemctl restart nginx` | `docker restart web` |
| **Recargar la configuración** | `systemctl reload nginx` | `docker exec web nginx -s reload` |
| Ver el estado | `systemctl status nginx` | `docker ps`, `docker logs web` |
| Arrancar al encender la máquina | `systemctl enable nginx` | `--restart unless-stopped` (o `restart:` en Compose) |

### 2.3 `reload` frente a `restart`

| | Recargar (`nginx -s reload`) | Reiniciar (`docker restart`) |
|--|------------------------------|------------------------------|
| Qué hace | El proceso maestro **vuelve a leer** la configuración, arranca *workers* nuevos y deja que los antiguos terminen | **Para** el servidor y lo **vuelve a arrancar** |
| Conexiones en curso | **Terminan con normalidad** | **Se cortan** |
| Si la configuración nueva tiene un error | Se **rechaza** y el servidor **sigue funcionando** con la anterior | El servidor **no arranca**: la web se cae |
| Cuándo usarlo | Casi siempre | Cuando cambias algo que no es configuración (la imagen, los volúmenes, los puertos publicados) |

> **Regla de oro:** después de cambiar la configuración, **comprueba la sintaxis y recarga**. Reinicia solo cuando sea imprescindible.

### 2.4 Un puerto, cuatro capas

Para que una petición desde Internet llegue a Nginx, el puerto tiene que estar abierto en **todas** estas capas:

```
navegador ─▶ NSG de Azure ─▶ VM (cortafuegos ufw) ─▶ docker -p 80:80 ─▶ Nginx: listen 80;
             (22, 80, 443)                            host:contenedor      (dentro del contenedor)
```

| Capa | Dónde se configura | Error típico |
|------|--------------------|--------------|
| **NSG** (grupo de seguridad de red) | Portal de Azure (dosier 1) | El servicio funciona dentro de la VM, pero desde fuera da *timeout* |
| **`ufw`** en la VM | `sudo ufw …` | Ojo: los puertos **publicados por Docker se saltan las reglas de `ufw`**. En Azure, quien filtra de verdad es el NSG |
| **Publicación de Docker** | `-p puerto_host:puerto_contenedor` o `ports:` en Compose | Publicar el puerto equivocado: `-p 8080:80` publica el 80 del contenedor en el 8080 de la VM |
| **El servidor** | `listen 80;` | Cambiar el `listen` de Nginx y olvidar cambiar el lado del contenedor en `-p` |

> En tu VM solo están abiertos el **22, el 80 y el 443**. Un contenedor publicado en el 8080 de la VM **no se ve desde Internet**: se prueba desde la propia VM (`curl localhost:8080`) o con un túnel SSH (`ssh -L 8080:localhost:8080 daw` y luego `http://localhost:8080` en tu navegador).

## 3. Nginx con la imagen oficial

### 3.1 Arrancarlo

```bash
docker run -d --name web -p 80:80 nginx:1.30
curl -I http://localhost
```

Con eso ya hay un Nginx funcionando. Dentro del contenedor, el proceso maestro corre como `root` (para abrir el puerto 80) y los *workers*, como el usuario sin privilegios `nginx`.

### 3.2 La estructura de la configuración

```
/etc/nginx/
├── nginx.conf            ← configuración global; incluye conf.d/*.conf
├── conf.d/
│   └── default.conf      ← el sitio por defecto
├── mime.types            ← extensión del fichero → Content-Type
└── modules/              ← módulos dinámicos (enlace a /usr/lib/nginx/modules)
/usr/share/nginx/html/    ← la web por defecto (index.html, 50x.html)
```

`nginx.conf` (resumido):

```nginx
user  nginx;
worker_processes  auto;            # un worker por núcleo de CPU

error_log  /var/log/nginx/error.log notice;

events {
    worker_connections  1024;      # conexiones simultáneas por worker
}

http {
    include       /etc/nginx/mime.types;
    access_log    /var/log/nginx/access.log  main;
    sendfile      on;
    keepalive_timeout  65;

    include /etc/nginx/conf.d/*.conf;   # aquí entran los sitios
}
```

`conf.d/default.conf` (sin comentarios):

```nginx
server {
    listen       80;
    listen  [::]:80;
    server_name  localhost;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}
```

### 3.3 Bloques (contextos) y directivas

La configuración de Nginx son **directivas** que terminan en **`;`** agrupadas en **bloques** `{ }` que se anidan:

```
main (nivel superior: user, worker_processes, load_module…)
├── events { … }        → cómo se gestionan las conexiones
└── http { … }          → todo lo relativo a HTTP
    └── server { … }    → un sitio web
        └── location { … }  → qué hacer con un grupo de URL
```

- Cada directiva solo se puede poner en **ciertos contextos**. Por ejemplo, `load_module` solo en `main`; `listen`, solo dentro de `server`.
- Una directiva puesta en un bloque exterior se **hereda** en los interiores. Por eso es habitual escribir `root` una sola vez en el `server` en lugar de repetirlo en cada `location`.

### 3.4 Directivas básicas

| Directiva | Contexto | Qué hace |
|-----------|----------|----------|
| `listen 80;` | `server` | Puerto (y opcionalmente IP) en el que escucha el sitio |
| `server_name tunombre.me;` | `server` | Nombre del sitio; con varios sitios, decide cuál responde (3.1.2) |
| `root /usr/share/nginx/html;` | `http`, `server`, `location` | Carpeta cuyos ficheros se publican |
| `index index.html;` | `http`, `server`, `location` | Fichero que se sirve al pedir una carpeta |
| `location /ruta { … }` | `server` | Configuración para las URL que empiezan por `/ruta`; `location = /ruta` solo para esa URL exacta |
| `error_page 404 /404.html;` | `http`, `server`, `location` | Página de error propia (3.1.2) |
| `access_log`, `error_log` | Varios | Dónde y con qué formato se escriben los logs (sección 6) |

> **El error más típico en Nginx es olvidar un `;`.** `nginx -t` te dirá en qué línea está (sección 5).

---

## 4. Módulos: ampliar la funcionalidad

### 4.1 Módulos estáticos y dinámicos

Toda la funcionalidad de Nginx está en **módulos**. Hay dos tipos:

| | Estáticos | Dinámicos |
|--|-----------|-----------|
| Dónde están | **Dentro** del ejecutable `nginx`, elegidos al compilar | En ficheros **`.so`** aparte |
| Cómo se activan | Siempre están; basta con usar sus directivas | Con **`load_module`** en `nginx.conf` |
| Cómo se ven | `nginx -V` (líneas `--with-…_module`) | `ls /etc/nginx/modules` |
| Ejemplos en la imagen oficial | `ssl`, `v2`, `v3`, `gzip_static`, `realip`, `stub_status`, `dav`, `auth_request`, `sub`… | `njs`, `image_filter`, `geoip`, `xslt`, `acme` |

Es la misma idea que `a2enmod` en Apache: activar una función sin recompilar el servidor.

```bash
docker exec web nginx -V 2>&1 | tr ' ' '\n' | grep _module   # módulos estáticos
docker exec web ls /etc/nginx/modules                       # módulos dinámicos disponibles
docker exec web sh -c 'nginx -T 2>/dev/null | grep load_module'  # dinámicos cargados
```

> `nginx -T` muestra **toda la configuración efectiva**, con todos los `include` ya resueltos. Muy útil para saber qué está leyendo Nginx de verdad.

### 4.2 Los módulos dinámicos más populares

**Oficiales, ya incluidos en la imagen `nginx:1.30`** (en `/etc/nginx/modules`):

| Módulo | Fichero `.so` | Para qué sirve |
|--------|---------------|----------------|
| **njs** | `ngx_http_js_module.so` (y `ngx_stream_js_module.so`) | Programar respuestas y lógica en **JavaScript** dentro de Nginx |
| **image_filter** | `ngx_http_image_filter_module.so` | **Redimensionar, recortar y girar imágenes** JPEG, GIF, PNG y WebP al vuelo |
| **acme** | `ngx_http_acme_module.so` | Pedir y renovar **certificados de Let's Encrypt** desde el propio Nginx, sin certbot (3.2.1) |
| **geoip** | `ngx_http_geoip_module.so` (y `ngx_stream_geoip_module.so`) | Saber el **país o la ciudad** del cliente por su IP (con las bases de datos GeoIP antiguas) |
| **xslt** | `ngx_http_xslt_filter_module.so` | Transformar respuestas XML con hojas XSLT |

Cada uno trae además una versión `-debug.so`, para depurar.

**De terceros, muy usados** (no vienen en la imagen oficial):

| Módulo | Para qué sirve |
|--------|----------------|
| **brotli** | Compresión **Brotli**, que reduce más que gzip (3.2.2) |
| **headers-more** | Añadir, cambiar o **quitar cualquier cabecera**, incluida `Server` entera |
| **geoip2** | Geolocalización con las bases de datos actuales de MaxMind (sustituye a geoip) |
| **ModSecurity** | **Cortafuegos de aplicaciones web** (WAF): bloquea inyecciones SQL, XSS… con las reglas OWASP CRS |
| **lua** | Programar en **Lua** dentro de Nginx; es la base de **OpenResty** |
| **fancyindex** | Listados de directorios más bonitos y configurables que `autoindex` |
| **cache-purge** | Borrar elementos concretos de la caché del proxy (3.2.2) |
| **rtmp** | Servidor de *streaming* de vídeo en directo |

¿Cómo se consiguen los de terceros?

- **Con el Nginx de Debian/Ubuntu,** vienen empaquetados: `apt install libnginx-mod-http-brotli-filter`, `libnginx-mod-http-headers-more-filter`, `libnginx-mod-http-geoip2`, `libnginx-mod-http-modsecurity`… El paquete deja el `load_module` en `/etc/nginx/modules-enabled/` y queda activado.
- **Con la imagen oficial,** hay que **compilarlos** contra el código fuente de **exactamente la misma versión** de Nginx (normalmente, en un *multi-stage build*, UD1) y copiar el `.so`.

> **Un `.so` compilado para otra versión no carga.** Por ejemplo, el módulo `headers-more` del paquete de Debian (Nginx 1.26.3) en la imagen oficial (1.30.6):
> ```
> nginx: [emerg] module "/etc/nginx/modules/ngx_http_headers_more_filter_module.so" version 1026003 instead of 1030006
> ```

### 4.3 Cargar un módulo: `load_module`

`load_module` va **al principio de `nginx.conf`**, en el contexto `main`, **fuera** de cualquier bloque:

```nginx
load_module modules/ngx_http_image_filter_module.so;
load_module modules/ngx_http_js_module.so;

user  nginx;
worker_processes  auto;
...
```

La ruta `modules/…` es relativa a `/etc/nginx/`. Los dos errores típicos:

```
# Usar una directiva del módulo sin haberlo cargado:
nginx: [emerg] unknown directive "image_filter" in /etc/nginx/conf.d/default.conf:3

# Poner load_module dentro de http { }:
nginx: [emerg] "load_module" directive is not allowed here in /etc/nginx/nginx.conf:16
```

> Como `nginx.conf` es un fichero de la imagen, para añadirle `load_module` lo copiamos con un `Dockerfile` (sección 5) o lo montamos desde la VM.

### 4.4 Ejemplo: miniaturas al vuelo con `image_filter`

Queremos que `/miniatura/foto.jpg?w=200` devuelva `foto.jpg` reducida a 200 píxeles de ancho, **sin crear ningún fichero nuevo**.

1. Cargar el módulo en `nginx.conf` (4.3).
2. En `conf.d/default.conf`:

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location /miniatura/ {
        alias /usr/share/nginx/html/img/;   # /miniatura/foto.jpg → img/foto.jpg
        image_filter resize $arg_w -;       # ancho = parámetro w; alto proporcional (-)
        image_filter_buffer 10M;            # tamaño máximo de la imagen original
    }
}
```

3. Comprobarlo:

```bash
curl -s -o original.jpg  http://localhost/img/foto.jpg
curl -s -o miniatura.jpg "http://localhost/miniatura/foto.jpg?w=200"
ls -l original.jpg miniatura.jpg
```

Con una foto de 1200 × 800 píxeles, la original ocupa unos **15 KB** y la miniatura (200 × 133) poco más de **1 KB**. En el navegador se ve directamente al abrir `http://tunombre.me/miniatura/foto.jpg?w=200`.

- `$arg_w` es el valor del parámetro `w` de la URL (`?w=200`). Nginx tiene una variable `$arg_…` para cada parámetro.
- `alias` sustituye el prefijo de la URL por otra carpeta (se amplía en 3.1.2).
- Otras acciones: `image_filter crop 200 200;`, `image_filter rotate 90;`, `image_filter size;` (devuelve las medidas en JSON).

> **Recuadro — `njs`: JavaScript dentro de Nginx**
>
> Con el módulo `ngx_http_js_module.so` cargado, se puede generar una respuesta con JavaScript. En `nginx.conf`, dentro de `http { }`:
>
> ```nginx
> js_path   /etc/nginx/njs/;
> js_import hola from hola.js;
> ```
>
> El fichero `/etc/nginx/njs/hola.js`:
>
> ```javascript
> function saludo(r) {
>     r.return(200, `Hola desde njs. Has pedido ${r.uri} con ${r.method}\n`);
> }
> export default { saludo };
> ```
>
> Y en el `server`:
>
> ```nginx
> location = /hola {
>     js_content hola.saludo;
> }
> ```
>
> ```
> $ curl http://localhost/hola
> Hola desde njs. Has pedido /hola con GET
> ```
>
> `r` es la petición: `r.uri`, `r.method`, `r.args`, `r.headersIn`… No es Node.js (no hay `npm` ni `require` de paquetes), pero sirve para pequeñas lógicas: validar una cabecera, montar una respuesta JSON o decidir a qué backend mandar una petición.

---

## 5. Cambiar la configuración sin romper nada

### 5.1 ¿Dónde se cambia la configuración de un contenedor?

| Forma | Ejemplo | Cuándo |
|-------|---------|--------|
| **En la imagen** (`Dockerfile`) | `FROM nginx:1.30` + `COPY nginx.conf /etc/nginx/nginx.conf` | Lo que forma parte del servidor: módulos cargados, ajustes globales de seguridad. Se aplica reconstruyendo (`docker compose up -d --build`) |
| **Montada desde la VM** (*bind mount*, UD1) | `-v ./conf.d:/etc/nginx/conf.d:ro` | Los sitios, que cambias a menudo. Se edita en la VM y se recarga |
| ~~**Dentro del contenedor** (`docker exec`)~~ | `docker exec web vi /etc/nginx/conf.d/default.conf` | Solo para **probar**: el cambio **se pierde** al recrear el contenedor |

Un `Dockerfile` para llevar dentro el `nginx.conf` con los módulos cargados:

```dockerfile
FROM nginx:1.30
COPY nginx.conf /etc/nginx/nginx.conf
COPY njs/ /etc/nginx/njs/
```

> **Cuidado al montar un solo fichero** (`-v ./default.conf:/etc/nginx/conf.d/default.conf`). Muchos editores guardan creando un fichero nuevo, y el contenedor sigue viendo el antiguo. Es más seguro **montar la carpeta** (`./conf.d:/etc/nginx/conf.d`).

### 5.2 Comprobar antes de recargar

```bash
docker exec web nginx -t           # comprobar la sintaxis
docker exec web nginx -s reload    # recargar
```

Si todo está bien:

```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

Si hay un error, te dice el fichero y la línea:

```
nginx: [emerg] unexpected "}" in /etc/nginx/conf.d/default.conf:7
nginx: configuration file /etc/nginx/nginx.conf test failed
```

(Aquí faltaba el `;` al final de la línea 6: Nginx se da cuenta al llegar a la llave de la línea 7).

### 5.3 Por qué un error de sintaxis puede tumbar el servicio

- Al **recargar** con una configuración rota, Nginx la **rechaza** y sigue funcionando con la anterior. Hasta aquí, no pasa nada.
- Pero la configuración rota sigue en disco. **El próximo reinicio** (un `docker restart`, un reinicio de la VM, un `docker compose up` después de un cambio…) arranca Nginx con ella, el proceso principal falla y **el contenedor se para**. La web se cae, y quizá horas después del cambio que la rompió.
- Si usas `restart: unless-stopped`, Docker intentará arrancarlo una y otra vez (`docker ps` mostrará `Restarting`).

**El ciclo de trabajo, siempre igual:**

```
editar ─▶ comprobar (nginx -t) ─▶ recargar ─▶ probar con curl ─▶ mirar los logs
```

---

## 6. Logs: qué está pasando en el servidor

### 6.1 Dónde están

| | En una máquina (paquete) | En la imagen oficial |
|--|--------------------------|----------------------|
| Log de acceso | `/var/log/nginx/access.log` | `/var/log/nginx/access.log` es un enlace a **`/dev/stdout`** |
| Log de errores | `/var/log/nginx/error.log` | `/var/log/nginx/error.log` es un enlace a **`/dev/stderr`** |

Hay **dos logs** con propósitos distintos:

- **Log de acceso**: **una línea por cada petición** atendida, vaya bien o mal.
- **Log de errores**: avisos de arranque, errores de configuración, ficheros que no se pueden leer… **El primer sitio donde mirar** cuando algo falla.

### 6.2 Verlos con `docker logs`

Como la imagen oficial envía el log de acceso a la **salida estándar** y el de errores a la **salida de error**, Docker los recoge:

```bash
docker logs web                  # todo
docker logs -f web               # en directo (Ctrl+C para salir)
docker logs --tail 20 web        # las últimas 20 líneas
docker logs --since 10m web      # los últimos 10 minutos
docker logs web 2>/dev/null      # solo el log de acceso (stdout), más los mensajes de arranque de la imagen
docker logs web 2>&1 >/dev/null  # solo el log de errores (stderr)
```

> **¿Por qué enlazarlos a `/dev/stdout`?** Si Nginx escribiera ficheros dentro del contenedor, `docker logs` no mostraría nada y, al borrar el contenedor, los logs desaparecerían con él. Si necesitas conservarlos, puedes montar un volumen en `/var/log/nginx` y cambiar `access_log` para que escriba en un fichero normal.

### 6.3 Leer una línea del log de acceso

El formato `main` de `nginx.conf`:

```nginx
log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                  '$status $body_bytes_sent "$http_referer" '
                  '"$http_user_agent" "$http_x_forwarded_for"';
```

Produce líneas como esta:

```
81.45.12.200 - - [12/Nov/2026:10:15:32 +0100] "GET /index.html HTTP/1.1" 200 10958 "https://www.google.com/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ..." "-"
```

| Campo | Variable | Ejemplo | Qué es |
|-------|----------|---------|--------|
| IP del cliente | `$remote_addr` | `81.45.12.200` | Quién hace la petición |
| Usuario | `$remote_user` | `-` | Solo aparece si hay autenticación (3.2.1) |
| Fecha y hora | `$time_local` | `[12/Nov/2026:10:15:32 +0100]` | Cuándo; `+0100` es la zona horaria |
| Línea de petición | `$request` | `"GET /index.html HTTP/1.1"` | Método, ruta y versión de HTTP (bloque 2.1) |
| Código de estado | `$status` | `200` | Cómo ha ido (2xx, 3xx, 4xx, 5xx) |
| Tamaño | `$body_bytes_sent` | `10958` | Bytes del cuerpo de la respuesta |
| *Referer* | `$http_referer` | `"https://www.google.com/"` | Desde qué página venía el enlace (cabecera `Referer`) |
| *User-Agent* | `$http_user_agent` | `"Mozilla/5.0 …"` | Qué programa hace la petición (navegador, `curl`, un bot…) |
| IP original | `$http_x_forwarded_for` | `"-"` | La IP real del cliente cuando hay un proxy delante (3.2.2) |

Y una línea del log de errores:

```
2026/11/12 10:16:01 [error] 23#23: *3 open() "/usr/share/nginx/html/nada" failed (2: No such file or directory), client: 81.45.12.200, server: localhost, request: "GET /nada HTTP/1.1", host: "tunombre.me"
```

Fecha, **gravedad** (`[error]`), proceso, número de conexión (`*3`), el **mensaje** y los datos de la petición que lo causó.

### 6.4 Un servidor público recibe visitas que no has pedido

En cuanto tu VM tenga el puerto 80 abierto, verás en el log peticiones como estas, aunque no se lo hayas dicho a nadie:

```
45.148.10.81 - - [12/Nov/2026:03:12:09 +0100] "GET /wp-login.php HTTP/1.1" 404 153 "-" "Mozilla/5.0" "-"
45.148.10.81 - - [12/Nov/2026:03:12:10 +0100] "GET /.env HTTP/1.1" 404 153 "-" "Mozilla/5.0" "-"
194.26.29.15 - - [12/Nov/2026:04:40:51 +0100] "GET /phpmyadmin/ HTTP/1.1" 404 153 "-" "zgrab/0.x" "-"
```

Son **bots que recorren Internet** buscando WordPress mal configurados, ficheros `.env` con contraseñas o paneles de administración olvidados. Que devuelvan **404** es buena señal. Dos lecciones:

- Nunca dejes en la carpeta publicada ficheros que no deban verse (`.env`, copias de seguridad, `.git/`).
- Revisa los logs de vez en cuando. En 3.2.2 aprenderemos a analizarlos. Como adelanto, para contar los códigos de estado:

```bash
docker logs web 2>/dev/null | grep 'HTTP/' | awk '{print $9}' | sort | uniq -c
```

---

## 7. Permisos y usuario del servicio

- El proceso maestro arranca como `root` (para poder abrir el puerto 80), pero **las peticiones las atienden los *workers***, que corren como el usuario sin privilegios **`nginx`** (UID 101) en la imagen oficial (en el paquete de Debian/Ubuntu, `www-data`).
- Ese usuario tiene que poder **leer** los ficheros y **atravesar** (permiso `x`) todas las carpetas de la ruta. Si no puede, Nginx responde **403 Forbidden**.

| Elemento | Permisos habituales | En octal |
|----------|---------------------|----------|
| Ficheros de la web | lectura para todos | `644` (`rw-r--r--`) |
| Carpetas de la web | lectura y paso para todos | `755` (`rwxr-xr-x`) |

Qué se ve en cada caso:

| Situación | Respuesta | Log de errores |
|-----------|-----------|----------------|
| Fichero con permisos `600` de otro usuario | **403** | `open() "…/privado.html" failed (13: Permission denied)` |
| Carpeta sin `index.html` (y sin `autoindex`) | **403** | `directory index of "…/docs/" is forbidden` |
| El fichero no existe | **404** | `open() "…/nada" failed (2: No such file or directory)` |

> **Un 403 casi siempre es un problema de permisos o de configuración, no de la web.** El log de errores te dice cuál de los dos.

> **Ojo con los *bind mounts*:** en la VM Linux, los ficheros montados conservan el propietario y los permisos que tienen en la VM. Si subes un fichero con permisos `600`, el contenedor devolverá 403. En **Docker Desktop** (Windows y macOS) esto **no pasa**, porque los permisos se traducen, así que algo que funciona en tu portátil puede fallar en la VM. Corrígelo en la VM con `chmod 644` (ficheros) y `chmod 755` (carpetas).

---

## 8. Primeras medidas de seguridad

### 8.1 Ocultar la versión

Por defecto, Nginx anuncia su versión en la cabecera `Server` y en las páginas de error:

```
$ curl -I http://localhost
Server: nginx/1.30.6
```

Así, un atacante sabe exactamente qué vulnerabilidades probar. Para ocultarla, en el bloque `http` de `nginx.conf` (o dentro de un `server`):

```nginx
server_tokens off;
```

```
$ curl -I http://localhost
Server: nginx
```

> Ocultar la versión **no sustituye a actualizar**. Solo pone las cosas algo más difíciles. Con Docker, actualizar es cambiar la etiqueta de la imagen (`nginx:1.30` → la versión nueva) o reconstruir con la base al día (`docker compose build --pull`). Para quitar también la palabra `nginx` hace falta el módulo de terceros `headers-more` (4.2).

### 8.2 El listado de directorios

Con `autoindex on;`, si una carpeta no tiene `index.html`, Nginx muestra la **lista de sus ficheros**, incluidos los que no querías enseñar:

```nginx
location /docs/ {
    autoindex on;     # ¡cuidado! muestra todo lo que hay en la carpeta
}
```

- En Nginx viene **desactivado** por defecto (`autoindex off;`): pedir una carpeta sin `index.html` devuelve **403** (sección 7).
- Actívalo solo en carpetas pensadas para descargar ficheros, y nunca en la raíz de la web.
- En Apache (Debian) ocurre lo contrario: viene **activado** (`Options Indexes`) y hay que desactivarlo.

---

## 9. Todo junto: Nginx en la VM

En la VM (`ssh daw`), una carpeta con todo lo de hoy:

```
servidor/
├── compose.yaml
├── nginx/
│   ├── Dockerfile          ← FROM nginx:1.30 + COPY (sección 5)
│   ├── nginx.conf          ← con load_module, server_tokens off y njs
│   ├── njs/hola.js         ← el ejemplo de njs
│   └── conf.d/default.conf ← el sitio, con /miniatura/ y /hola
└── html/
    ├── index.html          ← tu web
    └── img/foto.jpg
```

```yaml
services:
  web:
    build: ./nginx
    image: miweb-nginx:1.0
    ports:
      - "80:80"                          # http://tunombre.me
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./html:/usr/share/nginx/html:ro
    restart: unless-stopped
```

```bash
docker compose up -d --build
curl -I http://tunombre.me
curl -s -o mini.jpg "http://tunombre.me/miniatura/foto.jpg?w=200"
curl http://tunombre.me/hola
```

- `nginx.conf` y `njs/` van **dentro de la imagen** (cambian poco y forman parte del servidor). Los sitios (`conf.d/`) y la web (`html/`) van **montados** (cambian a menudo).
- `:ro` monta en **solo lectura**: Nginx no puede modificar la web ni su configuración.
- Después de editar `conf.d/`: `docker compose exec web nginx -t` y `docker compose exec web nginx -s reload`. Después de editar `nginx.conf`: `docker compose up -d --build`.

### Qué viene en el siguiente bloque

Hoy Nginx sirve **una** web. En el bloque 3.1.2 veremos cómo un mismo servidor sirve **varias** (`tunombre.me` y `tienda.tunombre.me`) gracias a la cabecera `Host` y a los **bloques `server`** (hosts virtuales), y cómo enviar al cliente a otra URL con **redirecciones**.

---

## Ideas clave del bloque

- **Apache** reparte el trabajo con un **MPM** (`prefork`, `worker` o `event`), se amplía con módulos, en Debian organiza la configuración en `*-available` / `*-enabled` y permite `.htaccess`. **Nginx** usa un maestro y pocos *workers* con eventos asíncronos, y es el que usamos en el curso.
- Usamos la **imagen oficial** `nginx:1.30`, y una imagen propia `FROM nginx:1.30` cuando queremos llevar la configuración dentro.
- En un contenedor **no hay systemd**: Nginx es el **proceso principal** y se arranca en primer plano (`nginx -g 'daemon off;'`).
- **Recargar** (`nginx -s reload`) relee la configuración sin cortar conexiones y rechaza una configuración rota. **Reiniciar** corta las conexiones y, con una configuración rota, deja el servicio caído.
- Configuración: `nginx.conf` (global) incluye `conf.d/*.conf` (los sitios). Bloques anidados `main` → `events` / `http` → `server` → `location`; directivas terminadas en `;`, que se heredan hacia dentro.
- Directivas básicas: `listen`, `server_name`, `root`, `index`, `location`, `error_page`.
- **Módulos estáticos** (dentro del binario, `nginx -V`) y **dinámicos** (`.so`, cargados con **`load_module`** en el contexto `main`). La imagen oficial trae `njs`, `image_filter`, `acme`, `geoip` y `xslt`. Los de terceros (brotli, headers-more, ModSecurity…) deben estar compilados para **la misma versión** de Nginx.
- **Siempre comprobar antes de recargar:** `nginx -t`. `nginx -T` muestra la configuración completa.
- Para que llegue una petición, el puerto debe estar abierto en el **NSG**, publicado con **`-p`** y configurado con **`listen`**.
- **Log de acceso**: una línea por petición (IP, fecha, petición, código, tamaño, *referer*, *user-agent*). **Log de errores**: el primero que se mira cuando algo falla. En la imagen oficial se leen con `docker logs`.
- Un **403** suele ser de **permisos** (el usuario `nginx` no puede leer) o de una **carpeta sin índice**.
- Seguridad mínima: **ocultar la versión** (`server_tokens off;`) y no activar `autoindex` donde no toca.

---

## Anexo para el docente

### Comprobado en contenedores reales

Todo lo de este documento se ha probado con `nginx:1.30` (1.30.6) en Docker:

- Módulos dinámicos de la imagen (`/etc/nginx/modules` → `/usr/lib/nginx/modules`): `acme`, `geoip` (http y stream), `image_filter`, `js` (http y stream) y `xslt`, cada uno también en versión `-debug`. **No trae `otel`.**
- El ejemplo de `image_filter` reduce una imagen de 1200 × 800 (15 630 bytes) a 200 × 133 (1 158 bytes). El ejemplo de `njs` responde `Hola desde njs. Has pedido /hola con GET`.
- Mensajes reales: `unknown directive "image_filter"` (sin `load_module`), `"load_module" directive is not allowed here` (dentro de `http`) y `version 1026003 instead of 1030006` (el `.so` de `headers-more` del paquete de Debian 13 en la imagen oficial).
- Paquetes de terceros en Debian 13: `libnginx-mod-http-brotli-filter`, `-headers-more-filter`, `-geoip2`, `-modsecurity`, `-lua`, `-fancyindex`, `-cache-purge`, `libnginx-mod-rtmp`, entre otros (`apt-cache search libnginx-mod`).
- 403 por permisos (`13: Permission denied`), 403 por carpeta sin índice (`directory index of … is forbidden`), 404 (`2: No such file or directory`), `server_tokens off` → `Server: nginx`, y el `compose.yaml` de la sección 9 con `nginx -t` correcto.
- **En Docker Desktop (macOS/Windows) el 403 por permisos no se reproduce con *bind mounts*:** para provocarlo en clase, hazlo **en la VM Linux** o con un fichero creado dentro del contenedor (`docker exec … chmod 600`).

### Relación con los RA

- **RA2 b)** (ampliar la funcionalidad del servidor con módulos): sección 4, con dos módulos cargados y configurados (`image_filter` y `njs`).
- Apache no es obligatorio según el BOE (los RA hablan de «servidores web» sin nombrar ninguno), pero el **RA1 d)** pide describir los principales: de ahí la sección 1.

### Para las diapositivas (hilo del restaurante)

**Montar la barra**: elegir el mueble (Apache o Nginx), instalarlo en el local alquilado (la VM), ponerlo en marcha (el proceso principal) y **apuntar cada comanda en el libro** (log de acceso) y cada incidencia en el parte (log de errores). Los **módulos** son los electrodomésticos que se enchufan a la barra cuando hacen falta (la cortadora que hace miniaturas, `image_filter`). El camarero (`nginx`) no tiene llave de todos los armarios: si falta un permiso, no puede servir el plato (**403**).

### Para la práctica

- Nginx en el **80** de la VM, accesible desde `http://tunombre.me`.
- Que copien una foto grande en `html/img/` y prueben distintos anchos con `?w=`.
- Para que vean bots en el log de acceso, conviene que el contenedor esté publicado en el 80 desde el principio de la sesión.
