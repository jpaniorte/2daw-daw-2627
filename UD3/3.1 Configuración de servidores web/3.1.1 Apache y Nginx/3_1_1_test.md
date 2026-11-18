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
- Tiempo orientativo: 70 minutos.

## 1. Apache y Nginx

**1.** ¿Qué problema se propuso resolver Nginx cuando nació, en 2004?

- A) Ejecutar páginas PHP sin necesidad de un servidor de aplicaciones.
- B) El problema C10k: atender 10 000 conexiones simultáneas en una sola máquina.
- C) Sustituir el protocolo HTTP por otro más rápido para servir ficheros.
- D) Ofrecer una alternativa libre a Apache, que entonces era de pago.

**2.** ¿Quién mantiene Apache HTTP Server?

- A) F5, que también vende la versión comercial NGINX Plus.
- B) El W3C, que es quien define los estándares de la web.
- C) Microsoft, junto con su servidor IIS.
- D) La Apache Software Foundation.

**3.** ¿Con qué licencia se distribuye Nginx?

- A) BSD de 2 cláusulas.
- B) Apache 2.0.
- C) GPL versión 3.
- D) Propietaria: solo es gratuita para uso educativo.

**4.** Apache HTTP Server nació en 1995. ¿A partir de qué?

- A) Del código fuente de Nginx.
- B) Del servidor IIS de Microsoft.
- C) Del servidor NCSA httpd.
- D) Del navegador Netscape Navigator.

**5.** ¿Por qué el curso usa Nginx para las prácticas?

- A) Porque Apache no puede servir HTTPS ni ampliarse con módulos.
- B) Porque los resultados de aprendizaje del módulo obligan a usar Nginx.
- C) Es el servidor web más usado y el que suele ir delante de las aplicaciones como proxy inverso.
- D) Porque Apache no tiene imagen oficial de Docker.

**6.** ¿Qué comando de Apache (Debian) equivale a activar un módulo dinámico en Nginx con `load_module`?

- A) `a2enmod`
- B) `a2ensite`
- C) `apachectl -t`
- D) `apt install apache2`

## 2. Nginx en Docker

**7.** Según el bloque, ¿qué inconveniente tiene instalar Nginx con `sudo apt install nginx`?

- A) No se puede gestionar con systemd: hay que arrancarlo a mano cada vez.
- B) Solo funciona si después se mete dentro de un contenedor.
- C) Obliga a escribir un `Dockerfile` con la configuración.
- D) Se mezcla con el sistema, es difícil de repetir igual en otra máquina y la versión es la de la distribución.

**8.** ¿Qué es una **imagen propia** de Nginx?

- A) La imagen oficial `nginx:1.30` descargada con `docker pull`.
- B) Una imagen construida con un `Dockerfile` `FROM nginx:1.30` que copia tu configuración dentro.
- C) Un contenedor en el que se ha entrado con `docker exec` para editar la configuración.
- D) El paquete `nginx` de Debian instalado directamente en la VM.

**9.** ¿Por qué la imagen oficial arranca Nginx con `nginx -g 'daemon off;'`?

- A) Para desactivar los *workers* y atender las peticiones con un solo proceso.
- B) Para que no escriba logs y el contenedor ocupe menos.
- C) Para que arranque sin leer los sitios de `conf.d/`.
- D) Para que se quede en primer plano como proceso principal: si termina, el contenedor se para.

**10.** En un contenedor, ¿qué equivale a `systemctl reload nginx`?

- A) `docker restart web`
- B) `docker exec web nginx -s reload`
- C) `docker start web`
- D) `docker compose up -d --build`

**11.** En un contenedor, ¿qué equivale a `systemctl enable nginx` (arrancar el servicio al encender la máquina)?

- A) `docker start web`
- B) `docker exec web nginx -s reload`
- C) La política `--restart unless-stopped` (o `restart:` en Compose).
- D) La opción `-d` de `docker run`.

**12.** ¿Qué pasa con las conexiones en curso al hacer `nginx -s reload`?

