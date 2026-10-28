---
layout: default
title: "Arquitecturas Web — Bloque 2.1: Fundamentos web (Teoría)"
permalink: /web/semana-1/teoria/
pdf: "/UD2/2.1%20Fundamentos%20web/web_1_teoria_presentacion.pdf"
pdf_label: "Presentación"
---

# Bloque 2.1 — Fundamentos web: redes, HTTP y arquitecturas

**Módulo:** Despliegue de Aplicaciones Web (0614) · 2º DAW · UD2: Arquitecturas web

> Con Git aprendimos a versionar código y con Docker a empaquetarlo y ejecutarlo igual en cualquier sitio. Nos falta una pieza: ¿cómo "habla" exactamente una aplicación web con quien la usa, y cómo se organiza por dentro? Eso es lo que vemos en este bloque.

## Planificación orientativa (2 h de teoría)

| # | Sección | 
|---|---------|
| 1 | Redes y modelos de comunicación (OSI, TCP/IP) | 
| 2 | Cliente-servidor, URL y DNS | 
| 3 | El protocolo HTTP | 
| 4 | Estado y sesiones: cookies | 
| 5 | Arquitecturas en capas | 
| 6 | Arquitecturas a gran escala | 
| 7 | Arquitecturas de diseño interno del código | 
| 8 | Panorama general y cierre |

---

## 1. Redes y modelos de comunicación

### 1.1 Qué es una red y de dónde viene

Una **red de comunicaciones** está compuesta por dos o más entidades cuya finalidad es intercambiar información.

- **1969:** se establece la primera conexión de **ARPANET**, la red precursora de Internet, financiada por el Departamento de Defensa de EE. UU.
- **Años 70:** fabricantes y organismos crean sus propias redes, **incompatibles entre sí**.
- **Solución: estandarizar.** La **ISO** publica el **modelo de referencia OSI** (1984). En paralelo, ARPANET adopta **TCP/IP** como protocolo oficial (1 de enero de 1983), que es el que acabó imponiéndose en Internet.

### 1.2 Modelo, arquitectura y protocolo

| Concepto | Definición |
|----------|-----------|
| **Modelo** | Determina la manera en la que se tiene que establecer y producir la comunicación (un marco teórico). |
| **Arquitectura** | Conjunto de niveles (capas) y protocolos utilizados para implementar las funciones del proceso de comunicación. |
| **Protocolo** | Conjunto de reglas y normas que rigen las tareas para prestar un servicio concreto (p. ej. HTTP, TCP, IP). |

### 1.3 El modelo OSI (7 capas)

La comunicación se divide en capas. En el **emisor**, los datos bajan de la capa 7 a la 1; en el **receptor**, suben de la 1 a la 7. Cada capa añade su propia información de control (**encapsulación**) y la capa equivalente del receptor la retira.

| Capa | Nombre | Función | Unidad de datos |
|------|--------|---------|-----------------|
| 7 | **Aplicación** | Interfaz entre las aplicaciones del usuario y la red. | Datos |
| 6 | **Presentación** | Da formato a la información para que el receptor la interprete; puede comprimirla y cifrarla. | Datos |
| 5 | **Sesión** | Establece, mantiene y controla el diálogo entre las aplicaciones origen y destino. | Datos |
| 4 | **Transporte** | Divide la información en **segmentos** y asegura que llegan al destino (y en orden, si el protocolo lo garantiza). | Segmento |
| 3 | **Red** | Encapsula en **paquetes** y los **enruta** por la mejor ruta hasta su destino. | Paquete |
| 2 | **Enlace de datos** | Encapsula en **tramas** para transmitirlas entre equipos contiguos, detectando y corrigiendo errores. | Trama |
| 1 | **Física** | Especificaciones eléctricas, mecánicas y funcionales de los medios físicos (cables, señales). | Bits |

### 1.4 El modelo TCP/IP (4 capas)

OSI es un modelo **de referencia** (se usa para explicar y clasificar). **TCP/IP** es el que **realmente** usa Internet, y agrupa las capas de OSI así:

| Modelo OSI | Modelo TCP/IP |
|------------|---------------|
| 7 Aplicación · 6 Presentación · 5 Sesión | **Aplicación** |
| 4 Transporte | **Transporte** |
| 3 Red | **Internet** |
| 2 Enlace de datos · 1 Física | **Acceso a la red** |

### 1.5 Protocolos de cada capa

| Capa TCP/IP | Protocolo | Para qué sirve | Puerto típico |
|-------------|-----------|----------------|---------------|
| **Aplicación** | HTTP / HTTPS | Publicar e intercambiar documentos web (texto, imágenes, vídeo…). | 80 / 443 |
| | SMTP, POP3, IMAP | Enviar (SMTP) y recibir (POP3, IMAP) correo electrónico. | 25/587, 110, 143 |
| | DHCP | Asignar automáticamente la configuración IP a un equipo. | 67/68 (UDP) |
| | DNS | Traducir nombres de dominio a direcciones IP. | 53 |
| | FTP / FTPS / SFTP | Transferir ficheros. | 21 / 990 / 22 |
| | SSH (antes Telnet) | Conexión remota a otro equipo para trabajar sobre él. | 22 (23) |
| | TLS (antes SSL) | Cifrar la comunicación para que solo el receptor pueda descifrarla. | — |
| **Transporte** | TCP | Envío **orientado a conexión**: conexión previa, confirmación de llegada y orden garantizado. | — |
| | UDP | Envío **sin conexión**: lo más rápido posible, sin confirmar llegada ni orden. | — |
| **Internet** | IP | Enviar paquetes por la mejor ruta posible (**enrutamiento**). | — |
| | NAT | Traducir direcciones IP privadas a públicas. | — |
| **Acceso a la red** | Ethernet | Reglas de la comunicación por cable. | — |
| | WLAN (Wi-Fi) | Reglas de la comunicación inalámbrica. | — |
| | ARP / RARP | Asociar direcciones IP con direcciones MAC (y viceversa). | — |

