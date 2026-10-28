---
layout: default
title: "Arquitecturas Web — Bloque 2.1: Fundamentos web (Test)"
permalink: /web/semana-1/test/
---

# Bloque 2.1 — Test de fundamentos web: redes, HTTP y arquitecturas

**Módulo:** Despliegue de Aplicaciones Web (0614) · 2º DAW · UD2: Arquitecturas web

## Instrucciones

- 80 preguntas con 4 opciones y **una sola respuesta correcta**.
- Puntuación: acierto **+1** · error **−1/3** · en blanco **0**.
- Nota sobre 10 = (aciertos − errores / 3) × 10 / 80. Si el resultado es negativo, la nota es 0.
- Con esta penalización, responder al azar da de media un 0: si no sabes la respuesta, déjala en blanco.
- Tiempo orientativo: 70 minutos.


## 1. Redes y modelos de comunicación

**1.** Según el bloque, ¿qué ocurrió el 1 de enero de 1983?

- A) Se estableció la primera conexión de ARPANET.
- B) ARPANET adoptó TCP/IP como protocolo oficial.
- C) Se publicó la primera versión estable de HTTP.
- D) La ISO publicó el modelo de referencia OSI.

**2.** ¿Qué afirmación distingue correctamente un **modelo** de una **arquitectura**?

- A) El modelo es el marco teórico; la arquitectura, las capas y protocolos concretos que lo implementan.
- B) La arquitectura es el marco teórico y el modelo es su implementación concreta con protocolos.
- C) El modelo define las reglas de un servicio concreto, como HTTP o FTP, y la arquitectura define los medios físicos y el cableado de la red.
- D) Modelo y arquitectura son sinónimos; solo el protocolo es un concepto distinto.

**3.** ¿En qué capa del modelo OSI se encapsulan los datos en tramas y se detectan y corrigen errores al transmitirlas entre equipos contiguos?

- A) Física (capa 1).
- B) Red (capa 3).
- C) Transporte (capa 4).
- D) Enlace de datos (capa 2).

**4.** ¿Qué capa OSI «establece, mantiene y controla el diálogo entre las aplicaciones origen y destino»?

- A) Presentación (capa 6).
- B) Aplicación (capa 7).
- C) Transporte (capa 4).
- D) Sesión (capa 5).

**5.** ¿Cuál es el orden correcto de las unidades de datos de las capas OSI 4, 3 y 2, en ese orden?

- A) Paquete → segmento → trama.
- B) Segmento → paquete → trama.
- C) Segmento → trama → paquete.
- D) Trama → paquete → segmento.

**6.** En el modelo TCP/IP, ¿a qué capa o capas de OSI corresponde la capa **Internet**?

- A) Solo a la capa 3 (Red).
- B) A las capas 3 y 4.
- C) A las capas 2 y 3.
- D) A las capas 5, 6 y 7.

**7.** ¿Cuál de estas correspondencias entre OSI y TCP/IP es **INCORRECTA**?

- A) Transporte de OSI corresponde a Transporte de TCP/IP.
- B) Aplicación, Presentación y Sesión de OSI se agrupan en la capa Aplicación de TCP/IP.
- C) Transporte y Red de OSI se agrupan en la capa Internet de TCP/IP.
- D) Enlace de datos y Física de OSI se agrupan en la capa Acceso a la red de TCP/IP.

**8.** ¿Qué pareja protocolo/puerto típico es **INCORRECTA** según la tabla de protocolos?

- A) IMAP → 143.
- B) POP3 → 110.
- C) DNS → 53.
- D) FTPS → 22.

**9.** ¿Qué afirmación sobre DHCP es correcta?

- A) Asigna automáticamente la configuración IP a un equipo, usando los puertos 67/68 (UDP).
- B) Traduce nombres de dominio a direcciones IP usando el puerto 53.
- C) Asocia cada dirección IP con su dirección MAC, en la capa de acceso a la red, y viceversa.
- D) Traduce las direcciones IP privadas de la red local a direcciones IP públicas, en la capa Internet.

**10.** Según la tabla de protocolos, ARP y RARP…

- A) pertenecen a la capa de acceso a la red y asocian direcciones IP con direcciones MAC.
- B) pertenecen a la capa Internet y traducen direcciones IP privadas a públicas.
- C) pertenecen a la capa de transporte y numeran los segmentos para garantizar que llegan en orden.
- D) pertenecen a la capa de aplicación y asignan direcciones IP automáticamente.