- A) Terminan con normalidad: los *workers* antiguos acaban lo que tienen y los nuevos atienden lo que llega.
- B) Se cortan todas, igual que en un reinicio.
- C) Se quedan en espera hasta que el contenedor se reinicia.
- D) Reciben un `503 Service Unavailable` mientras se recarga.

**13.** Cambias la configuración, tiene un error de sintaxis y haces `nginx -s reload`. ¿Qué ocurre?

- A) Nginx rechaza la configuración nueva y sigue funcionando con la anterior.
- B) Nginx se para y la web se cae inmediatamente.
- C) Nginx carga la parte correcta e ignora la línea con el error.
- D) Docker reconstruye la imagen con la última configuración válida.

**14.** ¿Cuándo hay que reiniciar o recrear el contenedor en lugar de recargar?

- A) Siempre que cambias un fichero de `conf.d/`.
- B) Cada vez que modificas el `index.html` de la web.
- C) Cuando cambias algo que no es configuración de Nginx: la imagen, los volúmenes o los puertos publicados.
- D) Nunca: `nginx -s reload` sirve para cualquier cambio.

**15.** En `docker run -d -p 8080:80 nginx:1.30`, ¿qué significa `-p 8080:80`?

- A) El puerto 80 de la máquina se redirige al puerto 8080 del contenedor.
- B) El puerto 8080 de la máquina se redirige al puerto 80 del contenedor.
- C) Nginx escucha a la vez en el 8080 y en el 80 dentro del contenedor.
- D) Se abren los puertos 8080 y 80 en el cortafuegos de la máquina.

**16.** Cambias en Nginx `listen 80;` por `listen 8080;` pero el contenedor sigue publicado con `-p 80:80`. ¿Qué pasa?

- A) Funciona igual, porque Docker detecta el puerto nuevo de Nginx.
- B) Responde en el 8080 de la máquina sin cambiar nada más.
- C) Docker cambia la publicación a `-p 80:8080` al recargar.
- D) Deja de responder: Docker envía las peticiones al 80 del contenedor, donde ya no escucha nadie.

**17.** En la VM, `curl localhost` devuelve 200, pero desde tu navegador la web da *timeout*. ¿Qué capa es la sospechosa?

- A) El `listen` de Nginx, que está mal puesto.
- B) El NSG de Azure, que no deja pasar el puerto.
- C) Falta el `index.html` en la carpeta publicada.
- D) La directiva `server_tokens`, que bloquea a los navegadores.

**18.** ¿Qué relación hay entre los puertos publicados por Docker y el cortafuegos `ufw` de la VM?

- A) `ufw` bloquea siempre los puertos publicados por Docker.
- B) Docker desactiva `ufw` al instalarse.
- C) `ufw` solo filtra el puerto 22 de SSH.
- D) Los puertos publicados por Docker se saltan las reglas de `ufw`.

**19.** En tu VM solo están abiertos el 22, el 80 y el 443, y publicas un contenedor en el 8080. ¿Cómo lo pruebas?

- A) Desde la propia VM con `curl localhost:8080`, o con un túnel SSH.
- B) Abriendo `http://tunombre.me:8080` en el navegador.
- C) Cambiando el `listen` de Nginx a `8080`.
- D) No se puede probar hasta que se abra el 8080 en el NSG.

**20.** Dentro del contenedor, ¿por qué el proceso maestro de Nginx corre como `root`?

- A) Para poder ejecutar los ficheros PHP de la web.
- B) Porque los *workers* necesitan escribir en la carpeta de la web.
- C) Para poder abrir el puerto 80.
- D) Porque Docker obliga a que todos los procesos sean de `root`.

## 3. La configuración de Nginx

**21.** En la imagen oficial, ¿dónde está la configuración del sitio por defecto?

- A) `/etc/nginx/sites-enabled/default`
- B) `/usr/share/nginx/html/default.conf`
- C) `/etc/nginx/conf.d/default.conf`
- D) `/var/www/html/nginx.conf`

**22.** ¿Cómo llega `conf.d/default.conf` a la configuración de Nginx?

