---
marp: true
theme: default
paginate: true
backgroundColor: white
footer: 'Despliegue de Aplicaciones Web (0614) · UD2: Arquitecturas Web'
layout: default
title: "Arquitecturas Web — Bloque 2.2: Servidores y despliegue (Banco de test)"
permalink: /web/semana-2/test/
---

<!-- _class: lead -->
# arquitecturas web
## Test de repaso — bloque 2.2: servidores y despliegue
### 100 preguntas · 4 opciones, 1 correcta

---

## Cómo usar este banco de preguntas

- Cada diapositiva contiene una pregunta con 4 opciones (A-D), solo 1 correcta.
- No incluye las respuestas: úsalo para practicar de cara al cuestionario. TODAS las preguntas del cuestionario saldrán de este banco de preguntas.

---

<!-- _class: lead -->
# Bloque 1
## Contenido estático vs. dinámico

---

## Pregunta 1

¿Qué caracteriza al contenido estático servido por un servidor web?

A) Se genera ejecutando código distinto en cada petición
B) Se envía tal cual está guardado en disco, sin ejecutar código por petición
C) Solo puede tratarse de imágenes
D) Nunca puede cachearse

---

## Pregunta 2

¿Cuál de estos recursos es previsiblemente contenido dinámico?

A) Un fichero `estilos.css`
B) El resultado de una búsqueda personalizada en una tienda online
C) Una imagen `logo.png`
D) Una fuente tipográfica `.woff2`

---

## Pregunta 3

Un servidor genera el HTML de una página consultando datos actualizados de una base de datos en cada visita. ¿Qué tipo de contenido es?

A) Estático
B) Dinámico
C) Ninguno de los dos, no existe esa categoría
D) Depende solo del navegador usado

---

## Pregunta 4

¿Por qué el contenido estático suele servirse más rápido que el dinámico?

A) Porque pesa siempre menos en bytes
B) Porque el servidor solo tiene que leer un fichero, sin ejecutar lógica adicional
C) Porque usa un protocolo distinto a HTTP
D) Porque nunca pasa por DNS

---

## Pregunta 5

Una página HTML generada dinámicamente referencia internamente un fichero `app.js`. ¿Qué es más probable respecto a `app.js`?

A) Que también se genere de cero en cada petición con datos distintos
B) Que sea un recurso estático servido tal cual desde disco
C) Que sea imposible de servir junto con contenido dinámico
D) Que sustituya al servidor de aplicaciones

---

## Pregunta 6

¿Cuál de estas afirmaciones es correcta sobre una misma página web?

A) Una página debe ser siempre 100% estática o 100% dinámica, nunca ambas
B) Puede combinar HTML dinámico con recursos estáticos como CSS, JS o imágenes
C) El contenido dinámico nunca puede incluir imágenes
D) El contenido estático solo existe en servidores de aplicaciones

---

## Pregunta 7

¿Qué ejemplo representa mejor contenido estático?

A) El precio actualizado en tiempo real de una acción bursátil
B) Un documento PDF descargable que no cambia
C) El feed personalizado de un usuario en una red social
D) El resultado de iniciar sesión con credenciales concretas

---

## Pregunta 8

¿Qué ventaja operativa tiene identificar bien qué partes de una web son estáticas?

A) Ninguna, da igual cómo se sirvan todos los recursos
B) Permite servirlas de la forma más eficiente posible y, si hace falta, cachearlas
C) Obliga a ejecutar siempre una base de datos
D) Impide usar HTTPS en esos recursos

---

## Pregunta 9

¿Qué ocurre si intentas tratar contenido claramente dinámico (p. ej. el carrito de la compra de un usuario) como si fuera estático?

A) No pasa nada, funciona exactamente igual
B) Todos los usuarios verían el mismo contenido fijo, en vez del que les corresponde a cada uno
C) El servidor lo rechaza automáticamente con un error
D) Se vuelve automáticamente más rápido sin ningún problema

---

## Pregunta 10

En el esquema `GET /tienda` que devuelve HTML dinámico referenciando `/css/estilos.css`, ¿qué parte es estática?

A) Todo el conjunto, incluido el HTML
B) Solo `/css/estilos.css`
C) Solo el HTML generado
D) Ninguna parte lo es

---

<!-- _class: lead -->
# Bloque 2
## Servidor web

---

## Pregunta 11

¿Cuál es la función principal de un servidor web como Apache o Nginx?

A) Ejecutar exclusivamente lógica de negocio compleja
B) Recibir peticiones HTTP y responder, típicamente sirviendo contenido estático con eficiencia
C) Gestionar copias de seguridad de bases de datos
D) Resolver nombres de dominio