**11.** En una misma máquina se ejecutan Nginx (puertos 80 y 443) y MySQL (puerto 3306). ¿Qué es cierto?

- A) Se distinguen por la dirección MAC que el sistema asigna a cada programa.
- B) Comparten el puerto y se distinguen por el protocolo de transporte que usa cada uno.
- C) Comparten IP y se distinguen por el puerto, que identifica el programa que escucha.
- D) Necesitan direcciones IP distintas, porque cada dirección IP solo puede ofrecer un único servicio.


## 2. Cliente-servidor, URL y DNS

**12.** En `https://www.ejemplo.com:443/productos/42?color=rojo&talla=m#resenas`, ¿qué parte **nunca** llega al servidor?

- A) `#resenas`
- B) `:443`
- C) `?color=rojo&talla=m`
- D) `/productos/42`

**13.** En la query string `?color=rojo&talla=m`, ¿qué carácter separa un parámetro del siguiente?

- A) `&`
- B) `=`
- C) `#`
- D) `?`

**14.** Un usuario escribe `http://www.miweb.com/documento.html`. ¿A qué puerto se conectará el navegador?

- A) Al 80, porque es el puerto por defecto de HTTP y no hace falta escribirlo.
- B) Al 8080, porque es el puerto alternativo cuando no se indica ninguno.
- C) Al 443, porque es el puerto web estándar para cualquier esquema.
- D) A ninguno: sin puerto explícito en la URL no se puede abrir la conexión TCP.

**15.** Cuando un nombre no está en ninguna caché, ¿qué secuencia de resolución DNS describe el bloque?

- A) El sistema pregunta primero al resolver y solo consulta el fichero `hosts` si el resolver no responde a tiempo.
- B) El resolver consulta primero a ejemplo.com, después a .com y por último a la raíz.
- C) El sistema mira sus cachés y el fichero `hosts`; si no está, un resolver recorre raíz → .com → ejemplo.com.
- D) El navegador pregunta directamente a un servidor raíz, que conoce todas las IP y devuelve la de www.ejemplo.com.

**16.** ¿Por qué, al cambiar la IP de un dominio, el cambio «tarda en propagarse»?

- A) Porque las conexiones persistentes de HTTP/1.1 mantienen la IP antigua.
- B) Porque el fichero `hosts` de cada equipo debe actualizarse a mano.
- C) Porque los servidores raíz solo sincronizan sus datos con los demás servidores una vez al día.
- D) Porque las respuestas DNS se guardan en caché durante un tiempo (TTL).

**17.** ¿Cuál de estas herramientas **NO** aparece en el bloque como herramienta de consulta DNS?

- A) `nslookup`
- B) `dig`
- C) `curl`
- D) `host`

**18.** Según el bloque, ¿qué afirmación sobre el modelo cliente-servidor es correcta?

- A) El servidor inicia la comunicación y envía la página en cuanto detecta que un cliente se ha conectado a la red.
- B) El cliente siempre inicia; el servidor es un programa que escucha en un puerto.
- C) Cliente y servidor se turnan para iniciar la comunicación según quién tenga datos nuevos.
- D) El servidor tiene que ser necesariamente una máquina física dedicada.


## 3. El protocolo HTTP

**19.** ¿Quién creó HTTP y dónde?

- A) La ISO, en 1984, junto con el modelo OSI.
- B) Tim Berners-Lee, en ARPANET, en 1983, al adoptar TCP/IP.
- C) Tim Berners-Lee, en el CERN, entre 1989 y 1991.
- D) El equipo de ARPANET, en 1969, para su primera conexión.

**20.** ¿Qué afirmación sobre HTTPS es correcta?

- A) Funciona sobre UDP en el puerto 443 para ser más rápido que HTTP.
- B) Cifra solo el cuerpo de las peticiones POST; las cabeceras viajan en claro.
- C) Es HTTP cifrado con TLS: el mismo protocolo, que viaja protegido por el puerto 443.
- D) Es un protocolo distinto de HTTP, con sus propios métodos, cabeceras y códigos de estado cifrados.

**21.** Una página HTML referencia 2 hojas CSS, 3 imágenes y 1 fichero JS. Sin caché, ¿cuántas peticiones HTTP hace como mínimo el navegador para cargarla entera?

