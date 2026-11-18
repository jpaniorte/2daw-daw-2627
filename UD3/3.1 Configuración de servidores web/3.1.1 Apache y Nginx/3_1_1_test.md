---
layout: default
title: "Servidores Web — Bloque 3.1.1: Instalación y configuración básica de Nginx (Test)"
permalink: /servidores-web/semana-1/test/
---

# Bloque 3.1.1 — Test de instalación y configuración básica de Nginx

**Módulo:** Despliegue de Aplicaciones Web (0614) · 2º DAW · UD3: Administración de servidores web

## Instrucciones

- 80 preguntas con 4 opciones y **una sola respuesta correcta**.
- Puntuación: acierto **+1** · error **−1/3** · en blanco **0**.
- Nota sobre 10 = (aciertos − errores / 3) × 10 / 80. Si el resultado es negativo, la nota es 0.
- Con esta penalización, responder al azar da de media un 0: si no sabes la respuesta, déjala en blanco.
- Tiempo orientativo: 80 minutos.

## 1. Apache y Nginx

**1.** ¿Cuál de estas afirmaciones sobre el origen de Apache y Nginx es correcta?

- A) Apache (1995) nació para atender 10 000 conexiones simultáneas; Nginx (2004), a partir de NCSA httpd.
- B) Apache (1995) nació a partir de NCSA httpd; Nginx (2004), para atender 10 000 conexiones simultáneas.
- C) Apache (2004) nació a partir de NCSA httpd; Nginx (1995), para atender 10 000 conexiones simultáneas.
- D) Los dos nacieron de NCSA httpd, y Nginx se reescribió en 2004 para atender 10 000 conexiones.

**2.** ¿Qué combinación de quién lo mantiene y licencia es la correcta?

- A) Apache: Apache Software Foundation y licencia BSD de 2 cláusulas. Nginx: F5 y licencia Apache 2.0.
- B) Apache: F5 y licencia Apache 2.0. Nginx: Apache Software Foundation y licencia BSD de 2 cláusulas.
- C) Apache: Apache Software Foundation y licencia Apache 2.0. Nginx: F5 y licencia comercial NGINX Plus.
- D) Apache: Apache Software Foundation y licencia Apache 2.0. Nginx: F5 y licencia BSD de 2 cláusulas.

**3.** ¿Cuál de estos **no** es uno de los motivos por los que el curso usa Nginx?

- A) Apache no permite configurar HTTPS ni sitios virtuales, que son contenidos del módulo.
- B) Es el servidor web más usado y el que suele ir delante de las aplicaciones como proxy inverso.
- C) Su imagen oficial de Docker es de las más descargadas, está al día y es sencilla.
- D) Lo que pide el módulo se puede hacer con él, y las ideas sirven igual para Apache.

**4.** En Apache (Debian), un módulo se activa con `a2enmod`. ¿Qué es lo equivalente con la imagen oficial de Nginx?

- A) Añadir `load_module` con la ruta del `.so` dentro del bloque `http` y recargar con `nginx -s reload`.
- B) Instalar el paquete `libnginx-mod-…` dentro de la imagen oficial y recargar con `nginx -s reload`.
- C) Añadir `load_module` con la ruta del `.so` al principio de `nginx.conf` y aplicar el cambio.
- D) Copiar el `.so` del módulo en `conf.d/`, porque `nginx.conf` incluye todo lo que hay en esa carpeta.

**5.** Pasas una web de Apache (Debian) a Nginx (imagen oficial). La carpeta `/descargas/` no tiene `index.html` y en Apache se veía la lista de sus ficheros. ¿Qué pasa ahora con Nginx?

- A) Muestra la lista de ficheros igual, porque `autoindex` viene activado por defecto.
- B) Responde 404, porque sin `index.html` la carpeta no existe para Nginx.
- C) Responde 403, porque en Nginx `autoindex` viene desactivado por defecto.
- D) Sirve el primer fichero de la carpeta por orden alfabético.

**6.** Según el bloque, ¿dónde sigue Apache especialmente presente?

- A) En el alojamiento compartido.
- B) Delante de las aplicaciones, como proxy inverso.
- C) En las imágenes oficiales de Docker más descargadas.
- D) En los servidores que deben atender el problema C10k.

## 2. Nginx en Docker

**7.** Quieres que la configuración global de Nginx, con sus módulos cargados, viaje versionada en el repositorio y se despliegue igual en cualquier máquina. ¿Qué forma de instalación propone el bloque?

- A) El paquete del sistema (`apt install nginx`), gestionado con systemd.
- B) La imagen oficial `nginx:1.30`, editando la configuración con `docker exec`.
- C) La imagen oficial `nginx:1.30`, cargando los módulos con `nginx -s reload` al arrancar.
- D) Una imagen propia `FROM nginx:1.30` con un `COPY` de esa configuración.

**8.** Un contenedor de la imagen oficial, arrancado con `docker run -d` sin política de reinicio. Ejecutas `docker exec web nginx -s stop`. ¿Qué pasa?

