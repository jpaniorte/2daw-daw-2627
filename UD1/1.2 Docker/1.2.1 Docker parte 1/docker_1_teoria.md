---
marp: true
theme: default
paginate: true
backgroundColor: white
footer: 'Despliegue de Aplicaciones Web (0614) · UD1: Git & Docker'
layout: default
title: "Docker — Semana 1: Fundamentos (Teoría)"
permalink: /docker/semana-1/teoria/
pdf: "/UD1/1.2%20Docker/1.2.1%20Docker%20parte%201/pdf/docker_1_teoria.pdf"
---

<!-- _class: lead -->
# docker
## parte 1: fundamentos de Docker

---

<!-- _class: lead -->
# 1. Por qué hace falta Docker

---

## De Git a Docker

- Con **Git** aprendimos a gestionar versiones del código.
- Ahora el siguiente paso en el despliegue: ¿cómo hacemos que ese código se ejecute igual en cualquier sitio?
- Esa es la pregunta que responde **Docker**.

---

## El problema: "en mi máquina funciona"

- Tu aplicación funciona perfecto en tu portátil...
- ...pero falla en el servidor, o en el portátil de un compañero.
- Motivo habitual: **diferencias de entorno** (versión de lenguaje, librerías, configuración del sistema operativo...).

---

## Otra cara del mismo problema: estructura de equipos

No es solo un problema técnico: también es organizativo.

- Equipo de **desarrollo**: escribir código, entregar funcionalidades rápido.
- Equipo de **operaciones**: desplegar y mantener los sistemas estables.
- Objetivos en tensión: velocidad de entrega vs. estabilidad.
- → Solución habitual: metodologías ágiles y cultura **DevOps**.

---

## Cultura DevOps

- Enfoque que busca romper las barreras tradicionales entre Dev y Ops, fomentando una colaboración más estrecha.
- ⚠️ No confundas la cultura DevOps con las **herramientas** que ayudan a lograrla.
- **Docker ayuda a lograr una cultura DevOps, pero Docker no es DevOps.**

---

## Lectura recomendada

> *Accelerate. La ciencia del desarrollo Lean y DevOps* — Dra. Nicole Forsgren.

La cultura DevOps nos dice el **qué** (romper barreras, entregar con confianza). A partir de aquí nos centramos en una de las herramientas que lo hacen posible: **Docker**.

---

## Repaso — Sección 1, Pregunta 1

¿Cuál es la causa más habitual de que "en mi máquina funcione" pero falle en el servidor?

A) El servidor tiene menos RAM que tu portátil
B) Diferencias de entorno: versiones de lenguaje, librerías o configuración distintas
C) El código se corrompe al subirlo a GitHub
D) El servidor no tiene conexión a internet

---

## Repaso — Sección 1, Pregunta 1 (solución)

✅ **B)** Diferencias de entorno: versiones de lenguaje, librerías o configuración distintas

---

## Repaso — Sección 1, Pregunta 2

Según la cultura DevOps, ¿cuál de estas afirmaciones es correcta?

A) Docker es lo mismo que DevOps
B) DevOps es una herramienta que se instala junto con Docker
C) Docker ayuda a lograr una cultura DevOps, pero no es DevOps en sí misma
D) DevOps sustituye por completo al equipo de operaciones

---

## Repaso — Sección 1, Pregunta 2 (solución)

✅ **C)** Docker ayuda a lograr una cultura DevOps, pero no es DevOps en sí misma

---

## Repaso — Sección 1, Pregunta 3

¿Cuál es la tensión típica entre el equipo de desarrollo y el de operaciones?

A) Desarrollo quiere entregar rápido, operaciones quiere estabilidad
B) Ambos equipos persiguen exactamente el mismo objetivo
C) Operaciones escribe el código y desarrollo lo despliega
D) No existe ninguna tensión, es un problema inventado

---

## Repaso — Sección 1, Pregunta 3 (solución)

✅ **A)** Desarrollo quiere entregar rápido, operaciones quiere estabilidad