- A) 6
- B) 7
- C) 2
- D) 1

**22.** ¿Qué versión de HTTP hizo obligatoria la cabecera `Host`?

- A) HTTP/2
- B) HTTP/1.1
- C) HTTP/0.9
- D) HTTP/1.0

**23.** ¿Qué versión de HTTP **no** funciona sobre TCP?

- A) HTTP/1.0
- B) HTTP/3
- C) HTTP/2
- D) HTTP/1.1

**24.** ¿Cuál fue la novedad principal de HTTP/2?

- A) Funcionar sobre QUIC en lugar de TCP.
- B) Conexiones persistentes y cabecera `Host` obligatoria para todos los dominios.
- C) Introducir los métodos POST y HEAD, los códigos de estado y los tipos MIME.
- D) Formato binario y multiplexación de peticiones.

**25.** Según el bloque, ¿qué cambia entre HTTP/1.1, HTTP/2 y HTTP/3?

- A) Cómo viajan los mensajes; métodos, códigos y cabeceras se mantienen.
- B) Los códigos de estado, que en HTTP/2 pasan a enviarse en binario con una numeración nueva.
- C) Los métodos disponibles, que se amplían en cada versión.
- D) Las cabeceras obligatorias de cada petición.

**26.** ¿Qué afirmación sobre la conexión TCP en HTTP es correcta?

- A) En HTTP/1.1 la conexión solo se mantiene abierta si se usa HTTPS.
- B) Tanto HTTP/1.0 como HTTP/1.1 cierran la conexión tras cada petición; solo HTTP/2 la reutiliza.
- C) En HTTP/1.0 se usa una conexión por petición; desde HTTP/1.1 las conexiones son persistentes por defecto.
- D) En HTTP/1.0 las conexiones eran persistentes, y HTTP/1.1 las cierra tras cada petición para ahorrar recursos.

**27.** ¿Qué método es seguro e idempotente, no lleva cuerpo y hace que el servidor devuelva solo las cabeceras del recurso, sin su contenido?

- A) GET
- B) HEAD
- C) DELETE
- D) OPTIONS

**28.** Según la tabla de métodos, ¿cuál de estos **NO** es idempotente?

- A) GET
- B) POST
- C) DELETE
- D) PUT

**29.** ¿Qué combinación de características corresponde a PUT?

- A) No es seguro, sí es idempotente, lleva cuerpo y reemplaza el recurso completo.
- B) No es seguro, es idempotente, no lleva cuerpo y elimina el recurso.
- C) No es seguro, no es idempotente, lleva cuerpo y modifica solo una parte concreta del recurso.
- D) Es seguro e idempotente, no lleva cuerpo y devuelve los métodos admitidos.

**30.** Un cliente envía dos veces seguidas el mismo `POST /pedidos` (crear pedido) y, aparte, dos veces `DELETE /pedidos/42`. ¿Qué ocurre?

- A) Ambos casos duplican su efecto: dos pedidos creados y dos pedidos borrados.
- B) Se crea un solo pedido, y el segundo DELETE provoca un error que deshace el borrado.
- C) Ambos casos dejan el servidor igual que con una sola petición, porque HTTP descarta los duplicados.
- D) Se crean dos pedidos; el pedido 42 queda borrado igual que si se hubiera enviado una sola vez.

**31.** ¿Qué método usan los navegadores en las comprobaciones previas de CORS?

- A) OPTIONS
- B) CONNECT
- C) TRACE
- D) HEAD

**32.** Sobre GET y POST, ¿qué afirmación es **FALSA**?

- A) POST cifra el cuerpo, así que sirve para enviar contraseñas aunque no haya HTTPS.
- B) POST se usa típicamente para enviar formularios o subir ficheros.
- C) En GET los datos van en la query string y quedan visibles en el historial y en los logs.
- D) La longitud de los datos en GET está limitada por navegadores y servidores.

**33.** ¿Qué es WebDAV?

- A) La versión cifrada de FTP, que funciona en el puerto 990 y sustituye a SFTP en servidores web.
- B) Un protocolo de transporte alternativo a TCP para ficheros grandes.
- C) Una extensión de HTTP para gestionar ficheros y carpetas remotos (PROPFIND, MKCOL…).
- D) La versión de HTTP que añadió los métodos PUT y DELETE para gestionar ficheros en el servidor.