> **Idea clave para el resto del curso:** un servicio en red se localiza por **IP + puerto**. La IP identifica la máquina; el puerto identifica el programa que escucha dentro de ella (p. ej. Nginx en el 80 y el 443, MySQL en el 3306).

---

## 2. Cliente-servidor, URL y DNS

### 2.1 Arquitectura cliente-servidor

- **Cliente:** quien pide algo (normalmente, el navegador).
- **Servidor:** quien responde a esa petición (un programa escuchando en una máquina, en un puerto).
- Es el modelo base de toda la web: **el cliente siempre inicia** la comunicación y el servidor contesta.

### 2.2 El viaje de una petición, de un vistazo

```
navegador → DNS (resuelve el nombre) → servidor (IP:puerto) → respuesta → el navegador pinta la página
```

En el resto del bloque desmontamos cada pieza de este esquema.

### 2.3 Anatomía de una URL

```
https://www.ejemplo.com:443/productos/42?color=rojo&talla=m#resenas
└─┬─┘   └──────┬──────┘└┬┘└─────┬─────┘└────────┬────────┘└──┬──┘
esquema      host    puerto   ruta        query string   fragmento
```

| Parte | Descripción |
|-------|-------------|
| **Esquema** | Protocolo que se usará (`http`, `https`). |
| **Host** | Nombre de dominio o dirección IP del servidor. |
| **Puerto** | Opcional. Por defecto, 80 en HTTP y 443 en HTTPS. |
| **Ruta** | Qué recurso se pide dentro del servidor. |
| **Query string** | Parámetros `clave=valor` separados por `&`. |
| **Fragmento** | Lo usa solo el navegador (p. ej. para saltar a una sección); **nunca llega al servidor**. |

Formato general: `esquema://host[:puerto][/ruta][?query][#fragmento]`

### 2.4 DNS: de nombres a direcciones IP

Los ordenadores se localizan en la red por su **dirección IP** (p. ej. `93.184.216.34`), no por nombres. El **DNS** (*Domain Name System*) traduce nombres de dominio (`www.ejemplo.com`) a direcciones IP. Es, en esencia, la "agenda de contactos" de Internet.

**Resolución paso a paso (simplificada):**

```
navegador → ¿tengo "www.ejemplo.com" en caché? No →
   pregunta a un servidor DNS (resolver, normalmente el del proveedor o la red) →
   el resolver pregunta a la jerarquía DNS (raíz → .com → ejemplo.com) →
   devuelve la IP → el navegador ya puede conectar por HTTP(S)
```

- Cada respuesta DNS se guarda en **caché** durante un tiempo (**TTL**). Por eso, al registrar un dominio o cambiar su IP, el cambio "tarda en propagarse".
- Antes de preguntar al DNS, el sistema consulta el fichero local **`hosts`** (`/etc/hosts` en Linux, `C:\Windows\System32\drivers\etc\hosts` en Windows). Muy útil en prácticas para "inventar" dominios que apunten a nuestra máquina.
- Herramientas para consultar DNS: `nslookup`, `dig`, `host`.

---

## 3. El protocolo HTTP

### 3.1 Qué es

El **protocolo de transferencia de hipertexto** o **HTTP** (*HyperText Transfer Protocol*) establece la **sintaxis y semántica** para el intercambio de documentos **entre clientes y servidores web**.

- Creado en el **CERN** por **Tim Berners-Lee** (1989-1991) para intercambiar información científica de forma rápida y con un coste moderado.
- Basado en el esquema **petición → respuesta**.
- Funciona **sobre TCP** (puerto 80 por defecto).
- En HTTP/1.x es un **protocolo de texto**: los mensajes se pueden leer a simple vista.
- **HTTPS** es HTTP cifrado con **TLS**: mismo protocolo, pero viaja protegido (puerto 443). Lo veremos en detalle en la UD3.

### 3.2 HTTP como lenguaje común entre sistemas

Hoy HTTP no solo sirve páginas web: es el **protocolo estándar** para intercomunicar casi cualquier tipo de sistema informático mediante **APIs**:

- Subsistemas de la empresa: **ERP / CRM**.
- **Pasarelas de pago.**
- Proveedores de contenidos: sistemas de publicidad, venta de productos por referencia (afiliación).
- Aplicaciones móviles que consultan a su backend.

### 3.3 Funcionamiento paso a paso