---

## Pregunta 12

¿Cuál de estos es un servidor web, no un servidor de aplicaciones?

A) Tomcat
B) Nginx
C) Node.js ejecutando Express
D) PHP-FPM

---

## Pregunta 13

Además de servir contenido, ¿qué otra función puede cumplir un servidor web como Nginx?

A) Actuar como proxy inverso, reenviando peticiones a otros servicios
B) Sustituir completamente al DNS
C) Eliminar la necesidad de certificados HTTPS
D) Compilar código fuente de la aplicación

---

## Pregunta 14

¿Por qué los servidores web están especialmente optimizados para servir contenido estático?

A) Porque no saben interpretar HTTP
B) Porque su diseño prioriza responder rápido a muchísimas conexiones simultáneas con ficheros ya preparados
C) Porque ejecutan bases de datos internamente
D) Porque solo funcionan con HTTPS

---

## Pregunta 15

¿Qué significa que Apache y Nginx sean, en el fondo, programas que "hablan HTTP"?

A) Que entienden y responden siguiendo las reglas del protocolo HTTP visto en el bloque 2.1
B) Que solo funcionan dentro de contenedores Docker
C) Que sustituyen completamente a los navegadores
D) Que no pueden servir imágenes

---

## Pregunta 16

¿En qué se diferenciaría, a nivel de uso típico, Apache/Nginx de un servidor de aplicaciones puro?

A) El servidor web no suele ejecutar por sí mismo la lógica de negocio de la aplicación
B) El servidor web nunca puede recibir peticiones HTTP
C) Apache y Nginx solo existen en entornos de pruebas
D) No existe ninguna diferencia de uso típico

---

## Pregunta 17

¿Qué tienen en común Apache y Nginx frente a Tomcat o Node.js, en el contexto visto en teoría?

A) Ambos son, ante todo, servidores web pensados para servir contenido HTTP de forma eficiente
B) Ambos ejecutan directamente código Java por diseño
C) Ambos son exclusivamente bases de datos
D) Ambos sustituyen al DNS

---

## Pregunta 18

Una empresa necesita servir miles de imágenes de producto rápidamente. ¿Qué tipo de servidor encaja mejor para esa tarea concreta?

A) Un servidor de aplicaciones puro, sin servidor web
B) Un servidor web como Nginx, optimizado para servir ese tipo de contenido
C) Ninguno, hace falta un servidor de bases de datos
D) Un cliente DNS

---

## Pregunta 19

¿Qué rol puede jugar un servidor web situado "por delante" de otros servicios, en el esquema visto en teoría?

A) Puerta de entrada (proxy inverso) hacia servicios internos, además de servir lo estático
B) Sustituir completamente a la base de datos
C) Eliminar la necesidad de contenedores
D) Generar automáticamente certificados sin ninguna configuración

---

## Pregunta 20

¿Qué detalle se profundiza específicamente en la UD3, relacionado con los servidores web vistos hoy?

A) La sintaxis básica de HTML
B) La configuración real de Apache/Nginx: hosts virtuales, HTTPS, proxy inverso y rendimiento
C) El funcionamiento interno de Git
D) El PID1 de un contenedor

---

<!-- _class: lead -->
# Bloque 3
## Servidor de aplicaciones

---

## Pregunta 21

¿Cuál es la función principal de un servidor de aplicaciones?

A) Servir ficheros estáticos de la forma más eficiente posible
B) Ejecutar la lógica de negocio de la aplicación para generar contenido dinámico
C) Resolver nombres de dominio
D) Cifrar el tráfico de red exclusivamente

---

## Pregunta 22

¿Cuál de estos es un ejemplo de servidor de aplicaciones?

A) Nginx
B) Apache HTTP Server
C) Tomcat
D) DNS

---

## Pregunta 23

¿Qué necesita entender un servidor de aplicaciones que un servidor web puro no necesita?

A) El protocolo DNS exclusivamente
B) El lenguaje o framework concreto en el que está escrita la lógica de la aplicación (Java, Node.js, Python...)
C) Únicamente ficheros de imagen
D) El hardware físico del servidor

---

## Pregunta 24

Gunicorn y uWSGI son ejemplos de servidores de aplicaciones típicos de qué lenguaje?

A) Java
B) Python
C) PHP únicamente
D) Ninguno, son servidores DNS

---

## Pregunta 25

PHP-FPM actúa como:

A) Un servidor de aplicaciones que ejecuta código PHP para generar contenido dinámico
B) Un servidor DNS especializado en dominios .php
C) Un tipo de base de datos NoSQL
D) Un sustituto directo de Docker

---

## Pregunta 26

