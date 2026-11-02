---
layout: default
title: "Arquitecturas Web — Bloque 2.2: Servidores web y de aplicaciones (Test)"
permalink: /web/semana-2/test/
---

# Bloque 2.2 — Test de servidores web, servidores de aplicaciones y despliegue

**Módulo:** Despliegue de Aplicaciones Web (0614) · 2º DAW · UD2: Arquitecturas web

## Instrucciones

- 80 preguntas con 4 opciones y **una sola respuesta correcta**.
- Puntuación: acierto **+1** · error **−1/3** · en blanco **0**.
- Nota sobre 10 = (aciertos − errores / 3) × 10 / 80. Si el resultado es negativo, la nota es 0.
- Con esta penalización, responder al azar da de media un 0: si no sabes la respuesta, déjala en blanco.
- Tiempo orientativo: 70 minutos.


## 1. Contenido estático y dinámico

**1.** ¿Qué caracteriza al contenido **estático**?

- A) El servidor ejecuta un programa en cada petición para generar la respuesta.
- B) Solo puede ser HTML: las imágenes y las hojas de estilo se consideran dinámicas.
- C) Se envía tal cual está guardado en disco, sin ejecutar código por petición.
- D) Se genera una vez por usuario y se guarda en su sesión para las visitas siguientes.

**2.** ¿Cuál de estos es un ejemplo de contenido **dinámico**?

- A) La hoja de estilos `estilos.css` de la web.
- B) El logotipo `logo.png` que aparece en la cabecera.
- C) El resultado de una búsqueda en la tienda.
- D) Una fuente tipográfica que descarga el navegador.

**3.** Una petición `GET /tienda` devuelve un HTML con los precios y el stock actuales, que referencia `/css/estilos.css` y `/img/logo.png`. ¿Qué es correcto?

- A) El HTML es dinámico; el CSS y el logo son estáticos, aunque se pidan después.
- B) Todo es dinámico, porque la página muestra precios que cambian.
- C) Todo es estático, porque se sirve por HTTP desde el mismo servidor.
- D) El HTML es estático y el CSS es dinámico, porque se descarga después.


## 2. Renderizado, CDN y SEO

**4.** En una aplicación con **CSR** (*Client-Side Rendering*), ¿qué envía inicialmente el servidor?

- A) El HTML completo de la página, con todos los datos ya incluidos dentro.
- B) Solo un JSON con los datos, sin ninguna página HTML que lo acompañe.
- C) Un HTML casi vacío (`<div id="app"></div>`) y mucho JavaScript.
- D) Una imagen de la página que el navegador muestra mientras carga los datos.

**5.** ¿Cuál es el inconveniente típico del CSR, según el bloque?

- A) La navegación entre páginas es lenta, porque cada clic recarga la página entera.
- B) Necesita un servidor de aplicaciones en producción para montar el HTML.
- C) La primera carga es lenta: la página sale en blanco hasta que acaba el JavaScript.
- D) Solo funciona con frameworks de backend como Django, Laravel o Spring.

**6.** ¿Qué frameworks cita el bloque para hacer **SSR** moderno con React y Vue?

- A) Vite y webpack.
- B) Nginx y Apache.
- C) Gunicorn y uWSGI.
- D) Next.js y Nuxt.

**7.** ¿Qué es la **hidratación** (*hydration*)?

- A) Recargar la página automáticamente cada cierto tiempo para mostrar datos frescos.
- B) Generar todo el HTML una sola vez, en tiempo de build, antes de desplegar.
- C) Comprimir el HTML que genera el servidor antes de enviarlo, para que ocupe menos.
- D) El navegador engancha el JavaScript al HTML ya renderizado por el servidor.

**8.** En **SSG** (*Static Site Generation*), ¿cuándo se genera el HTML?

- A) Una sola vez, en tiempo de build, antes de desplegar la web.
- B) En el navegador, al ejecutar el JavaScript de la página.
- C) En el servidor, en cada petición que llega.
- D) En la CDN, cada vez que un usuario pide la página.

**9.** ¿Para cuál de estas páginas **no basta** SSG por sí solo?

- A) Un carrito con precios actualizados al momento.
- B) Un blog personal con artículos que se publican cada semana.
- C) La página «Quiénes somos» de una empresa.
- D) La documentación de una librería, con su buscador.