1. El usuario introduce una URL en la **barra de direcciones** del navegador (p. ej. `http://www.miweb.com/documento.html`).
2. El navegador **descompone la URL** (esquema, host, puerto, ruta) y realiza la **consulta DNS** para obtener la IP del host.
3. Abre una **conexión TCP** con el servidor en el puerto indicado. Si es HTTPS, además negocia el cifrado TLS.
4. Envía una **petición HTTP** con un método (`GET`, `POST`, `HEAD`…).
5. El servidor devuelve una **respuesta HTTP** con:
   - un **código de estado** (¿ha ido bien?),
   - el **tipo de dato** enviado (tipo **MIME**, en la cabecera `Content-Type`),
   - y el contenido.
6. El navegador interpreta la respuesta. Si es un HTML que referencia CSS, imágenes o JS, **lanza una petición nueva por cada recurso**.
7. La conexión TCP **se cierra** (HTTP/1.0) o **se reutiliza** para más peticiones (conexiones persistentes, por defecto desde HTTP/1.1).

### 3.4 Versiones de HTTP

| Versión | Año | Novedad principal |
|---------|-----|-------------------|
| HTTP/0.9 | 1991 | Solo `GET`, solo HTML, sin cabeceras. |
| HTTP/1.0 | 1996 | Cabeceras, códigos de estado, tipos MIME, `POST` y `HEAD`. Una conexión TCP por petición. |
| HTTP/1.1 | 1997 | Conexiones persistentes, cabecera `Host` obligatoria (varios dominios en una misma IP), más métodos (`PUT`, `DELETE`, `OPTIONS`…). |
| HTTP/2 | 2015 | Formato **binario** y **multiplexación**: muchas peticiones simultáneas por una sola conexión. |
| HTTP/3 | 2022 | Funciona sobre **QUIC** (basado en UDP) en lugar de TCP: conexiones más rápidas y robustas. |

La **semántica** (métodos, códigos de estado, cabeceras) es la misma en todas las versiones desde 1.1; lo que cambia es cómo viajan los mensajes por la red.

### 3.5 Métodos HTTP

Un método indica **qué quiere hacer** el cliente con el recurso.

| Método | Para qué sirve | ¿Lleva cuerpo? | ¿Seguro? | ¿Idempotente? |
|--------|----------------|----------------|----------|---------------|
| **GET** | Pedir un recurso (HTML, CSS, imagen, datos JSON…). | No | Sí | Sí |
| **HEAD** | Como GET, pero el servidor devuelve **solo las cabeceras**, sin el contenido. Lo usan cachés y proxies para saber si un recurso ha cambiado (tipo, tamaño, fecha de modificación). | No | Sí | Sí |
| **POST** | Enviar datos para crear o procesar algo: un formulario, un nuevo registro en la base de datos, subir un fichero. | Sí | No | No |
| **PUT** | **Reemplazar** un recurso completo en una URL concreta (o crearlo si no existe). | Sí | No | Sí |
| **PATCH** | Modificar **parcialmente** un recurso. | Sí | No | No (en general) |
| **DELETE** | Eliminar un recurso. | No (normalmente) | No | Sí |
| **OPTIONS** | Preguntar qué métodos y capacidades admite el servidor para una URL (o para todo el servidor con `*`). Los navegadores lo usan en las comprobaciones previas de CORS (bloque 2.2). | No | Sí | Sí |

- **Seguro:** no modifica nada en el servidor (solo lee).
- **Idempotente:** repetir la misma petición varias veces deja el servidor en el mismo estado que hacerla una vez. Por ejemplo, borrar el recurso 42 dos veces deja el mismo resultado; enviar dos veces un `POST` de "crear pedido" crea dos pedidos.

Existen otros métodos menos habituales: `TRACE` y `CONNECT` (usado por los proxies para túneles HTTPS).

#### GET vs POST, en la práctica

| | GET | POST |
|--|-----|------|
| Los datos van en… | La URL (*query string*) | El cuerpo de la petición |
| ¿Visibles en el historial y los logs? | Sí | No directamente |
| Longitud | Limitada (límites de navegadores y servidores) | Prácticamente sin límite |
| Uso típico | Buscar, leer, filtrar | Enviar un formulario, subir un fichero |

> **Cuidado:** POST **no cifra** nada. Sin HTTPS, los datos de un POST viajan igual de legibles que los de un GET; simplemente no aparecen en la URL.

### 3.6 HTTP no es el único protocolo de aplicación

- **WebDAV** (*Web Distributed Authoring and Versioning*): extiende HTTP con métodos adicionales (`PROPFIND`, `MKCOL`, `COPY`, `LOCK`…) para gestionar ficheros y carpetas remotos como si fueran un sistema de ficheros (lo usan, p. ej., algunos clientes de sincronización de documentos).
- Otros protocolos que conviven con HTTP en una infraestructura típica: **FTP/SFTP** (transferencia de ficheros, UD4), **SMTP** (envío de correo), **SSH** (acceso remoto seguro).
- Todos comparten la idea cliente-servidor, pero cada uno está pensado para una tarea distinta: no todo tiene que resolverse "metiéndolo por HTTP".

### 3.7 Mensajes HTTP

Hay dos tipos de mensajes:

- **Petición** (*request*): del cliente al servidor.
- **Respuesta** (*response*): del servidor al cliente.

#### Estructura de un mensaje de petición