**34.** En un mensaje de petición HTTP, ¿qué marca el final de las cabeceras?

- A) Una línea en blanco (CRLF).
- B) La cabecera `Content-Length`.
- C) Nada: el servidor sabe cuántas cabeceras hay por la versión del protocolo.
- D) Una cabecera especial `End-Headers`.

**35.** ¿Cuál de estas es una línea de **petición** bien formada?

- A) `HTTP/1.1 200 OK`
- B) `HTTP/1.1 GET /index.html`
- C) `GET /index.html HTTP/1.1`
- D) `GET HTTP/1.1 /index.html`

**36.** En el POST de ejemplo, con cuerpo `nombre=Ana&edad=20`, la cabecera `Content-Length` vale 18. ¿Qué indica?

- A) La longitud total del mensaje, incluidas las cabeceras.
- B) El número de cabeceras del mensaje.
- C) El tamaño del cuerpo en bytes.
- D) El número de caracteres de la línea de petición.

**37.** ¿Qué `Content-Type` corresponde a un formulario HTML **sin ficheros adjuntos** enviado por POST?

- A) `text/html`
- B) `application/json`
- C) `multipart/form-data`
- D) `application/x-www-form-urlencoded`

**38.** ¿Cuál es el tipo MIME correcto para datos JSON?

- A) `text/json`
- B) `application/javascript`
- C) `text/plain+json`
- D) `application/json`

**39.** Una API recibe un encargo que procesará en segundo plano y responde inmediatamente, antes de haberlo procesado. ¿Qué código encaja?

- A) 201 Created
- B) 202 Accepted
- C) 204 No Content
- D) 100 Continue

**40.** Un cliente reanuda una descarga pidiendo solo una parte del fichero. ¿Qué es correcto?

- A) El servidor responde 206; el cliente pide la parte con `Range` y la respuesta trae `Content-Range`.
- B) El servidor responde 203 Non-Authoritative Information, porque el contenido está incompleto.
- C) El servidor responde 200 OK; el cliente indica la parte con `Content-Length`.
- D) El servidor responde 206; el cliente envía `Content-Range` y la respuesta incluye la cabecera `Range`.

**41.** ¿Qué diferencia hay entre 301 y 302?

- A) 301 es definitivo (los buscadores actualizan su índice) y 302 temporal; ambos usan `Location`.
- B) 301 indica el destino en la cabecera `Location`; 302 lo indica en el cuerpo HTML de la respuesta.
- C) 302 obliga a repetir la petición con el mismo método y 301 permite cambiarlo a GET.
- D) 301 indica un traslado temporal y 302, uno definitivo.

**42.** Tras procesar un formulario enviado por POST, el servidor quiere que el navegador cargue `/gracias` **con GET**, para que recargar la página no reenvíe el formulario. ¿Qué código usa?

- A) 304 Not Modified
- B) 303 See Other
- C) 308 Permanent Redirect
- D) 307 Temporary Redirect

**43.** ¿Qué diferencia a 308 Permanent Redirect de 301 Moved Permanently?

- A) Indica un traslado temporal, mientras que 301 es definitivo.
- B) Solo existe en HTTP/2 y HTTP/3.
- C) No utiliza la cabecera `Location`, sino el cuerpo.
- D) Obliga a repetir la petición con el mismo método.

**44.** El navegador envía `If-None-Match` con la versión que tiene en caché, y el recurso no ha cambiado. ¿Qué responde el servidor?

- A) 302 Found, redirigiendo a la caché del navegador.
- B) 204 No Content, para indicar que no hay nada nuevo.
- C) 304 Not Modified, sin cuerpo.
- D) 200 OK con el cuerpo vacío y `Content-Length: 0`.

**45.** Un usuario que ha iniciado sesión correctamente intenta entrar en el panel de administración, pero no tiene permisos. ¿Qué código corresponde?

- A) 405 Method Not Allowed
- B) 403 Forbidden
- C) 404 Not Found
- D) 401 Unauthorized

**46.** ¿Qué cabecera debe acompañar obligatoriamente a una respuesta 401?

- A) `Authorization`
- B) `Location`
- C) `Set-Cookie`
- D) `WWW-Authenticate`