- A) Nginx termina, pero el contenedor sigue en marcha esperando a que vuelvas a lanzarlo.
- B) Nginx termina y, como es el proceso principal, el contenedor se para.
- C) Nginx se vuelve a arrancar solo, porque systemd lo vigila dentro del contenedor.
- D) No pasa nada: dentro de un contenedor Nginx solo se para con `docker stop`.

**9.** ¿Qué pasaría si la imagen arrancara Nginx sin `daemon off;`, es decir, en segundo plano, como en una máquina normal?

- A) Funcionaría igual, pero los logs irían a ficheros y dejarían de verse con `docker logs`.
- B) Funcionaría igual, pero el servicio pasaría a gestionarlo systemd dentro del contenedor.
- C) Los *workers* no arrancarían, porque solo se crean cuando el maestro está en segundo plano.
- D) El proceso principal terminaría al pasar Nginx a segundo plano, y el contenedor se pararía.

**10.** ¿Cuál de estas equivalencias entre systemd y Docker es **incorrecta**?

- A) `systemctl start nginx` ↔ `docker start web`
- B) `systemctl reload nginx` ↔ `docker restart web`
- C) `systemctl enable nginx` ↔ `--restart unless-stopped`
- D) `systemctl status nginx` ↔ `docker ps` y `docker logs web`

**11.** ¿Qué hace exactamente `nginx -s reload`?

- A) El maestro se para y arranca otro maestro que vuelve a leer la configuración, cortando las conexiones en curso.
- B) Los *workers* vuelven a leer la configuración uno a uno, mientras el maestro sigue con la anterior.
- C) El maestro relee la configuración, arranca *workers* nuevos y deja que los antiguos terminen sus conexiones.
- D) El maestro vuelve a leer la configuración y se la aplica a los *workers* que ya existen, sin crear procesos nuevos.

**12.** Guardas en `default.conf` un error de sintaxis, ejecutas `nginx -s reload` y después `curl -I http://localhost`. ¿Qué ves?

- A) El `reload` muestra el error y `curl` recibe un 200: Nginx sigue con la configuración anterior.
- B) El `reload` no dice nada y `curl` recibe un 502 hasta que corrijas el error.
- C) El `reload` muestra el error y `curl` no conecta, porque el contenedor se ha parado.
- D) El `reload` muestra el error y `curl` recibe un 200, porque se ha cargado todo menos la línea errónea.

**13.** En `compose.yaml` cambias la publicación de `"8080:80"` a `"8081:80"`. ¿Cómo se aplica?

- A) Recreando el contenedor con `docker compose up -d`, porque los puertos los gestiona Docker.
- B) Con `docker compose exec web nginx -s reload`, porque es un cambio de configuración del servicio.
- C) Cambiando también `listen 80;` por `listen 8081;` y recargando Nginx.
- D) Con `docker compose exec web nginx -t`, que aplica el cambio si la sintaxis es correcta.

**14.** Arrancas `docker run -d -p 8081:80 nginx:1.30` en una máquina donde no hay nada más escuchando. ¿Qué pasa con `curl http://localhost` (puerto 80)?

- A) Responde 200, porque Nginx sigue escuchando en el 80 dentro del contenedor.
- B) Responde 301 y redirige al puerto 8081.
- C) No conecta: en la máquina solo se ha publicado el 8081.
- D) Responde 404, porque el 80 de la máquina no tiene web.

**15.** Tu `compose.yaml` publica `"80:8080"` y `default.conf` tiene `listen 80;`. ¿Qué pasa al pedir `http://localhost`?

- A) Responde, porque Docker reenvía la petición al puerto en el que esté escuchando Nginx.
- B) No responde: Docker envía las peticiones al 8080 del contenedor, donde no escucha nadie.
- C) Responde, pero por el 8080 de la máquina en lugar de por el 80.
- D) Responde, porque Nginx detecta el puerto publicado y empieza a escuchar en el 8080.

**16.** Desde la VM, `curl http://localhost` devuelve 200. Desde casa, `http://tunombre.me` da *timeout*, y `dig +short tunombre.me` devuelve la IP correcta. ¿Dónde está el problema?

- A) En `ufw`, que no tiene abierto el puerto 80 en la VM.
- B) En la publicación de Docker, que no tiene el `-p` puesto.
- C) En el `listen` de Nginx, que solo acepta peticiones de `localhost`.
- D) En el NSG de Azure, que no deja pasar el puerto.

**17.** Tu VM tiene `ufw` activado y solo permite el 22, el 80 y el 443. Publicas un contenedor con `-p 8080:80`. ¿Qué pasa con el 8080?

- A) `ufw` lo bloquea, y hay que abrirlo con `ufw allow 8080` además de publicarlo con `-p`.
- B) `ufw` no lo filtra: los puertos publicados por Docker se saltan sus reglas.
- C) Docker no consigue publicarlo, porque `ufw` no lo permite.
- D) `ufw` lo bloquea desde Internet, pero desde la propia VM el 8080 funciona con normalidad.