```
MÉTODO espacio RUTA espacio VERSIÓN CRLF      ← línea de petición
Cabecera: valor CRLF                          ┐
Cabecera: valor CRLF                          ┘ cabeceras
CRLF                                          ← línea en blanco (obligatoria)
[cuerpo]                                      ← vacío en GET; con datos en POST/PUT/PATCH
```

1. **Línea de petición:** método, recurso solicitado y versión del protocolo.
2. **Cabeceras** (*header fields*): información adicional sobre la petición (navegador, idiomas aceptados, cookies…).
3. **Línea en blanco** (`CRLF`, retorno de carro + salto de línea): marca el final de las cabeceras.
4. **Cuerpo** (opcional): los datos que se envían (p. ej. los campos de un formulario en un POST).

**Ejemplo GET:**

```http
GET /index.html HTTP/1.1
Host: www.elpais.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/131.0
Accept: text/html
Accept-Language: es-ES,es;q=0.9
If-Modified-Since: Wed, 15 Jan 2020 14:37:11 GMT

```

**Ejemplo POST (envío de un formulario):**

```http
POST /registro HTTP/1.1
Host: www.miweb.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 18

nombre=Ana&edad=20
```

#### Estructura de un mensaje de respuesta

```
VERSIÓN espacio CÓDIGO espacio FRASE CRLF     ← línea de estado
Cabecera: valor CRLF                          ┐
Cabecera: valor CRLF                          ┘ cabeceras
CRLF                                          ← línea en blanco
[cuerpo]                                      ← el recurso solicitado (HTML, imagen, JSON…)
```

1. **Línea de estado:** versión del protocolo, código de estado y texto descriptivo.
2. **Cabeceras de la respuesta:** información adicional (tipo de contenido, tamaño, fecha, servidor…).
3. **Línea en blanco.**
4. **Cuerpo:** el contenido solicitado.

**Ejemplo:**

```http
HTTP/1.1 200 OK
Date: Wed, 18 Sep 2019 19:44:53 GMT
Server: Apache/2.4.38 (Debian)
Last-Modified: Sat, 14 Sep 2019 17:22:37 GMT
ETag: "d-592869df67140"
Accept-Ranges: bytes
Content-Length: 144
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html>
<head><title>Mi primera web</title></head>
<body>
<h1>This is a Heading</h1>
<p>This is a paragraph.</p>
</body>
</html>
```

### 3.8 Códigos de estado

Cada respuesta incluye un código numérico de 3 cifras que resume el resultado. La primera cifra indica la familia:

| Rango | Significado |
|-------|-------------|
| **1xx** | Respuestas informativas (poco habituales en el día a día). |
| **2xx** | Éxito. |
| **3xx** | Redirección: el cliente debe hacer algo más (ir a otra URL, usar su caché…). |
| **4xx** | Error del **cliente** (la petición está mal o no está permitida). |
| **5xx** | Error del **servidor** (la petición era correcta pero el servidor ha fallado). |

#### 1xx — Informativos

| Código | Nombre | Significado |
|--------|--------|-------------|
| 100 | Continue | El servidor ha recibido las cabeceras; el cliente puede enviar el cuerpo. |
| 101 | Switching Protocols | El servidor acepta cambiar de protocolo (p. ej. a WebSocket, mediante la cabecera `Upgrade`). |

#### 2xx — Éxito

| Código | Nombre | Significado |
|--------|--------|-------------|
| **200** | OK | La petición se ha completado correctamente. |
| **201** | Created | Se ha creado un recurso nuevo (típico tras un POST o PUT). La cabecera `Location` indica su URL. |
| 202 | Accepted | La petición se ha aceptado, pero **todavía no se ha procesado** (procesamiento en segundo plano). |
| 203 | Non-Authoritative Information | La información viene modificada por un intermediario (proxy), no directamente del servidor original. Poco habitual. |
| **204** | No Content | Correcto, pero no hay contenido que devolver (típico tras un DELETE). |
| 205 | Reset Content | Correcto; el cliente debe reiniciar la vista (p. ej. vaciar el formulario). Poco habitual. |
| 206 | Partial Content | Se devuelve solo una parte del recurso, porque el cliente la pidió con la cabecera `Range` (descargas reanudables, vídeo). La respuesta incluye `Content-Range`. |

#### 3xx — Redirección

| Código | Nombre | Significado |
|--------|--------|-------------|
| **301** | Moved Permanently | El recurso se ha movido **definitivamente** a la URL indicada en `Location`. Los buscadores actualizan su índice. |
| **302** | Found | El recurso está **temporalmente** en otra URL (`Location`). |
| 303 | See Other | El cliente debe pedir **con GET** la URL indicada. Típico después de un POST, para que recargar la página no reenvíe el formulario. |
| **304** | Not Modified | Respuesta a un GET condicional (`If-Modified-Since`, `If-None-Match`): el recurso no ha cambiado, el cliente puede usar su copia en caché. No lleva cuerpo. |
| 307 / 308 | Temporary / Permanent Redirect | Como 302 / 301, pero obligando a repetir la petición con **el mismo método**. |

#### 4xx — Error del cliente

