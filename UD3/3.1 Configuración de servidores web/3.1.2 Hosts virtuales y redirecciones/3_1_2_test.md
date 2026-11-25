---
layout: default
title: "Servidores Web — Bloque 3.1.2: Hosts virtuales y redirecciones (Test)"
permalink: /servidores-web/semana-2/test/
---

# Bloque 3.1.2 — Test de hosts virtuales y redirecciones

**Módulo:** Despliegue de Aplicaciones Web (0614) · 2º DAW · UD3: Administración de servidores web

## Instrucciones

- 80 preguntas con 4 opciones y **una sola respuesta correcta**.
- Puntuación: acierto **+1** · error **−1/3** · en blanco **0**.
- Nota sobre 10 = (aciertos − errores / 3) × 10 / 80. Si el resultado es negativo, la nota es 0.
- Con esta penalización, responder al azar da de media un 0: si no sabes la respuesta, déjala en blanco.
- Tiempo orientativo: 80 minutos.

## 1. Hosts virtuales y la cabecera `Host`

**1.** Tu VM tiene una sola IP y los nombres `a.com` y `b.com` apuntan a ella. Un cliente pide `http://b.com/`. ¿Qué parte de la petición permite a Nginx saber que se trata de `b.com`?

- A) El nombre `b.com`, que viaja en la IP de destino del paquete TCP.
- B) La línea `Host: b.com`, que el navegador añade a la cabecera.
- C) El nombre `b.com`, escrito en la primera línea como `GET b.com/ HTTP/1.1`.
- D) El puerto de destino, que es distinto para cada nombre de dominio.

**2.** Un compañero propone alojar tus tres webs en la VM con un puerto cada una (8081, 8082 y 8083) en lugar de hosts por nombre. ¿Cuál es la objeción principal?

- A) Nginx no permite que dos `server` escuchen en puertos distintos del 80.
- B) Cada puerto adicional necesita su propio certificado de Let's Encrypt.
- C) Docker solo publica un puerto por contenedor, y el 8080 está reservado.
- D) Habría que escribir el puerto, y el NSG solo abre 22, 80 y 443.

**3.** Sin tocar el DNS, `http://tienda.localhost/` funciona en tu ordenador. En el ordenador de un compañero, ese mismo nombre apunta a la VM de la clase. ¿Qué ocurre si lo intenta?

- A) No llega a la VM: `tienda.localhost` apunta siempre a su propio equipo.
- B) Llega a la VM, porque el DNS del aula resuelve `.localhost` a la IP de la VM.
- C) Llega a la VM, siempre que ya haya un `server_name tienda.localhost` allí.
- D) Falla con un 404, porque el nombre no está en el `hosts` de su ordenador.

**4.** Quieres comprobar qué `server` responderá a `shop.midominio.me` antes de crear el registro DNS. La IP de la VM es `203.0.113.5`. ¿Qué comando usas?

- A) `curl -X Host:shop.midominio.me http://203.0.113.5/ -I`
- B) `curl http://203.0.113.5/shop.midominio.me`
- C) `curl -H "Host: shop.midominio.me" http://203.0.113.5/`
- D) `curl -I shop.midominio.me@203.0.113.5`

**5.** Llega una petición con `Host: Tienda.Localhost` y hay un `server_name tienda.localhost;`. ¿Qué pasa?

- A) No coincide, porque `server_name` distingue mayúsculas y minúsculas.
- B) Coincide, pero Nginx devuelve un 301 a la versión en minúsculas.
- C) Coincide: los nombres no distinguen mayúsculas.
- D) No coincide, salvo que el `server_name` se escriba como regex con `~*`.

**6.** En el fichero aparece primero `server_name *.localhost;` y después otro `server` con `server_name tienda.localhost;`. Llega `Host: tienda.localhost`. ¿Qué `server` responde?

- A) El del comodín, porque está antes y Nginx usa el primero que coincide.
- B) El del nombre exacto, aunque esté escrito después en el fichero.
- C) El del comodín, porque Nginx prefiere siempre el patrón más general.
- D) Los dos: Nginx reparte las peticiones entre los `server` que coinciden.

**7.** ¿En qué orden compara Nginx los `server_name` cuando llega un `Host`?

- A) Expresión regular, nombre exacto, comodín al principio y comodín al final.
- B) Comodín al principio, comodín al final, nombre exacto y expresión regular.
- C) Nombre exacto y, después, todos los demás por orden de aparición en el fichero.
- D) Exacto, comodín al principio, comodín al final y regex (la primera).

**8.** Tienes `server_name ~^(?<sub>web\d)\.localhost$;` en un `server` y `server_name *.localhost;` en otro. Llega `Host: web1.localhost`. ¿Cuál responde?