**18.** ¿Qué hace `ssh -L 8080:localhost:8080 daw`?

- A) Abre el 8080 de la VM en el NSG mientras dure la sesión SSH.
- B) Abre el 8080 de la VM y lo lleva por SSH al `localhost:8080` de tu ordenador.
- C) Publica el 8080 del contenedor en el 8080 de la VM sin usar `-p`.
- D) Abre el 8080 de tu ordenador y lo lleva por SSH al `localhost:8080` de la VM.

**19.** En la imagen oficial, `docker top web` muestra un proceso de `root` y varios con UID 101. ¿Qué afirmación es correcta?

- A) El de `root` es el maestro, que abre el puerto; los del UID 101 son los *workers*, que atienden las peticiones.
- B) El de `root` es el *worker* que atiende las peticiones; los del UID 101 son copias de reserva del proceso maestro.
- C) El de `root` atiende las peticiones de HTTPS, y los del UID 101, las de HTTP.
- D) Todos atienden peticiones; el de `root` solo se encarga además de escribir los logs.

**20.** Con `apt install nginx` en Debian 13 obtienes la versión 1.26.3, y la imagen `nginx:1.30` trae la 1.30.6. Según el bloque, ¿por qué?

- A) La imagen oficial siempre lleva una versión de pruebas, que aún no es estable.
- B) La 1.26.3 es la última versión libre; la imagen lleva la de NGINX Plus.
- C) Con el paquete del sistema, la versión es la que empaqueta la distribución.
- D) `apt` instala la versión mínima compatible con systemd.

## 3. La configuración de Nginx

**21.** En la imagen oficial, ¿qué terna es la correcta: configuración global, sitio por defecto y web por defecto?

- A) `/etc/nginx/nginx.conf`, `/etc/nginx/sites-enabled/default` y `/var/www/html`
- B) `/etc/nginx/conf.d/nginx.conf`, `/etc/nginx/default.conf` y `/usr/share/nginx/html`
- C) `/etc/nginx/nginx.conf`, `/etc/nginx/conf.d/default.conf` y `/usr/share/nginx/html`
- D) `/usr/share/nginx/nginx.conf`, `/etc/nginx/conf.d/default.conf` y `/var/www/html`

**22.** Creas `conf.d/tienda.conf` con un bloque `server`. ¿Por qué lo lee Nginx sin tocar nada más?

- A) Porque `nginx.conf` incluye `conf.d/*.conf` dentro del bloque `http`.
- B) Porque `nginx.conf` incluye `conf.d/*.conf` en el contexto `main`, fuera de cualquier bloque.
- C) Porque Nginx lee todos los ficheros que hay en `/etc/nginx` y sus subcarpetas.
- D) Porque `default.conf` incluye el resto de ficheros de su misma carpeta.

**23.** Escribes en `conf.d/extra.conf` solo la línea `worker_processes 2;`. ¿Qué dice `nginx -t`?

- A) Que la sintaxis es correcta: los ficheros de `conf.d/` pueden cambiar cualquier directiva global de Nginx.
- B) Que la sintaxis es correcta, pero la directiva se ignora porque ya está en `nginx.conf`.
- C) `unknown directive "worker_processes"`, porque esa directiva solo existe en Apache.
- D) `"worker_processes" directive is not allowed here`, porque `conf.d/*.conf` se incluye dentro de `http`.

**24.** En tu `nginx.conf` has borrado `include /etc/nginx/mime.types;`. Ahora un `informe.pdf` se descarga en vez de abrirse en el navegador. ¿Por qué?

- A) Sin `mime.types`, Nginx no sabe servir ficheros que no sean `.html` y devuelve un 415.
- B) Sin `mime.types`, Nginx no sabe el `Content-Type` del fichero y envía el `default_type` (`application/octet-stream`).
- C) Sin `mime.types`, Nginx cifra los ficheros binarios y el navegador no puede mostrarlos.
- D) Sin `mime.types`, Nginx envía todo como `Content-Type: text/html` y el navegador no sabe abrir el PDF como página.

**25.** En una máquina de 2 núcleos, con `worker_processes auto;` y `worker_connections 1024;`, ¿cuántas conexiones simultáneas puede atender Nginx como máximo, aproximadamente?

- A) Unas 1024.
- B) Unas 512.
- C) Unas 4096.
- D) Unas 2048.

**26.** En `default.conf`, la línea 5 es `root /usr/share/nginx/html` (sin `;`) y la 6 es `index index.html;`. ¿Qué dice `nginx -t`?

- A) `directive "root" is not terminated by ";" in /etc/nginx/conf.d/default.conf:5`
- B) `invalid number of arguments in "root" directive … default.conf:6`
- C) `unknown directive "index" … default.conf:6`
- D) `unexpected "}" … default.conf:7`

**27.** ¿Cuál de estas estructuras es válida en Nginx?

- A) `server { http { location / { root /web; } } }`
- B) `http { location / { server { root /web; } } }`
- C) `http { server { location / { root /web; } } }`
- D) `events { server { location / { root /web; } } }`

