# Bloque 2.2 — Servidores web, servidores de aplicaciones y despliegue

**Módulo:** Despliegue de Aplicaciones Web (0614) · 2º DAW · UD2: Arquitecturas web

> En el bloque 2.1 vimos cómo se organiza una aplicación web (capas, microservicios, MVC, hexagonal…) y cómo se comunica (HTTP). Hoy vemos **dónde vive físicamente** ese código, **quién lo sirve** cuando llega una petición y **qué significa desplegarlo**.

## Planificación orientativa (2 h de teoría)

| # | Sección | Tiempo aprox. |
|---|---------|---------------|
| 1 | Contenido estático vs. dinámico | 10 min |
| 2 | Renderizado, CDN y SEO | 25 min |
| 3 | Servidor web vs. servidor de aplicaciones | 45 min |
| 4 | Qué significa "desplegar" | 30 min |
| 5 | Todo junto: de la petición al despliegue | 10 min |

---

## 1. Contenido estático vs. dinámico

### 1.1 Contenido estático

- Ficheros que el servidor envía **tal cual están guardados en disco**, sin ejecutar ningún código por petición.
- Ejemplos: HTML fijo, CSS, JavaScript del cliente, imágenes, PDF, fuentes.
- **Muy rápido** de servir: el servidor solo lee el fichero y lo envía.

### 1.2 Contenido dinámico

- El servidor **ejecuta código en cada petición** para generar la respuesta (p. ej. consulta una base de datos y monta el HTML o el JSON al vuelo).
- Ejemplos: el resultado de una búsqueda, el precio actualizado de un producto, el feed personalizado de un usuario.
- Más lento que el estático (hay que ejecutar lógica), pero imprescindible para cualquier aplicación cuyos datos cambian.

### 1.3 Una misma página puede mezclar ambos

```
GET /tienda           →  HTML generado dinámicamente (precios, stock)
                         que a su vez referencia:
                           /css/estilos.css  → estático
                           /img/logo.png     → estático
                           /js/analytics.js  → estático
```

Lo habitual es servir lo estático de la forma más directa posible y reservar el coste de "ejecutar código" solo para lo que de verdad cambia.

---

## 2. Renderizado, CDN y SEO

### 2.1 ¿Dónde se "monta" el HTML que ve el usuario?

Hasta ahora hemos hablado de "generar HTML dinámico" como si fuera una sola cosa. En realidad, importa mucho **dónde** se monta ese HTML: en el servidor o en el navegador.

### 2.2 CSR: *Client-Side Rendering*

- El servidor envía un HTML casi vacío (un `<div id="app"></div>`) junto con un paquete grande de JavaScript.
- El navegador ejecuta ese JavaScript, que construye el HTML real y lo pinta en pantalla.
- Típico de las **SPA** (*Single Page Applications*) hechas con React, Vue o Angular en su configuración por defecto.
- **Ventaja:** navegación muy fluida entre páginas una vez cargado. **Inconveniente:** la primera carga tarda más y la página está "en blanco" hasta que el JavaScript termina de ejecutarse.

### 2.3 SSR: *Server-Side Rendering*

- El servidor ejecuta la lógica de la aplicación y genera el **HTML ya completo** en cada petición, igual que hacían los servidores de aplicaciones "clásicos" (PHP, JSP…).
- El navegador recibe una página ya pintada, visible de inmediato, aunque el JavaScript aún no se haya cargado del todo.
- Frameworks modernos como **Next.js** (React) o **Nuxt** (Vue) permiten hacer SSR combinando lo mejor de ambos mundos.

### 2.4 Hidratación (*hydration*)

- Técnica habitual en el SSR moderno: el servidor manda el HTML ya renderizado y después el navegador "engancha" el JavaScript a ese HTML para que vuelva a ser interactivo (clics, formularios…), sin redibujarlo desde cero.
- Es el punto intermedio entre SSR puro y CSR puro: **carga inicial rápida** (como SSR) + **interactividad rica** después (como CSR).

### 2.5 SSG: *Static Site Generation*