**10.** Según la tabla comparativa del bloque, ¿qué modelos de renderizado **no necesitan** un servidor de aplicaciones en producción?

- A) Solo SSR.
- B) SSR y SSG.
- C) CSR y SSG.
- D) Los tres lo necesitan.

**11.** ¿Por qué un CSR puro dificulta el SEO?

- A) Porque los buscadores penalizan cualquier página que use React, Vue o Angular.
- B) Porque el crawler recibe un HTML casi vacío y debe ejecutar el JavaScript.
- C) Porque en CSR no se pueden usar las etiquetas `<title>` ni `<meta>` en la cabecera de la página.
- D) Porque las páginas CSR no tienen URL propia y los buscadores no pueden enlazarlas.

**12.** ¿Cuál de estos factores **NO** aparece en el bloque entre los aspectos de SEO que sí controlamos?

- A) Escribir bien `<title>` y `<meta name="description">` en cada página.
- B) Aumentar el número de servidores de aplicaciones.
- C) Conseguir tiempos de carga bajos.
- D) Mantener URLs legibles y estables, redirigiendo con 301 si cambian.

**13.** Una página bien posicionada cambia de URL de forma definitiva. ¿Qué respuesta conviene dar en la URL antigua para no perder el posicionamiento?

- A) Una redirección `301`.
- B) Una redirección `302`.
- C) Un error `404`.
- D) Un error `503`.

**14.** ¿Qué es una **CDN**?

- A) Una red de servidores repartidos por el mundo con copias cacheadas del contenido.
- B) Un servidor central muy potente que sustituye a todos los servidores de la aplicación web.
- C) Una base de datos distribuida que replica los datos de los usuarios en varios países.
- D) Un algoritmo de compresión que reduce el tamaño de las imágenes antes de enviarlas.

**15.** ¿Cuál de estos servicios **NO** es una CDN?

- A) Cloudflare.
- B) Gunicorn.
- C) Akamai.
- D) Amazon CloudFront.

**16.** ¿Qué contenido aprovecha **peor** una CDN?

- A) El carrito personalizado de cada usuario.
- B) Las imágenes del catálogo de productos.
- C) El HTML de un blog generado con SSG.
- D) Las hojas de estilo CSS de la web.

**17.** Despliegas un `estilos.css` nuevo con el mismo nombre, pero muchos usuarios siguen viendo los estilos antiguos. ¿Cuál es la causa más probable?

- A) La CDN o el navegador siguen sirviendo la copia antigua que tenían en caché.
- B) El servidor web no ha comprimido el fichero nuevo.
- C) Los ficheros CSS no se pueden cachear, así que el navegador usa sus estilos por defecto.
- D) El DNS todavía apunta al servidor anterior.

**18.** ¿En qué consiste el ***cache busting***?

- A) En enviar `Cache-Control: no-store` en todas las respuestas del servidor web.
- B) En desactivar la caché del navegador para todos los ficheros de la web.
- C) En reiniciar la CDN después de cada despliegue para vaciar todas sus copias.
- D) En incluir un hash o una versión en el nombre de cada fichero que cambia.


## 3. Servidor web y servidor de aplicaciones

**19.** ¿Cuál es la función principal de un **servidor web**?

- A) Recibir peticiones HTTP y responder, sobre todo con contenido estático.
- B) Almacenar los datos de la aplicación de forma persistente y segura.
- C) Compilar el código de la aplicación antes de cada petición.
- D) Ejecutar la lógica de negocio de la aplicación y generar el contenido dinámico.

**20.** ¿Cuál de estos programas es un **servidor web**?

- A) Gunicorn.
- B) Tomcat.
- C) PHP-FPM.
- D) Nginx.

**21.** ¿Cuál de estos programas es un **servidor de aplicaciones**?

- A) Apache HTTP Server.
- B) Nginx.
- C) Gunicorn.
- D) Cloudflare.

**22.** Para la compresión, ¿con qué cabecera indica el navegador lo que acepta y con cuál indica el servidor lo que ha aplicado?

- A) `Accept-Encoding` (navegador) y `Content-Encoding` (servidor).
- B) `Accept` (navegador) y `Content-Type` (servidor).
- C) `Content-Encoding` (navegador) y `Accept-Encoding` (servidor).
- D) `Accept-Language` (navegador) y `Content-Language` (servidor).