| Código | Nombre | Significado |
|--------|--------|-------------|
| **400** | Bad Request | La petición está mal formada (sintaxis incorrecta, datos inválidos). |
| **401** | Unauthorized | Falta autenticación o es incorrecta: **no te has identificado (o lo has hecho mal)**. Debe ir acompañada de la cabecera `WWW-Authenticate`. |
| 402 | Payment Required | Reservado para usos futuros relacionados con pagos; apenas se usa. |
| **403** | Forbidden | **Te has identificado, pero no tienes permiso** para ese recurso. |
| **404** | Not Found | El recurso no existe en esa URL. |
| 405 | Method Not Allowed | El recurso existe, pero no admite ese método (p. ej. DELETE sobre una página estática). |
| 429 | Too Many Requests | Has superado el límite de peticiones permitido. |

#### 5xx — Error del servidor

| Código | Nombre | Significado |
|--------|--------|-------------|
| **500** | Internal Server Error | Algo ha fallado dentro del servidor (p. ej. una excepción en el código). No es culpa del cliente. |
| 501 | Not Implemented | El servidor no soporta la funcionalidad necesaria para atender la petición. |
| **502** | Bad Gateway | El servidor actúa como pasarela o proxy y ha recibido una respuesta no válida del servidor al que reenviaba. |
| **503** | Service Unavailable | El servidor no puede atender ahora mismo (sobrecarga o mantenimiento). Hay que reintentar más tarde. |
| **504** | Gateway Timeout | El servidor que actúa como pasarela o proxy no ha recibido respuesta a tiempo del servidor de detrás. |

#### Códigos que conviene distinguir bien

- **401 vs 403:** 401 = falta **autenticación** (¿quién eres?); 403 = falta **autorización** (sé quién eres, pero no puedes).
- **404 vs 500:** 404 = lo que pides no existe (error del cliente); 500 = el servidor ha fallado al procesar algo que sí existe.
- **502 / 504:** aparecen cuando hay un **proxy** delante (p. ej. Nginx delante de una aplicación) y la aplicación de detrás falla o tarda demasiado. Los veremos a menudo en el bloque 2.2 y en la UD3.

### 3.9 Cabeceras HTTP

Las **cabeceras** son pares `Clave: Valor` que acompañan a toda petición y respuesta con **metadatos**. Los nombres no distinguen mayúsculas de minúsculas (`Content-Type` = `content-type`).

Clasificación clásica (HTTP/1.1, RFC 2616):

| Tipo | Quién las usa | Ejemplos |
|------|---------------|----------|
| **Generales** | Peticiones y respuestas. | `Date`, `Cache-Control`, `Connection`, `Upgrade` |
| **De petición** | El cliente, para dar información sobre la petición o sobre sí mismo. | `Host`, `User-Agent`, `Referer`, `Accept`, `Cookie`, `Authorization` |
| **De respuesta** | El servidor, para dar información adicional al cliente. | `Server`, `Location`, `WWW-Authenticate`, `Set-Cookie` |
| **De entidad** | Describen el propio contenido (el cuerpo) que se transmite. | `Content-Type`, `Content-Length`, `Content-Encoding`, `Last-Modified` |

> La especificación actual (RFC 9110, 2022) ya no usa el término "entidad" y habla de cabeceras de **representación** o **de contenido**, pero la idea es la misma.

#### Cabeceras generales

| Cabecera | Para qué sirve |
|----------|----------------|
| `Date` | Fecha y hora en que se generó el mensaje. |
| `Cache-Control` | Directivas de caché (p. ej. `no-cache`, `max-age=3600`). |
| `Connection` | Si la conexión TCP se mantiene abierta (`keep-alive`) o se cierra (`close`). |
| `Upgrade` | El cliente propone cambiar a otro protocolo (p. ej. WebSocket o una versión superior de HTTP) y el servidor decide si acepta. |

#### Cabeceras de petición

| Cabecera | Para qué sirve |
|----------|----------------|
| `Host` | Nombre del servidor al que va dirigida la petición. **Obligatoria en HTTP/1.1.** Permite que un mismo servidor (una sola IP) atienda varios dominios distintos (**hosts virtuales**, UD3). |
| `User-Agent` | Identifica el cliente que hace la petición (navegador, versión, sistema operativo). |
| `Referer` | URL de la página desde la que se ha enlazado al recurso pedido. |
| `Accept` | Tipos de contenido que acepta el cliente (`text/html`, `application/json`…). |
| `Accept-Language` | Idiomas preferidos (`es-ES, en`). |
| `Accept-Encoding` | Compresiones que entiende el cliente (`gzip`, `br`). |
| `Accept-Charset` | Juegos de caracteres aceptados (`UTF-8`). Hoy prácticamente en desuso. |
| `Cookie` | Cookies que el navegador reenvía al servidor (sección 4). |
| `Authorization` | Credenciales del cliente (p. ej. `Basic …`, `Bearer …`). |
| `If-Modified-Since` / `If-None-Match` | Peticiones **condicionales**: "dámelo solo si ha cambiado". Si no ha cambiado, el servidor responde `304`. |

#### Cabeceras de respuesta

| Cabecera | Para qué sirve |
|----------|----------------|
| `Server` | Como `User-Agent`, pero del servidor (`Apache/2.4.38`, `nginx/1.26`). |
| `Location` | Nueva URL del recurso. Acompaña a las redirecciones (301, 302…) y a `201 Created`. |
| `WWW-Authenticate` | Obligatoria con `401`: indica cómo debe autenticarse el cliente. |
| `Set-Cookie` | Pide al navegador que guarde una cookie (sección 4). |