- Variante en la que el HTML no se genera en cada petición, sino **una sola vez, en tiempo de build** (antes de desplegar).
- El resultado es, en la práctica, **contenido estático**: ideal para contenido que no cambia por usuario (un blog, una documentación).
- Si el contenido cambia (precios, sesión de usuario…), SSG no basta por sí solo: hace falta SSR o contenido dinámico real.

| | CSR | SSR | SSG |
|--|-----|-----|-----|
| ¿Dónde se genera el HTML? | En el navegador | En el servidor, en cada petición | En el build, una sola vez |
| Primera carga | Lenta | Rápida | Muy rápida |
| ¿Necesita servidor de aplicaciones en producción? | No | Sí | No |
| SEO | Más difícil | Bueno | Muy bueno |
| Caso típico | Panel de administración, app interna | Tienda online, red social | Blog, documentación |

### 2.6 ¿Por qué importa esto para el SEO?

- Los buscadores usan **crawlers** (rastreadores) que visitan las páginas para indexarlas.
- Un crawler que recibe un CSR puro ve, al principio, un HTML casi vacío: tiene que ejecutar el JavaScript para ver el contenido real, y no todos los rastreadores lo hacen igual de bien ni con la misma rapidez.
- SSR (o SSG) entrega el contenido ya visible en el HTML inicial, lo que facilita muchísimo un indexado correcto y rápido.

### 2.7 SEO: no es solo el crawler

Además del renderizado, el SEO depende de cosas que sí controlamos:

- Etiquetas `<title>` y `<meta name="description">` bien escritas en cada página.
- URLs legibles y estables (si cambian, redirigir con **`301`**, visto en el bloque 2.1).
- Tiempos de carga bajos: Google penaliza las páginas lentas.
- Contenido esencial (texto, enlaces) accesible sin depender de JavaScript.

### 2.8 CDN: *Content Delivery Network*

- Red de servidores **distribuidos geográficamente** que guardan **copias cacheadas** del contenido, cerca de cada usuario.
- Un usuario en Tokio no tiene por qué ir hasta un servidor en Madrid: la CDN le sirve una copia desde un nodo cercano.
- Ejemplos: Cloudflare, Akamai, Fastly, Amazon CloudFront.

**Qué aprovecha mejor una CDN:**

- El **contenido estático** (CSS, JS, imágenes, incluso HTML generado con SSG): no cambia por usuario, así que es fácil de cachear.
- El **contenido dinámico y personalizado** (tu carrito, tu sesión) normalmente no se cachea en la CDN.
- Por eso separar bien estático de dinámico (sección 1) también ayuda a sacarle partido a una CDN.

### 2.9 El problema de invalidar la caché

- Si despliegas una nueva versión de `estilos.css` pero la CDN (o el propio navegador) sigue sirviendo la copia antigua, los usuarios no ven el cambio.
- Solución habitual: ***cache busting***, incluir un hash o versión en el nombre del fichero (`estilos.a3f9c1.css`). Al cambiar el contenido cambia el nombre, y la caché antigua deja de usarse automáticamente porque la URL es distinta.
- Las herramientas de build de los frameworks frontend (Vite, webpack…) lo hacen automáticamente.

---

## 3. Servidor web vs. servidor de aplicaciones

### 3.1 Servidor web

- Programa cuya función principal es **recibir peticiones HTTP y responder**, típicamente sirviendo **contenido estático** con muchísima eficiencia.
- Ejemplos: **Apache HTTP Server**, **Nginx**.
- También puede actuar de "puerta de entrada" (**proxy inverso**) hacia otros servicios (UD3).

### 3.2 Una optimización típica del servidor web: la compresión

- Antes de enviar contenido (sobre todo texto: HTML, CSS, JS, JSON), el servidor web puede comprimirlo con **gzip** o, más modernamente, **brotli**.
- El navegador indica qué compresiones acepta con `Accept-Encoding`; el servidor responde con `Content-Encoding` y el cuerpo comprimido (cabeceras vistas en el bloque 2.1):