**23.** Sobre la compresión con gzip o brotli, ¿qué afirmación es correcta?

- A) Hay que modificar el código de la aplicación para que comprima cada respuesta.
- B) Solo tiene sentido para imágenes y vídeos, que son los ficheros más grandes.
- C) Es configuración del servidor web y reduce lo transferido sin tocar la aplicación.
- D) Cifra el contenido, así que puede sustituir a HTTPS en las conexiones internas.

**24.** ¿Qué afirmación sobre un **servidor de aplicaciones** es correcta?

- A) Un servidor web puro también sabe ejecutar código PHP o Java por sí mismo.
- B) Su función principal es servir ficheros estáticos con la máxima eficiencia.
- C) Sustituye a la base de datos, porque guarda el estado de la aplicación.
- D) Entiende el lenguaje o framework de la aplicación y ejecuta su lógica.

**25.** ¿Qué servidor de aplicaciones suele usar una aplicación **Spring Boot**?

- A) Gunicorn.
- B) Tomcat.
- C) Puma.
- D) PHP-FPM.

**26.** ¿Qué servidor de aplicaciones es típico para una aplicación **Django** o **Flask**?

- A) PHP-FPM o Tomcat.
- B) Tomcat.
- C) Gunicorn o uWSGI.
- D) Puma o Unicorn.

**27.** ¿Y para una aplicación **Laravel** o **Symfony**?

- A) PHP-FPM.
- B) Unicorn.
- C) Tomcat.
- D) uWSGI.

**28.** ¿Qué ejecuta una aplicación hecha con **Express** o **NestJS**?

- A) Tomcat, embebido en un `.jar`.
- B) El propio proceso Node.js.
- C) Apache HTTP Server con PHP-FPM.
- D) Gunicorn.

**29.** ¿Qué son **Vue, Angular y React**?

- A) Frameworks de backend que sustituyen a Spring, Django o Laravel.
- B) Servidores de aplicaciones para JavaScript.
- C) Frameworks de frontend, cuyo código se ejecuta en el navegador.
- D) Servidores web alternativos a Nginx y Apache.

**30.** ¿Qué genera `npm run build` en un proyecto de Vue, Angular o React con CSR?

- A) Una carpeta (`dist/`) con `index.html`, `.js` y `.css` compilados.
- B) Un servidor Node.js listo para arrancar en producción con la aplicación.
- C) Una imagen Docker con el frontend y su servidor de aplicaciones.
- D) Un fichero `.jar` con el frontend, que después se despliega en Tomcat.

**31.** ¿Cómo se sirve en producción una SPA hecha con CSR?

- A) Con Node.js en producción, porque el código está escrito en JavaScript.
- B) Con Tomcat, porque necesita un servidor de aplicaciones para ejecutarse.
- C) Con Nginx o Apache, como contenido estático; Node.js solo hace falta en el build.
- D) Obligatoriamente con una plataforma serverless, porque una SPA no tiene backend propio.

**32.** ¿Cuándo **sí** necesita un frontend un servidor de aplicaciones (un proceso Node.js) en producción?

- A) Siempre que esté hecho con React o Vue.
- B) Cuando usa CSR y llama a una API.
- C) Cuando usa SSR, como Next.js o Nuxt.
- D) Cuando lo sirve Nginx como estático.

**33.** ¿Qué combinación define un **origen**, a efectos de CORS?

- A) Dominio + ruta del recurso.
- B) Esquema + host + puerto.
- C) Dirección IP + puerto.
- D) Dominio + query string.

**34.** ¿Cuál de estas URL es del **mismo origen** que `https://miapp.com`?

- A) `https://miapp.com/api/productos`
- B) `http://miapp.com/api/productos`
- C) `https://api.miapp.com`
- D) `https://miapp.com:8080`

**35.** ¿Son del mismo origen `https://miapp.com` y `https://miapp.com:8080`?

- A) Sí, porque el dominio es el mismo.
- B) No, porque cambia el esquema.
- C) Sí, porque los dos usan HTTPS.
- D) No, porque cambia el puerto.

**36.** ¿Con qué cabecera de respuesta indica el backend qué origen externo puede leer sus respuestas?