- A) El del comodín `*.localhost`, porque las regex se miran después.
- B) El de la regex, porque es más específica que un comodín.
- C) El que esté primero en el fichero, sea comodín o regex.
- D) El de la regex, porque captura `sub` y eso tiene prioridad.

**9.** Dos ficheros de `conf.d/` definen `server_name tienda.localhost;` en el puerto 80. Haces `nginx -t`. ¿Qué ocurre?

- A) Falla con un `[emerg]` y no se puede recargar hasta quitar uno de los dos.
- B) Es válida y sin aviso; responde el segundo, que sustituye al primero.
- C) Es válida y Nginx reparte las peticiones entre los dos `server`.
- D) Avisa con `conflicting server name … ignored` y responde el primero.

**10.** ¿Qué significa `server_name _;`?

- A) Un comodín que coincide con cualquier `Host`, aunque no haya `default_server`.
- B) Un nombre que nunca coincide con un `Host`; se usa en `default_server`.
- C) Un nombre reservado que Nginx sustituye por el `Host` de cada petición.
- D) La forma de decir que el `server` no tiene nombre y atiende solo por IP.

**11.** Cambias un `server_name` en un fichero de `conf.d/` montado en el contenedor. ¿Cómo lo aplicas sin cortar las conexiones activas?

- A) `docker compose restart web`, que reinicia el contenedor con la nueva configuración.
- B) `docker compose up -d --build`, que reconstruye la imagen con la configuración.
- C) `docker compose exec web nginx -t && docker compose exec web nginx -s reload`
- D) `docker compose exec web nginx -s stop && docker compose up -d`


## 2. El servidor por defecto y los registros

**12.** Entras en la VM por su IP (`http://203.0.113.5/`) y ves la web de uno de tus clientes. Hay varios `server` en el puerto 80 y ninguno con `default_server`. ¿Por qué ocurre?

- A) Nginx redirige las visitas por IP al primer dominio que se registró en el servidor.
- B) El navegador reutiliza el último `Host` que visitaste y lo envía junto a la IP.
- C) El NSG de Azure añade el nombre del primer cliente a la cabecera `Host`.
- D) Ningún `server_name` coincide con la IP y responde el primer `server`.

**13.** En Apache añades `aaa-cliente.conf` a `sites-enabled/`. Estaba `000-default.conf`. ¿Qué efecto tiene en las peticiones con un `Host` desconocido?

- A) Responde `aaa-cliente`: se carga primero por orden alfabético.
- B) Responde `000-default`: el `000` le da prioridad frente a cualquier otro fichero.
- C) Apache rechaza el arranque, porque hay dos `VirtualHost` que podrían ser el primero.
- D) No cambia nada: Apache solo carga `000-default` y los activados con `a2ensite`.

**14.** Quieres que los bots que entran por la IP no reciban nada: ni página ni cabeceras como `Server`. ¿Qué pones en el servidor por defecto?

- A) `return 403;`
- B) `return 444;`
- C) `return 204;`
- D) `server_tokens off;`

**15.** Añades un segundo `server { listen 80 default_server; … }` en otro fichero de `conf.d/`. ¿Qué dice `nginx -t`?

- A) Un aviso de que el segundo `default_server` se ignora, y la configuración sigue siendo válida.
- B) `[emerg] a duplicate default server for 0.0.0.0:80`, y la configuración no es válida.
- C) Nada: el último `default_server` sustituye al anterior sin avisar.
- D) Que `default_server` solo puede ir en el primer fichero que se carga.

**16.** Un `server` por defecto responde con `return 444;`. Con `curl -H "Host: otro.com" http://localhost/`, ¿qué ves?

- A) `HTTP/1.1 444` y una página de error de Nginx.
- B) `curl: (7) Failed to connect to localhost port 80`
- C) `HTTP/1.1 404 Not Found` con la página de error de Nginx.
- D) `curl: (52) Empty reply from server`

**17.** Defines `access_log /var/log/nginx/tienda.access.log;` en el `server` de la tienda. ¿Dónde ves las peticiones de esa web?

- A) En `docker logs`, que junta todos los ficheros de `/var/log/nginx/`.
- B) Solo dentro del fichero: `docker logs` recoge únicamente stdout y stderr.
- C) En `docker logs`, pero solo si lo ejecutas con `-f` para seguir el fichero.
- D) En ningún sitio, porque Nginx exige crear el fichero antes de escribir en él.

**18.** ¿Qué ventaja tiene que cada host virtual tenga su propio `access_log`?

- A) Miras solo el registro de esa web, sin la mezcla de todas las demás.
- B) Nginx responde más rápido porque cada `server` escribe en un fichero distinto.
- C) `docker logs` muestra entonces un registro ordenado por cada `server_name`.
- D) Los registros por sitio evitan que se duplique la cabecera `Host`.


## 3. `location`

**19.** Hay tres `location`: `/`, `/img/` y `~ \.png$`. ¿Cuál atiende `/img/logo.png`?

