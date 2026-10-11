---
marp: true
theme: default
paginate: true
backgroundColor: white
footer: 'Despliegue de Aplicaciones Web (0614) · UD2: Arquitecturas Web'
layout: default
title: "Arquitecturas Web — Bloque 2.1: Fundamentos web (Banco de test)"
permalink: /web/semana-1/test/
---

<!-- _class: lead -->
# arquitecturas web
## Test de repaso — bloque 2.1: fundamentos web
### 100 preguntas · 4 opciones, 1 correcta

---

## Cómo usar este banco de preguntas

- Cada diapositiva contiene una pregunta con 4 opciones (A-D), solo 1 correcta.
- No incluye las respuestas: úsalo para practicar de cara al cuestionario. TODAS las preguntas del cuestionario saldrán de este banco de preguntas.

---

<!-- _class: lead -->
# Bloque 1
## Cliente-servidor y métodos HTTP

---

## Pregunta 1

En el modelo cliente-servidor de la web, ¿quién inicia típicamente la comunicación?

A) El servidor, enviando datos sin que nadie los pida
B) El cliente, haciendo una petición
C) Ambos a la vez, siempre de forma simultánea
D) Ninguno: la comunicación la inicia el DNS

---

## Pregunta 2

¿Qué método HTTP se considera el adecuado para pedir un recurso sin modificar nada en el servidor?

A) POST
B) DELETE
C) GET
D) PUT

---

## Pregunta 3

Un formulario web envía los datos de un usuario nuevo para crear su cuenta. ¿Qué método HTTP es el más apropiado?

A) GET
B) POST
C) HEAD
D) OPTIONS

---

## Pregunta 4

¿Qué diferencia hay, en esencia, entre `PUT` y `PATCH`?

A) No hay diferencia, son sinónimos
B) `PUT` reemplaza el recurso completo; `PATCH` lo modifica parcialmente
C) `PATCH` solo sirve para borrar recursos
D) `PUT` nunca lleva cuerpo en la petición

---

## Pregunta 5

¿Qué método HTTP se usa típicamente para eliminar un recurso?

A) GET
B) DELETE
C) HEAD
D) CONNECT

---

## Pregunta 6

Al enviar un formulario con el método GET, ¿dónde terminan apareciendo los datos introducidos?

A) En el cuerpo de la petición, ocultos
B) En la URL, como parte de la query string
C) Nunca llegan al servidor
D) En una cabecera llamada `Body`

---

## Pregunta 7

¿Cuál de estas afirmaciones sobre GET y POST es correcta?

A) GET es más adecuado para enviar contraseñas porque es más rápido
B) POST permite enviar más cantidad de datos y no los deja visibles en la URL
C) GET y POST son exactamente intercambiables en todos los casos
D) POST no puede usarse para enviar ficheros

---

## Pregunta 8

¿Qué método HTTP devuelve solo las cabeceras de la respuesta, sin el cuerpo?

A) HEAD
B) GET
C) TRACE
D) OPTIONS

---

## Pregunta 9

Una API REST bien diseñada usa `GET /productos/7` para consultar un producto. ¿Qué método usarías para actualizar completamente ese producto?

A) GET /productos/7
B) POST /productos
C) PUT /productos/7
D) DELETE /productos/7

---

## Pregunta 10

¿Por qué se dice que `GET` debería ser una operación "segura" (sin efectos secundarios)?

A) Porque usa HTTPS obligatoriamente
B) Porque, en teoría, repetir la misma petición GET no debería cambiar el estado del servidor
C) Porque no puede fallar nunca
D) Porque no puede llevar parámetros

---

<!-- _class: lead -->
# Bloque 2
## Códigos de estado HTTP

---

## Pregunta 11

¿A qué rango de códigos de estado HTTP pertenece un error causado por el propio cliente (p. ej. una URL mal escrita)?

A) 2xx
B) 3xx
C) 4xx
D) 5xx

---

## Pregunta 12

Un servidor sufre una caída interna al procesar una petición válida del cliente. ¿Qué rango de código de estado es esperable?

A) 2xx
B) 3xx
C) 4xx
D) 5xx

---

## Pregunta 13