```http
GET /css/estilos.css HTTP/1.1
Host: www.miweb.com
Accept-Encoding: gzip, br
```

```http
HTTP/1.1 200 OK
Content-Type: text/css
Content-Encoding: br
```

- Reduce mucho el tamaño transferido **sin tocar una línea de la aplicación**: es configuración del servidor web, no del código.

### 3.3 Servidor de aplicaciones

- Programa diseñado para **ejecutar la lógica de la aplicación** (el código de negocio) y generar **contenido dinámico**.
- Ejemplos: **Tomcat** (Java), **Node.js** ejecutando una app Express, **Gunicorn / uWSGI** (Python), **PHP-FPM**.
- Entiende el lenguaje o framework de la aplicación; un servidor web puro no sabe "ejecutar" ese código por sí mismo.

| | Servidor web | Servidor de aplicaciones |
|--|--------------|--------------------------|
| Función principal | Recibir peticiones HTTP y servir ficheros | Ejecutar la lógica de negocio |
| Tipo de contenido | Estático | Dinámico |
| Ejemplos | Apache, Nginx | Tomcat, Node.js, Gunicorn, PHP-FPM |
| ¿Entiende el lenguaje de la app? | No | Sí |

### 3.4 Frameworks de backend y su servidor de aplicaciones

Cada framework de backend necesita, por detrás, un servidor de aplicaciones que lo ejecute:

| Lenguaje | Framework | Servidor de aplicaciones típico |
|----------|-----------|---------------------------------|
| Java | Spring (Spring Boot) | Tomcat (a menudo **embebido** dentro del propio `.jar`) |
| Python | Django, Flask | Gunicorn o uWSGI |
| PHP | Laravel, Symfony | PHP-FPM |
| Node.js | Express, NestJS | El propio proceso Node.js |
| Ruby | Ruby on Rails | Puma o Unicorn |

### 3.5 ¿Y Vue, Angular o React? Son frontend

- Vue, Angular y React son **frameworks de frontend**: su código se ejecuta **en el navegador** (CSR, sección 2), no en un servidor de aplicaciones.
- No sustituyen a Spring, Django o Laravel: **conviven** con ellos. Lo habitual es un backend (p. ej. Laravel) que expone una **API** y un frontend (p. ej. Vue) que la consume desde el navegador.

### 3.6 Entonces, ¿quién sirve ese frontend? Un servidor web

- `npm run build` en Vue/Angular/React **no genera un servidor**: genera una carpeta (`dist/`, `build/`) con `index.html`, `.js` y `.css` ya compilados, es decir, **contenido estático**.
- Ese resultado se sirve como cualquier otro estático: con **Nginx o Apache**, copiando esa carpeta al directorio raíz que expone el servidor web.
- Por eso una SPA en CSR **no necesita Node.js en producción**: Node.js solo hizo falta en tiempo de build (en tu máquina o en el pipeline de CI/CD, UD5).
- **Caso distinto:** si el frontend usa **SSR** (Next.js, Nuxt), entonces sí hace falta un servidor de aplicaciones en producción —un proceso Node.js— porque el HTML se genera en cada petición.

### 3.7 CORS: frontend y backend en orígenes distintos

Un **origen** es la combinación de **esquema + host + puerto**. Dos URL son del mismo origen solo si coinciden las tres partes:

| Comparado con `https://miapp.com` | ¿Mismo origen? | Motivo |
|-----------------------------------|----------------|--------|
| `https://miapp.com/api/productos` | Sí | Solo cambia la ruta |
| `http://miapp.com` | No | Cambia el esquema |
| `https://api.miapp.com` | No | Cambia el host |
| `https://miapp.com:8080` | No | Cambia el puerto |

- Por seguridad, los navegadores aplican la **política del mismo origen** (*same-origin policy*): el JavaScript de un origen no puede leer las respuestas de otro origen, salvo que ese otro lo permita explícitamente.
- **CORS** (*Cross-Origin Resource Sharing*) es el mecanismo con el que el backend indica, mediante cabeceras HTTP, qué orígenes externos pueden llamarle:

```http
HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://miapp.com
Content-Type: application/json
```

- Sin esa cabecera (o con un valor que no coincide), el navegador **descarta la respuesta** antes de entregársela al JavaScript, **aunque la petición haya llegado bien al servidor**.
- Para peticiones "no simples" (p. ej. un `PUT`, un `DELETE` o un JSON con cabeceras propias), el navegador envía antes una petición **`OPTIONS`** de comprobación (*preflight*) para preguntar si está permitido.
- Es uno de los errores más comunes al separar frontend y backend: la petición "funciona" con `curl` o Postman, pero **falla solo desde el navegador**, porque CORS lo aplica el navegador, no el servidor.

### 3.8 Cómo atienden las peticiones por dentro (modelo de concurrencia)

| Servidor | Modelo | Consecuencia |
|----------|--------|--------------|
| **Nginx** | Eventos asíncronos: pocos procesos atienden miles de conexiones sin bloquearse. | Muy eficiente para servir estático y hacer de proxy. |
| **Apache** (modo clásico, `prefork`) | Un proceso o hilo por conexión. | Sencillo de entender, más pesado con mucha concurrencia. (Las versiones modernas tienen también un modo `event`.) |
| **Node.js** | Un único hilo con un *event loop*. | Muy bueno con operaciones de E/S (red, disco); malo si una petición hace cálculos pesados que bloquean el hilo. |
| **Gunicorn / Tomcat** | Varios *workers* (procesos o hilos) en paralelo, cada uno con una petición a la vez. | La concurrencia depende de cuántos workers se configuren. |

**¿Por qué importa?**

- Determina cuántas peticiones simultáneas puede atender un servidor con los mismos recursos de CPU y RAM.
- Explica por qué **Nginx se pone tan a menudo delante** de los servidores de aplicaciones: aguanta mucha concurrencia sirviendo lo estático y repartiendo lo dinámico, mientras los workers del servidor de aplicaciones se dedican solo a ejecutar lógica.
- No hace falta memorizar los detalles internos, pero sí entender que servidor web y servidor de aplicaciones no solo se diferencian en **qué** sirven, sino en **cómo** están diseñados para servirlo.

### 3.9 Los dos a la vez: el patrón habitual en producción

Un **servidor web** (Nginx/Apache) por delante, que sirve directamente lo estático y **reenvía** (hace de **proxy inverso**) las peticiones dinámicas a uno o varios **servidores de aplicaciones** por detrás. Se profundiza en la UD3 (proxy inverso) y la UD4 (servidores de aplicaciones).

```
navegador → Nginx (servidor web)
              ├── /css/*, /img/*  → responde directamente (estático)
              └── /api/*          → reenvía a Node.js / Tomcat (servidor de aplicaciones)
                                      → ese código consulta la base de datos
                                      → genera la respuesta dinámica
```

> Aquí cobran sentido los códigos **502 Bad Gateway** (la aplicación de detrás ha devuelto una respuesta no válida o no está arrancada) y **504 Gateway Timeout** (la aplicación ha tardado demasiado) vistos en el bloque 2.1.

### 3.10 Varios servidores de aplicaciones: balanceo de carga

- Si una sola instancia no da abasto, se levantan **varias instancias idénticas** (varios *backends*).
- El servidor web (o un **balanceador** dedicado) reparte las peticiones entre ellas. La estrategia más sencilla es **round robin**: una petición a cada backend por turnos.
- Otras estrategias que solo citamos (se amplían en UD3/UD5):

| Estrategia | Idea |
|------------|------|
| *Round robin* | Por turnos, uno tras otro. |
| *Weighted round robin* | Por turnos, pero los backends más potentes reciben más peticiones. |
| *Least connections* | Al backend con menos conexiones activas en ese momento. |
| *IP hash* | Según la IP del cliente: el mismo cliente va siempre al mismo backend (útil si la sesión se guarda en memoria). |

"Servidor de aplicaciones" no tiene por qué significar "una única instancia".

### 3.11 Escalado vertical vs. horizontal

