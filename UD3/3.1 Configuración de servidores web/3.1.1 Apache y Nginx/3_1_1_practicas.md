---
layout: default
title: "Servidores Web — Bloque 3.1.1: Nginx (Prácticas)"
permalink: /servidores-web/semana-1/practicas/
---

# Práctica 3.1.1 — Tu Nginx en Internet

**Módulo:** Despliegue de Aplicaciones Web (0614) · 2º DAW · UD3: Administración de servidores web

## Objetivos

- Poner en marcha **Nginx** en un contenedor en tu VM y servir tu web en **`http://tunombre.me`**.
- Entender la **configuración** de Nginx: `nginx.conf`, `conf.d/`, bloques y directivas.
- Cambiar la configuración **sin romper el servicio**: `nginx -t` antes de `reload`.
- **Ampliar Nginx con módulos dinámicos**: miniaturas de imágenes (`image_filter`) y JavaScript (`njs`).
- Leer los **logs** de acceso y de errores, y diagnosticar un **403** y un **404**.
- Aplicar las **primeras medidas de seguridad**.

## Cómo funciona esta práctica

- **Se hace en clase**, en tu VM de Azure (`ssh daw`).
- Hay **puntos de control 🧑‍🏫**: cuando llegues a uno, **avisa al profesor**, que lo revisará contigo en tu pantalla antes de que sigas. Así se corrige sobre la marcha.
	- **Además, se entrega**: un documento con la **respuesta a cada pregunta ❓** (P1, P2…) y **cada evidencia 📸** (E1, E2…). En cada respuesta, incluye el comando que has usado y **solo el fragmento relevante** de la salida.
- En todos los comandos, **cambia `tunombre.me` por tu dominio**.

| Parte | Tiempo aprox. |
|-------|---------------|
| 0. Preparación | 5 min |
| 1. Tu primer Nginx | 10 min |
| 2. Tu web con tu configuración | 15 min |
| 3. Romper y arreglar | 10 min |
| 4. Módulos dinámicos | 20 min |
| 5. Logs, 403 y 404 | 15 min |
| 6. Seguridad | 5 min |

---

## 0. Preparación (5 min)

Desde tu ordenador (Git Bash en Windows):

```bash
ssh daw
```

Ya **dentro de la VM**:

```bash
docker ps                      # ¿hay algo usando el puerto 80?
docker rm -f prueba            # si sigue el contenedor de prueba del dosier 1
dig +short tunombre.me         # debe devolver la IP de tu VM
mkdir -p ~/daw/3.1.1 && cd ~/daw/3.1.1
```

> Si `dig` no devuelve tu IP, revisa el dosier 2 antes de seguir. Si `ssh daw` no funciona, revisa el dosier 1.

---

## 1. Tu primer Nginx (10 min)

### 1.1 Un comando, un servidor web

```bash
docker run -d --name primero -p 80:80 nginx:1.30
```

Abre `http://tunombre.me` en el navegador (**escribe `http://`**). Desde **tu ordenador** (no desde la VM):

```bash
curl -I http://tunombre.me
```

📸 **E1.** Captura del navegador con *Welcome to nginx!* y tu dominio en la barra de direcciones.

❓ **P1.** ¿Qué dice la cabecera `Server` de la respuesta? ¿Por qué puede ser un problema que un servidor público dé esa información?

### 1.2 Quién ejecuta qué

```bash
docker top primero
```

❓ **P2.** ¿Cuántos procesos hay? ¿Cuál es el **maestro** y con qué usuario corre? ¿Y los **workers**? ¿Por qué el maestro necesita ser `root` y los *workers* no? (Pista: el puerto 80.)

### 1.3 Dónde está la configuración

```bash
docker exec primero ls -l /etc/nginx /etc/nginx/conf.d /etc/nginx/modules/
docker exec primero cat /etc/nginx/nginx.conf
docker exec primero cat /etc/nginx/conf.d/default.conf
```