¿Qué código de estado indica que una petición se completó con éxito y no hay contenido que devolver?

A) 200
B) 201
C) 204
D) 404

---

## Pregunta 14

Tras enviar un formulario que crea un nuevo recurso, ¿qué código de estado sería el más preciso devolver?

A) 200
B) 201
C) 204
D) 400

---

## Pregunta 15

Visitas `http://miempresa.com` y el servidor te lleva automáticamente a `https://miempresa.com`. ¿Qué tipo de código de estado está implicado?

A) 2xx
B) 3xx
C) 4xx
D) 5xx

---

## Pregunta 16

¿Qué código de estado verías si intentas acceder a una sección que exige haber iniciado sesión y no lo has hecho?

A) 200
B) 401
C) 403
D) 500

---

## Pregunta 17

Ya has iniciado sesión, pero intentas entrar al panel de administración sin tener permisos de administrador. ¿Qué código es más apropiado?

A) 401
B) 403
C) 404
D) 503

---

## Pregunta 18

¿Qué código de estado HTTP se asocia habitualmente a "recurso no encontrado"?

A) 400
B) 404
C) 410
D) 500

---

## Pregunta 19

Un servidor está temporalmente saturado y no puede atender más peticiones. ¿Qué código de estado encajaría mejor?

A) 404
B) 409
C) 503
D) 301

---

## Pregunta 20

¿Qué significa, en general, un código de estado que empieza por `5`?

A) Un error cometido por el cliente al construir la petición
B) Una redirección
C) Un error ocurrido dentro del servidor al procesar una petición válida
D) Que la petición fue exitosa

---

<!-- _class: lead -->
# Bloque 3
## Cabeceras HTTP

---

## Pregunta 21

¿Qué cabecera HTTP indica al cliente cómo debe interpretar el cuerpo de la respuesta (HTML, JSON, imagen...)?

A) Content-Type
B) Host
C) User-Agent
D) Accept-Language

---

## Pregunta 22

¿Qué cabecera de petición identifica el dominio al que va dirigida la petición (importante si un servidor aloja varios sitios)?

A) Host
B) Content-Length
C) Set-Cookie
D) ETag

---

## Pregunta 23

¿Qué cabecera usa el servidor para indicarle al navegador que guarde una cookie?

A) Cookie
B) Set-Cookie
C) Authorization
D) Accept

---

## Pregunta 24

Un cliente envía `Accept: application/json` en su petición. ¿Qué está indicando?

A) Que solo acepta recibir la respuesta en formato JSON
B) Que está enviando datos en JSON
C) Que quiere forzar una redirección
D) Que no quiere recibir cookies

---

## Pregunta 25

¿Qué cabecera suele llevar el token de autenticación en muchas APIs modernas?

A) Authorization
B) Host
C) Referer
D) Content-Length

---

## Pregunta 26

¿Para qué sirve la cabecera `Content-Length` en una respuesta HTTP?

A) Indica el idioma del contenido
B) Indica el tamaño en bytes del cuerpo de la respuesta
C) Indica cuántas cookies se han enviado
D) Indica el método HTTP usado

---

## Pregunta 27

¿Qué cabecera de petición identifica, de forma orientativa, el navegador o cliente que hace la petición?

A) User-Agent
B) Host
C) Set-Cookie
D) ETag

---

## Pregunta 28

Quieres que el servidor sepa que la petición trae un cuerpo en formato JSON. ¿Qué cabecera deberías enviar en la petición?

A) Accept: application/json
B) Content-Type: application/json
C) Host: application/json
D) Cookie: application/json

---

## Pregunta 29

¿Qué diferencia hay entre las cabeceras `Cookie` y `Set-Cookie`?

A) Son exactamente la misma cabecera con dos nombres
B) `Cookie` la envía el cliente al servidor; `Set-Cookie` la envía el servidor al cliente
C) `Set-Cookie` solo existe en HTTPS
D) `Cookie` solo puede usarse una vez por sesión

---

## Pregunta 30

Si una respuesta HTTP no incluye la cabecera `Content-Type`, ¿qué problema puede causar en el cliente?