¿Puede un servidor de aplicaciones recibir peticiones HTTP directamente, sin un servidor web por delante?

A) No, es técnicamente imposible
B) Sí, es posible, aunque en producción es habitual poner un servidor web delante por eficiencia y otras ventajas
C) Solo si usa exclusivamente HTTPS
D) Solo los fines de semana

---

## Pregunta 27

¿Qué tipo de servidor sería responsable de ejecutar el código que consulta la base de datos para montar el feed personalizado de un usuario?

A) El servidor web puro
B) El servidor de aplicaciones
C) El servidor DNS
D) Ninguno, lo hace directamente el navegador

---

## Pregunta 28

¿Qué diferencia de "entendimiento" hay entre un servidor web puro y uno de aplicaciones frente al código de la app?

A) El servidor web entiende y ejecuta cualquier lenguaje de programación igual que el de aplicaciones
B) El servidor de aplicaciones sabe ejecutar el código de la app; el servidor web puro no sabe interpretarlo por sí mismo
C) Ninguno de los dos puede interactuar con el código de la aplicación
D) Solo el servidor web puede ejecutar JavaScript

---

## Pregunta 29

Node.js ejecutando una aplicación Express actúa, en esta clasificación, como:

A) Un servidor web puro, sin más
B) Un servidor de aplicaciones
C) Un servidor DNS
D) Un proveedor de hosting compartido

---

## Pregunta 30

¿Por qué no sería buena idea exponer directamente a internet un servidor de aplicaciones sin ningún servidor web ni proxy por delante en un entorno de producción con mucho tráfico?

A) Porque los servidores de aplicaciones no entienden HTTP
B) Porque se perderían ventajas de eficiencia, balanceo y gestión centralizada de HTTPS que aporta un servidor web por delante
C) Porque es ilegal
D) Porque el servidor de aplicaciones no puede ejecutarse en un contenedor

---

<!-- _class: lead -->
# Bloque 4
## Servidor web + aplicaciones combinados

---

## Pregunta 31

En el patrón habitual de producción visto en teoría, ¿qué hace el servidor web con las peticiones a `/api/*`?

A) Las responde directamente sin reenviarlas a ningún sitio
B) Las reenvía (hace de proxy) hacia el servidor de aplicaciones correspondiente
C) Las descarta siempre con un error
D) Las convierte automáticamente en contenido estático

---

## Pregunta 32

¿Qué hace el servidor web con las peticiones a rutas como `/css/*` o `/img/*` en ese mismo patrón?

A) Las reenvía siempre al servidor de aplicaciones
B) Las responde directamente él mismo, al ser contenido estático
C) Las rechaza con un error 404 por defecto
D) Consulta la base de datos antes de responder

---

## Pregunta 33

¿Qué ventaja aporta que el servidor web gestione el HTTPS en un único punto, en vez de que cada servidor de aplicaciones lo haga por su cuenta?

A) Ninguna, da exactamente igual
B) Simplifica la gestión de certificados al centralizarla en un solo sitio
C) Hace innecesario el DNS
D) Elimina por completo la necesidad de HTTP

---

## Pregunta 34

¿Qué nombre recibe la técnica por la que un servidor web recibe la petición y la reenvía a otro servidor, devolviendo luego la respuesta al cliente como si fuera suya?

A) Proxy inverso
B) DNS recursivo
C) Contenedorización
D) Serverless

---

## Pregunta 35

Si un servidor web actuando como proxy inverso cae, ¿qué efecto tiene habitualmente sobre el acceso al servidor de aplicaciones de detrás?

A) Ninguno, el servidor de aplicaciones sigue siendo accesible igual desde fuera
B) Los usuarios probablemente no puedan acceder, al perderse el punto de entrada
C) Se vuelve automáticamente estático
D) El DNS lo sustituye automáticamente

---

## Pregunta 36

¿Qué combinación describe mejor un escenario típico de producción visto en teoría?

A) Solo servidor de aplicaciones, sin servidor web
B) Solo servidor web, sin ningún tipo de lógica dinámica
C) Un servidor web por delante sirviendo estático y reenviando lo dinámico a un servidor de aplicaciones por detrás
D) Solo una base de datos, sin ningún servidor HTTP

---

## Pregunta 37

¿Qué ventaja de rendimiento se consigue separando contenido estático (servidor web) de dinámico (servidor de aplicaciones)?

A) El servidor de aplicaciones solo gasta recursos en lo que realmente necesita ejecutar código
B) El servidor web deja de necesitar CPU por completo
C) Se elimina la necesidad de bases de datos
D) El tráfico deja de pasar por DNS

---

## Pregunta 38