❓ **P3.** En los ficheros anteriores, localiza un ejemplo de cada **contexto** (`main`, `events`, `http`, `server`, `location`) y escribe una directiva que esté dentro de cada uno. ¿Qué línea de `nginx.conf` hace que se lea `default.conf`?

❓ **P4.** ¿En qué carpeta están los ficheros que se publican? ¿Qué fichero se sirve al pedir `/`? Indica las dos directivas que lo deciden.

Borra este contenedor; en la parte 2 lo haremos bien:

```bash
docker rm -f primero
```

---

## 2. Tu web con tu configuración (15 min)

Ahora la web y la configuración van a estar **en la VM** y se **montarán** en el contenedor.

### 2.1 Crear los ficheros

```bash
cd ~/daw/3.1.1
mkdir -p nginx/conf.d nginx/njs html/img html/descargas html/docs
```

**La web.** Crea `html/index.html` con tu nombre (usa `nano html/index.html` o pega el bloque):

```bash
cat > html/index.html <<'EOF'
<!doctype html>
<html lang="es">
<head><meta charset="utf-8"><title>Mi web</title></head>
<body>
  <h1>Web de TU NOMBRE</h1>
  <p>Servida por Nginx desde un contenedor en mi VM de Azure.</p>
</body>
</html>
EOF
```

**El sitio.** Crea `nginx/conf.d/default.conf`, con **tu dominio**:

```bash
cat > nginx/conf.d/default.conf <<'EOF'
server {
    listen 80;
    server_name tunombre.me www.tunombre.me;

    root  /usr/share/nginx/html;
    index index.html;
}
EOF
```

**El `compose.yaml`:**

```bash
cat > compose.yaml <<'EOF'
services:
  web:
    image: nginx:1.30
    ports:
      - "80:80"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./html:/usr/share/nginx/html:ro
    restart: unless-stopped
EOF
```

### 2.2 Levantarlo

```bash
docker compose up -d
docker compose ps
```

Abre `http://tunombre.me` y `http://www.tunombre.me`.

📸 **E2.** Captura del navegador con **tu** web en `http://tunombre.me`.

❓ **P5.** Explica qué hace cada línea de `volumes:`. ¿Qué significa `:ro` y por qué es buena idea aquí? Si haces `docker compose down` y luego `up -d`, ¿se pierde tu web? ¿Por qué?

### 2.3 ¿Cuándo hay que recargar?

1. Cambia el texto de `html/index.html` y recarga el navegador **sin hacer nada más**.
2. Ahora, en `nginx/conf.d/default.conf`, cambia `index index.html;` por `index portada.html index.html;`, crea `html/portada.html` con otro contenido y recarga el navegador.
3. Aplica el cambio de configuración:

```bash
docker compose exec web nginx -t
docker compose exec web nginx -s reload
```

4. Recarga el navegador otra vez. Al terminar, deja `index index.html;` como estaba, comprueba, recarga y borra `html/portada.html`.

❓ **P6.** ¿En qué casos has visto el cambio **sin** recargar Nginx y en cuáles **solo después** de recargarlo? ¿Por qué hay esa diferencia?

🧑‍🏫 **Punto de control 1:** enseña al profesor tu web en `http://tunombre.me` y `docker compose ps`.

---

## 3. Romper y arreglar (10 min)

### 3.1 Un `;` olvidado

Edita `nginx/conf.d/default.conf` y **quita el `;`** del final de la línea `index index.html;`.

```bash
docker compose exec web nginx -t
```

❓ **P7.** Copia el mensaje de error. ¿Qué información te da para encontrar el fallo?

Ahora intenta recargar igualmente, y comprueba si la web sigue funcionando:

```bash
docker compose exec web nginx -s reload
curl -s -o /dev/null -w "%{http_code}\n" http://localhost
```

### 3.2 El siguiente reinicio

Sin arreglar el error, reinicia el contenedor:

```bash
docker compose restart web
docker compose ps
```

Recarga el navegador.

📸 **E3.** Salida de `docker compose ps` justo después del reinicio.