A) Ninguno, es opcional y nunca afecta nada
B) El cliente puede no saber cómo interpretar correctamente el cuerpo recibido
C) La petición se convierte automáticamente en POST
D) El servidor rechaza la petición

---

<!-- _class: lead -->
# Bloque 4
## URLs y DNS

---

## Pregunta 31

En la URL `https://tienda.com:8443/productos/3?color=rojo#opiniones`, ¿qué parte es `8443`?

A) El host
B) El puerto
C) La ruta
D) El fragmento

---

## Pregunta 32

En la misma URL, ¿qué parte es `color=rojo`?

A) El fragmento
B) El host
C) La query string (parámetros)
D) El esquema

---

## Pregunta 33

¿Qué parte de una URL nunca se envía al servidor en la petición HTTP?

A) El host
B) La ruta
C) El fragmento (lo que va después de #)
D) El puerto

---

## Pregunta 34

Si una URL no especifica puerto y usa `https://`, ¿qué puerto se usa por defecto?

A) 21
B) 80
C) 443
D) 8080

---

## Pregunta 35

¿Qué función cumple el DNS en la navegación web?

A) Cifra el tráfico HTTP
B) Traduce nombres de dominio a direcciones IP
C) Comprime las imágenes de una página
D) Gestiona las sesiones de usuario

---

## Pregunta 36

La primera vez que visitas un dominio tarda un poco más en cargar que las siguientes veces, aun con la misma conexión. ¿Qué explicación es más plausible desde el punto de vista de DNS?

A) La segunda vez el servidor pesa menos
B) La resolución DNS puede quedar cacheada tras la primera consulta
C) El navegador borra la caché DNS automáticamente
D) HTTPS solo funciona a partir de la segunda visita

---

## Pregunta 37

Si registras un dominio nuevo y apuntas sus registros DNS a un servidor, ¿por qué el cambio puede tardar en verse para todo el mundo?

A) Porque las direcciones IP cambian cada segundo
B) Porque hay cachés DNS intermedias que tardan en actualizarse
C) Porque HTTP no admite dominios nuevos
D) Porque hace falta reiniciar el navegador de cada visitante manualmente

---

## Pregunta 38

¿Qué comando de terminal usarías para consultar a qué IP resuelve un dominio?

A) ping -t
B) curl -X POST
C) nslookup (o dig)
D) docker inspect

---

## Pregunta 39

¿Cuál de estas NO es una parte estándar de una URL?

A) Esquema
B) Host
C) Query string
D) Docker tag

---

## Pregunta 40

¿Qué ocurre si cambias solo el fragmento de una URL (la parte después de `#`) y recargas?

A) Se envía una nueva petición HTTP completa al servidor
B) El navegador la gestiona localmente, sin que el servidor la reciba como tal
C) El servidor devuelve siempre un error 404
D) Se invalida automáticamente la sesión

---

<!-- _class: lead -->
# Bloque 5
## Estado, cookies y sesiones

---

## Pregunta 41

¿Por qué se dice que HTTP es un protocolo "sin estado" (stateless)?

A) Porque no puede transportar datos binarios
B) Porque cada petición es independiente y el servidor no recuerda las anteriores por sí solo
C) Porque no puede usarse con HTTPS
D) Porque no tiene códigos de estado

---

## Pregunta 42

¿Qué mecanismo permite que un servidor "recuerde" que ya iniciaste sesión en peticiones posteriores?

A) El propio protocolo HTTP, que guarda memoria por defecto
B) Cookies, junto con un estado de sesión guardado en el servidor
C) El DNS, que asocia tu IP a tu usuario
D) El método HTTP usado

---

## Pregunta 43

¿Qué suele contener realmente la cookie de sesión de un usuario autenticado, en vez de todos sus datos?

A) La contraseña en texto plano
B) Un identificador de sesión, que el servidor usa para localizar el estado real
C) El historial completo de navegación
D) El código fuente de la aplicación

---

## Pregunta 44

Si un usuario borra manualmente las cookies de su navegador, ¿qué efecto típico tiene sobre una sesión iniciada?

A) Ninguno, la sesión sigue activa igual
B) Probablemente se cierre su sesión, al perder el identificador que la vinculaba
C) Se elimina su cuenta de usuario
D) El servidor deja de responder a ese dominio