#### Cabeceras de entidad (contenido)

| Cabecera | Para qué sirve |
|----------|----------------|
| `Content-Type` | Tipo **MIME** del cuerpo: le dice al cliente cómo interpretarlo. |
| `Content-Length` | Tamaño del cuerpo en bytes. |
| `Content-Encoding` | Codificación aplicada al cuerpo, normalmente compresión (`gzip`, `br`). |
| `Last-Modified` | Fecha de la última modificación del recurso. |
| `ETag` | Identificador de la versión concreta del recurso (para cachés). |

#### Tipos MIME más habituales

| Tipo MIME | Contenido |
|-----------|-----------|
| `text/html` | Página HTML |
| `text/css` | Hoja de estilos |
| `text/javascript` | Código JavaScript |
| `application/json` | Datos JSON (APIs) |
| `image/png`, `image/jpeg`, `image/svg+xml` | Imágenes |
| `application/pdf` | Documento PDF |
| `application/x-www-form-urlencoded` | Datos de un formulario HTML enviado por POST |
| `multipart/form-data` | Formulario con ficheros adjuntos |

---

## 4. HTTP no recuerda nada: estado y sesiones

### 4.1 HTTP es "sin estado" (*stateless*)

Cada petición HTTP es **independiente**: el servidor no recuerda, por sí mismo, las peticiones anteriores.

**Problema:** ¿cómo sabe el servidor que sigues siendo "tú" entre una petición y la siguiente (por ejemplo, que ya iniciaste sesión o qué hay en tu carrito)?

### 4.2 Cookies: la memoria prestada del navegador

1. El servidor envía una cookie en la respuesta con la cabecera **`Set-Cookie`**.
2. El navegador la guarda y la **reenvía automáticamente** (cabecera **`Cookie`**) en cada petición siguiente a ese dominio.
3. Así, aunque HTTP no tenga estado, el servidor puede "reconocerte" mirando la cookie que llega.

```http
HTTP/1.1 200 OK
Set-Cookie: SESSIONID=a8f3k29xq; Path=/; HttpOnly; Secure; SameSite=Lax
```

```http
GET /carrito HTTP/1.1
Host: www.tienda.com
Cookie: SESSIONID=a8f3k29xq
```

### 4.3 Sesiones: el estado vive en el servidor

- Lo habitual no es guardar todos los datos en la cookie, sino solo un **identificador de sesión** (un ID aleatorio y difícil de adivinar).
- El servidor guarda el **estado real** (usuario, carrito, permisos…) asociado a ese ID, normalmente en memoria, en ficheros o en una base de datos.
- La cookie solo transporta la "llave" para encontrar ese estado.

```
Navegador                         Servidor
   │  Cookie: SESSIONID=a8f3k29xq    │
   │ ──────────────────────────────▶ │  busca "a8f3k29xq" en su almacén de sesiones
   │                                 │  → usuario: ana, carrito: [3 productos], rol: cliente
```

### 4.4 El lado oscuro de las cookies

Mal gestionadas, las cookies son una vía de ataque habitual:

- **Robo de sesión** (*session hijacking*): si un atacante consigue leer tu cookie de sesión (p. ej. con un script malicioso inyectado en la página, un ataque **XSS**), puede hacerse pasar por ti sin conocer tu contraseña.
- **CSRF** (*Cross-Site Request Forgery*): el navegador envía tus cookies automáticamente a un sitio aunque la petición la haya iniciado otra página distinta. Un atacante puede aprovecharlo para ejecutar acciones en tu nombre sin que te des cuenta.
- **Seguimiento entre sitios** (*tracking*): cookies de terceros usadas para rastrear tu navegación por distintas páginas.

### 4.5 Mitigaciones básicas (se amplía en la UD3)

| Atributo | Efecto |
|----------|--------|
| `HttpOnly` | La cookie no se puede leer desde JavaScript: reduce el riesgo de robo por XSS. |
| `Secure` | La cookie solo se envía por HTTPS, nunca en claro por HTTP. |
| `SameSite` | Restringe el envío de la cookie en peticiones iniciadas desde otros sitios: mitiga CSRF. |

Ninguna de estas opciones sustituye a una aplicación bien validada: son una capa extra de defensa, no la única.

---

## 5. Arquitecturas en capas

### 5.1 El problema de meterlo todo junto

Imagina una página escrita en un único fichero con HTML, consultas a la base de datos y lógica de negocio, todo mezclado. Funciona… hasta que hay que cambiar algo: tocar el diseño obliga a rozar la lógica de negocio y las consultas SQL.

**Solución:** separar responsabilidades en **capas**.

### 5.2 Arquitectura de 1 capa

- Interfaz, lógica y datos en el mismo bloque de código, ejecutándose en la misma máquina.
- Típica de scripts pequeños o aplicaciones de escritorio muy simples.
- No escala ni en complejidad ni en usuarios: cualquier cambio toca "todo a la vez".

### 5.3 Arquitectura de 2 capas (cliente-servidor clásica)

- Separa al menos el **cliente** (interfaz) del **servidor** (lógica + datos).
- Ejemplo clásico: una aplicación de escritorio que se conecta directamente a una base de datos remota.
- Mejora el reparto, pero la lógica de negocio y el acceso a datos siguen mezclados.