**28.** ¿Cuál de estas directivas **no** se puede escribir dentro de un bloque `server`?

- A) `user`
- B) `root`
- C) `index`
- D) `error_page`

**29.** En el `server` tienes `root /web;` y dentro `location /img/ { root /fotos; }`. ¿Qué fichero lee Nginx al pedir `/img/a.png`?

- A) `/fotos/img/a.png`
- B) `/fotos/a.png`
- C) `/web/img/a.png`
- D) `/web/fotos/img/a.png`

**30.** Con `index index.html;`, pides `/docs/`. La carpeta `docs/` existe y tiene un `index.htm`, pero no `index.html`. ¿Qué responde Nginx?

- A) 200 con `index.htm`, porque Nginx prueba también esa extensión por defecto.
- B) 404, porque la carpeta no tiene el fichero índice.
- C) 403: no encuentra el índice indicado y `autoindex` está desactivado.
- D) 200 con la lista de ficheros de la carpeta.

**31.** Con `location /pre { … }`, ¿cuál de estas URL **no** entra en ese `location`?

- A) `/premio`
- B) `/pr`
- C) `/pre/x`
- D) `/pre`

**32.** Con `location = /hola { … }` y sin carpeta `hola/` en la web, ¿qué pasa al pedir `/hola/`, con barra final?

- A) Entra en el `location`, porque Nginx ignora la barra final al comparar las URL.
- B) Nginx responde 301 y redirige a `/hola`, sin barra.
- C) Entra en el `location` y se ejecuta con `r.uri` igual a `/hola/`.
- D) No entra en el `location` exacto: Nginx busca `hola/index.html` y responde 404.

**33.** Tienes un único `server` con `server_name tunombre.me;`. Alguien pide `http://IP-de-la-VM/`. ¿Qué pasa?

- A) Responde 404, porque el nombre pedido no coincide con ningún `server_name` configurado.
- B) Responde ese sitio: con un solo `server` en el puerto, atiende todas las peticiones.
- C) Responde 400 Bad Request, porque la petición no trae un nombre de dominio.
- D) Responde 301 y redirige a `http://tunombre.me/`.

**34.** Quieres comprobar si el `load_module` que añadiste está de verdad en la configuración que lee Nginx. ¿Qué ejecutas?

- A) `nginx -t`, que lista los módulos cargados si la sintaxis es correcta.
- B) `nginx -V`, que muestra los módulos con los que arranca Nginx.
- C) `ls /etc/nginx/modules`, que muestra solo los módulos cargados.
- D) `nginx -T`, y buscas `load_module` en la salida.

## 4. Módulos

**35.** Buscas el módulo `gzip_static` y no aparece en `ls /etc/nginx/modules`. ¿Qué concluyes?

- A) Que puede ser un módulo estático: hay que mirarlo con `nginx -V`.
- B) Que no está en la imagen y hay que compilarlo para la 1.30.6.
- C) Que está, pero hay que cargarlo con `load_module` antes de usarlo.
- D) Que está en `conf.d/`, porque los módulos estáticos se configuran allí.

**36.** ¿Qué afirmación sobre los módulos **estáticos** de Nginx es correcta?

- A) Se cargan con `load_module` desde `/etc/nginx/modules`, como los dinámicos.
- B) Solo se activan recompilando, con la directiva `static_module` en `nginx.conf`.
- C) Siempre están disponibles: basta con usar sus directivas, sin `load_module`.
- D) Son los módulos de terceros que vienen empaquetados en Debian.

**37.** ¿Qué comando muestra los módulos dinámicos que están **cargados**?

- A) `docker exec web ls /etc/nginx/modules`
- B) `docker exec web nginx -V | grep load_module`
- C) `docker exec web nginx -T | grep load_module`
- D) `docker exec web nginx -t | grep load_module`

**38.** ¿Qué lista contiene **solo** módulos dinámicos que ya trae la imagen oficial `nginx:1.30`?

- A) njs, image_filter, acme, geoip y xslt
- B) njs, image_filter, brotli, geoip y xslt
- C) image_filter, headers-more, acme, geoip y xslt
- D) njs, lua, acme, geoip2 y xslt

**39.** Quieres bloquear las peticiones con inyecciones SQL antes de que lleguen a la aplicación. ¿Qué módulo usarías y de dónde sale?

- A) acme, que ya viene en la imagen oficial.
- B) njs, que ya viene en la imagen oficial, con las reglas OWASP CRS.
- C) geoip2, un módulo de terceros, bloqueando los países atacantes.
- D) ModSecurity, un módulo de terceros, con las reglas OWASP CRS.

**40.** Quieres certificados de Let's Encrypt sin instalar certbot. ¿Qué necesitas?

- A) Compilar el módulo `acme`, que es de terceros, para la 1.30.6.
- B) Cargar el módulo `acme`, que ya viene en la imagen oficial.
- C) Cargar el módulo `njs` y programar en JavaScript la petición del certificado.
- D) Instalar el paquete `libnginx-mod-acme` dentro de la imagen oficial.