---

## Pregunta 45

¿Dónde se guarda habitualmente el estado "real" de una sesión (usuario, carrito, permisos), y no solo su identificador?

A) Únicamente en la cookie del navegador
B) En el servidor (memoria o base de datos), asociado al ID de sesión
C) En la caché DNS
D) En la URL de cada petición

---

## Pregunta 46

¿Qué problema de fondo resuelven las cookies de sesión, dado que HTTP no guarda estado por sí mismo?

A) Permiten cifrar la conexión
B) Permiten que el servidor reconozca al mismo cliente a lo largo de varias peticiones
C) Permiten resolver nombres de dominio
D) Permiten comprimir las respuestas

---

## Pregunta 47

Dos pestañas del mismo navegador visitan el mismo sitio donde ya iniciaste sesión. ¿Qué suele ocurrir con la sesión?

A) Cada pestaña tiene una sesión completamente distinta e incompatible
B) Normalmente comparten la misma cookie de sesión, al ser el mismo navegador y dominio
C) Es imposible abrir el mismo sitio en dos pestañas
D) El servidor bloquea automáticamente la segunda pestaña

---

## Pregunta 48

¿Qué significa, en la práctica, que una cookie tenga marcada la opción `HttpOnly`?

A) Que solo puede usarse en peticiones HTTP, nunca HTTPS
B) Que no puede leerse mediante JavaScript, lo que reduce el riesgo de robo por scripts maliciosos
C) Que caduca en una hora exacta siempre
D) Que el servidor la ignora por completo

---

## Pregunta 49

Si un sistema no usa cookies ni ningún otro mecanismo de estado, ¿qué consecuencia tendría para el usuario al navegar entre páginas?

A) Ninguna, HTTP recordaría igualmente que ya inició sesión
B) El servidor no podría distinguir, por sí mismo, que las peticiones vienen del mismo usuario que ya se autenticó
C) La navegación sería más rápida, sin ningún efecto negativo
D) Las URLs dejarían de funcionar

---

## Pregunta 50

¿Qué alternativa a las cookies de sesión tradicionales se usa habitualmente en APIs, basada en un token que el propio cliente guarda y reenvía (p. ej. en la cabecera `Authorization`)?

A) DNS tokens
B) JWT (JSON Web Token) u otros tokens similares
C) Content-Length tokens
D) Fragmentos de URL

---

<!-- _class: lead -->
# Bloque 6
## Arquitecturas en capas

---

## Pregunta 51

¿Cuál es el problema típico de meter interfaz, lógica de negocio y acceso a datos en un único bloque de código?

A) Que el código ocupa menos espacio en disco
B) Que cualquier cambio obliga a tocar y entender todo el bloque a la vez, dificultando el mantenimiento
C) Que ya no se puede ejecutar en un servidor
D) Que deja de funcionar con HTTP

---

## Pregunta 52

¿Qué caracteriza a una arquitectura de 1 sola capa?

A) Interfaz, lógica y datos están separados en máquinas distintas
B) Todo (interfaz, lógica y datos) se ejecuta junto, típicamente en la misma máquina y bloque de código
C) Es exclusiva de aplicaciones con microservicios
D) Requiere obligatoriamente una base de datos distribuida

---

## Pregunta 53

En una arquitectura de 2 capas, como una app de escritorio que se conecta directamente a una base de datos remota, ¿qué suele seguir mezclado?

A) La interfaz y la red, que son indistinguibles
B) La lógica de negocio y el acceso a datos, en el mismo bloque
C) El DNS y el HTTP
D) Los microservicios y el monolito

---

## Pregunta 54

¿Cuáles son las tres capas típicas de una arquitectura de 3 capas?

A) Presentación, negocio y datos
B) Cliente, servidor y base de datos únicamente sin lógica
C) Frontend, backend y DNS
D) HTTP, HTTPS y FTP

---

## Pregunta 55

¿Qué responsabilidad corresponde a la capa de negocio en una arquitectura de 3 capas?

A) Mostrar el HTML al usuario
B) Aplicar las reglas, validaciones y cálculos propios de la aplicación
C) Almacenar físicamente los datos en disco
D) Resolver nombres de dominio