- A) `nginx.conf` lo incluye con `include /etc/nginx/conf.d/*.conf;` dentro de `http`.
- B) Nginx lee todos los ficheros de `/etc/nginx` en orden alfabético.
- C) Se carga con `load_module` al principio de `nginx.conf`.
- D) Docker lo copia dentro de `nginx.conf` al arrancar el contenedor.

**23.** ¿Para qué sirve el fichero `/etc/nginx/mime.types`?

- A) Lista los módulos dinámicos que se pueden cargar.
- B) Define los usuarios que pueden acceder a la web.
- C) Contiene las páginas de error de cada código de estado.
- D) Asocia la extensión de cada fichero con su `Content-Type`.

**24.** ¿Qué hace `worker_processes auto;`?

- A) Ajusta los *workers* según el número de visitas de cada momento.
- B) Arranca un *worker* por cada núcleo de CPU.
- C) Arranca un único *worker* que atiende todas las conexiones.
- D) Arranca tantos *workers* como indique `worker_connections`.

**25.** En el bloque `events`, ¿qué indica `worker_connections 1024;`?

- A) El número máximo de peticiones por segundo del servidor.
- B) El número máximo de ficheros que se pueden publicar.
- C) El tamaño máximo del log de acceso, en líneas.
- D) El número máximo de conexiones simultáneas de cada *worker*.

**26.** En la configuración de Nginx, ¿cómo terminan las directivas?

- A) Con un salto de línea.
- B) Con `;`
- C) Con `}`
- D) Con `.`

**27.** ¿Cuál es el anidamiento correcto de los bloques de Nginx?

- A) `main` → `server` → `http` → `location`
- B) `http` → `events` → `server` → `location`
- C) `main` → `http` → `server` → `location`
- D) `server` → `http` → `location` → `main`

**28.** ¿En qué contexto se puede escribir `load_module`?

- A) Solo en `main`, fuera de cualquier bloque.
- B) Dentro de `http { }`.
- C) Dentro del `server { }` que vaya a usar el módulo.
- D) Dentro del `location` que vaya a usar el módulo.

**29.** Escribes `root /usr/share/nginx/html;` en el `server` y no en sus `location`. ¿Qué pasa?

- A) Los `location` heredan el `root` del `server`.
- B) Los `location` no publican nada hasta que tengan su propio `root`.
- C) Nginx da un error, porque `root` solo se puede poner en un `location`.
- D) El `root` solo se aplica a `location /`.

**30.** ¿Qué directiva indica el fichero que se sirve al pedir una carpeta?

- A) `root`
- B) `listen`
- C) `index`
- D) `server_name`

**31.** ¿En qué se diferencian `location /hola { … }` y `location = /hola { … }`?

- A) La primera solo vale para `/hola` exacta; la segunda, para toda URL que empiece por `/hola`.
- B) La primera vale para toda URL que empiece por `/hola`; la segunda, solo para `/hola` exacta.
- C) Son equivalentes: el `=` solo mejora la legibilidad.
- D) La segunda redirige a `/hola` cualquier URL que no exista.

**32.** ¿Qué hace la directiva `server_name`?

- A) Cambia el nombre del contenedor de Docker.
- B) Fija el valor de la cabecera `Server` de las respuestas.
- C) Registra el dominio en el servidor DNS.
- D) Indica el nombre del sitio; con varios sitios, decide cuál responde.

**33.** ¿Qué muestra `nginx -T`?

- A) Solo si la sintaxis es correcta, sin mostrar la configuración.
- B) Toda la configuración efectiva, con los `include` ya resueltos.
- C) La versión de Nginx y sus módulos estáticos.
- D) Las últimas líneas del log de errores.

**34.** En la imagen oficial, ¿dónde está la web por defecto (`index.html` y `50x.html`)?

- A) `/etc/nginx/html`
- B) `/var/www/html`
- C) `/etc/nginx/conf.d`
- D) `/usr/share/nginx/html`

## 4. Módulos

**35.** ¿En qué se diferencian los módulos estáticos y los dinámicos de Nginx?

- A) Los estáticos están dentro del ejecutable, elegidos al compilar; los dinámicos son ficheros `.so` que se cargan con `load_module`.
- B) Los dinámicos están dentro del ejecutable; los estáticos son ficheros `.so` que se cargan con `load_module`.
- C) Los estáticos sirven ficheros y los dinámicos ejecutan código en cada petición.
- D) Los estáticos son los oficiales y los dinámicos, siempre de terceros.