**41.** Quieres que las respuestas no lleven **ninguna** cabecera `Server`. ¿Qué necesitas?

- A) `server_tokens off;` en el bloque `http`.
- B) `server_tokens off;` en el bloque `http` y en cada `server`.
- C) El módulo `xslt`, que reescribe las cabeceras de las respuestas.
- D) El módulo de terceros `headers-more`.

**42.** ¿En qué se diferencian `geoip` y `geoip2`?

- A) `geoip2` viene en la imagen oficial y usa las bases de datos actuales de MaxMind; `geoip` es de terceros y usa las GeoIP antiguas.
- B) `geoip` viene en la imagen oficial y usa las bases de datos GeoIP antiguas; `geoip2` es de terceros y usa las actuales de MaxMind.
- C) `geoip` localiza direcciones IPv4, y `geoip2` añade además la localización de direcciones IPv6.
- D) `geoip` da el país del cliente, y `geoip2`, la ciudad.

**43.** Para usar el módulo brotli con la imagen oficial `nginx:1.30`, ¿qué propone el bloque?

- A) Instalar `libnginx-mod-http-brotli-filter` con `apt` dentro de la imagen oficial y cargarlo.
- B) Descargar el `.so` de brotli de cualquier versión 1.x y cargarlo con `load_module`.
- C) Compilarlo contra el código fuente de la 1.30.6 y copiar el `.so` a la imagen.
- D) Cargarlo con `load_module`, porque ya viene en `/etc/nginx/modules`.

**44.** Al arrancar aparece: `module "…/ngx_http_headers_more_filter_module.so" version 1026003 instead of 1030006`. ¿Qué significa?

- A) El `.so` se compiló para Nginx 1.26.3 y lo intenta cargar un Nginx 1.30.6.
- B) El `.so` se compiló para Nginx 1.30.6 y lo intenta cargar un Nginx 1.26.3.
- C) El módulo necesita como mínimo la 1.26.3: se carga, pero avisa de la diferencia.
- D) El módulo es correcto, pero el `load_module` está dentro del bloque `http`.

**45.** ¿Qué indica cada error? (1) `unknown directive "image_filter"` (2) `"load_module" directive is not allowed here`

- A) (1) El módulo no está cargado; (2) `load_module` no está en el contexto `main`.
- B) (1) `image_filter` está fuera de un `location`; (2) el fichero `.so` del módulo no existe en la imagen.
- C) (1) El `.so` no está en la imagen; (2) el `load_module` está repetido.
- D) (1) Falta el `;` tras `image_filter`; (2) el `.so` es de otra versión de Nginx.

**46.** En `load_module modules/ngx_http_js_module.so;`, ¿respecto a qué carpeta es relativa la ruta?

- A) `/usr/share/nginx/`, la carpeta de la web por defecto.
- B) `/etc/nginx/conf.d/`, la carpeta de los sitios.
- C) `/etc/nginx/`, y `modules/` es un enlace a `/usr/lib/nginx/modules`.
- D) `/usr/lib/nginx/modules/`, la carpeta donde están de verdad los ficheros `.so`.

**47.** Quieres usar `image_filter`. ¿Dónde pones `load_module`?

- A) En `conf.d/default.conf`, al principio del fichero y fuera del `server`, para que se cargue antes.
- B) En tu propio `nginx.conf`, al principio, copiado a la imagen con un `Dockerfile` (o montado).
- C) En el `location /miniatura/`, junto a la directiva `image_filter`.
- D) En el `Dockerfile`, con una instrucción `RUN load_module`.

**48.** Tienes una foto de 1200 × 800 y `image_filter resize $arg_w -;`. Pides `/miniatura/foto.jpg?w=300`. ¿Qué devuelve Nginx?

- A) Una imagen de 300 × 800.
- B) Una imagen de 300 × 300.
- C) Una imagen de 1200 × 800, porque `-` desactiva el redimensionado.
- D) Una imagen de 300 × 200.

**49.** Con `location /miniatura/ { alias /usr/share/nginx/html/img/; }`, pides `/miniatura/foto.jpg`. ¿Qué fichero lee Nginx?

- A) `/usr/share/nginx/html/img/miniatura/foto.jpg`
- B) `/usr/share/nginx/html/img/foto.jpg`
- C) `/usr/share/nginx/html/miniatura/foto.jpg`
- D) Ninguno: responde 302 y redirige a `/img/foto.jpg`.

**50.** En njs, ¿qué es `r` en `function saludo(r) { r.return(200, …); }`?

- A) El objeto de la respuesta, que solo sirve para escribir el cuerpo que se envía.
- B) El *router* de Node.js que reparte las peticiones entre funciones.
- C) El resultado del `location` anterior en la cadena de procesamiento.
- D) El objeto de la petición: `r.uri`, `r.method`, `r.args`, `r.headersIn`…

## 5. Cambiar la configuración sin romper nada