---

## Pregunta 56

Si quieres cambiar el motor de base de datos de una aplicación bien organizada en 3 capas, ¿qué capa debería, idealmente, verse menos afectada?

A) La capa de presentación
B) La capa de negocio
C) Ambas por igual, siempre
D) Ninguna capa se ve afectada nunca

---

## Pregunta 57

¿Qué es la arquitectura N-capas en relación con la de 3 capas?

A) Una tecnología completamente distinta e incompatible
B) Una generalización: se pueden añadir capas intermedias según haga falta, siendo 3 capas el caso más común
C) Un sinónimo exacto de microservicios
D) Una arquitectura exclusiva para bases de datos NoSQL

---

## Pregunta 58

¿Cuál de estas secuencias describe mejor un flujo típico en una arquitectura N-capas con una capa de API intermedia?

A) Presentación → API/servicios → negocio → datos → base de datos
B) Base de datos → presentación → negocio
C) Negocio → presentación → base de datos → API
D) API → base de datos → presentación (sin negocio)

---

## Pregunta 59

¿Qué ventaja aporta poder escalar cada capa por separado?

A) Permite añadir más servidores donde realmente hace falta (p. ej. presentación con mucho tráfico) sin duplicar innecesariamente otras capas
B) Elimina la necesidad de tener una capa de datos
C) Hace innecesario el uso de HTTP
D) Impide que la aplicación falle nunca

---

## Pregunta 60

Un equipo divide su trabajo: unos en la interfaz, otros en las reglas de negocio, otros en el acceso a datos. ¿Qué arquitectura facilita este reparto?

A) Arquitectura de 1 capa
B) Arquitectura en capas (3 o N capas)
C) Arquitectura sin servidor en absoluto
D) No depende de la arquitectura

---

<!-- _class: lead -->
# Bloque 7
## Monolito, SOA y microservicios

---

## Pregunta 61

¿Qué significa que una aplicación esté "bien organizada en capas" internamente, incluso si se despliega como monolito?

A) Que obligatoriamente usa microservicios
B) Que, aunque se despliegue como una sola unidad, su código separa presentación, negocio y datos con claridad
C) Que no tiene base de datos
D) Que no puede escalar nunca

---

## Pregunta 62

¿Cuál de estas NO es una ventaja típica de separar en capas?

A) Facilitar el mantenimiento
B) Facilitar el trabajo en equipo por especialidad
C) Permitir escalar partes concretas
D) Garantizar automáticamente cero errores en producción

---

## Pregunta 63

En una arquitectura de 3 capas, ¿qué parte ve directamente el usuario final?

A) La capa de negocio
B) La capa de datos
C) La capa de presentación
D) Ninguna, el usuario nunca ve ninguna capa

---

## Pregunta 64

¿Qué relación hay entre "capas" y "arquitecturas a gran escala" como monolito o microservicios?

A) Son exactamente lo mismo
B) Las capas organizan el código dentro de una pieza; monolito/microservicios deciden cómo se reparte el sistema completo en piezas desplegables
C) Las capas sustituyen a los microservicios siempre
D) No tienen ninguna relación posible

---

## Pregunta 65

Separar la capa de datos del resto permite, entre otras cosas, cambiar de base de datos relacional a NoSQL con menor impacto. ¿Por qué?

A) Porque las capas de negocio y presentación no deberían depender de los detalles concretos de cómo se almacenan los datos
B) Porque NoSQL no necesita ningún tipo de capa de datos
C) Porque las capas eliminan la necesidad de bases de datos
D) Porque las capas obligan a usar siempre la misma base de datos

---

## Pregunta 66

¿Cómo se despliega típicamente un monolito?

A) Como muchos servicios pequeños e independientes
B) Como una sola unidad que incluye toda la aplicación
C) Solo como funciones serverless
D) Nunca se despliega, solo se ejecuta en el navegador

---

## Pregunta 67

¿Es correcto decir que "monolito" significa "código desordenado"?

A) Sí, por definición un monolito siempre tiene código desordenado
B) No: un monolito puede estar perfectamente organizado en capas por dentro; "monolito" se refiere a cómo se despliega, no a su calidad interna
C) Sí, porque no admite ningún tipo de organización interna
D) No, porque los monolitos no tienen código, solo configuración

