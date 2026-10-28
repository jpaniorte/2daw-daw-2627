---
layout: default
title: "Arquitecturas Web — Bloque 2.1: Fundamentos web (Prácticas)"
permalink: /web/semana-1/practicas/
---

# Práctica 2.1 — El protocolo HTTP por dentro: peticiones, respuestas, cookies y sesiones

**Módulo:** Despliegue de Aplicaciones Web (0614) · 2º DAW · UD2: Arquitecturas web

## Objetivos

- Ver con tus propios ojos los mensajes HTTP: línea de petición, cabeceras, línea en blanco y cuerpo.
- Usar distintos métodos HTTP y enviar datos al servidor.
- Provocar e interpretar códigos de estado, redirecciones y autenticación.
- Comprobar que HTTP **no tiene estado** y cómo las **cookies** y las **sesiones** lo resuelven.
- Entender por qué quien tiene tu ID de sesión "es tú".

## Qué hay que entregar

Un documento con la **respuesta a cada pregunta marcada con ❓** (P1, P2…). En cada una, incluye el comando que has usado y **solo el fragmento relevante** de la salida (no hace falta pegar respuestas enteras).

---

## 0. Preparación (5 min)

### El entorno

Usaremos dos servicios que se arrancan con Docker Compose (descarga y descomprime [`web_1_practica_entorno.zip`]({{ '/UD2/2.1%20Fundamentos%20web/web_1_practica_entorno.zip' | relative_url }})):

| Servicio | URL | Para qué |
|----------|-----|----------|
| **httpbin** | `http://localhost:8080` | Un "espejo" de HTTP: te devuelve en JSON lo que le has enviado. |
| **sesiones** | `http://localhost:8000` | Una mini aplicación PHP con login, página privada y logout. |

```bash
cd web_1_practica_entorno
docker compose up -d
docker compose ps          # los dos servicios deben aparecer en estado "running"
curl localhost:8080/get    # debe devolver un JSON
curl localhost:8000/       # debe devolver un texto con las rutas de la aplicación
```

> **Windows:** usa **Git Bash** (lo tienes instalado desde la UD1). Todos los comandos están escritos para bash. En PowerShell, `curl` es otro programa distinto y las comillas se comportan de otra forma.

> **Si Docker no funciona:** sigue el plan B del `README.md` de la carpeta del entorno (httpbin como ejecutable y la aplicación con `php -S`).
   
### Chuleta de curl

| Opción | Qué hace |
|--------|----------|
| `-v` | *Verbose*: muestra la petición enviada (`>`), la respuesta recibida (`<`) y la información de conexión (`*`). |
| `-i` | Muestra las cabeceras de la respuesta junto con el cuerpo. |
| `-I` | Envía una petición **HEAD**: solo cabeceras, sin cuerpo. |
| `-s` | Silencioso: oculta la barra de progreso. |
| `-X MÉTODO` | Usa el método indicado (`PUT`, `DELETE`…). |
| `-d "datos"` | Envía datos en el cuerpo (y cambia el método a POST). |
| `-H "Cabecera: valor"` | Añade o sustituye una cabecera. |
| `-A "texto"` | Cambia el `User-Agent`. |
| `-L` | Sigue las redirecciones automáticamente. |
| `-u usuario:clave` | Envía credenciales de autenticación básica. |
| `-c fichero` | Guarda las cookies recibidas en un fichero (*cookie jar*). |
| `-b fichero` o `-b "nombre=valor"` | Envía cookies desde un fichero o escritas a mano. |
| `-o /dev/null -w "%{http_code}\n"` | No muestra el cuerpo; solo imprime el código de estado. |

> **Pon siempre la URL entre comillas** si lleva `?` o `&`. Sin comillas, bash interpreta `&` como "ejecuta en segundo plano" y corta la URL.

---

## 1. Anatomía de un mensaje HTTP (12 min)

### 1.1 Una petición GET, con lupa

```bash
curl -v localhost:8080/get
```

En la salida verás tres tipos de líneas:

- `*` → información de curl (resolución del nombre, conexión TCP a IP y puerto…).
- `>` → lo que **tu cliente envía** al servidor (la petición).
- `<` → lo que **el servidor responde** (las cabeceras de la respuesta).

Después aparece el cuerpo de la respuesta (el JSON).

❓ **P1.** Copia la **línea de petición** y la **línea de estado**. Señala en cada una: método, ruta y versión (petición); versión, código y frase (respuesta). ¿Dónde está la **línea en blanco** que separa las cabeceras del cuerpo?

❓ **P2.** ¿Qué tres cabeceras ha enviado curl sin que tú se lo pidieras? ¿Qué te dice la cabecera `Content-Type` de la respuesta sobre el cuerpo que has recibido?

### 1.2 Solo las cabeceras

```bash
curl -i localhost:8080/get
curl -I localhost:8080/get
```

❓ **P3.** ¿Qué diferencia hay entre la salida de `-i` y la de `-I`? Usa `-v` junto con `-I` para comprobar qué **método** usa `-I`.

> No uses `-X HEAD` en su lugar: curl se quedaría esperando un cuerpo que nunca llega.

### 1.3 Las cabeceras las decide el cliente

```bash
curl -A "MiNavegador/1.0" -H "Accept-Language: es-ES" localhost:8080/headers
```

El endpoint `/headers` te devuelve las cabeceras que ha recibido el servidor.

❓ **P4.** ¿Puede un servidor fiarse del `User-Agent` para saber qué navegador usa realmente un visitante? Razona la respuesta con lo que acabas de hacer.

---

## 2. Métodos HTTP y envío de datos (10 min)

### 2.1 GET con parámetros en la URL

```bash
curl "localhost:8080/get?nombre=Ana&curso=2DAW"
```

Fíjate en el campo `args` de la respuesta: son los parámetros de la *query string*.

### 2.2 POST de un formulario

```bash
curl -v -d "nombre=Ana&edad=20" localhost:8080/post
```

❓ **P5.** Solo has añadido `-d`. ¿Qué **método** ha usado curl y qué **dos cabeceras** nuevas ha añadido a la petición? ¿Dónde viajan ahora los datos: en la URL o en el cuerpo? ¿En qué campo del JSON de respuesta los ves?

### 2.3 POST con JSON

```bash
curl -H "Content-Type: application/json" -d '{"nombre":"Ana","edad":20}' localhost:8080/post
```

❓ **P6.** Compara los campos `form` y `json` de la respuesta en 2.2 y en 2.3. ¿Qué cabecera hace que el servidor interprete el cuerpo como formulario o como JSON?

### 2.4 Otros métodos

```bash
curl -X PUT    -d "edad=21" localhost:8080/anything
curl -X PATCH  -d "edad=21" localhost:8080/anything
curl -X DELETE localhost:8080/anything
curl -i -X DELETE localhost:8080/get
```

El endpoint `/anything` acepta cualquier método y te dice cuál ha recibido. En cambio, `/get` solo acepta lecturas.

❓ **P7.** En la última petición, ¿qué código de estado obtienes? ¿Qué cabecera de la respuesta te indica qué métodos sí están permitidos en `/get`?

---

## 3. Códigos de estado, redirecciones y autenticación (10 min)

### 3.1 Provocar códigos de estado

El endpoint `/status/CÓDIGO` responde con el código que le pidas:

```bash
curl -s -o /dev/null -w "%{http_code}\n" localhost:8080/status/404
```

❓ **P8.** Repite el comando con estos códigos y completa la tabla:

| Código | Familia (1xx…5xx) | Nombre y significado |
|--------|-------------------|----------------------|
| 201 | | |
| 204 | | |
| 404 | | |
| 500 | | |
| 503 | | |

### 3.2 Redirecciones

```bash
curl -i localhost:8080/redirect/2
curl -L -v localhost:8080/redirect/2
```

❓ **P9.** Sin `-L`, ¿qué código recibes y qué cabecera indica a dónde hay que ir? Con `-L -v`, ¿cuántas peticiones ha hecho curl en total hasta obtener un `200`? Escribe la secuencia de rutas.