### 5.4 Arquitectura de 3 capas

La más habitual hoy en aplicaciones web:

1. **Presentación:** lo que ve el usuario (HTML/CSS/JS, o una app móvil).
2. **Negocio** (lógica de aplicación): reglas, validaciones, cálculos.
3. **Datos:** acceso y persistencia (base de datos, ficheros…).

**Por qué separar en 3 capas:**

- Cada capa se puede **cambiar** sin tocar las demás: puedes rediseñar la interfaz sin tocar la base de datos.
- Cada capa se puede **escalar** por separado: más servidores de presentación si hay muchas visitas, sin duplicar la base de datos.
- Facilita el **trabajo en equipo**: unos en presentación, otros en negocio, otros en datos.

> **Capa lógica vs. nivel físico.** En inglés se distingue entre *layer* (separación lógica del código) y *tier* (separación física en máquinas distintas). Una aplicación de 3 capas lógicas puede ejecutarse en una sola máquina o repartirse en tres servidores.

### 5.5 Arquitectura N-capas

- Generalización de la de 3 capas: se añaden capas intermedias según haga falta.
- Ejemplo: presentación → API/servicios → lógica de negocio → acceso a datos → base de datos.
- "3 capas" y "N capas" no son excluyentes: **3 capas es el caso particular más común de N capas**.

---

## 6. Arquitecturas a gran escala: cómo se organizan los servicios

Las capas organizan una aplicación **por dentro**. Cuando el sistema crece (muchos equipos, mucho tráfico), también hay que decidir **cómo se reparte el sistema completo en piezas desplegables**.

### 6.1 Monolito

- Toda la aplicación se construye, se despliega y se escala **como una sola unidad**.
- Internamente puede estar perfectamente organizada en capas: "monolito" **no** significa "código desordenado".
- **Ventaja:** sencillo de desarrollar y desplegar al principio. **Inconveniente:** al crecer, cualquier cambio obliga a volver a desplegarlo todo.

### 6.2 SOA (*Service-Oriented Architecture*)

- El sistema se divide en **servicios** que se comunican entre sí (típicamente con protocolos como **SOAP** o colas de mensajes).
- Precursora directa de los microservicios, pero con servicios normalmente más grandes y un middleware de comunicación centralizado: el **ESB** (*Enterprise Service Bus*).
- Habitual en entornos corporativos grandes con sistemas heredados.

### 6.3 Microservicios

- El sistema se divide en **servicios pequeños e independientes**, cada uno con su propia responsabilidad, que se **despliegan por separado**.
- Cada microservicio puede tener su propia base de datos y se puede escalar y desplegar sin tocar los demás.
- Encajan muy bien con **Docker**: cada microservicio suele vivir en su propio contenedor. Se profundiza en la UD5 (CI/CD).

### 6.4 Monolito vs. microservicios

| | Monolito | Microservicios |
|--|----------|----------------|
| Despliegue | Una sola unidad | Independiente por servicio |
| Complejidad inicial | Baja | Alta (hay que coordinar servicios) |
| Escalado | Toda la aplicación a la vez | Servicio a servicio |
| Fallos | Un fallo puede afectar a todo | Un fallo puede quedar aislado |
| Proyecto pequeño / equipo reducido | Buena opción | Puede ser sobreingeniería |

### 6.5 Arquitectura orientada a eventos (*Event-Driven*)

- Los componentes no se llaman directamente: **publican y reaccionan a eventos** ("pedido creado", "pago confirmado") a través de un intermediario (**cola o broker de mensajes**, p. ej. RabbitMQ o Kafka).
- **Desacopla** emisor y receptor: quien publica el evento no necesita saber quién lo consumirá.
- Muy usada junto con microservicios para que no dependan directamente unos de otros.

### 6.6 Serverless / FaaS

- **FaaS** (*Function as a Service*): despliegas **funciones sueltas** y la plataforma en la nube decide cuándo y dónde ejecutarlas (p. ej. AWS Lambda).
- No significa que "no haya servidores": significa que **tú no los gestionas** (ni los enciendes, ni los parcheas, ni decides cuántos hay).
- Se suele pagar solo por el tiempo de ejecución real, no por tener un servidor encendido todo el día.

### 6.7 Peer-to-peer (P2P)

- No hay un servidor central: cada nodo actúa a la vez como **cliente y servidor**.
- Ejemplo típico: redes de compartición de ficheros (BitTorrent).
- Poco habitual en aplicaciones web de negocio, pero útil como contraste frente al modelo cliente-servidor.

---

## 7. Arquitecturas de diseño interno del código

Los estilos de la sección 6 deciden cómo se reparte el sistema en piezas desplegables. Estos patrones deciden **cómo se organiza el código dentro de cada pieza**.

### 7.1 MVC (Modelo-Vista-Controlador)

| Componente | Responsabilidad |
|------------|-----------------|
| **Modelo** | Datos y lógica de negocio. |
| **Vista** | Lo que se muestra al usuario. |
| **Controlador** | Recibe la petición y coordina Modelo y Vista. |

Es, con diferencia, el patrón más usado en frameworks web: Spring MVC, Django, Ruby on Rails, Laravel…