**51.** ¿Qué reparto entre la imagen y los *bind mounts* propone el bloque?

- A) `nginx.conf` y `njs/` dentro de la imagen; `conf.d/` y `html/` montados.
- B) `nginx.conf`, `njs/`, `conf.d/` y `html/` montados, sin imagen propia.
- C) `conf.d/` y `html/` dentro de la imagen; `nginx.conf` y `njs/` montados.
- D) `nginx.conf` y `conf.d/` dentro de la imagen; `njs/` y `html/` montados.

**52.** En un contenedor **sin volúmenes**, editas `default.conf` con `docker exec`, recargas y funciona. ¿Cuándo se pierde ese cambio?

- A) Al recargar Nginx otra vez con `nginx -s reload`.
- B) Al reiniciar el contenedor con `docker restart`, que lo arranca de nuevo desde la imagen.
- C) Al recrear el contenedor (`docker rm` y un `docker run` nuevo).
- D) Nunca: el cambio queda guardado en la imagen.

**53.** Montas solo un fichero: `-v ./default.conf:/etc/nginx/conf.d/default.conf`. Lo editas, `nginx -t` dice que la sintaxis es correcta, recargas… y el cambio no se aplica. ¿Por qué?

- A) `nginx -s reload` no vuelve a leer los ficheros de `conf.d/`, solo los de `nginx.conf`.
- B) Los ficheros montados sueltos son de solo lectura y el cambio no se guarda.
- C) El editor guardó creando un fichero nuevo, y el contenedor sigue viendo el antiguo.
- D) `nginx -t` deshace los cambios que no superan la comprobación.

**54.** Cambias `nginx/nginx.conf`, que el `Dockerfile` copia con `COPY`, y ejecutas `docker compose restart web`. ¿Qué pasa?

- A) Nada: sigue la imagen antigua; hay que reconstruirla con `docker compose up -d --build`.
- B) El cambio se aplica, porque `restart` vuelve a copiar en el contenedor los ficheros del `Dockerfile`.
- C) El cambio se aplica, pero solo después de un `nginx -s reload`.
- D) Compose detecta el cambio en `nginx.conf` y reconstruye la imagen solo.

**55.** Si el `reload` ya rechaza las configuraciones con errores, ¿por qué se hace `nginx -t` **antes** de recargar?

- A) Porque el `reload` aplica la configuración aunque tenga errores, y `nginx -t` lo evita.
- B) Porque `nginx -t` aplica la configuración, y el `reload` después solo la confirma.
- C) Porque el `reload` no muestra ningún mensaje cuando la configuración tiene errores.
- D) Porque el error queda en disco y tumbará el servicio en el próximo arranque.

**56.** `nginx -t` dice `unexpected "}" in …/default.conf:5`. La línea 4 es `index index.html` y la 5 es `}`. ¿Qué hay que corregir?

- A) Borrar la llave de la línea 5, que sobra.
- B) Añadir el `;` al final de la línea 4.
- C) Añadir una `{` al final de la línea 4.
- D) Mover la directiva `index` dentro de un `location`.

**57.** El lunes cambias `default.conf`, el `reload` falla y no te das cuenta. El jueves se reinicia la VM. ¿Qué pasa?

- A) Nginx arranca con la configuración que tenía antes del cambio del lunes.
- B) Nginx arranca, pero rechaza el fichero roto y sirve el resto de sitios.
- C) Docker arranca Nginx con la configuración que trae la imagen oficial.
- D) Nginx no arranca con la configuración rota y la web se cae el jueves.

**58.** Con `restart: unless-stopped` y una configuración rota, `docker compose ps` muestra `Restarting (1)`. ¿Qué significa?

- A) Docker lo ha reiniciado una vez y espera a que corrijas la configuración para seguir.
- B) Nginx termina con el código de error 1, y Docker lo vuelve a arrancar en bucle.
- C) Nginx está arrancando con un solo *worker* hasta que se corrija el error.
- D) Docker espera 1 segundo y, si el error sigue, para el contenedor.

## 6. Logs

**59.** ¿Qué comando muestra **solo** el log de errores de Nginx?

- A) `docker logs web 2>/dev/null`
- B) `docker logs web >/dev/null 2>&1`
- C) `docker logs web 2>&1 >/dev/null`
- D) `docker logs web 1>&2`

**60.** Con `docker logs web 2>/dev/null` ves las peticiones y, además, unas líneas de `/docker-entrypoint.sh`. ¿Por qué?

- A) Los mensajes de arranque de la imagen también salen por la salida estándar.
- B) Son errores de arranque que Nginx escribe también en el log de acceso, además de en el de errores.
- C) Forman parte del formato `main` del log de acceso.
- D) Docker las añade a cualquier salida que no sea de error.

**61.** Pides `/noexiste`. ¿Dónde queda constancia?