❓ **P8.** ¿Qué ha pasado con la web después del `reload` y qué ha pasado después del `restart`? Explica por qué una configuración rota «no hace daño» hasta que alguien reinicia, y qué costumbre evita este problema.

Vuelve a poner el `;`, espera unos segundos y comprueba con `docker compose ps` que vuelve a estar `Up`. ¿Por qué arranca solo, sin que hagas nada? (Mira `compose.yaml`.)

---

## 4. Módulos dinámicos (20 min)

### 4.1 Qué módulos hay

```bash
docker compose exec web ls /etc/nginx/modules
docker compose exec web nginx -V 2>&1 | tr ' ' '\n' | grep _module
```

❓ **P9.** ¿Qué módulos **dinámicos** trae la imagen? (Ignora los `-debug`.) ¿Está el módulo `ssl` entre ellos o es **estático**? ¿Qué diferencia hay entre unos y otros a la hora de usarlos?

### 4.2 Una directiva sin su módulo

Añade este bloque **dentro** del `server` de `nginx/conf.d/default.conf`, antes de la llave final:

```nginx
    location /miniatura/ {
        alias /usr/share/nginx/html/img/;
        image_filter resize $arg_w -;
        image_filter_buffer 10M;
    }
```

```bash
docker compose exec web nginx -t
```

📸 **E4.** El mensaje de error de `nginx -t`.

❓ **P10.** ¿Por qué Nginx no conoce la directiva `image_filter` si el fichero del módulo está en `/etc/nginx/modules`?

### 4.3 Tu propia imagen con los módulos cargados

`load_module` va al principio de `nginx.conf`, que es un fichero **de la imagen**. Vamos a crear **tu propia imagen** a partir de la oficial.

1. Copia el `nginx.conf` original de la imagen a tu carpeta:

```bash
docker run --rm nginx:1.30 cat /etc/nginx/nginx.conf > nginx/nginx.conf
```

2. Edítalo (`nano nginx/nginx.conf`) y haz **tres cambios**:
   - **Al principio del todo**, antes de `user nginx;`, añade:
     ```nginx
     load_module modules/ngx_http_image_filter_module.so;
     load_module modules/ngx_http_js_module.so;
     ```
   - **Dentro de `http { }`**, antes de la línea `include /etc/nginx/conf.d/*.conf;`, añade:
     ```nginx
         js_path   /etc/nginx/njs/;
         js_import hola from hola.js;
     ```
   - Deja el resto como está.

3. Crea el `Dockerfile` de tu imagen:

```bash
cat > nginx/Dockerfile <<'EOF'
FROM nginx:1.30
COPY nginx.conf /etc/nginx/nginx.conf
COPY njs/ /etc/nginx/njs/
EOF
```

4. Crea `nginx/njs/hola.js`, **con tu nombre**:

```bash
cat > nginx/njs/hola.js <<'EOF'
function saludo(r) {
    const navegador = r.headersIn['User-Agent'];
    r.return(200, `Hola, soy el servidor de TU NOMBRE.\nHas pedido ${r.uri} con ${r.method}.\nTu navegador es: ${navegador}\n`);
}
export default { saludo };
EOF
```

5. En `nginx/conf.d/default.conf`, añade también dentro del `server`:

```nginx
    location = /hola {
        js_content hola.saludo;
    }
```

6. En `compose.yaml`, **cambia** la línea `image: nginx:1.30` por estas dos:

```yaml
    build: ./nginx
    image: miweb-nginx:1.0
```

7. Construye y levanta:

```bash
docker compose up -d --build
docker compose exec web nginx -t
docker compose exec web sh -c 'nginx -T 2>/dev/null | grep load_module'
```

> **Si `nginx -t` falla**, lee el mensaje: el error más probable es haber puesto `load_module` dentro de `http { }` (`"load_module" directive is not allowed here`) o haber olvidado un `;`. Corrige `nginx/nginx.conf` y repite `docker compose up -d --build`.

### 4.4 Miniaturas al vuelo

Sube una **foto tuya grande** (por ejemplo, una del móvil) desde **tu ordenador** (abre otro terminal; no dentro de la VM):