- **Escalado vertical:** dar más recursos (CPU, RAM) a la misma máquina. Tiene un límite físico y suele obligar a parar el servicio para ampliar.
- **Escalado horizontal:** añadir **más instancias** en paralelo, como en el apartado anterior. Es el enfoque habitual en la nube: no tiene un límite tan rígido y encaja con el balanceo de carga.
- **Docker** facilita especialmente el escalado horizontal: levantar una instancia más es, en esencia, arrancar un contenedor más de la misma imagen.

### 3.12 De gestionar contenedores a mano a los orquestadores

- Arrancar, vigilar y balancear a mano docenas de contenedores no escala.
- Los **orquestadores de contenedores** (el más conocido es **Kubernetes**) lo automatizan: deciden cuántas instancias levantar, las reinician si fallan, reparten el tráfico y facilitan los despliegues graduales de forma declarativa.
- No se usará en este módulo, pero es la evolución natural cuando "varios backends gestionados a mano" se queda corto.

### 3.13 Health checks: ¿sigue vivo el backend?

- Antes de enviarle tráfico, el servidor web o el balanceador comprueba periódicamente que cada backend responde bien: un **health check**, una petición de prueba a una ruta tipo `/health`.
- Si un backend deja de responder, se **retira temporalmente** de la rotación hasta que vuelva a estar sano, evitando que los usuarios reciban errores.

### 3.14 ¿Por qué no servirlo todo desde el servidor de aplicaciones?

- Técnicamente se puede, pero los servidores web están mucho más optimizados para servir ficheros estáticos y gestionar miles de conexiones simultáneas.
- Separar responsabilidades también facilita: **cachear** el contenido estático, aplicar **HTTPS en un único punto** y **balancear** la carga entre varios servidores de aplicaciones.

---

## 4. Qué significa "desplegar" una aplicación

### 4.1 Desplegar, en una frase

**Desplegar** es poner una aplicación a disposición de sus usuarios reales, ejecutándose en algún sitio accesible desde fuera de tu máquina de desarrollo.

### 4.2 Piezas que intervienen en un despliegue

| Pieza | Qué es |
|-------|--------|
| **Dominio** | El nombre (`miapp.com`) que escriben los usuarios. |
| **DNS** | Apunta ese dominio a la IP del servidor donde vive la aplicación (bloque 2.1). |
| **Hosting** | Dónde se ejecuta físicamente la aplicación. |
| **Certificado HTTPS** | Para que la comunicación vaya cifrada (UD3). |
| **Artefacto** | El "paquete" concreto y versionado de la aplicación que realmente se despliega. |

### 4.3 Tipos de hosting, de menos a más control

1. **Hosting compartido:** varias webs comparten un servidor gestionado por el proveedor. Barato, poco control.
2. **VPS** (servidor privado virtual): una máquina virtual para ti solo, con control total del sistema operativo.
3. **Servidor dedicado:** una máquina física entera para ti.
4. **Cloud** (AWS, Azure, Google Cloud…): recursos bajo demanda, escalables y facturados por uso. Puede ir desde alquilar máquinas virtuales (**IaaS**) hasta plataformas donde solo subes tu código o tu contenedor y el proveedor gestiona el resto (**PaaS**).

### 4.4 Entornos de despliegue: no hay un único "producción"

| Entorno | Para qué sirve |
|---------|----------------|
| **Desarrollo** | Tu máquina: programar y probar en local. |
| **Staging / preproducción** | Una réplica de producción para probar antes de publicar. |
| **Producción** | El entorno real, con usuarios de verdad. |

**Idea clave:** el **mismo artefacto versionado** (la misma imagen Docker, el mismo `.jar`, el mismo `.tar.gz`) se **promociona** de un entorno a otro **sin reconstruirlo**. Así se garantiza que lo probado en staging es exactamente lo que llega a producción. Si cada entorno reconstruye su propio artefacto, podrían colarse dependencias o versiones ligeramente distintas sin darse cuenta.

### 4.5 ¿Qué es exactamente un artefacto?