- A) `Origin`
- B) `Access-Control-Request-Method`
- C) `Allow`
- D) `Access-Control-Allow-Origin`

**37.** El JavaScript de `https://miapp.com` llama a una API de otro origen que **no** devuelve cabeceras CORS. ¿Qué ocurre?

- A) El servidor redirige la petición con un `302` al origen correcto para que se repita.
- B) El servidor rechaza la petición con un `403 Forbidden` antes de procesarla.
- C) La petición nunca llega a salir del navegador, así que el servidor no se entera de nada.
- D) El navegador no deja al JavaScript leer la respuesta, aunque el servidor la haya enviado.

**38.** ¿Qué petición provoca normalmente una comprobación previa (*preflight*) de CORS?

- A) La carga de una imagen con `<img>` desde otro dominio.
- B) Un `DELETE`, o un `PUT` con JSON, hacia otro origen.
- C) Un clic en un enlace `<a>` que lleva a otra web.
- D) La carga de una hoja de estilos con `<link>`.

**39.** Una petición a la API funciona con `curl` y con Postman, pero falla desde el frontend en el navegador. ¿Cuál es la explicación más probable?

- A) Falta configurar CORS: lo aplica el navegador, no el servidor.
- B) El servidor detecta el `User-Agent` del navegador y lo bloquea.
- C) Hay un error de DNS que solo afecta a los navegadores.
- D) `curl` y Postman usan un puerto distinto al del navegador.

**40.** ¿Qué modelo de concurrencia describe el bloque para **Nginx**?

- A) Un *worker* por petición, creado y destruido en cada una.
- B) Un proceso o un hilo distinto para cada conexión abierta.
- C) Un único hilo con un *event loop* que también ejecuta la lógica de negocio.
- D) Eventos asíncronos: pocos procesos para miles de conexiones.

**41.** ¿Qué modelo de concurrencia corresponde a **Apache** en su modo clásico (`prefork`)?

- A) Eventos asíncronos con muy pocos procesos.
- B) Un proceso o hilo por conexión.
- C) Un único hilo con un *event loop*.
- D) Funciones que se ejecutan bajo demanda.

**42.** ¿Qué afirmación sobre el modelo de **Node.js** es correcta?

- A) Un único hilo con *event loop*: bien con E/S, mal con cálculos pesados.
- B) Crea un proceso nuevo para cada conexión, como hace Apache en modo `prefork`.
- C) Usa muchos hilos en paralelo, así que los cálculos pesados no le afectan.
- D) No puede atender más de una petición a la vez, aunque sean operaciones de red.

**43.** En **Gunicorn** o **Tomcat**, ¿de qué depende cuántas peticiones simultáneas se atienden?

- A) Del número de núcleos de la máquina del cliente.
- B) De cuántos *workers* (procesos o hilos) se configuren.
- C) De la versión de HTTP que use el navegador.
- D) Del tamaño de la base de datos que consulta la aplicación.

**44.** En una aplicación Node.js, una petición hace un cálculo que tarda varios segundos. ¿Qué ocurre con las demás peticiones que llegan a esa instancia?

- A) Se redirigen solas a otra instancia, porque Node.js detecta el bloqueo.
- B) Nada: Node.js abre automáticamente un hilo nuevo para cada cálculo.
- C) Esperan, porque el cálculo bloquea el único hilo que las atiende.
- D) Reciben un `405 Method Not Allowed` hasta que termina el cálculo.

**45.** ¿Por qué se coloca tan a menudo **Nginx delante** de los servidores de aplicaciones?

- A) Porque ejecuta la lógica de negocio más rápido que el propio servidor de aplicaciones.
- B) Porque aguanta mucha concurrencia y reparte lo dinámico entre backends.
- C) Porque los servidores de aplicaciones no saben responder directamente a peticiones HTTP.
- D) Porque sustituye a la base de datos y guarda en caché todas las consultas.

**46.** En el patrón habitual de producción, ¿qué hace un **proxy inverso**?

- A) Guarda en caché las respuestas DNS para que los clientes resuelvan los nombres más rápido.
- B) Permite que los equipos de una red interna salgan a Internet a través de él, ocultando su IP.
- C) Cifra la base de datos para que los servidores de aplicaciones no puedan leerla directamente.
- D) Recibe las peticiones de los clientes y reenvía las dinámicas a los servidores de aplicaciones.