- A) `/img/`, porque es el prefijo más largo que coincide con la URL.
- B) `/`, porque es la primera `location` del fichero.
- C) `/img/` y la regex, aplicadas una detrás de otra.
- D) La regex `~ \.png$`, que gana a `/img/` sin `^~`.

**20.** Tienes `/`, `^~ /img/` y `~ \.png$`. ¿Cuál atiende `/img/logo.png`?

- A) La regex `~ \.png$`, porque las regex tienen prioridad sobre `^~`.
- B) `^~ /img/`, porque con `^~` no se evalúan las expresiones regulares.
- C) `/`, porque `^~` solo se aplica a las carpetas sin extensión.
- D) Ninguna: `^~` y `~` en el mismo fichero provocan un error de sintaxis.

**21.** Tienes `/`, `/img/`, `= /img/logo.png` y `~ \.png$`. ¿Cuál atiende `/img/logo.png`?

- A) `= /img/logo.png`: la exacta gana siempre y corta la búsqueda.
- B) `~ \.png$`, porque las regex se evalúan después de las exactas.
- C) `/img/`, porque es el prefijo más largo y tiene más peso.
- D) Las dos más específicas, `=` y la regex, en el orden del fichero.

**22.** Hay dos regex: `~ \.png$` (primera en el fichero) y `~ ^/img/` (segunda). Ambas coinciden con `/img/logo.png`. ¿Cuál se aplica?

- A) La segunda, porque su patrón empieza por `^` y es más específico.
- B) La primera en el fichero, `~ \.png$`.
- C) La que tenga el patrón más largo de las dos.
- D) Las dos, la primera y después la segunda con `add_header`.

**23.** Escribes `location /hola { … }` (sin barra final). ¿Qué URLs atiende?

- A) Solo `/hola` y las que están dentro de la carpeta `/hola/`.
- B) Solo `/hola`: un prefijo sin barra final se trata como exacta.
- C) Todas las que empiezan por `/hola`, incluida `/holanda`.
- D) Solo `/hola/…`: Nginx añade la barra final al prefijo.

**24.** Tienes `location ~ /pru { … }` (sin `^`). ¿Qué URLs atiende?

- A) Solo las que empiezan por `/pru`, como un prefijo normal.
- B) Cualquiera que contenga `/pru`, como `/a/pru` o `/otra/pruebas`.
- C) Solo `/pru`, porque `~` exige la URL completa.
- D) Ninguna: una regex de `location` debe empezar por `^`.

**25.** Con `location ~ ^/usuario/(\d+)$ { return 200 "Usuario $1\n"; }`, ¿qué ocurre al pedir `/usuario/abc`?

- A) Devuelve `Usuario abc`, porque `$1` recoge lo que hay tras `/usuario/`.
- B) No coincide con la regex, así que la atiende otra `location` o da 404.
- C) Devuelve `Usuario ` con un 200 y el número vacío.
- D) Nginx rechaza la petición con un 400, porque `abc` no es un número.

**26.** Con `location ~ \.PNG$ { … }`, ¿qué pasa con `/foto.png`?

- A) Coincide: las extensiones de fichero no distinguen mayúsculas en Nginx.
- B) Coincide, pero solo si el fichero existe en el `root`.
- C) No coincide: `~` distingue mayúsculas; `~*` no las distingue.
- D) No coincide, y `~*` tampoco la haría coincidir por la extensión.

**27.** Una página devuelve el texto con `location /sinct { return 200 "texto"; }`, pero el navegador lo descarga como fichero. ¿Por qué?

- A) Sin otro tipo, el `Content-Type` es `application/octet-stream` y se descarga.
- B) `return 200` solo envía el código de estado y el navegador no recibe cuerpo.
- C) Los navegadores descargan siempre las respuestas que no vienen de un fichero.
- D) Falta `index` en la `location`, así que Nginx responde con un binario.

**28.** Con `location /tmp { return 302 /nuevo.html; }`, ¿qué hace una petición a `/tmpfoo`?

- A) Responde con un 404, porque `/tmpfoo` no es la ruta `/tmp`.
- B) Redirige solo si existe una carpeta llamada `tmpfoo` en el `root`.
- C) También redirige: el prefijo `/tmp` coincide con `/tmpfoo`.
- D) Redirige con un 301, porque no hay barra final en la `location`.

**29.** Con `location /hola/ { }` y una carpeta `hola` en el `root`, `curl -I http://localhost/hola` devuelve un 301 que no has escrito. ¿Quién lo genera?

- A) Una regla `rewrite` heredada del bloque `http` de la imagen oficial.
- B) El `default_server`, que normaliza las URL de todas las webs.
- C) El navegador, que añade la barra antes de enviar la petición.
- D) Nginx: con una carpeta existente sin barra final, redirige a la barra.