Un **artefacto** es el **resultado empaquetado de construir la aplicación**: lo que de verdad se copia, instala o ejecuta en el servidor, no el código fuente suelto.

- **Lenguajes compilados:** el binario o paquete compilado (`.jar` / `.war` en Java, un `.exe`, un binario de Go…).
- **Lenguajes interpretados:** el artefacto también existe: es un paquete con el código listo para ejecutar **junto con sus dependencias**.

### 4.6 El caso de PHP (lenguaje que no se compila)

- El artefacto típico es un **`.tar.gz`** (o `.zip`) con el código fuente de la aplicación **más sus dependencias ya resueltas** (la carpeta `vendor/` de Composer), listo para descomprimir en el servidor.
- La idea es la misma que en un lenguaje compilado: generar **una vez** un paquete **inmutable**, probarlo y desplegar **exactamente ese paquete**, en lugar de hacer `git pull` en producción o reinstalar dependencias en cada servidor (con el riesgo de que una reinstalación traiga una versión distinta).
- Otros ejemplos en lenguajes interpretados: un paquete npm (Node.js), una *wheel* `.whl` (Python) o directamente una **imagen Docker**, que empaqueta el artefacto junto con todo su entorno de ejecución.

### 4.7 Repositorios de artefactos

- Igual que **Docker Hub** almacena y distribuye imágenes (UD1), existen repositorios para artefactos de cualquier tipo: **JFrog Artifactory**, **Sonatype Nexus** o los registros de paquetes de cada lenguaje (npm, PyPI…).
- Permiten **subir una vez** el artefacto (con su número de versión) y **descargar siempre la misma versión exacta** desde cualquier servidor.
- Son la "**fuente de verdad**": ante un incidente se puede comprobar qué versión está desplegada y descargarla para reproducir el problema.

### 4.8 Versionar bien los artefactos

- Cada build relevante debería generar un artefacto con **su propio número de versión**, siguiendo un esquema claro como **SemVer** (`MAJOR.MINOR.PATCH`, p. ej. `2.4.1`):

| Parte | Se incrementa cuando… | Ejemplo |
|-------|-----------------------|---------|
| `MAJOR` | Hay cambios **incompatibles** con la versión anterior. | `2.4.1` → `3.0.0` |
| `MINOR` | Se añade funcionalidad nueva **compatible**. | `2.4.1` → `2.5.0` |
| `PATCH` | Se corrigen errores. | `2.4.1` → `2.4.2` |

- Es la misma idea que el problema del tag `latest` en Docker (UD1): desplegar siempre "la última" sin fijar la versión impide saber qué hay exactamente en producción.
- Versionar explícitamente permite: saber qué hay desplegado en cada entorno, repetir exactamente el mismo despliegue en otra máquina y hacer **rollback** (volver atrás) a una versión anterior conocida si algo falla.

### 4.9 Configuración y secretos: lo único que cambia entre entornos

- Si el artefacto es el mismo en todos los entornos, ¿cómo sabe la aplicación a qué base de datos conectarse o qué credenciales usar en cada uno?
- Mediante **configuración externa al artefacto**: **variables de entorno**, ficheros de configuración montados aparte o un **gestor de secretos** (HashiCorp Vault, AWS Secrets Manager…).
- **Regla importante:** contraseñas, tokens y claves de API **nunca** deben quedar escritas en el código ni "horneadas" dentro de la imagen o el artefacto. Así el mismo artefacto sirve para todos los entornos, cambiando solo la configuración.

```bash
# Mismo artefacto, distinta configuración según el entorno
docker run -e DB_HOST=db-staging -e DB_PASSWORD=*** miapp:1.4.0   # staging
docker run -e DB_HOST=db-prod    -e DB_PASSWORD=*** miapp:1.4.0   # producción
```

### 4.10 Despliegue con contenedores