### 3.3 Autenticación: el código 401

```bash
curl -i localhost:8080/basic-auth/ana/1234
curl -v -u ana:1234 localhost:8080/basic-auth/ana/1234
```

❓ **P10.** Sin credenciales, ¿qué código obtienes y qué cabecera obligatoria lo acompaña? Con `-u`, busca la cabecera `Authorization` que envía curl y decodifica su valor:

```bash
echo "PEGA_AQUÍ_EL_VALOR" | base64 -d
```

¿Qué obtienes? ¿Es seguro usar autenticación básica sin HTTPS?

### 3.4 Petición condicional: el código 304 *(si te da tiempo)*

```bash
curl -i localhost:8080/etag/v1
curl -i -H 'If-None-Match: "v1"' localhost:8080/etag/v1
```

❓ **P11.** ¿Qué código devuelve la segunda petición y por qué no trae cuerpo? ¿Qué ventaja tiene esto para el navegador y para el servidor?

---

## 4. HTTP no recuerda nada: cookies (8 min)

### 4.1 El servidor pide guardar una cookie… pero nadie la guarda

```bash
curl localhost:8080/cookies
curl -i "localhost:8080/cookies/set?tema=oscuro&idioma=es"
curl localhost:8080/cookies
```

`/cookies` muestra las cookies que le llegan al servidor; `/cookies/set` le pide al cliente que guarde las que indiques.

❓ **P12.** En la segunda petición, ¿qué cabecera usa el servidor para pedir que se guarden las cookies? En la tercera, ¿por qué el servidor sigue sin ver ninguna cookie? ¿Qué propiedad de HTTP demuestra esto?

### 4.2 El "bote de cookies" (*cookie jar*)

Un navegador guarda las cookies y las reenvía solo. Con curl lo hacemos a mano: `-c` guarda y `-b` envía.

```bash
curl -c cookies.txt "localhost:8080/cookies/set?tema=oscuro&idioma=es"
cat cookies.txt
curl -b cookies.txt localhost:8080/cookies
```

❓ **P13.** En `cookies.txt`, las líneas empiezan por `#HttpOnly_localhost`. No son comentarios: ¿qué **atributo** traía la cabecera `Set-Cookie` que explica ese prefijo? ¿Qué impide ese atributo en un navegador?

### 4.3 Las cookies las controla el cliente

```bash
curl -b "tema=claro; rol=admin" localhost:8080/cookies
```

❓ **P14.** Te acabas de inventar una cookie `rol=admin` y el servidor la ha recibido sin rechistar. ¿Qué conclusión sacas sobre guardar información importante (permisos, precios, identidad…) directamente dentro de una cookie?

---

## 5. Sesiones: el estado vive en el servidor (15 min)

Ahora usamos la aplicación PHP de `localhost:8000`. Usuarios de prueba: **ana / 1234** y **luis / abcd**.

### 5.1 Intentar entrar sin sesión

```bash
curl -i localhost:8000/perfil.php
```

### 5.2 Iniciar sesión

```bash
curl -i -d "usuario=ana&password=0000" localhost:8000/login.php
curl -i -c sesion.txt -d "usuario=ana&password=1234" localhost:8000/login.php
```

❓ **P15.** ¿Qué código devuelve `/perfil.php` sin sesión, y a dónde te manda? ¿Qué código obtienes con la contraseña incorrecta y cuál con la correcta? El login correcto responde `303 See Other` en lugar de `200`: ¿por qué crees que se hace así? (Pista: piensa en qué pasa si recargas la página después de enviar un formulario.)

❓ **P16.** Copia la cabecera `Set-Cookie` del login correcto. ¿Cómo se llama la cookie y qué contiene? Explica para qué sirven los atributos `HttpOnly` y `SameSite`. ¿Por qué crees que no lleva el atributo `Secure`?

### 5.3 Usar la sesión

Ejecuta este comando **tres veces**:

```bash
curl -b sesion.txt localhost:8000/perfil.php
```