¿Qué facilita, además del rendimiento, tener un único servidor web como punto de entrada hacia varios servicios internos?

A) Balancear la carga entre varios servidores de aplicaciones de forma centralizada
B) Eliminar la necesidad de contenedores
C) Que el DNS deje de ser necesario
D) Que el contenido dinámico se convierta en estático automáticamente

---

## Pregunta 39

¿Es el patrón "servidor web delante + servidor de aplicaciones detrás" exclusivo de aplicaciones muy grandes?

A) Sí, nunca se usa en proyectos pequeños
B) No, es un patrón habitual independientemente del tamaño, aunque gana más relevancia cuanto más tráfico hay
C) Sí, es obligatorio por ley para cualquier web
D) No, solo se usa en aplicaciones sin base de datos

---

## Pregunta 40

¿Qué parte del esquema sería responsable de devolver finalmente la respuesta combinada (datos dinámicos ya generados) al navegador?

A) El servidor web, tras recibir la respuesta del servidor de aplicaciones
B) El DNS
C) El propio navegador, sin intervención del servidor
D) La base de datos directamente

---

<!-- _class: lead -->
# Bloque 5
## Dominio y DNS en el despliegue

---

## Pregunta 41

¿Qué papel juega el dominio (p. ej. `miapp.com`) en el despliegue de una aplicación?

A) Es el nombre legible que los usuarios escriben para acceder a la aplicación
B) Es el lenguaje de programación usado en el backend
C) Es un tipo de certificado HTTPS
D) Es sinónimo de servidor de aplicaciones

---

## Pregunta 42

¿Qué papel juega el DNS en ese mismo contexto de despliegue?

A) Ejecuta la lógica de negocio de la aplicación
B) Traduce el dominio que escribe el usuario a la IP del servidor donde vive la app
C) Sirve el contenido estático directamente
D) Genera automáticamente el contenido dinámico

---

## Pregunta 43

Si cambias la IP del servidor donde se ejecuta tu aplicación, ¿qué tendrías que actualizar para que el dominio siga apuntando correctamente?

A) El código fuente de la aplicación
B) El registro DNS correspondiente (p. ej. el registro A) para que apunte a la nueva IP
C) El servidor de aplicaciones, pero no el DNS
D) Nada, se actualiza solo sin configuración

---

## Pregunta 44

¿Qué pieza necesitas sí o sí para que un usuario pueda escribir `miapp.com` y llegar a tu aplicación, además de tener la app desplegada?

A) Que el dominio esté registrado y su DNS apunte a la IP correcta del servidor
B) Que el servidor use obligatoriamente Nginx
C) Que la aplicación sea completamente estática
D) Que el servidor de aplicaciones esté escrito en Java

---

## Pregunta 45

¿Qué relación hay entre lo visto sobre DNS en el bloque 2.1 y lo visto hoy sobre despliegue?

A) Ninguna relación, son conceptos independientes
B) El mismo mecanismo DNS que resuelve cualquier nombre de dominio es el que permite que el dominio de tu app apunte a su servidor real
C) El DNS solo se usa para servidores de aplicaciones, no para servidores web
D) El DNS sustituye por completo al servidor web

---

## Pregunta 46

Si olvidas configurar correctamente el DNS de tu dominio tras desplegar la aplicación en un nuevo servidor, ¿qué consecuencia es más probable?

A) Ninguna, el servidor web lo detecta y lo corrige automáticamente
B) Los usuarios que accedan por el dominio no llegarán al servidor correcto (o no llegarán a ninguno)
C) La aplicación se vuelve automáticamente estática
D) El servidor de aplicaciones deja de funcionar internamente

---

## Pregunta 47

¿Qué es más preciso decir sobre la relación entre "dominio" y "servidor"?

A) Son el mismo concepto exacto
B) El dominio es un nombre legible; el servidor es la máquina real donde se ejecuta la aplicación, localizada por su IP gracias al DNS
C) El servidor es el nombre y el dominio es la IP
D) No tienen ninguna relación entre sí

---

## Pregunta 48

¿Puede un mismo dominio apuntar, a través de DNS, a distintas IPs en momentos distintos (p. ej. al migrar de proveedor)?

A) No, un dominio queda fijado para siempre a su primera IP
B) Sí, los registros DNS pueden actualizarse para apuntar a una IP distinta
C) Solo si se cambia también el nombre de dominio
D) Solo si la aplicación es completamente estática

---

## Pregunta 49

¿Qué suele explicar que, tras cambiar un registro DNS, algunos usuarios sigan viendo la versión antigua durante un tiempo?