---

## Pregunta 68

¿Cuál es la principal desventaja de un monolito a medida que el proyecto crece mucho?

A) No puede tener base de datos
B) Cualquier cambio pequeño obliga a volver a desplegar toda la aplicación
C) No puede ejecutarse en un servidor real
D) No permite usar HTTP

---

## Pregunta 69

¿Qué caracteriza a una arquitectura SOA (Service-Oriented Architecture)?

A) El sistema se divide en servicios que se comunican entre sí, a menudo mediante un middleware centralizado
B) Todo el sistema es un único bloque indivisible
C) Es idéntica a una arquitectura de 1 capa
D) No permite ningún tipo de comunicación entre componentes

---

## Pregunta 70

¿Qué papel juega el ESB (Enterprise Service Bus) en una arquitectura SOA típica?

A) Es la base de datos principal del sistema
B) Actúa como middleware centralizado de comunicación entre servicios
C) Es el navegador del cliente
D) Es un tipo de contenedor Docker

---

<!-- _class: lead -->
# Bloque 8
## Event-driven, serverless y P2P

---

## Pregunta 71

¿Qué caracteriza principalmente a una arquitectura de microservicios?

A) Servicios pequeños e independientes, que se despliegan por separado, cada uno con su propia responsabilidad
B) Un único proceso que hace absolutamente todo
C) La ausencia total de bases de datos
D) Que solo puede ejecutarse en una máquina física

---

## Pregunta 72

¿Por qué los microservicios encajan especialmente bien con Docker?

A) Porque Docker obliga a usar microservicios
B) Porque cada microservicio puede empaquetarse y ejecutarse de forma aislada en su propio contenedor
C) Porque los microservicios no necesitan red
D) Porque Docker elimina la necesidad de bases de datos

---

## Pregunta 73

Un equipo pequeño (3 personas) va a construir un MVP sencillo con poco tiempo. ¿Qué arquitectura suele ser más razonable al principio?

A) Microservicios desde el primer día
B) Un monolito bien organizado en capas
C) SOA con ESB corporativo
D) Una arquitectura puramente P2P

---

## Pregunta 74

¿Qué ventaja ofrecen los microservicios frente a un monolito en cuanto a fallos?

A) Un fallo en un microservicio nunca afecta a nada más, bajo ninguna circunstancia
B) Un fallo puede quedar más aislado en el servicio afectado, en lugar de tumbar toda la aplicación
C) Los microservicios no pueden fallar nunca
D) El monolito aísla mejor los fallos que los microservicios

---

## Pregunta 75

¿Qué complejidad adicional suelen introducir los microservicios respecto a un monolito?

A) Ninguna, son siempre más simples
B) La necesidad de coordinar, desplegar y monitorizar múltiples servicios independientes que se comunican entre sí
C) Dejan de necesitar ningún tipo de red
D) Eliminan la necesidad de tener bases de datos

---

## Pregunta 76

¿En qué se diferencian principalmente SOA y microservicios?

A) No hay ninguna diferencia, son sinónimos exactos
B) SOA suele usar servicios más grandes y un middleware centralizado (ESB); los microservicios tienden a servicios más pequeños y autónomos
C) Microservicios es una tecnología anterior a SOA
D) SOA no permite ningún tipo de comunicación entre servicios

---

## Pregunta 77

¿Por qué podría una empresa con muchos sistemas heredados optar por SOA en vez de microservicios?

A) Porque SOA es incompatible con cualquier sistema antiguo
B) Porque SOA facilita integrar sistemas heredados distintos a través de un middleware común
C) Porque SOA no requiere ningún tipo de comunicación entre sistemas
D) Porque los sistemas heredados no pueden tener servicios

---

## Pregunta 78

Si cada microservicio de un sistema tiene su propia base de datos independiente, ¿qué ventaja de aislamiento se consigue?

A) Un cambio en el esquema de datos de un servicio no obliga a tocar los demás servicios directamente
B) Todos los servicios comparten obligatoriamente los mismos datos
C) Las bases de datos dejan de necesitar copias de seguridad
D) Se elimina la necesidad de desplegar cada servicio por separado