- Empaquetar la aplicación en una imagen Docker y ejecutarla como contenedor es hoy una de las formas más habituales de desplegar. La **imagen Docker es, en sí misma, un artefacto versionado** (por su tag).
- Ventaja clave (UD1): el mismo contenedor que probaste en tu portátil es, en esencia, el que se ejecuta en producción.
- En la UD5 (CI/CD) se automatizará: cada cambio de código podrá generar y desplegar automáticamente una nueva imagen versionada.

### 4.11 Un flujo de despliegue simple (sin CI/CD todavía)

1. Tienes el código (y su `Dockerfile`) en tu repositorio Git.
2. Construyes el artefacto, etiquetado con una versión.
3. Lo subes a un repositorio (un registry de Docker, o Artifactory/Nexus si no fuera Docker).
4. En el servidor, descargas esa versión exacta y la ejecutas.
5. El servidor web (Nginx) por delante enruta el tráfico hacia el contenedor.

```bash
# En tu máquina (o en el pipeline)
docker build -t usuario/miapp:1.4.0 .
docker push usuario/miapp:1.4.0

# En el servidor
docker pull usuario/miapp:1.4.0
docker run -d --name miapp -p 3000:3000 usuario/miapp:1.4.0   # o: docker compose up -d
```

---

## 5. Todo junto: de la petición al despliegue

### 5.1 El panorama completo

```
usuario escribe miapp.com
  → DNS resuelve la IP del servidor
  → llega al servidor web (Nginx), que escucha en el puerto 443 (HTTPS)
      ├── pide /css/estilo.css  → lo sirve Nginx directamente, o una CDN por delante (estático)
      └── pide /api/productos   → Nginx lo reenvía a uno de los backends sanos (health check)
                                   con el servidor de aplicaciones (dinámico)
                                   → consulta la base de datos
                                   → devuelve JSON
  → Nginx devuelve la respuesta final al navegador
```

### 5.2 ¿Qué artefacto hay corriendo ahí detrás?

- Cada backend del esquema ejecuta **una versión concreta de un artefacto** (p. ej. la imagen `miapp:1.4.0`), descargada de un repositorio de artefactos.
- Saber exactamente qué versión hay en cada entorno es lo que permite diagnosticar incidencias y volver atrás con confianza.

### 5.3 Desplegar una versión nueva sin cortar el servicio

Con usuarios reales no se puede simplemente "apagar y encender". Estrategias habituales (se profundizan en la UD5):

| Estrategia | Cómo funciona |
|------------|---------------|
| **Rolling** (progresivo) | Se sustituyen los backends antiguos por los nuevos **de uno en uno**, mientras los demás siguen atendiendo tráfico. |
| **Blue-green** | Se levanta en paralelo un entorno completo con la versión nueva (*green*). Cuando está verificado, el servidor web pasa todo el tráfico a él y el antiguo (*blue*) queda de respaldo para un rollback inmediato. |
| **Canary** | La versión nueva recibe primero solo un pequeño porcentaje del tráfico; si va bien, se amplía poco a poco. |

### 5.4 Feature flags: separar "desplegar" de "lanzar"

- Una ***feature flag*** (interruptor de funcionalidad) es una condición en el código que **activa o desactiva una funcionalidad sin volver a desplegar**.
- Permite desplegar código nuevo ya **apagado** y lanzarlo después, cuando se decida, incluso solo para un grupo reducido de usuarios (algo parecido a un canary sin tocar la infraestructura).
- Si algo falla tras activarla, basta con **apagar el flag**: un rollback casi instantáneo.

### 5.5 El rollback no siempre es gratis: migraciones de base de datos

- Si la versión nueva **cambia el esquema** de la base de datos (añade una columna, cambia un tipo…), volver a desplegar el artefacto anterior **no deshace** ese cambio.
- Por eso las migraciones se diseñan, siempre que se puede, para ser **compatibles hacia atrás** durante un tiempo (p. ej. añadir una columna opcional en lugar de renombrar una existente), de modo que la versión antigua y la nueva del código convivan con el mismo esquema durante el despliegue.
- Idea para hoy: "desplegar código" y "migrar datos" están relacionados pero son cosas distintas.

### 5.6 Monitorización y rollback