---

<!-- _class: lead -->
# 2. Docker, comparado con lo que ya conoces

---

## ¿Qué es Docker?

**Docker** es una plataforma que permite empaquetar una aplicación junto con todo lo que necesita para funcionar (código, dependencias, configuración) en una unidad llamada **contenedor**.

- Proyecto de código abierto, nacido en 2013.
- Hoy en día, el estándar de facto para contenerizar aplicaciones.

---

## ¿Qué aporta Docker?

- El mismo entorno en desarrollo, pruebas y producción.
- Portabilidad: funciona igual en cualquier máquina con Docker instalado.
- Despliegues más rápidos y reproducibles.
- Aislamiento entre aplicaciones que corren en la misma máquina.

---

## Contenedores vs. máquinas virtuales

Seguro que ya conoces las máquinas virtuales (VirtualBox, VMware...). Docker se parece, pero no es lo mismo.

---

## Máquina virtual: virtualiza el hardware

- Un **hipervisor** reparte el hardware físico.
- Cada VM ejecuta un **sistema operativo invitado completo**.
- Aislamiento muy fuerte, pero "pesado": arranque lento, mucho consumo de disco/RAM.

---

## Contenedor: virtualiza el sistema operativo

- Los contenedores **comparten el kernel** del sistema operativo host.
- No necesitan arrancar un SO completo: solo el proceso de la aplicación.
- Arranque casi instantáneo, mucho más ligeros.

---

## Comparativa rápida

| | Máquina virtual | Contenedor Docker |
| --- | --- | --- |
| Virtualiza | Hardware completo | Sistema operativo (procesos) |
| Incluye SO propio | Sí | No (comparte el del host) |
| Arranque | Lento (minutos) | Rápido (segundos) |
| Peso | Pesado (GBs) | Ligero (MBs) |
| Aislamiento | Muy fuerte | Fuerte, pero comparte kernel |

---

## ¿Se pueden combinar?

Sí: es muy habitual tener una **máquina virtual** (en un servidor físico o en la nube) que, dentro, ejecuta **varios contenedores Docker**.

---

## Repaso — Sección 2, Pregunta 1

¿Qué virtualiza una máquina virtual tradicional?

A) Solo el proceso de la aplicación
B) El hardware completo, mediante un hipervisor
C) Únicamente la red
D) Nada, las VMs no virtualizan nada

---

## Repaso — Sección 2, Pregunta 1 (solución)

✅ **B)** El hardware completo, mediante un hipervisor

---

## Repaso — Sección 2, Pregunta 2

¿Por qué un contenedor arranca mucho más rápido que una VM?

A) Porque usa menos CPU que la VM
B) Porque comparte el kernel del sistema operativo host, no arranca un SO completo
C) Porque los contenedores no tienen sistema de ficheros
D) Porque Docker desactiva el hipervisor

---

## Repaso — Sección 2, Pregunta 2 (solución)

✅ **B)** Porque comparte el kernel del sistema operativo host, no arranca un SO completo

---

## Repaso — Sección 2, Pregunta 3

¿Es posible ejecutar contenedores Docker dentro de una máquina virtual?

A) No, son tecnologías incompatibles
B) Sí, de hecho es una combinación muy habitual
C) Solo si la VM tiene Windows
D) Solo en la nube, nunca en local

---

## Repaso — Sección 2, Pregunta 3 (solución)

✅ **B)** Sí, de hecho es una combinación muy habitual

---

<!-- _class: lead -->
# 3. Los conceptos clave: imagen y contenedor

---

## Imagen vs. contenedor (la diferencia clave)

Ya sabemos que un contenedor es como una VM ligera que comparte el kernel. Pero, ¿de dónde sale exactamente ese contenedor?

- **Imagen**: plantilla de solo lectura (como una "foto" de un sistema con todo instalado).
- **Contenedor**: una instancia en ejecución (o parada) creada a partir de una imagen.

A partir de **una** imagen se pueden crear **muchos** contenedores distintos.