**36.** ¿Qué comando muestra los módulos dinámicos disponibles en la imagen oficial?

- A) `docker exec web nginx -V`
- B) `docker exec web nginx -t`
- C) `docker exec web ls /etc/nginx/modules`
- D) `docker images nginx`

**37.** ¿Cómo se ven los módulos **estáticos** de Nginx?

- A) Con `ls /etc/nginx/modules`.
- B) Con `nginx -T | grep load_module`.
- C) Con `nginx -V`, en las líneas `--with-…_module`.
- D) Con `cat /etc/nginx/mime.types`.

**38.** ¿Cuál de estos módulos **no** viene en la imagen oficial `nginx:1.30`?

- A) brotli
- B) njs
- C) image_filter
- D) acme

**39.** ¿Para qué sirve el módulo `image_filter`?

- A) Para comprimir las imágenes con Brotli antes de enviarlas.
- B) Para convertir páginas HTML en imágenes JPEG.
- C) Para impedir que se descarguen las imágenes de la web.
- D) Para redimensionar, recortar y girar imágenes al vuelo.

**40.** ¿Para qué sirve el módulo `acme`?

- A) Para saber el país del cliente a partir de su IP.
- B) Para pedir y renovar certificados de Let's Encrypt desde el propio Nginx, sin certbot.
- C) Para bloquear inyecciones SQL y XSS como un cortafuegos.
- D) Para programar respuestas en JavaScript dentro de Nginx.

**41.** ¿Qué es ModSecurity?

- A) Un módulo para mostrar listados de directorios más bonitos.
- B) Un módulo de compresión que reduce más que gzip.
- C) Un servidor de *streaming* de vídeo en directo.
- D) Un cortafuegos de aplicaciones web (WAF) que bloquea inyecciones SQL, XSS… con las reglas OWASP CRS.

**42.** ¿Para qué se usa el módulo de terceros `headers-more`?

- A) Para arrancar más *workers* cuando aumentan las visitas.
- B) Para añadir, cambiar o quitar cualquier cabecera, incluida `Server` entera.
- C) Para aumentar el tamaño máximo de las cabeceras de petición.
- D) Para guardar todas las cabeceras en el log de acceso.

**43.** ¿Qué hace falta para usar un módulo de terceros con la imagen oficial de Nginx?

- A) Basta con instalar dentro el paquete `libnginx-mod-…` de Debian.
- B) Basta con descargar cualquier `.so` del módulo y copiarlo en `modules/`.
- C) Compilarlo contra el código fuente de exactamente la misma versión de Nginx y copiar el `.so`.
- D) Basta con activarlo con `nginx -s reload`.

**44.** Al arrancar Nginx aparece `module "…headers_more_filter_module.so" version 1026003 instead of 1030006`. ¿Qué significa?

- A) El `.so` está compilado para otra versión de Nginx (1.26.3) distinta de la que lo carga (1.30.6).
- B) Falta la directiva `load_module` en `nginx.conf`.
- C) El `load_module` está dentro del bloque `http`.
- D) Hay que bajar la imagen a la versión 1.26 para poder usar módulos.

**45.** `nginx -t` dice `unknown directive "image_filter"`. ¿Qué pasa?

- A) Se usa una directiva de un módulo que no está cargado.
- B) `image_filter` solo se puede escribir dentro de `http`.
- C) La imagen oficial no trae el módulo `image_filter`.
- D) Falta el `;` al final de la línea de `image_filter`.

**46.** `nginx -t` dice `"load_module" directive is not allowed here`. ¿Qué pasa?

- A) El fichero `.so` del módulo no existe.
- B) El módulo ya estaba cargado y se ha repetido.
- C) `load_module` está dentro de un bloque (por ejemplo, `http`) en lugar de en `main`.
- D) El módulo está compilado para otra versión de Nginx.

**47.** ¿Por qué, para usar `image_filter` con la imagen oficial, hay que llevar un `nginx.conf` propio?