- Tras desplegar, hay que vigilar métricas básicas: **errores 5xx** y **tiempo de respuesta**.
- Si el artefacto nuevo falla, tener la versión anterior bien identificada en el repositorio permite un **rollback rápido**: volver a desplegar la versión anterior conocida, en lugar de intentar arreglarlo en caliente.

### 5.7 Por qué esto no es "una caja negra" y qué viene después

Cada pieza del esquema es algo que ya conoces o vas a tocar pronto:

| Pieza | Dónde se ve |
|-------|-------------|
| Docker, imágenes, registries | UD1 |
| DNS, HTTP, arquitecturas | UD2 · bloque 2.1 |
| Apache/Nginx a fondo: hosts virtuales, HTTPS, proxy inverso, rendimiento | UD3 |
| Servidores de aplicaciones (Tomcat y similares) y transferencia de ficheros | UD4 |
| Automatización del despliegue (CI/CD) | UD5 |

---

## Ideas clave del bloque

- **Estático** = fichero servido tal cual; **dinámico** = código ejecutado en cada petición. Una página real suele mezclar ambos.
- **CSR** monta el HTML en el navegador; **SSR** en el servidor en cada petición; **SSG** en el build. SSR y SSG favorecen el SEO.
- Una **CDN** sirve copias cacheadas cerca del usuario; aprovecha sobre todo el contenido estático. El *cache busting* evita servir versiones antiguas.
- **Servidor web** (Apache, Nginx): sirve estático, comprime, hace de proxy. **Servidor de aplicaciones** (Tomcat, Node.js, Gunicorn, PHP-FPM): ejecuta la lógica.
- El patrón de producción habitual es **Nginx delante** (estático + proxy inverso) y **varios backends detrás**, con **balanceo** y **health checks**.
- Un frontend en CSR es **contenido estático** tras el build: lo sirve un servidor web, no necesita Node.js en producción.
- **CORS**: el backend autoriza con cabeceras `Access-Control-Allow-*` qué orígenes (esquema + host + puerto) pueden llamarle; lo aplica el navegador.
- **Desplegar** = poner la aplicación al alcance de los usuarios reales. Se despliega un **artefacto inmutable y versionado** (SemVer), el mismo en todos los entornos, con la **configuración y los secretos fuera**.
- Desplegar sin cortar el servicio: **rolling**, **blue-green**, **canary**, **feature flags**. Ojo con las **migraciones** de base de datos al hacer rollback.

---

## Anexo para el docente: cambios respecto a las diapositivas originales

Este documento se basa en *Bloque 2.2: Servidores web, de aplicaciones y despliegue*. Cambios realizados:

1. **"Despliegue continuo/rolling":** se renombra a **rolling (progresivo)**. El despliegue continuo (*continuous deployment*) es otra cosa —desplegar automáticamente cada cambio que supera el pipeline— y se verá en la UD5. Se añade **canary** con una línea, ya que el original lo menciona sin definirlo.
2. **CORS:** se añade qué es un **origen** (tabla de ejemplos), la petición **OPTIONS de preflight** (enlaza con el método OPTIONS del bloque 2.1) y se precisa que el navegador bloquea la **lectura de la respuesta**, no necesariamente el envío de la petición.
3. **Apache:** se menciona que el modelo "un proceso/hilo por conexión" corresponde al modo clásico (`prefork`) y que existe el modo `event`.
4. **Estrategias de balanceo:** el original solo las cita; se añade una línea de definición para cada una, por si surge la pregunta en clase.
5. Se añaden: tabla comparativa **CSR/SSR/SSG**, tabla **servidor web vs. servidor de aplicaciones**, ejemplos de cabeceras de **compresión** y de **CORS**, relación de **502/504** con el proxy inverso, ejemplo de **variables de entorno** por entorno, comandos del **flujo de despliegue**, tabla **SemVer** y la distinción **IaaS/PaaS** en el hosting cloud.
6. Se han dejado fuera las **preguntas de repaso** de las diapositivas originales para reutilizarlas al preparar el banco de preguntas tipo test.