---

## Analogía

- La **imagen** es como la clase de una aplicación (el molde).
- El **contenedor** es como un objeto/instancia creado a partir de esa clase.
- Puedes crear varios contenedores a partir de la misma imagen, cada uno independiente.

---

## ¿Qué mantiene vivo a un contenedor?

- Un contenedor sigue vivo mientras su **proceso principal** (PID1) siga en ejecución.
- En Linux, el **PID1** es el primer proceso que arranca el sistema (tradicionalmente `init`/`systemd`).

---

## Contenedor = imagen + PID1

- Al hacer `docker run imagen comando`, ese `comando` se convierte en el **PID1** del contenedor.
- Si el PID1 termina, por el motivo que sea, **el contenedor se detiene automáticamente**.

---

## Ejemplo: PID1 en la práctica

```bash
docker run -it ubuntu:22.04 bash
```

- Aquí, `bash` es el PID1 del contenedor.
- Si escribes `exit`, `bash` termina → el contenedor pasa a "Exited".
- Si en vez de `bash` lanzas `ubuntu:22.04 echo hola`, el PID1 es `echo`: termina al instante y el contenedor se para casi enseguida.

---

## Repaso — Sección 3, Pregunta 1

¿Cuál es la diferencia principal entre una imagen y un contenedor?

A) Son exactamente lo mismo, solo cambia el nombre
B) La imagen es una plantilla de solo lectura; el contenedor es una instancia en ejecución creada a partir de ella
C) El contenedor se descarga de Docker Hub; la imagen no
D) La imagen solo existe mientras el contenedor está en marcha

---

## Repaso — Sección 3, Pregunta 1 (solución)

✅ **B)** La imagen es una plantilla de solo lectura; el contenedor es una instancia en ejecución creada a partir de ella

---

## Repaso — Sección 3, Pregunta 2

En un contenedor creado con `docker run -it ubuntu:22.04 bash`, ¿qué es el PID1?

A) El proceso `dockerd`
B) El proceso `bash`
C) El propio comando `docker run`
D) No existe el concepto de PID1 en Docker

---

## Repaso — Sección 3, Pregunta 2 (solución)

✅ **B)** El proceso `bash`

---

## Repaso — Sección 3, Pregunta 3

Si el proceso PID1 de un contenedor termina, ¿qué ocurre?

A) No pasa nada, el contenedor sigue corriendo
B) El contenedor se detiene automáticamente
C) Docker lo reinicia siempre sin que se pueda evitar
D) Se convierte automáticamente en una imagen

---

## Repaso — Sección 3, Pregunta 3 (solución)

✅ **B)** El contenedor se detiene automáticamente

---

<!-- _class: lead -->
# 4. De dónde salen las imágenes

---

## Ya sabemos qué es una imagen. ¿De dónde sale?

Para entender de dónde se consigue una imagen, hace falta ver primero cómo funciona Docker por dentro.

---

## Arquitectura de Docker: cliente y daemon

- **Docker client**: el comando `docker` que escribimos en la terminal.
- **Docker daemon** (`dockerd`): proceso en segundo plano que realmente gestiona contenedores, imágenes, redes y volúmenes.
- Cliente y daemon se comunican mediante una API (socket local o red).

---

## Esquema básico

```
tú → docker run nginx → [Docker client] → API → [Docker daemon]
                                                      │
                                      ¿tengo la imagen "nginx"?
                                      no → la pido a un registry
                                      sí → creo el contenedor
```

---

## Registries: de dónde vienen las imágenes

- Un **registry** es un servidor donde se almacenan y distribuyen imágenes.
- El más conocido: **Docker Hub** (registry público oficial).
- Existen otros: GitHub Container Registry, Amazon ECR, registries privados de empresa...

---

## Docker Hub

- Registro público con miles de imágenes listas para usar.
- **Imágenes oficiales**: mantenidas/revisadas por Docker o el propio proyecto (`ubuntu`, `nginx`, `python`, `node`...).
- Se pueden **descargar imágenes públicas sin necesidad de cuenta**.
- Hace falta cuenta y `docker login` solo para **subir** imágenes propias.