**47.** Nginx hace de proxy inverso y devuelve **502 Bad Gateway**. ¿Qué indica?

- A) Que la aplicación de detrás no está arrancada o responde mal.
- B) Que el cliente no tiene permisos para acceder al recurso que ha pedido.
- C) Que el recurso solicitado no existe en el servidor.
- D) Que la aplicación de detrás ha tardado demasiado en responder y Nginx ha dejado de esperar.

**48.** ¿Cómo reparte las peticiones la estrategia de balanceo ***round robin***?

- A) Al backend con menos conexiones activas en ese momento.
- B) Por turnos: una petición a cada backend, uno tras otro.
- C) Según la IP del cliente, siempre al mismo backend.
- D) Al backend que haya respondido más rápido la última vez.

**49.** ¿Cómo reparte las peticiones la estrategia ***least connections***?

- A) Por turnos, uno tras otro.
- B) Siempre al backend más potente, hasta que se satura.
- C) Según un hash de la IP del cliente que hace la petición.
- D) Al backend con menos conexiones activas.

**50.** Una aplicación guarda la sesión de cada usuario en la **memoria** de la instancia que le atiende y hay varios backends. ¿Qué estrategia de las que cita el bloque hace que un cliente vaya siempre al mismo backend?

- A) *IP hash*.
- B) *Weighted round robin*.
- C) *Round robin*.
- D) *Least connections*.

**51.** ¿Qué es el ***weighted round robin***?

- A) Un reparto según la IP del cliente, ponderado por su país de origen.
- B) Por turnos, pero los backends más potentes reciben más peticiones.
- C) Un reparto aleatorio entre los backends que superan el health check.
- D) Un reparto al backend que tenga menos conexiones activas en ese momento.

**52.** ¿Qué es el **escalado vertical**?

- A) Añadir más instancias idénticas de la aplicación en paralelo, detrás de un balanceador.
- B) Dar más CPU o RAM a la misma máquina; tiene un límite físico y suele obligar a parar.
- C) Mover el contenido estático a una CDN para descargar de trabajo al servidor.
- D) Dividir la aplicación en microservicios que se despliegan por separado.

**53.** ¿Qué afirmación sobre el **escalado horizontal** es correcta?

- A) Añade instancias en paralelo y es lo habitual en la nube.
- B) Consiste en ampliar la RAM y la CPU del servidor cuando se queda corto.
- C) Tiene un límite físico más rígido que el escalado vertical.
- D) Solo es posible si la aplicación está escrita en Java y se despliega en Tomcat.

**54.** ¿Por qué **Docker** facilita especialmente el escalado horizontal?

- A) Porque aumenta automáticamente la CPU y la RAM de la máquina cuando hace falta.
- B) Porque levantar una instancia más es, en esencia, arrancar otro contenedor de la misma imagen.
- C) Porque elimina la necesidad de tener un balanceador de carga delante de las instancias.
- D) Porque todos los contenedores comparten la misma memoria y, por tanto, la misma sesión.

**55.** ¿Qué es **Kubernetes**?

- A) Un servidor web alternativo a Nginx y a Apache.
- B) Un servidor de aplicaciones para Java, como Tomcat.
- C) Un orquestador que automatiza la gestión de contenedores.
- D) Una CDN especializada en contenido estático.

**56.** ¿Qué es un ***health check***?

- A) Un registro con todas las peticiones que ha atendido cada backend.
- B) Un antivirus que analiza los contenedores antes de arrancarlos.
- C) Una revisión del código antes de aceptar un cambio en el repositorio del proyecto.
- D) Una petición de prueba periódica para ver si un backend responde.

**57.** Un backend deja de superar el *health check*. ¿Qué hace el servidor web o el balanceador?

- A) Reinicia todos los backends para evitar inconsistencias entre ellos.
- B) Lo retira temporalmente de la rotación hasta que vuelva a estar sano.
- C) Devuelve un `503` a todos los usuarios hasta que el backend se recupere.
- D) Borra el contenedor y su imagen para que no se vuelva a usar.

**58.** ¿Qué ventaja **NO** cita el bloque de separar el servidor web del servidor de aplicaciones?