A) Que el cambio es imposible de propagar
B) La existencia de cachés DNS intermedias que aún no han actualizado la información
C) Que el servidor de aplicaciones está caído
D) Que el contenido es dinámico

---

## Pregunta 50

¿Qué necesita configurarse para que tanto `miapp.com` como `www.miapp.com` lleven al mismo servidor?

A) Nada, funciona siempre automáticamente sin configurar nada
B) Los registros DNS correspondientes para ambos nombres, apuntando al servidor adecuado
C) Solo hace falta configurarlo en el servidor de aplicaciones, nunca en DNS
D) Solo es posible con hosting compartido

---

<!-- _class: lead -->
# Bloque 6
## Tipos de hosting

---

## Pregunta 51

¿Qué caracteriza al hosting compartido?

A) Una máquina física entera dedicada a un único cliente
B) Varias webs de distintos clientes compartiendo un mismo servidor gestionado por el proveedor
C) Recursos bajo demanda facturados por uso exacto
D) Control total sobre el sistema operativo del servidor

---

## Pregunta 52

¿Qué caracteriza a un VPS (servidor privado virtual)?

A) Es una máquina virtual para un único cliente, con control total sobre su propio sistema operativo, aunque comparte hardware físico con otros VPS
B) Es idéntico al hosting compartido
C) Es exclusivamente un servicio de DNS
D) No permite instalar software propio

---

## Pregunta 53

¿Qué caracteriza a un servidor dedicado?

A) Una máquina física entera reservada para un único cliente
B) Un tipo de contenido estático
C) Un servicio exclusivo de DNS
D) Una base de datos distribuida

---

## Pregunta 54

¿Qué caracteriza al hosting en la nube (cloud, tipo AWS/Azure/GCP)?

A) Recursos fijos que no pueden cambiar nunca
B) Recursos bajo demanda, escalables, facturados típicamente por uso
C) Es idéntico a un servidor dedicado clásico
D) Solo sirve para contenido estático

---

## Pregunta 55

Ordenando de menor a mayor control sobre el sistema operativo, ¿cuál sería el orden correcto entre estas cuatro opciones?

A) Hosting compartido, VPS, servidor dedicado, cloud (con recursos gestionados a medida)
B) Servidor dedicado, VPS, hosting compartido, cloud
C) Cloud, servidor dedicado, VPS, hosting compartido
D) VPS, servidor dedicado, hosting compartido, cloud

---

## Pregunta 56

¿Qué ventaja ofrece el hosting compartido frente a un VPS?

A) Mucho más control sobre el sistema operativo
B) Un coste típicamente menor, a cambio de menos control y recursos compartidos
C) Garantiza más potencia que cualquier otra opción
D) Es obligatorio para aplicaciones grandes

---

## Pregunta 57

Un proyecto necesita escalar automáticamente según la demanda, pagando solo por lo que usa. ¿Qué tipo de hosting encaja mejor?

A) Hosting compartido clásico
B) Cloud
C) Servidor dedicado fijo sin elasticidad
D) No existe una opción adecuada

---

## Pregunta 58

¿Por qué una empresa con requisitos muy específicos de hardware podría preferir un servidor dedicado?

A) Porque un servidor dedicado le da el control total de una máquina física completa, sin compartir recursos con nadie
B) Porque es la única opción compatible con HTTP
C) Porque un servidor dedicado no admite instalar Docker
D) Porque el hosting compartido ofrece más control que un dedicado

---

## Pregunta 59

¿Qué tienen en común el VPS y el servidor dedicado, frente al hosting compartido?

A) Ambos dan al cliente un control mucho mayor sobre su propio sistema operativo que el hosting compartido
B) Ambos son gratuitos
C) Ambos son exclusivamente de pago único sin mantenimiento
D) Ninguno de los dos puede alojar aplicaciones dinámicas

---

## Pregunta 60

¿Qué modelo de hosting sería razonable para una pequeña web personal con muy poco tráfico y presupuesto ajustado?

A) Un servidor dedicado de alta gama
B) Hosting compartido
C) Una infraestructura cloud compleja con autoescalado
D) Ninguno, no es posible alojar webs pequeñas

---

<!-- _class: lead -->
# Bloque 7
## Despliegue con contenedores Docker

---

## Pregunta 61

¿Qué ventaja de Docker (visto en la UD1) resulta especialmente relevante a la hora de desplegar en producción?

A) Que las imágenes nunca pueden actualizarse
B) Que el mismo contenedor probado en local es, en esencia, el que se ejecuta en producción
C) Que Docker elimina la necesidad de servidores
D) Que Docker sustituye al DNS

---

## Pregunta 62

En un flujo de despliegue simple con Docker, ¿qué paso suele ir justo después de `docker build`?