**47.** Se envía `DELETE` a una página estática que existe, pero que no admite ese método. ¿Qué código corresponde?

- A) 501 Not Implemented
- B) 404 Not Found
- C) 403 Forbidden
- D) 405 Method Not Allowed

**48.** Nginx está delante de una aplicación. La aplicación tarda demasiado en contestar y Nginx deja de esperar. ¿Qué código recibe el cliente?

- A) 504 Gateway Timeout
- B) 503 Service Unavailable
- C) 502 Bad Gateway
- D) 500 Internal Server Error

**49.** Sobre los códigos 5xx, ¿qué afirmación es **FALSA**?

- A) 501 indica que el servidor no soporta la funcionalidad necesaria para atender la petición.
- B) 503 indica que el servidor recibió una respuesta no válida del servidor al que reenviaba.
- C) 500 indica un fallo interno del servidor que no es culpa del cliente.
- D) 504 indica que la pasarela o proxy no recibió respuesta a tiempo del servidor de detrás.

**50.** Según la clasificación clásica de cabeceras del bloque, ¿cuál es una cabecera **general**?

- A) `Server`
- B) `Host`
- C) `Location`
- D) `Cache-Control`

**51.** ¿Qué afirmación sobre la cabecera `Host` es correcta?

- A) Indica la dirección IP del cliente, para que el servidor sepa a qué máquina debe responder.
- B) Es opcional en HTTP/1.1 y obligatoria solo desde HTTP/2.
- C) Es obligatoria en HTTP/1.1 y permite servir varios dominios desde una sola IP.
- D) Indica el puerto local que ha abierto el navegador.

**52.** ¿Qué afirmación sobre `Accept-Encoding` y `Content-Encoding` es correcta?

- A) Con `Content-Encoding` el cliente indica las compresiones que entiende; con `Accept-Encoding` el servidor indica la aplicada.
- B) `Content-Encoding` indica el juego de caracteres del cuerpo, por ejemplo UTF-8.
- C) Ambas son cabeceras de petición e indican el juego de caracteres del cliente.
- D) Con `Accept-Encoding` el cliente dice qué compresiones entiende; `Content-Encoding` indica la aplicada al cuerpo.

**53.** ¿Con qué cabeceras hace el cliente una petición **condicional** («dámelo solo si ha cambiado»)?

- A) `Last-Modified` y `ETag`.
- B) `Accept` y `Accept-Encoding`.
- C) `Cache-Control` y `Connection`.
- D) `If-Modified-Since` e `If-None-Match`.


## 4. Estado y sesiones

**54.** HTTP no tiene estado. Según el bloque, ¿cómo «recuerda» una tienda online lo que hay en tu carrito?

- A) El servidor guarda el carrito asociado a un ID de sesión que el navegador reenvía en una cookie.
- B) HTTP/1.1 mantiene la conexión persistente y el servidor asocia el carrito a esa conexión TCP.
- C) El servidor identifica al usuario por su `User-Agent` y guarda el carrito asociado a él.
- D) Lo habitual es que la cookie contenga todos los datos del carrito, para que el servidor no tenga que guardar nada.

**55.** ¿Qué cabecera usa el servidor para pedir que se guarde una cookie, y cuál usa el navegador para reenviarla?

- A) `Cookie` (servidor) y `Set-Cookie` (navegador).
- B) `Set-Cookie` (servidor) y `Cookie` (navegador).
- C) `Cookie` (servidor) y `Authorization` (navegador).
- D) `Set-Cookie` en ambos casos.

**56.** Una vez guardada una cookie, ¿en qué peticiones la reenvía automáticamente el navegador?

- A) En cada petición siguiente a ese dominio.
- B) En las peticiones a cualquier dominio que se visite después.
- C) Solo en las peticiones POST.
- D) Solo en la petición inmediatamente posterior.

**57.** En una sesión bien diseñada, ¿qué viaja realmente dentro de la cookie de sesión?

- A) Un hash de la IP del cliente.
- B) El usuario, el carrito y los permisos, serializados.
- C) Un identificador aleatorio y difícil de adivinar.
- D) El usuario y la contraseña cifrados.

**58.** Según el bloque, ¿dónde guarda normalmente el servidor el estado real de cada sesión?

- A) Solo en la memoria del proceso, nunca en ficheros ni en una base de datos.
- B) Únicamente en la cookie del navegador.
- C) En memoria, en ficheros o en una base de datos.
- D) En la caché DNS del servidor.