- A) Poder cachear el contenido estático.
- B) Aplicar HTTPS en un único punto.
- C) Balancear la carga entre varios servidores de aplicaciones.
- D) No tener que escribir lógica de negocio en la aplicación.


## 4. Qué significa desplegar

**59.** Según el bloque, ¿qué es **desplegar** una aplicación?

- A) Escribir y ejecutar las pruebas automáticas del código antes de publicarlo.
- B) Subir el código al repositorio Git del proyecto.
- C) Ponerla al alcance de sus usuarios reales, fuera de tu máquina.
- D) Compilar la aplicación en la máquina de desarrollo para generar el ejecutable.

**60.** ¿Qué pieza de un despliegue apunta el dominio a la IP del servidor?

- A) El artefacto.
- B) El hosting.
- C) El certificado HTTPS.
- D) El DNS.

**61.** ¿Qué tipo de hosting te da **una máquina virtual para ti solo**, con control total del sistema operativo?

- A) VPS.
- B) Hosting compartido.
- C) Servidor dedicado.
- D) PaaS.

**62.** En el cloud, ¿qué caracteriza a un servicio **PaaS** frente a uno **IaaS**?

- A) En PaaS alquilas máquinas virtuales y gestionas tú todo el sistema operativo.
- B) En PaaS te dan una máquina física entera para ti solo.
- C) En PaaS subes tu código o tu contenedor y el proveedor gestiona el resto.
- D) En PaaS varias webs comparten un mismo servidor gestionado por el proveedor.

**63.** ¿Para qué sirve el entorno de **staging** (preproducción)?

- A) Es el lugar donde se guardan las copias de seguridad de la base de datos.
- B) Es tu máquina, donde programas y pruebas en local.
- C) Es el entorno real, con los usuarios de verdad.
- D) Es una réplica de producción para probar antes de publicar.

**64.** ¿Cuál es la **idea clave** del bloque sobre los entornos de despliegue?

- A) Cada entorno debe reconstruir su propio artefacto a partir del código fuente.
- B) El mismo artefacto versionado se promociona de un entorno a otro sin reconstruirlo.
- C) Producción debe usar siempre la versión `latest` para tener las últimas correcciones.
- D) Staging trabaja con el código fuente y solo producción usa artefactos.

**65.** ¿Qué es un **artefacto**?

- A) El código fuente de la aplicación, tal cual está en el repositorio Git.
- B) El `Dockerfile` con las instrucciones para construir la imagen de la aplicación.
- C) El resultado empaquetado de construir la aplicación.
- D) La base de datos de producción con todos sus datos.

**66.** Según el bloque, ¿cuál es el artefacto típico de una aplicación **PHP**?

- A) Un `.jar` con el código PHP compilado a *bytecode*.
- B) Un `.tar.gz` con el código y la carpeta `vendor/`.
- C) Una *wheel* `.whl` generada por Composer.
- D) Un `.exe` generado por el intérprete de PHP.

**67.** ¿Por qué el bloque desaconseja hacer `git pull` en producción y reinstalar dependencias en cada servidor?

- A) Porque las licencias de las dependencias prohíben instalarlas en servidores.
- B) Porque Git no puede instalarse en los servidores de producción por motivos de seguridad.
- C) Porque descargar el código con Git es siempre más lento que compilarlo.
- D) Porque una reinstalación podría traer otras versiones de las dependencias.

**68.** ¿Qué permiten los **repositorios de artefactos** como JFrog Artifactory o Sonatype Nexus?

- A) Ejecutar los artefactos sin necesidad de servidor.
- B) Convertir el código fuente en artefacto automáticamente en cada servidor de destino.
- C) Subir el artefacto una vez y descargar siempre esa versión exacta.
- D) Sustituir al servidor web cuando se despliega contenido estático.

**69.** Según **SemVer**, la versión `2.4.1` corrige un error sin añadir nada nuevo. ¿Qué versión toca?

- A) `2.4.2`
- B) `2.5.0`
- C) `3.0.0`
- D) `2.4.1-latest`

**70.** Según **SemVer**, la versión `2.4.1` introduce un cambio **incompatible** con la anterior. ¿Qué versión toca?

- A) `2.4.2`
- B) `2.5.0`
- C) `3.0.0`
- D) `2.4.1.1`