---

## Imágenes que usaremos en la asignatura

- [`nginx`](https://hub.docker.com/_/nginx) — servidor web.
- [`mariadb`](https://hub.docker.com/_/mariadb) — base de datos relacional.
- [`redis`](https://hub.docker.com/_/redis) — almacén clave-valor / caché.
- [`php`](https://hub.docker.com/_/php) — runtime de PHP.
- [`mongo`](https://hub.docker.com/_/mongo) — base de datos documental.

---

## Cuidado con el tag `latest`

Ya sabemos que una imagen es una plantilla, y que de cada una puede haber varias versiones. Esas versiones se identifican con **tags**.

- Si no indicas tag, Docker usa `latest` por defecto.
- `latest` no significa "la mejor versión": es solo una etiqueta más, que puede apuntar a una versión distinta con el tiempo.
- **Buena práctica**: fija siempre una versión concreta.
  - ✅ `ubuntu:22.04`
  - ❌ `ubuntu` (usa `latest` sin que lo decidas tú)
  - ❌ `ubuntu:latest` (explícito, pero mismo problema)

---

## Repaso — Sección 4, Pregunta 1

¿Qué es un registry?

A) Un fichero de configuración de Docker
B) Un servidor donde se almacenan y distribuyen imágenes
C) El nombre técnico de un contenedor parado
D) Un comando para borrar imágenes

---

## Repaso — Sección 4, Pregunta 1 (solución)

✅ **B)** Un servidor donde se almacenan y distribuyen imágenes

---

## Repaso — Sección 4, Pregunta 2

¿Hace falta tener cuenta en Docker Hub para descargar una imagen pública?

A) Sí, siempre
B) No, solo hace falta cuenta para subir imágenes propias
C) Solo los fines de semana
D) Solo si la imagen es oficial

---

## Repaso — Sección 4, Pregunta 2 (solución)

✅ **B)** No, solo hace falta cuenta para subir imágenes propias

---

## Repaso — Sección 4, Pregunta 3

Si ejecutas `docker run ubuntu` sin especificar tag, ¿qué versión descarga Docker?

A) La versión LTS más reciente siempre
B) `latest`, que puede apuntar a una versión distinta con el tiempo
C) Pide que elijas una versión antes de continuar
D) La versión 1.0 por compatibilidad

---

## Repaso — Sección 4, Pregunta 3 (solución)

✅ **B)** `latest`, que puede apuntar a una versión distinta con el tiempo

---

<!-- _class: lead -->
# 5. Manos a la obra

---

## Con todo esto claro, a crear contenedores de verdad

Ya sabemos qué es Docker, qué es una imagen y de dónde sale. Toca usar la herramienta.

---

## `docker run` — crear y arrancar un contenedor

```bash
docker run nginx
```

- Si la imagen `nginx` no está descargada, Docker la descarga primero.
- Crea un contenedor nuevo y lo arranca.

---

## Opciones útiles de `docker run`

```bash
docker run -d --name miweb nginx       # segundo plano + nombre
docker run -it ubuntu bash             # sesión interactiva
docker run --rm hello-world            # se autoelimina al terminar
```

- `-d`: modo "detached" (segundo plano).
- `--name`: le pones un nombre fácil de recordar.
- `-it`: terminal interactiva.
- `--rm`: se borra solo al terminar (ideal para pruebas rápidas).

---

## Si no usas `--name`...

- Docker asigna automáticamente un **nombre aleatorio** (adjetivo + apellido de científico, p. ej. `silly_einstein`, `nostalgic_curie`).
- Por eso conviene usar `--name`: evita tener que buscar luego ese nombre con `docker ps`.

---

## `docker ps` — ¿qué está en marcha?

```bash
docker ps        # solo contenedores en ejecución
docker ps -a     # todos, incluidos los parados
```