---

## Pregunta 79

¿Cómo se comunican típicamente los componentes en una arquitectura orientada a eventos?

A) Llamándose directamente por su IP, sin intermediarios
B) Publicando y reaccionando a eventos a través de una cola o broker de mensajes
C) Compartiendo una única base de datos sin ningún tipo de mensaje
D) No se comunican entre sí en ningún caso

---

## Pregunta 80

¿Qué ventaja de desacoplamiento aporta una arquitectura orientada a eventos?

A) El que publica un evento no necesita saber quién (ni cuántos) lo van a consumir
B) Obliga a que emisor y receptor estén siempre en el mismo servidor
C) Elimina la necesidad de cualquier tipo de red
D) Hace innecesarios los microservicios

---

<!-- _class: lead -->
# Bloque 9
## Patrones de diseño interno (I)

---

## Pregunta 81

En un sistema de e-commerce con arquitectura orientada a eventos, al confirmarse un pago se publica un evento "pago confirmado". ¿Qué módulos podrían reaccionar a él?

A) Ninguno, los eventos no pueden tener más de un receptor
B) Potencialmente varios: envío de email, actualización de stock, generación de factura, todos de forma desacoplada
C) Solo el propio módulo de pagos
D) Solo el servidor DNS

---

## Pregunta 82

¿Qué significa realmente "serverless" (FaaS) para quien desarrolla la aplicación?

A) Que la aplicación se ejecuta sin ningún tipo de servidor físico en el mundo
B) Que no gestiona directamente los servidores: la plataforma los aprovisiona, escala y mantiene
C) Que obliga a usar siempre arquitectura P2P
D) Que no se puede cobrar por su uso

---

## Pregunta 83

¿Cuál es un modelo de facturación habitual en plataformas serverless/FaaS?

A) Se paga una cuota fija mensual por tener el servidor encendido, se use o no
B) Se paga principalmente por el tiempo de ejecución real de las funciones
C) Es siempre gratuito, sin ningún coste
D) Se paga por cada dirección IP registrada

---

## Pregunta 84

¿Qué tipo de carga de trabajo encaja especialmente bien con serverless/FaaS?

A) Un servicio con tráfico constante y perfectamente predecible las 24 horas
B) Tareas puntuales o con picos de carga impredecibles
C) Una base de datos que debe estar siempre encendida
D) Un sistema operativo completo

---

## Pregunta 85

¿Qué caracteriza a una arquitectura peer-to-peer (P2P)?

A) Existe siempre un único servidor central que controla todo
B) Cada nodo puede actuar a la vez como cliente y como servidor, sin un servidor central claro
C) Es idéntica a una arquitectura cliente-servidor clásica
D) Solo puede tener dos nodos como máximo

---

## Pregunta 86

¿Qué tipo de aplicación es un ejemplo clásico de arquitectura P2P?

A) Una tienda online corporativa típica
B) Una red de compartición de ficheros como BitTorrent
C) Una API REST de un banco
D) Un servidor de correo corporativo

---

## Pregunta 87

¿Por qué la arquitectura P2P es poco habitual en aplicaciones de negocio "normales" (tiendas online, bancos, etc.)?

A) Porque es técnicamente imposible de implementar
B) Porque este tipo de negocios suelen necesitar un control centralizado de datos, usuarios y transacciones que el modelo P2P no ofrece de forma natural
C) Porque P2P no puede usar internet
D) Porque P2P solo funciona con un único usuario

---

## Pregunta 88

Una arquitectura orientada a eventos y una arquitectura de microservicios, ¿pueden combinarse?

A) No, son mutuamente excluyentes
B) Sí: es habitual que microservicios se comuniquen entre sí mediante eventos para reducir el acoplamiento directo
C) Solo si ambos usan exactamente el mismo lenguaje de programación
D) Solo en sistemas P2P

---

## Pregunta 89

¿Qué problema de un sistema con muchas llamadas directas entre servicios ayuda a resolver el modelo orientado a eventos?

A) El acoplamiento fuerte: que cada servicio dependa de conocer y llamar directamente a los demás
B) El consumo de almacenamiento en disco
C) La necesidad de usar HTTPS
D) La resolución de nombres DNS