**59.** ¿Qué afirmación describe correctamente el **robo de sesión** (*session hijacking*)?

- A) Solo es posible si la cookie de sesión lleva el atributo `SameSite`.
- B) Consiste en que otra web provoque peticiones en tu nombre aprovechando que el navegador envía tus cookies solo.
- C) El atacante necesita tu cookie de sesión y también tu contraseña para suplantarte.
- D) Quien lea tu cookie de sesión (p. ej. por XSS) puede suplantarte sin conocer tu contraseña.

**60.** ¿Qué describe el ataque CSRF?

- A) Unas cookies de terceros rastrean tu navegación entre distintas páginas.
- B) El atacante adivina tu identificador de sesión probando valores consecutivos hasta dar con uno válido.
- C) El navegador envía tus cookies aunque la petición la inicie otra página, y el atacante actúa en tu nombre.
- D) Un script malicioso inyectado en la página lee tu cookie de sesión y se la envía al servidor del propio atacante.

**61.** ¿Qué atributo de cookie reduce el riesgo de que un script inyectado (XSS) robe la cookie de sesión?

- A) `Secure`
- B) `Path`
- C) `HttpOnly`
- D) `SameSite`

**62.** ¿Qué atributo restringe el envío de la cookie en peticiones iniciadas desde otros sitios, mitigando CSRF?

- A) `HttpOnly`
- B) `Domain`
- C) `SameSite`
- D) `Secure`

**63.** Sobre los atributos de las cookies, ¿qué afirmación es **FALSA**?

- A) `SameSite` restringe el envío de la cookie en peticiones iniciadas desde otros sitios.
- B) Con `HttpOnly`, `Secure` y `SameSite`, la aplicación ya no necesita validar los datos.
- C) `Secure` hace que la cookie solo se envíe por HTTPS, nunca en claro por HTTP.
- D) `HttpOnly` impide que la cookie se lea desde JavaScript.


## 5. Arquitecturas en capas

**64.** Una aplicación de escritorio se conecta directamente a una base de datos remota. Según el bloque, ¿cuál es la limitación de esta arquitectura de 2 capas?

- A) La lógica de negocio y el acceso a datos siguen mezclados.
- B) No permite que el cliente se ejecute en una máquina distinta de la base de datos.
- C) Obliga a tener servidores de presentación separados de los de negocio.
- D) Interfaz, lógica y datos están en el mismo bloque de código y en la misma máquina.

**65.** En una arquitectura de 3 capas, ¿en qué capa van las reglas, las validaciones y los cálculos?

- A) Acceso a la red.
- B) Negocio.
- C) Presentación.
- D) Datos.

**66.** Sobre *layer* y *tier*, ¿qué afirmación es correcta?

- A) Son sinónimos: los dos se refieren a la separación lógica del código.
- B) Una aplicación de 3 capas lógicas debe desplegarse obligatoriamente en 3 servidores físicos distintos.
- C) *Layer* es la separación física en máquinas distintas y *tier*, la separación lógica del código.
- D) *Layer* es la separación lógica y *tier* la física; 3 capas lógicas caben en una sola máquina.

**67.** Una aplicación web de 3 capas recibe muchísimas visitas. ¿Qué ventaja de esta arquitectura cita el bloque para este caso?

- A) Se puede duplicar la base de datos en cada servidor de presentación.
- B) Se puede escalar la capa de presentación por separado, sin duplicar la base de datos.
- C) Se puede eliminar la capa de negocio y conectar la presentación directamente a los datos.
- D) Se puede pasar a 1 capa para reducir la comunicación entre componentes.

**68.** ¿Qué relación hay entre la arquitectura de 3 capas y la de N capas?

- A) N capas implica siempre usar microservicios.
- B) N capas es un caso particular de 3 capas.
- C) 3 capas es el caso particular más común de N capas.
- D) Son arquitecturas excluyentes: o se usa una o la otra.

**69.** ¿Qué describe la arquitectura de 1 capa?

- A) Interfaz, lógica y datos juntos, en la misma máquina; no escala en complejidad ni en usuarios.
- B) Cliente y servidor separados en máquinas distintas, con la lógica en el servidor.
- C) Una sola capa de servicios a la que acceden varios clientes distintos.
- D) Presentación y negocio separados en máquinas distintas, pero con los datos dentro del bloque de negocio.