**30.** Tienes `location /api { return 200 "a"; }` y `location /api/ { return 200 "b"; }`. ¿Qué responde `/api/usuarios`?

- A) `a`, porque es la primera que aparece en el fichero.
- B) `b`: entre dos prefijos que coinciden, se usa el más largo.
- C) `b`, porque la barra final convierte la `location` en exacta.
- D) `a` y `b`: se ejecutan las dos en orden y el cliente recibe ambas.

**31.** ¿Qué respuesta da `location = /test { return 200 "exacta"; }` ante `/test?x=1`?

- A) Un 404, porque `?x=1` hace que la URL deje de ser exacta.
- B) `exacta`, pero solo si añades `$is_args` a la `location`.
- C) `exacta`: se compara la ruta, sin la cadena de consulta.
- D) Un 301 hacia `/test`, que elimina la cadena de consulta.

**32.** Quieres que `/hola/index.html` lo sirva `location /hola/ { }`, pero una regex `~ \.html$` con `add_header` lo atiende primero. ¿Qué cambio es correcto?

- A) Cambiar `location /hola/` por `location ^~ /hola/`.
- B) Colocar la `location /hola/` antes de la regex en el fichero.
- C) Cambiar la regex por `~* \.html$`, que tiene menos prioridad.
- D) Añadir `internal;` a la regex, para que no coincida con peticiones externas.

**33.** ¿Qué `location` usarías para atender solo la URL exacta `/estado` y nada más?

- A) `location /estado/ { … }`
- B) `location ^~ /estado { … }`
- C) `location ~ /estado { … }`
- D) `location = /estado { … }`

**34.** ¿Para qué sirve `location ^~ /img/ { … }`?

- A) Para que ninguna regex «robe» las peticiones bajo `/img/`.
- B) Para que la ruta `/img/` coincida sin importar mayúsculas y minúsculas.
- C) Para que Nginx busque `/img/` también dentro de las demás `location`.
- D) Para marcar `/img/` como ruta interna, inaccesible desde el exterior.


## 4. `root`, `alias` y `try_files`

**35.** Con `location /mundo/ { root /datos; }`, ¿qué fichero busca Nginx para `GET /mundo/index.html`?

- A) `/datos/index.html`, porque `root` sustituye la parte `/mundo/`.
- B) `/mundo/datos/index.html`, porque `root` se coloca tras la ruta.
- C) `/datos/mundo/`, porque solo busca el índice de la carpeta.
- D) `/datos/mundo/index.html`, porque `root` añade la ruta de la URL.

**36.** Con `location /mundo/ { alias /datos/; }`, ¿qué fichero busca Nginx para `GET /mundo/index.html`?

- A) `/datos/mundo/index.html`, porque `alias` añade la ruta de la URL.
- B) `/datos/index.html`, porque `alias` sustituye la parte `/mundo/`.
- C) `/mundo/datos/index.html`, porque `alias` va detrás de la ruta.
- D) `/datos/mundo/`, porque `alias` solo apunta a carpetas.

**37.** Escribes `location /malo/ { alias /sitios/docs; }` y pides `/malo/index.html`: da 404. ¿Qué verás en `error.log`?

- A) `open() "/sitios/docsindex.html" failed (2: No such file or directory)`
- B) `open() "/sitios/docs/malo/index.html" failed (2: No such file or directory)`
- C) `"/sitios/docs/" is not a directory`, porque falta la barra del `alias`.
- D) `[emerg] "alias" directive requires a trailing slash`

**38.** En `/malo/` (con el `alias` sin barra final) ves un 403 y, en el log, `directory index of "/sitios/docs" is forbidden`, aunque `docs/index.html` existe. ¿Por qué?

- A) Los permisos de `docs/` impiden al usuario `nginx` leer el `index.html`.
- B) `index.html` no está en la lista de la directiva `index` de esa `location`.
- C) El `alias` no puede apuntar a una carpeta; solo admite ficheros concretos.
- D) Busca `docsindex.html`, no existe y, sin `autoindex`, da 403.

**39.** Con `location /ro/ { root /usr/share/nginx/sitios/docs; }`, el log dice `open() "…/docs/ro/index.html" failed (2: No such file or directory)`. ¿Qué cambio resuelve el problema?

- A) Añadir `index index.html;` dentro de la `location`.
- B) Dar permisos de lectura a la carpeta `docs` para el usuario `nginx`.
- C) Usar `alias /usr/share/nginx/sitios/docs/;` en lugar de `root`.
- D) Añadir una barra final al `root`: `/usr/share/nginx/sitios/docs/`.

**40.** ¿Qué hace `try_files $uri $uri/ =404;` en una `location`?