```bash
scp ruta/a/tu/foto.jpg daw:~/daw/3.1.1/html/img/foto.jpg
```

> Si no tienes una a mano, desde la VM: `curl -L -o ~/daw/3.1.1/html/img/foto.jpg https://picsum.photos/1600/1000`

Comprueba en el navegador:

- `http://tunombre.me/img/foto.jpg`
- `http://tunombre.me/miniatura/foto.jpg?w=100`
- `http://tunombre.me/miniatura/foto.jpg?w=400`

Y mide lo que ocupa cada una, desde la VM:

```bash
for w in 100 400 800; do
  printf "w=%s -> " $w
  curl -s -o /dev/null -w "%{size_download} bytes\n" "http://localhost/miniatura/foto.jpg?w=$w"
done
curl -s -o /dev/null -w "original -> %{size_download} bytes\n" http://localhost/img/foto.jpg
```

📸 **E5.** Captura del navegador con una miniatura (`?w=400`) y tu dominio en la barra.

❓ **P11.** Completa una tabla con el tamaño en bytes de la original y de las tres miniaturas. ¿Cuántos ficheros de imagen hay en el disco de la VM? ¿Qué gana una web con móviles si sirve la miniatura en lugar de la original? ¿Qué es `$arg_w`?

### 4.5 JavaScript dentro de Nginx

Desde **tu ordenador**:

```bash
curl http://tunombre.me/hola
```

Y abre `http://tunombre.me/hola` en el navegador.

📸 **E6.** La salida de `curl` y la captura del navegador.

❓ **P12.** ¿Por qué el «navegador» es distinto en cada caso? ¿De dónde saca njs ese dato? (Pista: bloque 2.1, cabeceras.) La respuesta de `/hola`, ¿es contenido **estático** o **dinámico**?

🧑‍🏫 **Punto de control 2:** enseña al profesor una miniatura y `/hola` funcionando en tu dominio.

---

## 5. Logs, 403 y 404 (15 min)

### 5.1 Tu propia petición

En un **segundo terminal** (`ssh daw`):

```bash
cd ~/daw/3.1.1 && docker compose logs -f
```

Averigua tu IP pública desde **tu ordenador** con `curl ifconfig.me`. Después recarga `http://tunombre.me` en el navegador y busca **tu línea** en el log.

❓ **P13.** Copia tu línea del log de acceso y explica **cada campo**: IP, fecha, petición, código, tamaño, *referer* y *user-agent*. ¿Coincide la IP con la de `curl ifconfig.me`?

### 5.2 Provocar un 404 y dos 403

En el **primer terminal**:

```bash
cd ~/daw/3.1.1

# 404: un fichero que no existe
curl -s -o /dev/null -w "%{http_code}\n" http://localhost/noexiste.html

# 403 por permisos: un fichero que el usuario nginx no puede leer
echo "secreto" > html/secreto.html
chmod 600 html/secreto.html
ls -l html/secreto.html
curl -s -o /dev/null -w "%{http_code}\n" http://localhost/secreto.html

# 403 por carpeta sin index.html
echo "x" > html/docs/notas.txt
curl -s -o /dev/null -w "%{http_code}\n" http://localhost/docs/
```

Ahora mira **solo el log de errores**:

```bash
docker compose logs web --no-log-prefix 2>&1 | grep -E "error|forbidden" | tail -5
docker logs $(docker compose ps -q web) 2>&1 >/dev/null | tail -5
```

📸 **E7.** Las líneas del log de errores de los tres casos.

❓ **P14.** Para cada caso (404, 403 de `secreto.html`, 403 de `docs/`), ¿qué dice el log de errores? ¿Por qué el usuario `nginx` no puede leer `secreto.html`? (Mira el propietario y los permisos de `ls -l`.) Arréglalo con `chmod 644 html/secreto.html` y comprueba que da 200.

### 5.3 Las visitas que no has pedido