## 6. Arquitecturas a gran escala

**70.** ¿Qué afirmación sobre un monolito es correcta?

- A) Implica necesariamente código desordenado y sin capas.
- B) Se despliega y escala como una sola unidad, y puede estar bien organizado en capas.
- C) Cada funcionalidad se construye y se despliega por separado, aunque todas comparten la misma base de datos.
- D) No puede usar una base de datos propia.

**71.** ¿Qué diferencia a SOA de los microservicios, según el bloque?

- A) Los microservicios necesitan obligatoriamente un ESB para comunicarse.
- B) En SOA los servicios son más pequeños y autónomos que en los microservicios, y no comparten middleware.
- C) En SOA los servicios suelen ser más grandes y usan un middleware central (ESB).
- D) No hay diferencia: son dos nombres para la misma arquitectura.

**72.** ¿Qué significan las siglas ESB?

- A) External Service Balancer.
- B) Enterprise Service Bus.
- C) Event Stream Broker.
- D) Enterprise Security Bridge.

**73.** En una arquitectura orientada a eventos, ¿qué es cierto?

- A) Los componentes se llaman directamente entre sí por su dirección IP, sin intermediarios ni colas de mensajes.
- B) Sustituye a HTTP como protocolo de transporte entre servicios.
- C) Quien publica un evento debe conocer a todos sus consumidores.
- D) Publican y reaccionan a eventos mediante un intermediario, sin que el emisor conozca a los consumidores.

**74.** ¿Qué afirmación sobre serverless / FaaS es correcta?

- A) Despliegas funciones; la plataforma decide cuándo y dónde ejecutarlas y pagas por ejecución.
- B) No hay servidores físicos en ningún lugar: el código se ejecuta en el navegador.
- C) Tú decides cuántos servidores hay y cuándo se encienden; la plataforma solo se encarga de parchearlos.
- D) Pagas por tener los servidores encendidos todo el día, aunque la plataforma los gestione por ti.

**75.** Según la comparativa entre monolito y microservicios, ¿qué afirmación es correcta?

- A) Con microservicios se escala toda la aplicación a la vez.
- B) Los microservicios tienen una complejidad inicial baja, porque cada servicio es pequeño y sencillo.
- C) En un monolito, un fallo suele quedar aislado en una parte del sistema.
- D) Para un proyecto simple, los microservicios pueden ser sobreingeniería.


## 7. Diseño interno del código

**76.** En el patrón MVC, ¿dónde reside la lógica de negocio?

- A) En el Controlador.
- B) En el Modelo.
- C) Repartida a partes iguales entre la Vista y el Controlador.
- D) En la Vista.

**77.** ¿Qué distingue a MVVM de MVP, según el bloque?

- A) MVVM es el patrón habitual de frameworks de backend como Django o Laravel.
- B) MVVM: el ViewModel expone el estado de forma reactiva y la Vista se sincroniza sola; MVP: el Presentador deja la Vista casi «tonta».
- C) MVP sustituye el Modelo por un Presentador que accede directamente a la base de datos.
- D) MVP: la Vista se sincroniza sola de forma reactiva con el Presentador; MVVM: el ViewModel asume la lógica y deja la Vista casi «tonta».

**78.** ¿Qué regla comparten la arquitectura hexagonal, Clean Architecture y Onion Architecture?

- A) Las dependencias apuntan hacia fuera: el dominio depende de la base de datos y del framework.
- B) Obligan a desplegar la aplicación como microservicios.
- C) Las dependencias apuntan hacia dentro: el dominio no depende de detalles técnicos.
- D) Son incompatibles con el patrón MVC.


## 8. Panorama general

**79.** ¿Cuál de estas opciones responde a la pregunta «¿cómo organizo el código dentro de cada pieza?» y no a «¿cómo reparto el sistema en piezas desplegables?»?

- A) Orientada a eventos.
- B) SOA.
- C) Serverless / FaaS.
- D) Arquitectura hexagonal.

**80.** Según la guía rápida, ¿qué arquitectura es razonable para integrar los sistemas heredados de una gran empresa?

- A) Microservicios.
- B) Monolito en 3 capas.
- C) Serverless / FaaS.
- D) SOA.


---

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