- A) En los dos: el 404 en el de acceso y `No such file or directory` en el de errores.
- B) Solo en el log de acceso, porque un 404 es una respuesta normal, no un error del servidor.
- C) Solo en el log de errores, porque el de acceso solo guarda las peticiones con éxito.
- D) En ninguno, porque Nginx no registra las peticiones a ficheros que no existen.

**62.** En `"GET /index.html HTTP/1.1" 200 10958`, ¿qué es `10958`?

- A) Los bytes de toda la respuesta, cabeceras incluidas.
- B) Los milisegundos que tardó la respuesta.
- C) Los bytes del cuerpo de la respuesta.
- D) El PID del *worker* que atendió la petición.

**63.** Con un proxy delante de Nginx, ¿qué campos del log de acceso tendrían la IP del proxy y la IP real del cliente?

- A) `$remote_addr` tendría la del cliente y `$http_x_forwarded_for`, la del proxy.
- B) `$remote_addr` tendría la del proxy y `$http_x_forwarded_for`, la del cliente.
- C) `$remote_addr` tendría la del proxy y `$http_referer`, la del cliente.
- D) Las dos estarían en `$remote_addr`, separadas por comas.

**64.** ¿En qué caso el campo `$remote_user` del log de acceso **no** es `-`?

- A) Cuando el usuario ha iniciado sesión en la aplicación con una cookie.
- B) Cuando la petición la hace un navegador y no un programa como `curl`.
- C) Cuando el cliente se conecta desde la misma máquina que el servidor.
- D) Cuando el servidor web pide autenticación y el cliente se identifica.

**65.** Una línea tiene `"https://www.google.com/"` en el campo `$http_referer`. ¿Qué significa?

- A) Que la petición la hizo el robot de Google para indexar la página.
- B) Que el usuario llegó siguiendo un enlace desde una página de Google.
- C) Que la petición pasó por un proxy de Google antes de llegar a Nginx.
- D) Que Nginx redirigió la respuesta a Google.

**66.** En el campo `[12/Nov/2026:10:15:32 +0100]` del log de acceso, ¿qué indica `+0100`?

- A) Que la respuesta tardó 100 milisegundos.
- B) Que es la conexión número 100 desde que arrancó Nginx.
- C) Que la atendió el *worker* número 1 de los 100 disponibles.
- D) La zona horaria: la hora está expresada en UTC+1.

**67.** Sobre esta línea: `45.148.10.81 - - [12/Nov/2026:03:12:10 +0100] "GET /.env HTTP/1.1" 404 153 "-" "Mozilla/5.0" "-"`, ¿qué afirmación es **incorrecta**?

- A) El fichero `.env` existe, pero Nginx no tiene permiso para leerlo.
- B) Se pidió `/.env` con el método GET y HTTP/1.1.
- C) No hubo *referer*: nadie llegó a esa URL siguiendo un enlace desde otra página.
- D) La petición se hizo a las 3:12 de la madrugada, hora UTC+1.

**68.** En el log de errores: `2026/11/12 10:16:01 [error] 23#23: *3 open() "…/nada" failed (2: No such file or directory)`. ¿Qué es `*3`?

- A) El PID del *worker*.
- B) El nivel de gravedad del error.
- C) El número de conexión.
- D) El número de veces que se ha intentado abrir el fichero.

**69.** ¿Qué *User-Agent* indica con más claridad que la petición la ha hecho un programa automático y no una persona con un navegador?

- A) `Mozilla/5.0 (Windows NT 10.0; Win64; x64) …`
- B) `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) …`
- C) `zgrab/0.x`
- D) `Mozilla/5.0 (X11; Linux x86_64) …`

**70.** Ves peticiones a `/wp-login.php` y `/phpmyadmin/` con 404 desde IP desconocidas. ¿Qué conclusión y qué medida propone el bloque?

- A) Son bots buscando fallos conocidos; el 404 es buena señal. No hay que dejar en la web nada que no deba verse.
- B) Alguien ha subido un WordPress al servidor: hay que borrarlo cuanto antes y cambiar todas las contraseñas.
- C) Hay un error de configuración: esas rutas deberían dar 200, así que hay que revisar el `root` del sitio.
- D) Es un ataque en curso: hay que cerrar el puerto 80 en el NSG hasta que pare.

## 7. Permisos y usuario del servicio

**71.** Al atender una petición, ¿qué usuario necesita poder leer los ficheros de la web?

- A) El del maestro: `root`, tanto en la imagen oficial como en el paquete de Debian/Ubuntu.
- B) El de los *workers*: `www-data` en la imagen oficial y `nginx` en el paquete de Debian/Ubuntu.
- C) El propietario de los ficheros, porque Nginx los abre en su nombre.
- D) El de los *workers*: `nginx` en la imagen oficial y `www-data` en el paquete de Debian/Ubuntu.

**72.** Un fichero tiene permisos `644`, pero la carpeta que lo contiene tiene `700` y es de otro usuario. ¿Qué pasa al pedirlo?