- A) Redirige con un 301 a `$uri/` y, si no existe, a `/404.html`.
- B) Sirve el fichero o la carpeta y, si no existe ninguno, el `error_page` 404 sin cambiar el código.
- C) Prueba el fichero y la carpeta a la vez y sirve el más grande.
- D) Prueba el fichero, luego la carpeta y, si no existe ninguno, responde 404.

**41.** Con `location /tfs/ { try_files $uri /index.html; }`, pides `/tfs/nada`. ¿Qué respuesta recibes?

- A) Un 404, porque `/tfs/nada` no existe y `try_files` no modifica el código.
- B) Un 302 que lleva el navegador a `/index.html`.
- C) Un 200 con el contenido de `/index.html`, sin cambiar la URL.
- D) Un 200 con el contenido de `/tfs/index.html`.

**42.** `nginx -t` dice «test is successful» pero la web da 404 en todas las rutas. En el log aparece `open() "/usr/share/nginx/sitios/pincipal/index.html" failed`. ¿Cuál es la causa?

- A) Errata en el `root`: `nginx -t` no comprueba que existan las rutas.
- B) La sintaxis es correcta, pero falta recargar: `nginx -t` no aplica los cambios.
- C) El `server_name` no coincide con el `Host` de la petición.
- D) Falta `index index.html;`, que obliga a Nginx a buscar el nombre del fichero.

**43.** Pones `root /usr/share/nginx/sitios/principal;` en el `server` y no repites `root` en cada `location`. ¿Qué ocurre con las `location` que no lo definen?

- A) Responden con un 404 hasta que definan su propio `root`.
- B) Usan el `root` de la imagen oficial, `/usr/share/nginx/html`.
- C) Heredan el `root` del `server`.
- D) Nginx rechaza la configuración al ejecutar `nginx -t`.


## 5. Redirecciones

**44.** Has migrado `/blog` a `/articulos` de forma definitiva y quieres que los buscadores trasladen la posición a la URL nueva. ¿Qué código usas?

- A) 302, porque indica que el recurso está ahora en otra URL.
- B) 301, porque indica que el cambio es permanente.
- C) 303, porque obliga al cliente a pedir la nueva URL con `GET`.
- D) 307, porque mantiene el método de la petición original.

**45.** Corriges una redirección 301 equivocada en Nginx, pero tu navegador sigue yendo al destino antiguo. ¿Cómo compruebas qué responde ahora el servidor?

- A) Con `curl -I`, que no usa la caché del navegador (o con una ventana privada).
- B) Con `nginx -t`, que muestra las redirecciones activas.
- C) Con `docker logs`, que muestra a dónde manda Nginx a cada cliente.
- D) Esperando a que el navegador renueve la redirección, que caduca a los 90 días.

**46.** ¿En qué se diferencian 302 y 307?

- A) El 307 es permanente y el 302 temporal, sin otras diferencias.
- B) El 307 solo funciona dentro del mismo dominio de la web.
- C) El 307 mantiene el método; el 302 puede cambiar `POST` a `GET`.
- D) El 307 obliga al navegador a guardar la respuesta en caché.

**47.** Una API recibe `POST` en una URL que has movido para siempre. Los clientes deben repetir el `POST` en la nueva dirección. ¿Qué código usas?

- A) 301, porque es permanente y los navegadores mantienen siempre el método.
- B) 308, porque es permanente y mantiene el método.
- C) 302, porque mantiene el método y es la redirección más extendida.
- D) 303, porque pide al cliente repetir la petición en la nueva URL.

**48.** ¿Qué hace este `server`?

```nginx
server {
    listen 80;
    server_name www.localhost;
    return 301 http://localhost$request_uri;
}
```

- A) Redirige a `http://localhost/` y pierde la ruta pedida.
- B) Sirve la misma web en `www.localhost` y en `localhost`, sin redirigir.
- C) Redirige `localhost` a `www.localhost` con un 301.
- D) Redirige `www.localhost` a `localhost` con 301, conservando la ruta.

**49.** Dentro de `location /vieja/` escribes `rewrite ^/vieja/(.*)$ /nuevo/$1 last;`. Se pide `/vieja/z`. ¿Qué valen `$uri` y `$request_uri` después?

- A) `$uri` vale `/vieja/z` y `$request_uri` pasa a `/nuevo/z`.
- B) Los dos valen `/nuevo/z`, porque `rewrite` cambia todas las variables.
- C) Los dos conservan `/vieja/z`, porque `last` no modifica la URL.
- D) `$uri` vale `/nuevo/z` y `$request_uri` conserva `/vieja/z`.

**50.** ¿Qué diferencia hay, para el cliente, entre `rewrite ^/vieja/(.*)$ /nuevo/$1 last;` y `rewrite ^/vieja/(.*)$ /nuevo/$1 redirect;`?