Después, mira el fichero de cookies y, a continuación, el fichero de sesión **dentro del servidor** (sustituye `ID` por tu ID de sesión):

```bash
cat sesion.txt
docker compose exec sesiones cat /tmp/sess_ID
```

❓ **P17.** El contador de visitas sube, pero ¿ha cambiado algo en `sesion.txt` entre una visita y otra? Entonces, ¿dónde se guarda el contador? Copia el contenido del fichero de sesión del servidor y explica qué datos contiene.

### 5.4 Robo de sesión

Abre **otra terminal**: será un atacante que, de alguna forma, ha conseguido el ID de sesión de Ana. Ese atacante **no conoce la contraseña**:

```bash
curl -b "PHPSESSID=ID_DE_ANA" localhost:8000/perfil.php
```

Prueba también con un ID inventado:

```bash
curl -i -b "PHPSESSID=soyunhacker123" localhost:8000/perfil.php
```

❓ **P18.** ¿Qué ocurre con el ID de Ana? ¿Y con el ID inventado? ¿Qué ha necesitado el atacante para suplantar a Ana? Explica cómo ayudarían `HttpOnly`, `Secure` y HTTPS a evitar que ese ID caiga en malas manos.

### 5.5 Cerrar sesión

```bash
curl -i -b sesion.txt localhost:8000/logout.php
docker compose exec sesiones ls /tmp
curl -i -b sesion.txt localhost:8000/perfil.php
```

❓ **P19.** ¿Qué le pide el servidor al cliente con la cabecera `Set-Cookie` del logout? ¿Qué ha pasado con el fichero de sesión en el servidor? Si el atacante de 5.4 vuelve a usar el ID antiguo, ¿qué obtiene ahora?

### 5.6 Todo el flujo en un solo comando *(si te da tiempo)*

```bash
curl -L -v -c s2.txt -b s2.txt -d "usuario=luis&password=abcd" localhost:8000/login.php
```

Observa cómo curl hace el `POST`, recibe el `303`, guarda la cookie y hace el `GET` a `/perfil.php` enviándola: exactamente lo que haría un navegador.

---

## ¿Y si no quiero usar curl?

Puedes hacer la práctica con otra herramienta, siempre que puedas **ver las cabeceras de la petición y de la respuesta**. Ten en cuenta:

| Herramienta | Notas |
|-------------|-------|
| **DevTools del navegador** (F12 → Red / *Network*) | Abre `localhost:8000/login.php` e inicia sesión con el formulario. En *Aplicación → Cookies* verás la cookie y sus atributos. No sirve para todo (p. ej. métodos PUT/DELETE). |
| **Postman / Bruno / Insomnia** | Desactiva "seguir redirecciones automáticamente" para ver los 302/303. Ojo: **guardan y reenvían las cookies solos**, así que en la parte 4.1 no verás el efecto "sin estado" a menos que desactives su gestor de cookies. |
| **HTTPie** (`http -v …`) | Equivalente a curl con una sintaxis más amigable. Las cookies se gestionan con `--session`. |

En el documento de entrega indica qué herramienta has usado.

---

## Ampliación (si terminas antes)

1. **HTTP es texto: escríbelo a mano.** En Linux, macOS o WSL:

   ```bash
   printf 'GET /get HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n' | nc localhost 8080
   ```

   ¿Qué pasa si quitas la cabecera `Host`? ¿Y si quitas el último `\r\n` (la línea en blanco)?

2. **`HttpOnly` en acción.** Inicia sesión en `localhost:8000/login.php` con el navegador, abre la consola de DevTools y escribe `document.cookie`. ¿Aparece `PHPSESSID`? ¿Por qué?

3. **Una web real.** Mira qué responde un sitio de verdad:

   ```bash
   curl -sI http://google.es | grep -iE "^HTTP|^location"
   curl -sI https://www.google.es | grep -iE "^HTTP|^set-cookie"
   ```

   ¿Qué código y qué `Location` devuelve el primero? ¿Qué atributos llevan las cookies del segundo?

---

## Al terminar

```bash
docker compose down
rm -f cookies.txt sesion.txt s2.txt
```