- A) Porque la imagen oficial no trae el fichero `.so` de `image_filter`.
- B) Porque `load_module` va en `nginx.conf`, que es un fichero de la imagen: hay que copiar el nuestro con un `Dockerfile` o montarlo.
- C) Porque los módulos dinámicos no funcionan con los sitios montados en `conf.d/`.
- D) Porque los módulos solo se pueden activar al compilar Nginx.

**48.** En `image_filter resize $arg_w -;`, ¿qué es `$arg_w`?

- A) El ancho original de la imagen guardada en disco.
- B) Una variable de entorno `W` del contenedor.
- C) El tamaño máximo de imagen fijado con `image_filter_buffer`.
- D) El valor del parámetro `w` de la URL (`?w=200`).

**49.** En `location /miniatura/ { alias /usr/share/nginx/html/img/; … }`, ¿qué hace `alias`?

- A) Crea una copia de `img/` llamada `miniatura/` al arrancar.
- B) Sustituye el prefijo de la URL por esa carpeta: `/miniatura/foto.jpg` → `img/foto.jpg`.
- C) Redirige el navegador a `/img/` con un `302`.
- D) Pone otro nombre al contenedor dentro de la red de Docker.

**50.** ¿Qué es njs?

- A) Una versión de Node.js que se instala dentro del contenedor de Nginx.
- B) Un módulo que ejecuta en el servidor el JavaScript de la página para mejorar el SEO.
- C) Un módulo que sirve los ficheros `.js` comprimidos.
- D) Un módulo para ejecutar JavaScript dentro de Nginx, para pequeñas lógicas, sin `npm` ni paquetes de Node.js.

## 5. Cambiar la configuración sin romper nada

**51.** ¿Dónde conviene poner los sitios (`conf.d/`), que cambias a menudo?

- A) Montados desde la máquina (*bind mount*), recargando después de editarlos.
- B) Dentro de la imagen con `COPY`, reconstruyéndola en cada cambio.
- C) Dentro del contenedor, editándolos con `docker exec`.
- D) En `/usr/share/nginx/html`, junto con la web.

**52.** Editas la configuración dentro del contenedor con `docker exec web vi /etc/nginx/conf.d/default.conf`. ¿Qué problema tiene?

- A) El cambio se guarda en la imagen y afecta a todos los contenedores.
- B) El cambio se copia automáticamente a la carpeta de la máquina.
- C) El cambio se pierde al recrear el contenedor.
- D) No se puede: los contenedores no permiten editar ficheros.

**53.** ¿Por qué es más seguro montar la carpeta `conf.d/` que un solo fichero `default.conf`?

- A) Porque Docker no permite montar un solo fichero.
- B) Porque un fichero suelto se monta siempre en solo escritura.
- C) Muchos editores guardan creando un fichero nuevo, y el contenedor sigue viendo el antiguo.
- D) Porque Nginx solo lee configuración de carpetas montadas.

**54.** Has cambiado `nginx.conf`, que va **dentro de la imagen** con un `Dockerfile`. ¿Cómo se aplica?

- A) `docker compose up -d --build`
- B) `docker compose exec web nginx -s reload`
- C) Editando también el `index.html`.
- D) `docker compose restart web`

**55.** ¿Cuál es el ciclo de trabajo para cambiar la configuración?

- A) Editar → reiniciar → comprobar (`nginx -t`) → probar con `curl`.
- B) Editar → recargar → comprobar (`nginx -t`) → mirar los logs.
- C) Editar → reconstruir la imagen → reiniciar → `nginx -T`.
- D) Editar → comprobar (`nginx -t`) → recargar → probar con `curl` → mirar los logs.

**56.** `nginx -t` dice `unexpected "}" in /etc/nginx/conf.d/default.conf:7`. ¿Qué es lo más probable?

- A) Que sobre la llave de la línea 7.
- B) Que falte el `;` al final de la línea anterior.
- C) Que falte un `load_module` en `nginx.conf`.
- D) Que el fichero tenga más de 7 líneas.

**57.** Un `reload` falló por un error y nadie lo corrigió. Horas después se reinicia la VM. ¿Qué pasa?