- A) 200: con el fichero en `644` basta para que Nginx lo lea.
- B) 403: el usuario de Nginx no puede atravesar la carpeta (le falta la `x`).
- C) 404: Nginx no puede entrar en la carpeta, así que para él el fichero no existe.
- D) 403 solo si el fichero también tuviera permisos `600`.

**73.** ¿Qué permisos en octal corresponden a `rw-r--r--`?

- A) `755`
- B) `640`
- C) `664`
- D) `644`

**74.** Tres peticiones dejan en el log de errores: (A) `(13: Permission denied)`, (B) `directory index of "…/docs/" is forbidden` y (C) `(2: No such file or directory)`. ¿Qué códigos devolvió Nginx?

- A) A: 403 · B: 404 · C: 404
- B) A: 403 · B: 403 · C: 404
- C) A: 401 · B: 403 · C: 404
- D) A: 500 · B: 403 · C: 404

**75.** Una web funciona en tu portátil con Docker Desktop, pero en la VM Linux da 403 con `Permission denied`. ¿Por qué?

- A) Docker Desktop usa una versión de Nginx distinta de la imagen oficial.
- B) En la VM Linux, los *bind mounts* se montan siempre con permisos `600` para proteger los ficheros.
- C) En Linux se conservan los permisos de los ficheros montados; en Docker Desktop se traducen.
- D) Azure bloquea la lectura de ficheros `.html` hasta que se abre el puerto 443.

**76.** En la VM, un fichero da 403 con `Permission denied`. ¿Qué arreglo propone el bloque?

- A) `chmod 644` a los ficheros y `chmod 755` a las carpetas, en la VM.
- B) Poner `user root;` en `nginx.conf` para que los *workers* puedan leer cualquier fichero.
- C) `chmod 777` a toda la carpeta de la web, para no tener más problemas.
- D) Quitar el `:ro` del volumen, para que Nginx tenga permisos de escritura.

## 8. Primeras medidas de seguridad

**77.** ¿Dónde se puede poner `server_tokens off;` para ocultar la versión?

- A) En el bloque `http` (para todos los sitios) o en un `server` concreto.
- B) Solo en el contexto `main`, junto a `user`, `worker_processes` y `load_module`.
- C) Solo dentro de un `location`, y hay que repetirlo en cada uno.
- D) Solo en el bloque `events`, porque afecta a todas las conexiones.

**78.** Según el bloque, ¿cómo se actualiza Nginx cuando lo ejecutas con Docker?

- A) Con `apt upgrade nginx` dentro del contenedor y después un `nginx -s reload`.
- B) Con `nginx -s reload`, que descarga la última versión de la misma etiqueta.
- C) Cambiando la etiqueta de la imagen o con `docker compose build --pull`.
- D) Con `server_tokens off`, que evita tener que actualizar.

**79.** Activas `autoindex on;` en `location /docs/`, y esa carpeta tiene un `index.html`. ¿Qué ve quien pide `/docs/`?

- A) La lista de ficheros, porque `autoindex on` tiene prioridad sobre el `index.html`.
- B) El `index.html`: el listado solo aparece en las carpetas sin fichero índice.
- C) Un 403, porque `autoindex` e `index` no se pueden usar a la vez.
- D) La lista de ficheros, con el `index.html` destacado al principio.

**80.** Tras añadir `server_tokens off;` y recargar, ¿qué muestra `curl -I http://localhost | grep Server`?

- A) Ninguna línea: la cabecera `Server` desaparece.
- B) `Server: nginx/1.30.6`, porque `server_tokens` solo afecta a las páginas de error.
- C) `Server: hidden`
- D) `Server: nginx`

## Hoja de respuestas

Nombre: ______________________________________

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| 1: ___ | 2: ___ | 3: ___ | 4: ___ | 5: ___ | 6: ___ | 7: ___ | 8: ___ | 9: ___ | 10: ___ |
| 11: ___ | 12: ___ | 13: ___ | 14: ___ | 15: ___ | 16: ___ | 17: ___ | 18: ___ | 19: ___ | 20: ___ |
| 21: ___ | 22: ___ | 23: ___ | 24: ___ | 25: ___ | 26: ___ | 27: ___ | 28: ___ | 29: ___ | 30: ___ |
| 31: ___ | 32: ___ | 33: ___ | 34: ___ | 35: ___ | 36: ___ | 37: ___ | 38: ___ | 39: ___ | 40: ___ |
| 41: ___ | 42: ___ | 43: ___ | 44: ___ | 45: ___ | 46: ___ | 47: ___ | 48: ___ | 49: ___ | 50: ___ |
| 51: ___ | 52: ___ | 53: ___ | 54: ___ | 55: ___ | 56: ___ | 57: ___ | 58: ___ | 59: ___ | 60: ___ |
| 61: ___ | 62: ___ | 63: ___ | 64: ___ | 65: ___ | 66: ___ | 67: ___ | 68: ___ | 69: ___ | 70: ___ |
| 71: ___ | 72: ___ | 73: ___ | 74: ___ | 75: ___ | 76: ___ | 77: ___ | 78: ___ | 79: ___ | 80: ___ |