```bash
docker logs $(docker compose ps -q web) 2>/dev/null | grep 'HTTP/' | awk '{print $9}' | sort | uniq -c
docker logs $(docker compose ps -q web) 2>/dev/null | grep 'HTTP/' | grep -v "TU_IP" | tail -20
```

(Cambia `TU_IP` por la IP de `curl ifconfig.me`).

📸 **E8.** La salida del recuento de códigos de estado.

❓ **P15.** ¿Hay peticiones que **no** son tuyas ni de tus compañeros? Copia dos y explica qué crees que buscaban. Si todavía no hay ninguna, déjalo abierto y vuelve a mirarlo al final de la clase.

---

## 6. Seguridad (5 min)

### 6.1 Ocultar la versión

```bash
curl -I http://tunombre.me | grep -i server
```

En `nginx/nginx.conf`, dentro de `http { }`, añade:

```nginx
    server_tokens off;
```

```bash
docker compose up -d --build
curl -I http://tunombre.me | grep -i server
```

📸 **E9.** La cabecera `Server` antes y después.

❓ **P16.** ¿Por qué ha hecho falta `--build` para este cambio y no para los cambios de `conf.d/`? Ocultar la versión, ¿hace que el servidor sea seguro? ¿Qué más hay que hacer?

### 6.2 Un listado de ficheros, solo donde toca

Pon un par de ficheros en `html/descargas/` y añade en `nginx/conf.d/default.conf`, dentro del `server`:

```nginx
    location /descargas/ {
        autoindex on;
    }
```

```bash
echo "apuntes" > html/descargas/apuntes.txt
docker compose exec web nginx -t && docker compose exec web nginx -s reload
```

Abre `http://tunombre.me/descargas/` y `http://tunombre.me/docs/`.

❓ **P17.** ¿Qué diferencia ves entre las dos carpetas? ¿Qué riesgo tendría poner `autoindex on;` para todo el `server`?

🧑‍🏫 **Punto de control 3:** enseña al profesor `curl -I` sin versión, `/descargas/` con listado y `/docs/` con 403.

---

## Ampliación (si terminas antes)

1. **Más filtros de imagen.** Crea una `location /cuadrada/` que use `image_filter crop 200 200;` y otra `location /medidas/` con `image_filter size;`. ¿Qué devuelve esta última? ¿En qué formato?
2. **`load_module` en el sitio equivocado.** Mueve una línea `load_module` dentro de `http { }`, reconstruye y lee el error. Vuelve a dejarla bien.
3. **La configuración completa.** Ejecuta `docker compose exec web nginx -T` y localiza en la salida tu `default.conf`. ¿Para qué sirve `-T` cuando hay muchos ficheros `include`?
4. **Un endpoint en JSON.** Cambia `hola.js` para que devuelva un JSON con la URI, el método y la fecha (`new Date().toISOString()`), con la cabecera `Content-Type: application/json` (`r.headersOut['Content-Type'] = 'application/json';`). Como `hola.js` está dentro de la imagen, ¿qué tienes que hacer para que el cambio se aplique?

---

## Al terminar

**No borres nada:** en la práctica 3.1.2 seguirás con esta misma carpeta (`~/daw/3.1.1`) para añadir más sitios. Puedes dejar el contenedor en marcha; así seguirán llegando visitas de bots a tu log.

Revisa que tu documento tiene:

| Evidencias | Preguntas |
|------------|-----------|
| E1 *Welcome to nginx!* en tu dominio | P1 – P4 (parte 1) |
| E2 Tu web en tu dominio | P5 – P6 (parte 2) |
| E3 `docker compose ps` tras el reinicio con la configuración rota | P7 – P8 (parte 3) |
| E4 Error `unknown directive` | P9 – P12 (parte 4) |
| E5 Miniatura en el navegador | |
| E6 `/hola` con `curl` y con el navegador | |
| E7 Log de errores del 404 y los dos 403 | P13 – P15 (parte 5) |
| E8 Recuento de códigos de estado | |
| E9 Cabecera `Server` antes y después | P16 – P17 (parte 6) |

Y que los tres **puntos de control 🧑‍🏫** están revisados por el profesor.
