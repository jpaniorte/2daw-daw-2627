---
marp: true
theme: default
paginate: true
backgroundColor: white
footer: 'Despliegue de Aplicaciones Web (0614) · UD1: Git & Docker'
layout: default
title: "Docker — Semana 3: Docker Compose (Prácticas)"
permalink: /docker/semana-3/practicas/
---

<!-- _class: lead -->
# docker
## Prácticas — parte 3: Docker Compose

---

## Antes de empezar

- Puedes usar el entorno en la nube propuesto (tipo iximiuz Labs) o tu propio Docker Desktop/VM/WSL2.
- Necesitarás la aplicación que creaste en la Semana 2 (o una nueva, sencilla) para combinarla con una base de datos.
- Recuerda (semana 1): en iximiuz Labs no hay `localhost` — para ver un puerto publicado usa el botón **"Expose Port"** (arriba a la derecha), no `http://localhost:8080`.
- Hoy hacemos los **Ejercicios 1 a 4** (miércoles) y seguimos con el resto el **viernes**, antes del cuestionario final del bloque.

---

<!-- _class: lead -->
# Ejercicios guiados

---

## Ejercicio 1 — Tu primer docker-compose.yml

1. Crea una carpeta `practica-compose` con un fichero `docker-compose.yml`.
2. Define un único servicio `web` usando la imagen `nginx:1.27` (versión concreta, nunca `latest`) y publicando el puerto 8080 → 80.
3. Levántalo con `docker compose up -d`.
4. Comprueba en el navegador y con `docker compose ps` que funciona.

**Resultado esperado**: ves la página de nginx en `http://localhost:8080`.

---

## Ejercicio 2 — Añade un segundo servicio

1. En el mismo fichero, añade un servicio `db` con la imagen `postgres:16` y una variable `POSTGRES_PASSWORD`.
2. Ejecuta `docker compose up -d` de nuevo.
3. Comprueba con `docker compose ps` que ahora hay dos servicios en marcha.

**Resultado esperado**: `docker compose ps` muestra `web` y `db`, ambos "running"/"Up".

---

## Ejercicio 3 — Comunicación por nombre

Este ejercicio usa un `docker-compose.yml` **aparte** para no tocar el stack `web` + `db` de los ejercicios anteriores.

1. Crea una carpeta nueva `practica-ubuntu` con un `docker-compose.yml` que defina **dos servicios** llamados `ubuntu1` y `ubuntu2`, ambos con la imagen `ubuntu:24.04` (versión concreta, nunca `latest`), **sin `ports`**.
2. Una imagen de Ubuntu se para en cuanto arranca porque no tiene ningún proceso que mantener. Añade a cada servicio `command: sleep infinity` para que se quede en marcha.
3. Levántalos con `docker compose up -d` y comprueba con `docker compose ps` que los dos están "Up".
4. La imagen de Ubuntu no trae `ping`. Instálalo en el primer contenedor:
   `docker compose exec ubuntu1 bash -c "apt-get update && apt-get install -y iputils-ping"`
5. Desde `ubuntu1`, haz ping a `ubuntu2` **por su nombre**:
   `docker compose exec ubuntu1 ping -c 3 ubuntu2`
6. Repite en sentido contrario: instala `ping` en `ubuntu2` y haz ping a `ubuntu1`.
7. Mira qué IP tiene cada nombre: `docker compose exec ubuntu1 getent hosts ubuntu2`.
8. Limpia: `docker compose down`.

**Resultado esperado**: `ubuntu1` y `ubuntu2` se hacen ping por nombre en los dos sentidos sin haber publicado ningún puerto ni haber creado ninguna red: Compose la crea sola.

---

## Ejercicio 4 — Persistencia con volúmenes

1. Añade un volumen con nombre al servicio `db` apuntando a la carpeta de datos de Postgres.
2. Levanta el stack, crea algún dato de prueba dentro de la base de datos (puedes usar `docker compose exec db psql -U postgres`).
3. Haz `docker compose down` (sin `-v`) y vuelve a hacer `docker compose up -d`.
4. Comprueba que el dato de prueba sigue ahí.

**Resultado esperado**: los datos sobreviven a `docker compose down`.

---

## Ejercicio 5 — depends_on y logs

1. Añade `depends_on` para que `web` (o tu propia app) dependa de `db`.
2. Para todo el stack y vuelve a levantarlo con `docker compose up` (sin `-d`, para ver los logs en directo).
3. Observa el orden en que arrancan los servicios en la salida.
4. En otra terminal, usa `docker compose logs -f db` para seguir solo los logs de la base de datos.

**Resultado esperado**: puedes explicar, con los logs delante, en qué orden arrancó cada servicio.

---

## Ejercicio 6 — Tu propia app + base de datos

1. Retoma la app de la Semana 2 (o crea una sencilla) y añádela como servicio `app` con `build: .` en el `docker-compose.yml`.
2. Conéctala a `db` usando el nombre del servicio en la cadena de conexión (variable de entorno `environment`).
3. Comprueba que `app` puede leer/escribir en la base de datos.

**Resultado esperado**: tu aplicación, levantada con `docker compose up -d`, se conecta correctamente a la base de datos del mismo stack.

---

<!-- _class: lead -->
# Retos

*Aquí no hay pasos: piensa qué claves y comandos necesitas.*

---

## Reto 1 — Variables desde `.env`

**Objetivo**: mueve la contraseña de la base de datos (y cualquier otro dato sensible) a un fichero `.env`, referenciado desde el `docker-compose.yml` con `${VARIABLE}`, de forma que no quede ninguna contraseña escrita directamente en el YAML.

---

## Reto 2 — Solo lo necesario, accesible

**Objetivo**: configura tu stack para que la base de datos NO sea accesible desde el navegador/host (sin `ports` para `db`), pero `app` siga funcionando perfectamente contra ella.

---

## Reto 3 — Migración puntual

**Objetivo**: usando `docker compose run`, ejecuta un comando puntual dentro de un contenedor nuevo del servicio `app` (por ejemplo, un script que imprima la fecha o una migración si tu app la tiene), sin afectar al contenedor de `app` que ya está en marcha.

---

## Reto 4 — Stack completo desde cero

**Objetivo**: con el stack parado y eliminado por completo (`docker compose down -v`), levanta todo de nuevo con un único `docker compose up -d --build` y demuestra que vuelve a funcionar igual (salvo los datos, que al usar `-v` se habrán perdido a propósito).

---

<!-- _class: lead -->
# Autoevaluación

---

## ¿Te ves capaz de...?

- [ ] Escribir un `docker-compose.yml` con dos o más servicios.
- [ ] Explicar cómo se comunican dos servicios de la misma Compose sin publicar puertos.
- [ ] Usar un volumen con nombre para persistir datos de una base de datos.
- [ ] Explicar qué garantiza (y qué NO garantiza) `depends_on`.
- [ ] Diferenciar `docker compose up/down` de `stop/start`.
- [ ] Revisar logs y entrar en un servicio concreto con `exec`.