A) Subir la imagen a un registry (p. ej. Docker Hub)
B) Borrar el Dockerfile
C) Configurar el DNS por primera vez, siempre en ese momento exacto
D) Eliminar el contenedor en producción

---

## Pregunta 63

¿Qué comandos se ejecutarían típicamente ya en el servidor de producción, tras haber subido la imagen a un registry?

A) `docker build` y `docker commit`
B) `docker pull` y `docker run` (o `docker compose up`)
C) `git clone` únicamente, sin Docker
D) `nslookup` y `dig`

---

## Pregunta 64

¿Qué papel juega un registry (como Docker Hub) en este flujo de despliegue?

A) Ejecuta directamente la aplicación en producción
B) Almacena la imagen construida para que el servidor de producción pueda descargarla
C) Resuelve nombres de dominio
D) Sustituye al servidor web

---

## Pregunta 65

¿Qué relación tiene este flujo de despliegue con lo que se verá en la UD5 (CI/CD)?

A) Ninguna relación
B) En la UD5 se automatiza este mismo flujo (build, subida de imagen, despliegue) para que ocurra solo con cada cambio de código
C) La UD5 elimina la necesidad de usar Docker
D) La UD5 sustituye el despliegue por hosting compartido obligatoriamente

---

## Pregunta 66

¿Qué parte del esquema de despliegue con Docker correspondería al servidor web (Nginx) visto antes en este mismo bloque?

A) Construir la imagen Docker
B) Enrutar el tráfico entrante hacia el contenedor correspondiente
C) Sustituir al registry
D) Generar el Dockerfile automáticamente

---

## Pregunta 67

Si despliegas tu aplicación como contenedor pero olvidas publicar el puerto necesario (`-p`), ¿qué problema es esperable?

A) Ninguno, Docker lo detecta y lo corrige solo
B) El servicio dentro del contenedor no será accesible desde fuera en ese puerto
C) El contenedor deja de arrancar por completo
D) El DNS deja de funcionar para todo el dominio

---

## Pregunta 68

¿Qué ventaja de reproducibilidad aporta usar la misma imagen Docker en desarrollo y en producción?

A) Reduce el riesgo de que algo que funciona en desarrollo falle en producción por diferencias de entorno
B) Garantiza al 100% que no habrá ningún error nunca
C) Elimina la necesidad de servidores de aplicaciones
D) Hace innecesario tener un dominio

---

## Pregunta 69

¿Qué comando usarías en el servidor de producción para traer la última versión de una imagen ya subida a un registry?

A) `docker build`
B) `docker pull`
C) `docker init`
D) `docker logs`

---

## Pregunta 70

¿Qué diferencia hay entre desplegar directamente copiando ficheros a un servidor y desplegar con contenedores?

A) Son exactamente lo mismo en todos los sentidos
B) Con contenedores se empaqueta también el entorno de ejecución (dependencias, configuración), reduciendo diferencias entre máquinas
C) Copiar ficheros siempre es más seguro
D) Los contenedores no pueden ejecutarse en servidores de producción

---

<!-- _class: lead -->
# Bloque 8
## Flujo de despliegue paso a paso

---

## Pregunta 71

En el flujo de despliegue simple visto en teoría, ¿qué es lo primero que debe existir antes de construir ninguna imagen?

A) El dominio ya apuntando por DNS
B) El código de la aplicación y su Dockerfile en el repositorio
C) El certificado HTTPS
D) El servidor de producción ya con Nginx instalado

---

## Pregunta 72

Después de tener el código y el Dockerfile, ¿cuál es el siguiente paso lógico del flujo visto?

A) Construir la imagen con `docker build`
B) Configurar el DNS
C) Contratar un servidor dedicado obligatoriamente
D) Escribir el banco de preguntas de test

---

## Pregunta 73

Tras construir la imagen, ¿qué paso permite que el servidor de producción pueda acceder a ella sin copiar ficheros manualmente?

A) Subirla a un registry
B) Borrarla de tu máquina local
C) Renombrar el Dockerfile
D) Cambiar el dominio

---

## Pregunta 74

Una vez la imagen está en el registry y se ha hecho `docker pull` en el servidor, ¿qué falta para que la aplicación esté realmente accesible?

A) Nada más, ya está accesible sin ejecutar nada
B) Arrancar el contenedor (`docker run` o `docker compose up`) y que el servidor web enrute el tráfico hacia él
C) Volver a escribir el código desde cero en el servidor
D) Eliminar el registry

---

## Pregunta 75

¿Qué papel tiene el servidor web (Nginx) al final de este flujo, una vez el contenedor ya está en marcha?