Muestra: ID, imagen, comando, fecha de creación, **estado**, puertos y nombre.

---

## `docker logs` — ver qué dice un contenedor

```bash
docker logs miweb
docker logs -f miweb      # en tiempo real
docker logs --tail 50 miweb
```

Imprescindible para depurar: si algo falla, aquí suele estar la pista.

---

## `docker images` y `docker pull`

```bash
docker images           # imágenes descargadas localmente
docker pull nginx:1.25  # descarga sin crear contenedor
```

- `docker pull` solo descarga.
- `docker run` descarga (si falta) **y además** crea y arranca un contenedor.

---

## Ciclo de vida de un contenedor

```
creado → en ejecución (running) → parado (exited) → eliminado
```

```bash
docker stop miweb     # parada ordenada
docker start miweb    # lo vuelve a arrancar (no crea uno nuevo)
docker restart miweb  # para y arranca de nuevo
docker rm miweb       # lo elimina definitivamente
```

---

## `docker stop` vs `docker kill`

- `docker stop`: intenta parar el contenedor de forma ordenada, con un margen de tiempo.
- `docker kill`: lo detiene de forma inmediata y brusca.
- Usa `kill` solo cuando `stop` no responde.

---

## `docker exec -it` — entrar en un contenedor vivo

```bash
docker exec -it miweb bash
docker exec -it miweb sh     # si no tiene bash (p.ej. alpine)
```

- A diferencia de `docker run`, **no crea** un contenedor nuevo.
- Abre una sesión dentro de un contenedor que **ya existe y está en ejecución**.
- Al salir con `exit`, el contenedor sigue funcionando con normalidad.

---

## `docker exec` sin sesión interactiva

```bash
docker exec miweb ls /app
docker exec miweb env
```

También sirve para lanzar un comando puntual sin abrir una terminal completa.

---

## Repaso visual del flujo de hoy

```
docker pull imagen     → la descargo
docker run imagen      → creo y arranco un contenedor
docker ps               → compruebo que está vivo
docker logs             → reviso qué dice
docker exec -it ... sh  → entro a inspeccionarlo
docker stop / rm         → lo paro y limpio
```

---

## Comandos que veremos hoy

- `docker run`, `docker ps`, `docker images`, `docker pull`
- `docker stop`, `docker start`, `docker restart`, `docker rm`
- `docker logs`, `docker exec -it`

---

## Repaso — Sección 5, Pregunta 1

¿Qué diferencia hay entre `docker run` y `docker start`?

A) Son exactamente el mismo comando
B) `docker run` crea un contenedor nuevo; `docker start` arranca uno que ya existe
C) `docker start` descarga la imagen y `docker run` no
D) `docker run` solo funciona con `-d`

---

## Repaso — Sección 5, Pregunta 1 (solución)

✅ **B)** `docker run` crea un contenedor nuevo; `docker start` arranca uno que ya existe

---

## Repaso — Sección 5, Pregunta 2

¿Qué hace la opción `--rm` en `docker run`?

A) Elimina la imagen después de usarla
B) Elimina automáticamente el contenedor en cuanto termina
C) Borra todos los contenedores parados del sistema
D) Impide que el contenedor se conecte a internet

---

## Repaso — Sección 5, Pregunta 2 (solución)

✅ **B)** Elimina automáticamente el contenedor en cuanto termina

---

## Repaso — Sección 5, Pregunta 3

¿Cuál es la diferencia entre `docker exec` y `docker run`?

A) `docker exec` entra en un contenedor que ya existe y está en marcha; `docker run` crea uno nuevo
B) Son sinónimos, hacen lo mismo
C) `docker exec` solo funciona con la imagen `nginx`
D) `docker run` no puede usarse con `-it`

---

## Repaso — Sección 5, Pregunta 3 (solución)

✅ **A)** `docker exec` entra en un contenedor que ya existe y está en marcha; `docker run` crea uno nuevo

---

<!-- _class: lead -->
# A practicar
## Primeros contenedores con Docker