- A) Con `last` recibe un 301 con `Location`; con `redirect`, un 302.
- B) Con `last` el cambio es interno; `redirect` es idéntico, pero con otro nombre.
- C) Con `last` el cambio es interno (200); con `redirect`, 302 con `Location`.
- D) Con `last` recibe un 302 y con `redirect` un 301 permanente.

**51.** Escribes `location /ciclo { rewrite ^ /ciclo; }`. Al pedir `/ciclo`, ¿qué ocurre?

- A) El cliente recibe un 301 en bucle hasta que `curl -L` se rinde a las 50.
- B) Nginx responde 500: el log dice `rewrite or internal redirection cycle`.
- C) Nginx sirve `/ciclo` una vez y la reescritura se ignora.
- D) `nginx -t` rechaza la configuración por una regla recursiva.

**52.** Con `curl -sIL http://localhost/a` ves `301 Location: /b`, luego `301 Location: /a`, y se repite. ¿Qué diagnóstico es correcto?

- A) Hay un bucle: `/a` redirige a `/b` y `/b` vuelve a `/a`.
- B) La caché del navegador guarda la redirección anterior.
- C) El `default_server` intercepta las peticiones y las devuelve al cliente.
- D) Nginx añade una barra final a cada URL y la repite en cada petición.

**53.** ¿Qué redirección envía todo el tráfico HTTP a HTTPS conservando el nombre y la ruta?

- A) `return 301 https://localhost/;`
- B) `rewrite ^ https://$host redirect;`
- C) `return 301 https://$host$request_uri;`
- D) `return 200 https://$host$request_uri;`

**54.** Quieres ver solo la URL a la que redirige una página, sin seguirla ni leer las cabeceras. ¿Qué comando usas?

- A) `curl -sL -o /dev/null -w '%{url_effective}\n' http://localhost/viejo`
- B) `curl -I http://localhost/viejo | grep Host`
- C) `curl -s http://localhost/viejo | grep redirect`
- D) `curl -s -o /dev/null -w '%{redirect_url}\n' http://localhost/viejo`

**55.** Publicas `-p 8080:80` y pruebas `curl -L http://localhost:8080/viejo`. Falla con `Failed to connect to localhost port 80`. ¿Por qué?

- A) `curl -L` no admite redirecciones cuando la URL original lleva un puerto.
- B) Nginx devuelve `Location` con el puerto 8080, que Docker no ha publicado.
- C) Nginx manda `Location: http://localhost/…` sin el 8080, porque usa su 80.
- D) El `server_name` no incluye el puerto 8080 y Nginx rechaza la petición.

**56.** ¿Qué efecto tiene `absolute_redirect off;` en un `server`?

- A) Nginx deja de generar redirecciones 301 automáticas para las carpetas.
- B) `Location` lleva solo la ruta (`/nuevo.html`), sin esquema, host ni puerto.
- C) Las redirecciones pasan a ser internas y el cliente no las ve.
- D) El `Location` se construye con el `server_name` en lugar del `Host`.

**57.** En Apache tienes `Redirect 301 /viejo /nuevo`. ¿Qué pasa con una petición a `/viejo/a/b.html`?

- A) Redirige a `/nuevo`: `Redirect` descarta la ruta restante.
- B) Redirige a `/nuevo/a/b.html`: `Redirect` conserva el resto de la ruta.
- C) Da un 404, porque `Redirect` solo coincide con la URL exacta `/viejo`.
- D) Redirige a `/nuevo/viejo/a/b.html`.

**58.** Con `location = /viejo { return 301 /nuevo; }`, ¿qué ocurre al pedir `/viejo/otra`?

- A) Redirige a `/nuevo`, porque `=` también incluye las rutas de dentro.
- B) Redirige a `/nuevo/otra`, porque `return` conserva el resto de la ruta.
- C) Nginx rechaza la petición con un 400 por tener una barra de más.
- D) No coincide con la exacta: la atiende otra `location` o da 404.

**59.** Un formulario envía un `POST` y, al terminar, quieres llevar al usuario a una página de confirmación que se pida con `GET`, para que al recargar no se repita el envío. ¿Qué código usas?

- A) 303, que indica al cliente que pida la nueva URL con `GET`.
- B) 301, porque es permanente y mantiene siempre el método `POST`.
- C) 307, porque mantiene el método y evita repetir el envío.
- D) 308, porque es permanente y obliga a repetir el `POST`.

**60.** Vas a poner la web en mantenimiento unas horas y redirigirás todas las peticiones a `/aviso.html`. ¿Qué es lo más prudente?

- A) Usar un 302, que no queda guardado de forma permanente en las cachés.
- B) Usar un 301, que las cachés actualizan rápido al volver a la normalidad.
- C) Usar un 308, para que no se cambie el método en las peticiones `POST`.
- D) Usar `return 444`, que cierra la conexión a los clientes durante el aviso.


## 6. Errores propios, variables y Apache