A) Construir una nueva imagen automáticamente
B) Enrutar las peticiones entrantes del dominio hacia el contenedor correspondiente
C) Sustituir el contenido del Dockerfile
D) Eliminar el contenedor cada cierto tiempo

---

## Pregunta 76

Si se despliega una nueva versión de la imagen, ¿qué pasos del flujo visto habría que repetir como mínimo?

A) Ninguno, se actualiza solo
B) Build de la nueva imagen, subirla al registry, y en el servidor hacer pull y volver a arrancar el contenedor con la nueva versión
C) Solo cambiar el DNS
D) Solo reiniciar el servidor web, sin tocar la imagen

---

## Pregunta 77

¿Qué ocurriría si en el servidor de producción ejecutas `docker run` con una imagen que no coincide con la última subida al registry?

A) Se ejecutaría igualmente esa versión concreta de la imagen, no necesariamente la más reciente
B) Docker la actualiza automáticamente a la última sin avisar
C) Es imposible, Docker lo impide siempre
D) El DNS corrige automáticamente la discrepancia

---

## Pregunta 78

¿Qué relación hay entre el Dockerfile del repositorio y la imagen que termina ejecutándose en producción?

A) Ninguna relación directa
B) El Dockerfile son las instrucciones a partir de las cuales se construye (`docker build`) la imagen que luego se despliega
C) El Dockerfile sustituye directamente al servidor web
D) El Dockerfile solo se usa en desarrollo, nunca influye en producción

---

## Pregunta 79

En este flujo, ¿en qué momento entraría en juego el DNS para que un usuario final pueda llegar a la aplicación ya desplegada?

A) Nunca, el DNS no interviene en absoluto en el despliegue
B) El dominio debe tener sus registros DNS apuntando a la IP del servidor donde se ha desplegado el contenedor
C) Solo si se usa hosting compartido
D) Solo si no se usa Docker

---

## Pregunta 80

¿Qué parte de este flujo se automatiza específicamente con herramientas de CI/CD, como se verá en la UD5?

A) Nada, la UD5 trata un tema completamente distinto
B) La secuencia completa (build, subida al registry, despliegue) para que se dispare sola con cada cambio de código
C) Solo la resolución de nombres DNS
D) Solo la redacción del Dockerfile

---

<!-- _class: lead -->
# Bloque 9
## Esquema completo petición → despliegue

---

## Pregunta 81

En el esquema completo visto en teoría, ¿qué es lo primero que ocurre cuando un usuario escribe `miapp.com` en su navegador?

A) El servidor de aplicaciones ejecuta código inmediatamente
B) El DNS resuelve el dominio a la IP del servidor
C) Se genera directamente el contenido dinámico sin más pasos
D) Se descarga automáticamente una imagen Docker

---

## Pregunta 82

Tras resolver la IP, ¿a qué suele llegar primero la petición en el esquema típico de producción?

A) Directamente a la base de datos
B) Al servidor web (p. ej. Nginx), que escucha en el puerto correspondiente
C) Al registry de Docker
D) Al servidor DNS de nuevo

---

## Pregunta 83

Si la petición es a una ruta de recursos estáticos, ¿qué hace el servidor web en ese esquema?

A) La reenvía siempre al servidor de aplicaciones
B) La responde directamente
C) La descarta
D) Consulta antes el registry de Docker

---

## Pregunta 84

Si la petición es a una ruta dinámica (p. ej. `/api/productos`), ¿qué hace el servidor web?

A) La responde directamente sin más
B) La reenvía a un contenedor con el servidor de aplicaciones correspondiente
C) La convierte en estática automáticamente
D) La elimina

---

## Pregunta 85

Una vez el servidor de aplicaciones genera la respuesta dinámica (p. ej. JSON tras consultar la base de datos), ¿qué ocurre después en el esquema?

A) Se pierde, nunca llega al usuario
B) Vuelve al servidor web, que la devuelve finalmente al navegador
C) Se guarda permanentemente sin enviarse
D) Sustituye al DNS para futuras peticiones

---

## Pregunta 86

¿Qué puerto es habitual que use el servidor web para atender tráfico HTTPS en este esquema?

A) 21
B) 25
C) 443
D) 3306

---

## Pregunta 87

¿Qué papel tiene la base de datos en el esquema completo?

A) Resolver nombres de dominio
B) Ser consultada por el servidor de aplicaciones para generar contenido dinámico
C) Servir el contenido estático
D) Sustituir al servidor web

---

## Pregunta 88

¿Qué bloques de contenidos de la asignatura se combinan en este esquema completo, según lo explicado en teoría?