---

## Pregunta 90

¿Cuál de estos NO es un estilo de arquitectura a gran escala visto en teoría?

A) Microservicios
B) Serverless
C) Arquitectura Hexagonal
D) SOA

---

<!-- _class: lead -->
# Bloque 10
## Patrones de diseño interno (II) y síntesis

---

## Pregunta 91

En el patrón MVC, ¿qué papel tiene el Modelo?

A) Mostrar el HTML al usuario
B) Contener los datos y la lógica de negocio
C) Recibir la petición HTTP directamente del navegador
D) Gestionar exclusivamente la base de datos de sesiones

---

## Pregunta 92

¿Qué componente de MVC suele encargarse de recibir la petición y coordinar Modelo y Vista?

A) El Modelo
B) La Vista
C) El Controlador
D) El Adaptador

---

## Pregunta 93

¿Qué diferencia principal introduce el patrón MVP (Modelo-Vista-Presentador) respecto a MVC?

A) Elimina por completo la Vista
B) El Presentador asume más lógica, dejando la Vista más "tonta" y fácil de probar automáticamente
C) El Presentador sustituye a la base de datos
D) No existe ninguna diferencia real

---

## Pregunta 94

¿Qué caracteriza al patrón MVVM (Modelo-Vista-Vistamodelo), muy usado en frameworks frontend modernos?

A) El ViewModel expone el estado de forma reactiva y la Vista se sincroniza automáticamente con él
B) La Vista contiene toda la lógica de negocio
C) El Modelo se comunica directamente con el navegador sin pasar por nada más
D) Es exclusivo de aplicaciones de escritorio sin interfaz web

---

## Pregunta 95

¿Cuál es la idea central de la arquitectura Hexagonal (puertos y adaptadores)?

A) Que la base de datos esté en el centro de todo el sistema
B) Aislar la lógica de negocio del exterior, comunicándose mediante puertos (interfaces) y adaptadores (implementaciones concretas)
C) Sustituir siempre al patrón MVC
D) Obligar a usar microservicios

---

## Pregunta 96

En arquitectura Hexagonal, si cambias de base de datos relacional a NoSQL, ¿qué se espera que ocurra con la lógica de negocio (el dominio)?

A) Debe reescribirse por completo junto con la base de datos
B) Debería poder mantenerse prácticamente intacta, cambiando solo el adaptador correspondiente
C) Deja de funcionar definitivamente
D) Se convierte automáticamente en un microservicio

---

## Pregunta 97

¿Qué tienen en común Clean Architecture y Onion Architecture con la arquitectura Hexagonal?

A) Las tres son completamente distintas sin ningún punto en común
B) Las tres sitúan la lógica de negocio en el centro, con las dependencias apuntando siempre hacia dentro
C) Las tres exigen usar exclusivamente microservicios
D) Las tres son patrones de capas de presentación, nada más

---

## Pregunta 98

¿Por qué estos patrones (Hexagonal, Clean, Onion, MVC con buena separación) facilitan las pruebas automáticas?

A) Porque obligan a desactivar los tests en producción
B) Porque permiten probar la lógica de negocio de forma aislada, sin depender de una base de datos o framework real
C) Porque eliminan la necesidad de escribir tests
D) Porque solo funcionan sin conexión a internet

---

## Pregunta 99

¿Es correcto decir que los patrones de diseño interno (MVC, Hexagonal...) son incompatibles con dividir el sistema en microservicios?

A) Sí, son mutuamente excluyentes por definición
B) No: un microservicio puede, perfectamente, organizarse internamente con MVC o Hexagonal
C) Sí, solo pueden usarse en monolitos
D) No tiene sentido la pregunta porque los microservicios no tienen código interno

---

## Pregunta 100

Una aplicación organizada con Hexagonal expone su lógica de negocio tanto a través de una API REST como de una cola de mensajes. ¿Qué concepto de esta arquitectura representa esa doble forma de entrada/salida?

A) Dos bases de datos distintas
B) Dos adaptadores distintos conectados a los puertos correspondientes del dominio
C) Dos monolitos ejecutándose en paralelo
D) Dos servidores DNS redundantes