- A) Nginx arranca con la última configuración que funcionaba.
- B) Docker restaura la configuración de la imagen original.
- C) Nginx arranca e ignora el fichero que tiene el error.
- D) Nginx arranca con la configuración rota, el proceso principal falla y la web se cae.

**58.** Tienes `restart: unless-stopped` y la configuración rota. ¿Qué muestra `docker ps` después de un reinicio?

- A) `Up`, porque Docker arranca el contenedor aunque Nginx falle.
- B) `Restarting`, porque Docker intenta arrancarlo una y otra vez.
- C) `Exited (0)`, y no lo vuelve a intentar.
- D) `Paused`, hasta que corrijas la configuración.

## 6. Logs

**59.** En la imagen oficial, ¿qué es `/var/log/nginx/access.log`?

- A) Un fichero normal que crece dentro del contenedor.
- B) Un enlace a `/dev/stderr`.
- C) Un enlace a `/dev/stdout`.
- D) No existe: la imagen oficial no tiene log de acceso.

**60.** ¿En qué se diferencian el log de acceso y el de errores?

- A) El de acceso tiene una línea por petición atendida; el de errores, avisos y fallos (configuración, ficheros que no se pueden leer…).
- B) El de acceso solo guarda las peticiones con éxito; el de errores, las que dan 4xx o 5xx.
- C) El de acceso es para el dominio público y el de errores, para `localhost`.
- D) Guardan lo mismo, pero el de errores usa un formato más detallado.

**61.** ¿Cómo se ve el log de Nginx en directo?

- A) `docker logs -f web`
- B) `docker logs --tail web`
- C) `docker inspect web`
- D) `docker exec web cat /var/log/nginx/access.log`

**62.** ¿Qué muestra `docker logs web 2>/dev/null`?

- A) Solo el log de errores (stderr).
- B) Nada: `/dev/null` descarta toda la salida.
- C) Solo el log de acceso (stdout), además de los mensajes de arranque de la imagen.
- D) Todo, y además borra el log después de mostrarlo.

**63.** ¿Por qué la imagen oficial envía los logs a la salida estándar y a la de error?

- A) Para que ocupen menos espacio en el disco del contenedor.
- B) Para que Docker los recoja y se puedan ver con `docker logs`.
- C) Porque Nginx no sabe escribir en ficheros.
- D) Para que se vean en el navegador al abrir la web.

**64.** En la línea `81.45.12.200 - - [12/Nov/2026:10:15:32 +0100] "GET /index.html HTTP/1.1" 200 10958 …`, ¿qué es `10958`?

- A) El puerto de origen del cliente.
- B) Los milisegundos que tardó la respuesta.
- C) El número de petición desde que arrancó Nginx.
- D) Los bytes del cuerpo de la respuesta.

**65.** En esa misma línea, ¿qué es `81.45.12.200`?

- A) La IP pública del servidor.
- B) La IP del cliente (`$remote_addr`).
- C) La IP del proxy que hay delante de Nginx.
- D) La IP del servidor DNS que resolvió el dominio.

**66.** ¿Qué guarda el campo `$http_user_agent` del log de acceso?

- A) El usuario que ha iniciado sesión en la aplicación.
- B) El sistema operativo del servidor.
- C) La página desde la que venía el enlace.
- D) Qué programa hace la petición: un navegador, `curl`, un bot…

**67.** ¿Qué guarda el campo `$http_referer`?

- A) La página desde la que venía el enlace (cabecera `Referer`).
- B) La IP real del cliente cuando hay un proxy delante.
- C) El usuario autenticado con HTTP.
- D) Los tipos de contenido que acepta el cliente.

**68.** ¿Cuándo aparece algo distinto de `-` en el campo `$remote_user`?

- A) Cuando el usuario ha iniciado sesión en la aplicación con una cookie.
- B) Siempre que la petición la hace un navegador.
- C) Cuando hay autenticación en el servidor web.
- D) Cuando el cliente se conecta como `root`.

**69.** ¿Qué guarda el campo `$http_x_forwarded_for`?