A) Solo lo visto en esta misma semana, sin relación con nada más
B) DNS y HTTP del bloque 2.1, Docker de la UD1, y lo que se ampliará en UD3/UD4/UD5
C) Únicamente contenidos de UD5
D) Ninguno, es un esquema completamente nuevo sin relación con el resto del curso

---

## Pregunta 89

¿Por qué se insiste en que este esquema "no es una caja negra"?

A) Porque es un esquema inventado sin relación con la realidad
B) Porque cada pieza (DNS, HTTP, Docker, servidor web, servidor de aplicaciones) es algo que ya se ha visto o se profundizará pronto en UDs concretas
C) Porque no se puede explicar con palabras
D) Porque solo se aplica a aplicaciones muy pequeñas

---

## Pregunta 90

¿Qué UD trata en detalle los servidores de aplicaciones vistos de forma introductoria en este esquema?

A) UD1
B) UD2
C) UD3
D) UD4

---

<!-- _class: lead -->
# Bloque 10
## Síntesis y relación entre bloques/UDs

---

## Pregunta 91

¿Qué diferencia principal separa lo visto en el bloque 2.1 de lo visto en el bloque 2.2?

A) El 2.1 trata cómo se organiza una aplicación (capas, microservicios...) y el 2.2 trata dónde vive y quién la sirve físicamente
B) No hay ninguna diferencia, tratan exactamente lo mismo
C) El 2.1 es solo práctica y el 2.2 solo teoría
D) El 2.2 no tiene ninguna relación con HTTP

---

## Pregunta 92

¿Qué relación hay entre "servidor web vs. servidor de aplicaciones" (2.2) y "arquitectura en capas" (2.1)?

A) Ninguna relación posible
B) La capa de presentación y la de negocio de una arquitectura en capas pueden, en la práctica, ejecutarse en un servidor web y uno de aplicaciones respectivamente
C) Son términos exactamente sinónimos
D) El servidor de aplicaciones sustituye siempre a todas las capas

---

## Pregunta 93

¿Qué conexión hay entre microservicios (visto en 2.1) y despliegue con contenedores (visto en 2.2)?

A) Ninguna, son conceptos de asignaturas distintas
B) Cada microservicio suele desplegarse en su propio contenedor, usando el flujo de despliegue visto en 2.2
C) Los microservicios no pueden desplegarse nunca con Docker
D) El despliegue con contenedores solo aplica a monolitos

---

## Pregunta 94

Si una aplicación usa arquitectura Hexagonal (2.1) y se despliega como contenedor Docker detrás de Nginx (2.2), ¿son compatibles ambas decisiones?

A) No, son mutuamente excluyentes
B) Sí, son decisiones de niveles distintos (organización interna del código vs. infraestructura de despliegue) y se combinan sin problema
C) Solo si se elimina el servidor web
D) Solo si la aplicación es completamente estática

---

## Pregunta 95

¿Qué UD retoma y profundiza específicamente la configuración de Apache/Nginx introducida en el bloque 2.2?

A) UD1
B) UD3
C) UD4
D) UD5

---

## Pregunta 96

¿Qué UD retoma y profundiza específicamente los servidores de aplicaciones introducidos en el bloque 2.2?

A) UD1
B) UD2
C) UD3
D) UD4

---

## Pregunta 97

¿Qué UD automatiza el flujo de despliegue con Docker visto de forma manual en el bloque 2.2?

A) UD1
B) UD3
C) UD4
D) UD5

---

## Pregunta 98

¿Qué papel cumple el DNS tanto en el bloque 2.1 (fundamentos web) como en el 2.2 (despliegue)?

A) En 2.1 resuelve nombres para cualquier navegación; en 2.2 es la pieza que permite que el dominio de tu app apunte al servidor donde la has desplegado
B) En 2.1 no se menciona el DNS en absoluto
C) En 2.2 el DNS deja de ser necesario por usar Docker
D) El DNS solo aplica a contenido estático

---

## Pregunta 99

De todo lo visto en el bloque 2.2, ¿qué pieza sería imprescindible tanto si usas hosting compartido como si usas Docker en un VPS?

A) Ninguna, son flujos totalmente independientes sin nada en común
B) Tener un dominio con DNS apuntando correctamente al punto de entrada de la aplicación
C) Usar obligatoriamente Tomcat
D) Evitar por completo el uso de servidores web

---

## Pregunta 100

En resumen, ¿qué pregunta responde principalmente el bloque 2.2 que no respondía el 2.1?

A) Cómo se organiza el código de la aplicación por dentro
B) Dónde se ejecuta físicamente la aplicación y cómo llega hasta ahí una petición real de un usuario
C) Qué es un método HTTP
D) Qué es una cookie de sesión