**71.** ¿Qué problema tiene desplegar siempre la etiqueta `latest`?

- A) Que las imágenes con la etiqueta `latest` son más lentas de descargar del registry.
- B) Que Docker no permite arrancar contenedores a partir de `latest`.
- C) Que no se sabe qué versión exacta hay en producción, lo que dificulta el rollback.
- D) Que borra automáticamente las imágenes anteriores que había en el servidor.

**72.** ¿Dónde deben guardarse las contraseñas, tokens y claves de API de la aplicación?

- A) Dentro de la imagen Docker, para que el artefacto esté completo.
- B) Fuera del artefacto: variables de entorno o un gestor de secretos.
- C) En el código fuente, en un fichero de constantes que no se publica.
- D) En el nombre o la etiqueta del artefacto, para identificarlos fácilmente al desplegar.

**73.** Se ejecutan `docker run -e DB_HOST=db-staging … miapp:1.4.0` en staging y `docker run -e DB_HOST=db-prod … miapp:1.4.0` en producción. ¿Qué es correcto?

- A) Son dos artefactos distintos, uno para cada entorno.
- B) Staging reconstruye la imagen antes de arrancarla.
- C) Es el mismo artefacto, con distinta configuración en cada entorno.
- D) Docker copia el valor de `DB_HOST` dentro de la imagen al arrancar el contenedor.

**74.** ¿Qué afirmación sobre una **imagen Docker** es correcta, según el bloque?

- A) Es en sí misma un artefacto versionado, identificado por su tag.
- B) No es un artefacto, porque no contiene código compilado.
- C) Solo cuenta como artefacto si la aplicación está escrita en Java.
- D) Solo cuenta como artefacto si se sube a GitHub.

**75.** ¿Cuál es el orden del flujo de despliegue simple (sin CI/CD) que describe el bloque?

- A) `docker push` → `docker build` → `docker run` → `docker pull`.
- B) `docker pull` → `docker build` → `docker push` → `docker run`.
- C) `docker run` → `docker build` → `docker push` → `docker pull`.
- D) `docker build` → `docker push` → `docker pull` → `docker run`.


## 5. De la petición al despliegue

**76.** ¿En qué consiste un despliegue ***rolling*** (progresivo)?

- A) En levantar en paralelo un entorno completo con la versión nueva y pasarle todo el tráfico.
- B) En enviar primero solo un pequeño porcentaje del tráfico a la versión nueva.
- C) En apagar todos los backends, actualizarlos y volver a encenderlos.
- D) En sustituir los backends de uno en uno, mientras los demás atienden.

**77.** ¿Qué caracteriza a un despliegue ***blue-green***?

- A) Los backends se actualizan de uno en uno, sin levantar ningún entorno paralelo.
- B) Un entorno nuevo completo en paralelo recibe todo el tráfico de golpe.
- C) La versión nueva recibe primero solo un pequeño porcentaje del tráfico.
- D) Las funcionalidades nuevas se activan con un interruptor sin volver a desplegar.

**78.** ¿Qué es un despliegue ***canary***?

- A) Sustituir los backends antiguos por los nuevos de uno en uno.
- B) Desplegar automáticamente cada cambio que supera el pipeline.
- C) Mantener dos entornos completos y alternar entre ellos en cada versión.
- D) Dar a la versión nueva un pequeño porcentaje del tráfico al principio.

**79.** ¿Qué es una ***feature flag***?

- A) La etiqueta de versión de una imagen Docker.
- B) Una cabecera HTTP que indica la versión de la API.
- C) Una estrategia de balanceo que envía a cada usuario a la versión que prefiere usar.
- D) Una condición en el código que activa o desactiva una funcionalidad.

**80.** Una versión nueva añade una migración que **renombra una columna** y falla en producción. ¿Qué es cierto al hacer rollback?

- A) Basta con desplegar el artefacto anterior: la base de datos vuelve sola a su estado previo.
- B) Volver al artefacto anterior no deshace el cambio de esquema: las migraciones deben ser compatibles hacia atrás.
- C) Docker deshace los cambios del esquema al eliminar el contenedor de la versión nueva.
- D) La base de datos se restaura automáticamente desde la copia de seguridad del día anterior.


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
