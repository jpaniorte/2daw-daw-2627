---
marp: true
theme: default
paginate: true
backgroundColor: white
footer: 'Despliegue de Aplicaciones Web (0614) · UD1: Git & Docker'
layout: default
title: "Docker — Semana 2: Imágenes y Dockerfile (Prácticas)"
permalink: /docker/semana-2/practicas/
---

<!-- _class: lead -->
# docker
## Prácticas — parte 2: imágenes y Dockerfile

---

## Antes de empezar

- Puedes usar el entorno en la nube propuesto (tipo iximiuz Labs) o tu propio Docker Desktop/VM/WSL2.
- Necesitarás una cuenta gratuita en [Docker Hub](https://hub.docker.com/) para el último ejercicio.
- Recuerda (semana 1): en iximiuz Labs no hay `localhost` — para ver un puerto publicado usa el botón **"Expose Port"** (arriba a la derecha), no `http://localhost:8080`.
- Ve resolviendo los ejercicios en orden, cada uno se apoya en el anterior.
- Los **retos** (al final) no traen los pasos, solo el objetivo: decides tú los comandos.

---

<!-- _class: lead -->
# Ejercicios guiados

---

## Ejercicio 1 — Tu primera imagen

1. Crea una carpeta `practica-docker` con un fichero `index.html` con contenido a tu elección.
2. Crea un `Dockerfile` que, a partir de `nginx:alpine`, copie `index.html` a `/usr/share/nginx/html/`.
3. Construye la imagen con el nombre `mi-web:1.0`.
4. Comprueba con `docker images` que aparece.

**Resultado esperado**: `docker images` muestra `mi-web` con tag `1.0`.

---

## Ejercicio 2 — Ejecútala y publícala

1. Ejecuta un contenedor a partir de `mi-web:1.0` publicando el puerto 80 del contenedor en el 8080 de tu máquina.
2. Abre `http://localhost:8080` (o la URL equivalente de tu entorno) y comprueba que ves tu página.
3. Para el contenedor y bórralo.

**Resultado esperado**: ves tu `index.html` en el navegador a través del puerto 8080.

---

## Ejercicio 3 — Una app con dependencias

1. Crea una carpeta nueva `practica-app` con un pequeño script (Node, Python o el lenguaje que prefieras) que imprima algo o levante un mini-servidor. He dejado un ejemplo al final del ejercicio.
2. Si tu lenguaje usa gestor de dependencias (`package.json`, `requirements.txt`...), créalo con al menos una dependencia.
3. Escribe un `Dockerfile` que: copie primero el fichero de dependencias, instale dependencias, copie después el resto del código, y defina `CMD` para ejecutar tu script.
4. Construye la imagen como `mi-app:1.0`.

**Resultado esperado**: `docker build` termina sin errores y `docker images` muestra `mi-app:1.0`.

Fichero app.py
```python
import os

from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify(message="Mini servidor listo")


@app.get("/health")
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
```

Fichero requirements.txt
```txt
Flask>=3.0,<4.0
```

Para instalar dependencias y arrancar servidor:
```bash
pip install -r requirements.txt
python app.py
```

---

## Ejercicio 4 — Aprovecha la caché

1. Ejecuta de nuevo `docker build` sobre `mi-app:1.0` sin cambiar nada. Fíjate en los mensajes "Using cache".
2. Modifica solo el código (no las dependencias) y reconstruye. ¿Qué capas se reconstruyen y cuáles no?
3. Modifica ahora el fichero de dependencias y reconstruye. ¿Qué cambia esta vez?

**Resultado esperado**: sabes explicar, con tus palabras, por qué cambiar el código no obliga a reinstalar dependencias si el Dockerfile está bien ordenado.

---

## Ejercicio 5 — Variables de entorno (`ENV` y `-e`)

`ENV` en el Dockerfile define un valor **por defecto** dentro de la imagen. `-e` en `docker run` lo **sobrescribe** solo para ese contenedor, sin reconstruir la imagen.

1. Modifica la ruta `/` de `app.py` para que devuelva un mensaje leído de una variable de entorno:
   ```python
   @app.get("/")
   def index():
       return jsonify(message=os.environ.get("MENSAJE", "Mini servidor listo"))
   ```
2. Añade al `Dockerfile` (antes del `CMD`): `ENV MENSAJE="Hola desde el Dockerfile"` y reconstruye como `mi-app:1.1`.
3. Ejecútala sin `-e`: `docker run -d --name app-env -p 5000:5000 mi-app:1.1` y haz `curl http://localhost:5000` (o "Expose Port"). Verás el mensaje del `ENV`.
4. Páralo y bórralo (`docker rm -f app-env`). Lánzalo otra vez **con la misma imagen** pero sobrescribiendo la variable:
   `docker run -d --name app-env -p 5000:5000 -e MENSAJE="Hola desde docker run" mi-app:1.1`
5. Vuelve a hacer `curl` y comprueba que el mensaje ha cambiado.

**Resultado esperado**: la misma imagen `mi-app:1.1` responde con dos mensajes distintos según uses o no `-e`.

---

## Ejercicio 6 — Bind mount (`-v ruta_host:ruta_contenedor`)

Un *bind mount* enlaza una carpeta **de tu máquina** con una carpeta del contenedor: ambos ven los mismos ficheros.

1. En la carpeta de `mi-app`, crea una carpeta vacía en el host: `mkdir datos`.
2. Ejecuta el contenedor montándola en `/datos`:
   `docker run -d --name app-bind -v "$(pwd)/datos:/datos" mi-app:1.1`
3. Crea un fichero **desde dentro del contenedor**:
   `docker exec app-bind sh -c 'echo hola > /datos/prueba.txt'`
4. En el host, comprueba que existe: `cat datos/prueba.txt`.
5. Ahora al revés: crea `datos/desde_host.txt` en el host y mira si el contenedor lo ve: `docker exec app-bind ls /datos`.
6. Limpia: `docker rm -f app-bind`.

**Resultado esperado**: los ficheros creados en un lado aparecen en el otro, y siguen en `./datos` aunque borres el contenedor.

---

## Ejercicio 7 — Volúmenes con nombre (`docker volume create`)

Aquí **no eliges ninguna carpeta del host**: es Docker quien crea y gestiona el almacenamiento. Solo usas un nombre.

1. Crea un volumen: `docker volume create datos-app`. Compruébalo con `docker volume ls`.
2. Inspecciónalo: `docker volume inspect datos-app`. Fíjate en el campo `Mountpoint` (dónde lo guarda Docker).
3. Ejecuta un contenedor usándolo (sin ruta del host, solo el nombre):
   `docker run -d --name app-vol -v datos-app:/datos mi-app:1.1`
4. Crea un fichero dentro: `docker exec app-vol sh -c 'echo persistente > /datos/nota.txt'`. Comprueba que **no** aparece en ninguna carpeta de tu proyecto.
5. Borra el contenedor: `docker rm -f app-vol`.
6. Crea un contenedor **nuevo** con el mismo volumen y lee el fichero:
   `docker run --rm -v datos-app:/datos mi-app:1.1 cat /datos/nota.txt`
7. Limpia: `docker volume rm datos-app`.

**Resultado esperado**: el fichero sobrevive al borrado del primer contenedor. Sabes explicar la diferencia con el bind mount: en el bind mount decides tú la carpeta del host; en el volumen con nombre la gestiona Docker.

---

## Ejercicio 8 — Publica tu imagen en Docker Hub

1. Haz `docker login` con tu cuenta de Docker Hub.
2. Retaguea `mi-app:1.0` como `tu_usuario/mi-app:1.0`.
3. Súbela con `docker push`.
4. Borra la imagen local y descárgala de nuevo con `docker pull tu_usuario/mi-app:1.0`.

**Resultado esperado**: tu imagen aparece en tu perfil de Docker Hub y puedes volver a descargarla.

---

<!-- _class: lead -->
# Retos

*Aquí no hay pasos: piensa qué instrucciones y comandos necesitas.*

---

## Reto 1 — Dockerfile mal escrito, a propósito

En las siguientes diapositivas tienes un `Dockerfile` por lenguaje (Node, Python y Java) que copia todo el código **antes** de instalar las dependencias.

**Objetivo**: elige el lenguaje que quieras (o hazlos los tres), reordena el `Dockerfile` para aprovechar la caché correctamente y demuestra, con dos builds (antes/después de un cambio de código), que ahora es más rápido.

*Pista: ¿qué fichero (y solo ese) necesita cada gestor de dependencias para descargarlas?*

---

## Reto 1 — Dockerfile roto (Node)

Proyecto con `package.json` y `server.js`.

```dockerfile
FROM node:20
WORKDIR /app
COPY . .
RUN npm install
CMD ["node", "server.js"]
```

---

## Reto 1 — Dockerfile roto (Python)

Proyecto con `requirements.txt` y `app.py` (puedes usar el del Ejercicio 3).

```dockerfile
FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

---

## Reto 1 — Dockerfile roto (Java)

Proyecto Maven con `pom.xml` y `src/` (el `pom.xml` debe generar `target/app.jar`, p. ej. con `<finalName>app</finalName>`).

```dockerfile
FROM maven:3.9-eclipse-temurin-21
WORKDIR /app
COPY . .
RUN mvn -q package
CMD ["java", "-jar", "target/app.jar"]
```

**Demuestra el fallo**: construye, cambia una línea de código y vuelve a construir. Verás que se vuelven a descargar **todas** las dependencias.

---

## Reto 2 — Reduce el tamaño de tu imagen

**Objetivo**: consigue que tu imagen `mi-app` ocupe menos espacio en disco (usa `docker images` para comparar), usando una imagen base más ligera y/o eliminando herramientas que solo hacían falta durante el build.

---

## Reto 3 — Dos contenedores que se hablan

**Objetivo**: crea una red Docker personalizada, levanta dos contenedores conectados a ella (por ejemplo, tu app y una base de datos como `mysql` o `postgres`) y demuestra que uno puede comunicarse con el otro **por nombre**, sin publicar puertos al host.

---

## Reto 4 — El puerto ocupado

**Objetivo**: provoca a propósito un error de "puerto ya en uso" ejecutando dos contenedores publicando el mismo puerto del host, interpreta el mensaje de error y resuélvelo sin parar ningún contenedor (usando otro puerto de host).

---

<!-- _class: lead -->
# Autoevaluación

---

## ¿Te ves capaz de...?

- [ ] Escribir un `Dockerfile` básico con `FROM`, `WORKDIR`, `COPY`, `RUN` y `CMD`.
- [ ] Explicar la diferencia entre `CMD` y `ENTRYPOINT`.
- [ ] Explicar por qué el orden de las instrucciones afecta a la caché de build.
- [ ] Construir una imagen con `docker build -t nombre:tag .`.
- [ ] Publicar y descargar una imagen propia en Docker Hub.
- [ ] Definir una variable con `ENV` y sobrescribirla con `-e` en `docker run`.
- [ ] Usar un bind mount (`-v ruta_host:ruta_contenedor`) para compartir una carpeta con el contenedor.
- [ ] Crear un volumen con `docker volume create` y usarlo para persistir datos de un contenedor.
- [ ] Explicar la diferencia entre bind mount y volumen con nombre.