**61.** Defines `error_page 404 /errores/404.html;` con una página propia. ¿Qué código recibe el cliente ante una URL inexistente?

- A) Un 200, porque la página propia existe en el servidor.
- B) Un 302, que redirige al cliente a `/errores/404.html`.
- C) Un 500, porque la página de error es una petición interna.
- D) Un 404: `error_page` cambia el contenido, no el código.

**62.** ¿Qué efecto tiene `error_page 404 =200 /w404;`?

- A) Sirve `/w404` solo si el cliente repite la petición con un 200.
- B) Sirve `/w404` con 404, y `=200` solo lo escribe en el log.
- C) Redirige al cliente a `/w404` con un 200 en lugar de un 302.
- D) Sirve `/w404` y cambia el código de respuesta a 200.

**63.** Con `error_page 404 /errores/404.html;`, `location /errores/ { alias …; internal; }` y una regex `~ \.html$ { … }`, sale la 404 de Nginx y no la tuya. ¿Por qué?

- A) La regex `\.html$` atiende la petición interna; se arregla con `^~ /errores/`.
- B) `internal;` impide que Nginx sirva esa página como respuesta a un error 404.
- C) `error_page` no admite ficheros `.html` dentro de una carpeta con `alias`.
- D) La regex se aplica solo a las peticiones externas, no a las internas.

**64.** ¿Qué hace `internal;` en una `location`?

- A) Solo sirve como destino interno de Nginx; pedirla directamente da 404.
- B) Solo permite peticiones que llegan desde la red interna del servidor.
- C) Oculta esa `location` del listado que muestra `nginx -T`.
- D) Obliga a que las peticiones a esa ruta lleguen cifradas con TLS.

**65.** El `server_name` de un `server` es `a.localhost b.localhost;` y llega `Host: b.localhost`. Dentro de una `location`, ¿qué valen `$host` y `$server_name`?

- A) Los dos valen `b.localhost`, el nombre con el que se ha pedido.
- B) `$host` es `b.localhost` y `$server_name` es `a.localhost`.
- C) `$host` vale `a.localhost` y `$server_name` vale `b.localhost`.
- D) Los dos valen `a.localhost`, el primer nombre del `server`.

**66.** En `return 200 "…$request_uri…"`, se pide `/info?x=1`. ¿Qué contiene `$request_uri` y qué contiene `$uri`?

- A) `$request_uri` contiene `/info` y `$uri` contiene `/info?x=1`.
- B) Los dos contienen `/info?x=1`.
- C) `$request_uri` contiene `/info?x=1` y `$uri` contiene `/info`.
- D) Los dos contienen `/info`, y los argumentos se guardan en `$args`.

**67.** Migras un sitio de Apache a Nginx. En un `.htaccess` había `Redirect 301 /viejo /nuevo`. ¿Dónde lo pones en Nginx?

- A) En un fichero `.htaccess` en la misma carpeta, que Nginx leerá si activas `AllowOverride`.
- B) En un fichero `.nginx` dentro de la carpeta, que Nginx busca en cada petición.
- C) En el `server`, con una `location`: `location = /viejo { return 301 /nuevo; }`.
- D) En `nginx.conf`, dentro de `events`, que controla las conexiones.

**68.** Un `.htaccess` con reglas de redirección no hace nada en un servidor Apache. ¿Qué es lo más probable?

- A) `AllowOverride` está en `None`: Apache ignora ese fichero.
- B) Falta `RewriteEngine Off`, que activa la lectura del `.htaccess`.
- C) El módulo `mod_alias` sustituye siempre las reglas del `.htaccess`.
- D) Apache solo lee `.htaccess` en la carpeta raíz, no en subcarpetas.

**69.** En Apache, un `RewriteRule` escrito en un `.htaccess` y el mismo en un `<VirtualHost>`: ¿qué diferencia hay en el patrón?

- A) En `.htaccess` el patrón no lleva barra inicial; en el `VirtualHost`, sí.
- B) Ninguna: el patrón es el mismo en los dos casos.
- C) En el `VirtualHost` el patrón no lleva barra inicial; en el `.htaccess` sí.
- D) En el `.htaccess` solo se admiten patrones exactos, sin expresiones regulares.

**70.** Con `Alias /docs /var/docs` en Apache, `/docs/` da un 403. La carpeta existe y tiene permisos. ¿Qué falta?

- A) Un bloque `<Directory /var/docs>` con `Require all granted`.
- B) `ServerAlias /docs`, que declara la ruta como alias del `VirtualHost`.
- C) `AllowOverride All`, que activa los alias de rutas.
- D) `Options +Indexes` en el `VirtualHost`, que habilita las carpetas.

**71.** Un `server_name a.com b.com;` en Nginx, ¿cómo se escribiría en Apache?