- A) La IP del servidor al que se reenvía la petición.
- B) La URL a la que se redirige al cliente.
- C) La IP real del cliente cuando hay un proxy delante.
- D) El puerto publicado por Docker.

**70.** Tu log muestra peticiones a `/wp-login.php`, `/.env` y `/phpmyadmin/` con 404 que nadie de tu equipo ha hecho. ¿Qué son?

- A) Bots que recorren Internet buscando fallos conocidos; que den 404 es buena señal.
- B) Pruebas que hace Nginx al arrancar para comprobar la configuración.
- C) Indicios de que alguien ha instalado un WordPress en tu servidor.
- D) Errores de tu configuración, que deberían dar 200.

## 7. Permisos y usuario del servicio

**71.** En la imagen oficial, ¿con qué usuario corren los *workers* de Nginx?

- A) `root`
- B) `www-data`
- C) El usuario de la máquina que lanzó el contenedor.
- D) `nginx` (UID 101).

**72.** En el Nginx del paquete de Debian/Ubuntu, ¿con qué usuario corren los *workers*?

- A) `nginx`
- B) `www-data`
- C) `root`
- D) `apache`

**73.** ¿Qué permisos son los habituales en los ficheros y las carpetas de la web?

- A) `600` en los ficheros y `700` en las carpetas.
- B) `777` en los ficheros y en las carpetas.
- C) `755` en los ficheros y `644` en las carpetas.
- D) `644` en los ficheros y `755` en las carpetas.

**74.** Una página da 403 y el log de errores dice `open() "…/privado.html" failed (13: Permission denied)`. ¿Qué pasa?

- A) El fichero no existe en la carpeta publicada.
- B) El usuario de los *workers* no puede leer el fichero: hay que darle permiso de lectura (`644`).
- C) Falta cargar el módulo que sirve ficheros HTML.
- D) Hay que activar `autoindex` en esa carpeta.

**75.** Una URL da 403 y el log dice `directory index of "…/docs/" is forbidden`. ¿Qué pasa?

- A) El usuario `nginx` no puede leer los ficheros de la carpeta.
- B) La carpeta `docs/` no existe.
- C) Se ha pedido una carpeta sin `index.html` y `autoindex` está desactivado.
- D) `server_tokens off` impide mostrar carpetas.

**76.** Una web funciona en tu portátil con Docker Desktop, pero en la VM Linux da 403. ¿Cuál es la causa probable?

- A) En Linux, los ficheros montados conservan sus permisos, y en Docker Desktop se traducen: un `600` no se nota en el portátil.
- B) Docker Desktop usa una versión de Nginx distinta de la imagen oficial.
- C) La VM Linux no permite montar carpetas en los contenedores.
- D) Azure bloquea por defecto los ficheros `.html`.

## 8. Primeras medidas de seguridad

**77.** ¿Qué consigue `server_tokens off;`?

- A) Que la cabecera `Server` diga `nginx`, sin la versión.
- B) Que la cabecera `Server` desaparezca de las respuestas.
- C) Que no se escriba el log de acceso.
- D) Que Nginx deje de aceptar HTTP/1.1.

**78.** ¿Por qué ocultar la versión de Nginx no es suficiente?

- A) Porque Nginx sigue escribiendo la versión en cada línea del log.
- B) Porque `server_tokens off` no funciona en Docker.
- C) Porque no sustituye a actualizar: solo pone las cosas algo más difíciles a un atacante.
- D) Porque los navegadores necesitan la versión para mostrar la web.

**79.** ¿Qué hace `autoindex on;`?

- A) Crea un `index.html` automático con una plantilla.
- B) Si una carpeta no tiene `index.html`, muestra la lista de sus ficheros.
- C) Sirve el primer fichero de la carpeta por orden alfabético.
- D) Avisa a los buscadores para que indexen la web.

**80.** ¿Cómo viene configurado por defecto el listado de directorios?

- A) Activado en los dos servidores.
- B) Desactivado en los dos servidores.
- C) En Nginx, activado; en Apache de Debian, desactivado.
- D) En Nginx, desactivado (`autoindex off`); en Apache de Debian, activado (`Options Indexes`).

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