```
petición HTTP → Controlador → pide datos al Modelo → elige la Vista → respuesta HTML
```

### 7.2 Variantes de MVC: MVP y MVVM

- **MVP** (Modelo-Vista-Presentador): el Presentador asume más lógica; la Vista queda casi "tonta", lo que facilita probarla automáticamente.
- **MVVM** (Modelo-Vista-VistaModelo): el ViewModel expone el estado de forma **reactiva** y la Vista se sincroniza sola con él. Muy habitual en frameworks frontend modernos (Vue, Angular).
- Los tres resuelven el mismo problema: **separar qué se ve de cómo se calcula**.

### 7.3 Arquitectura hexagonal (puertos y adaptadores)

- La lógica de negocio (**el dominio**) se coloca en el centro, totalmente aislada de los detalles técnicos.
- Se comunica con el exterior a través de **puertos** (interfaces) y **adaptadores** (implementaciones concretas: una API REST, una base de datos, una cola de mensajes…).
- **Ventaja clave:** puedes cambiar la base de datos o el framework web sin tocar la lógica de negocio.

### 7.4 Clean Architecture / Onion Architecture

- Familia de ideas muy cercana a la hexagonal: **capas concéntricas**, con las reglas de negocio en el centro y los detalles técnicos (frameworks, interfaz, base de datos) en los anillos exteriores.
- **Regla común a las tres** (hexagonal, Clean, Onion): las dependencias **siempre apuntan hacia dentro**; el dominio nunca depende de un detalle técnico externo.

### 7.5 ¿Por qué importan estos patrones?

- Facilitan las **pruebas automáticas**: se puede probar la lógica de negocio sin levantar una base de datos real.
- Facilitan el **mantenimiento** a largo plazo: cambiar de framework o de base de datos no debería obligar a reescribir las reglas de negocio.
- Se **combinan** con las capas y los microservicios: p. ej., un microservicio organizado internamente con arquitectura hexagonal y MVC en su capa de presentación.

---

## 8. Panorama general: ¿cuándo uso cada una?

### 8.1 Dos preguntas distintas, dos familias de arquitecturas

1. **¿Cómo reparto el sistema completo en piezas desplegables?** → monolito, SOA, microservicios, event-driven, serverless, P2P.
2. **¿Cómo organizo el código dentro de cada pieza?** → capas (1/2/3/N), MVC/MVP/MVVM, hexagonal/Clean/Onion.

Estas dos familias **no compiten: se combinan**. Un microservicio puede estar organizado por dentro en 3 capas con arquitectura hexagonal.

### 8.2 Guía rápida

| Escenario | Arquitectura razonable |
|-----------|------------------------|
| Proyecto pequeño, equipo reducido, primera versión | Monolito en 3 capas |
| Sistema grande, muchos equipos, despliegues independientes | Microservicios |
| Integrar sistemas heredados de una gran empresa | SOA |
| Picos de carga impredecibles, tareas puntuales | Serverless / FaaS |
| Componentes que deben reaccionar a cambios sin acoplarse | Event-driven |
| Lógica de negocio compleja que debe sobrevivir a cambios de framework | Hexagonal / Clean Architecture |

### 8.3 El viaje completo de una petición, con todo lo visto

```
navegador ──DNS──▶ IP:puerto del servidor
   ──petición HTTP (método, cabeceras, cookie de sesión)──▶
      capa de presentación (p. ej. el Controlador de un MVC)
         ──▶ capa de negocio (dominio, aislado si se usa hexagonal)
            ──▶ capa de datos ──▶ base de datos
   ◀──respuesta HTTP (código de estado + cabeceras + cuerpo)──
navegador pinta la página (y pide CSS, JS, imágenes…)
```

### 8.4 Qué viene en el siguiente bloque

Hoy hemos visto **cómo se organiza y se reparte** una aplicación web. En el bloque 2.2 veremos **dónde vive físicamente** todo esto: servidores web vs. servidores de aplicaciones, contenido estático vs. dinámico, y qué significa realmente "desplegar".

---

## Ideas clave del bloque

- OSI es un modelo de referencia de 7 capas; TCP/IP es el modelo real de Internet, con 4 capas. HTTP vive en la capa de aplicación y se apoya en TCP (e IP).
- Un servicio se localiza por **IP + puerto**; el **DNS** traduce nombres de dominio a IP.
- HTTP funciona con **petición → respuesta**. La petición lleva método, ruta, versión, cabeceras y (opcionalmente) cuerpo; la respuesta lleva versión, código de estado, cabeceras y cuerpo.
- Métodos: **GET** lee, **POST** crea/procesa, **PUT** reemplaza, **PATCH** modifica en parte, **DELETE** borra, **HEAD** solo cabeceras, **OPTIONS** capacidades.
- Códigos: **2xx** éxito, **3xx** redirección, **4xx** error del cliente, **5xx** error del servidor. 401 = no identificado; 403 = sin permiso.
- `Content-Type` indica el tipo MIME del cuerpo; `Host` permite varios dominios en una IP.
- HTTP es **stateless**: el estado se mantiene con **cookies** que transportan un **ID de sesión**; el estado real vive en el servidor.
- **Capas** (cómo se organiza el código) y **microservicios/monolito/serverless** (cómo se reparte el sistema) son decisiones complementarias.