- A) `ServerName a.com b.com` en una sola línea del `<VirtualHost>`.
- B) `ServerAlias a.com b.com` y se omite el `ServerName` principal.
- C) `ServerName a.com` y `ServerAlias b.com` en el `<VirtualHost>`.
- D) `<VirtualHost a.com b.com>` y no hace falta más directivas.


## 7. Casos completos

**72.** Tienes `server_name localhost;` (con `location /hola/ { }`) y `server_name tienda.localhost;` (solo `root`). ¿Qué responde `curl -i http://tienda.localhost/hola/`?

- A) Un 200 con la web de `/hola/`, porque `location /hola/` es de todo el servidor.
- B) Un 301 a `http://localhost/hola/`, porque Nginx busca el `server` que la define.
- C) Un 404: `tienda.localhost` no tiene `/hola/`.
- D) Un 403, porque la tienda no tiene la `location /hola/` y no hay índice.

**73.** En un `server` has escrito `return 301 /nuevo.html` (sin `;`) y ejecutas `nginx -s reload` sin `nginx -t`. ¿Qué ocurre?

- A) El `reload` se aplica a medias: solo se cargan los `server` que están antes del error.
- B) Nginx se detiene y deja el servicio caído hasta que se corrige el fichero.
- C) Falla con un `[emerg]` y el servidor sigue funcionando con la configuración anterior.
- D) Nginx ignora la línea y recarga el resto de la configuración.

**74.** Rompes un fichero de `conf.d/` y haces `docker compose restart web`. ¿Qué ocurre?

- A) No arranca: Nginx falla al leer la configuración y queda caído.
- B) El contenedor arranca con la última configuración que funcionó.
- C) El contenedor arranca y Nginx ignora el fichero roto.
- D) El contenedor arranca, pero solo sirve el `default_server`.

**75.** Con `location /tmp { return 302 /nuevo.html; }` y `/nuevo.html` existente, ¿qué devuelve `curl -sL http://localhost/tmp`?

- A) Un 302 sin cuerpo, porque curl no sigue las redirecciones sin `-i`.
- B) Un 404, porque `-L` no admite redirecciones a rutas relativas.
- C) El contenido de `/tmp`, porque `-L` revierte las redirecciones.
- D) El contenido de `/nuevo.html`, tras seguir el 302.

**76.** En una VM, el NSG solo permite 22, 80 y 443. Publicas `-p 8080:80` y `curl http://tunombre.me:8080/` desde fuera da *timeout*. ¿Por qué?

- A) `ufw` bloquea el puerto 8080 de la VM aunque Docker lo publique.
- B) El NSG bloquea el 8080: todas las capas deben abrir el puerto.
- C) Nginx escucha en el 80 y no atiende peticiones recibidas por el 8080.
- D) El `server_name` no incluye el puerto, y Nginx descarta la petición.

**77.** Quieres que `http://localhost/viejo` redirija con 301 a `/nuevo` **y** que `/viejo/foto.png` no se redirija. ¿Qué configuración sirve?

- A) `location /viejo { return 301 /nuevo; }`, porque el prefijo excluye las imágenes.
- B) `location = /viejo { return 301 /nuevo; }`, porque solo coincide con esa URL.
- C) `location ^~ /viejo { return 301 /nuevo; }`, porque `^~` solo coincide con la ruta exacta.
- D) `location ~ /viejo { return 301 /nuevo; }`, porque `~` solo coincide con el final.

**78.** Quieres servir `/mundo/` desde otra carpeta y que `/mundo/index.html` funcione. ¿Cuál de estas es correcta?

- A) `location /mundo/ { alias /sitios/docs; }`
- B) `location /mundo { alias /sitios/docs/; }`
- C) `location /mundo/ { root /sitios/docs/; }`
- D) `location /mundo/ { alias /sitios/docs/; }`

**79.** Un script `bash` recorre una lista de URL con `curl -sI` y solo quiere ver el código de estado de cada una. ¿Qué argumentos son más adecuados?

- A) `curl -sL URL | grep -m1 HTTP | cut -d' ' -f2`
- B) `curl -s URL | grep -c 200 | cut -c1-3`
- C) `curl -s -w '%{url_effective}\n' -o /dev/null URL`
- D) `curl -s -o /dev/null -w '%{http_code}' URL`

**80.** Tu `compose.yaml` monta `./conf.d` y `./sitios` con `:ro`. Cambias un fichero de `sitios/` y el cambio se ve al instante. ¿Por qué no hace falta recargar Nginx?

- A) Porque `:ro` hace que Nginx vuelva a leer los ficheros cada vez que cambian.
- B) Porque Docker sincroniza el volumen y avisa a Nginx de forma automática.
- C) Los ficheros se leen en cada petición; solo la configuración exige `reload`.
- D) Porque `sitios/` se monta como `tmpfs` y siempre está en memoria.


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
