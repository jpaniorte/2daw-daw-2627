# 1.2 Docker

Bloque de la UD1 ("Git & Docker") del módulo **Despliegue de Aplicaciones Web (0614)**, 2º CFGS DAW.

Docker no aparece citado literalmente en el currículo oficial, pero se incluye como contenido propio porque es la herramienta real con la que hoy en día se empaquetan, ejecutan y publican aplicaciones web: es la continuación natural de lo aprendido en **1.1 Git** dentro del flujo de trabajo de desarrollo y despliegue.

## Calendario

3 semanas, 3h/semana repartidas en dos sesiones:

| Semana | Carpeta | Miércoles (2h) | Viernes (1h) | Tema |
| --- | --- | --- | --- | --- |
| 1 | `1.2.1 Docker parte 1` | 7 oct | 9 oct | Fundamentos de Docker |
| 2 | `1.2.2 Docker parte 2` | 14 oct | 16 oct | Imágenes y Dockerfile |
| 3 | `1.2.3 Docker parte 3` | 21 oct | 23 oct | Docker Compose |

Reparto semanal: **1h de teoría + 2h de práctica** (teoría y arranque de la práctica el miércoles, cierre de la práctica y cuestionario el viernes).

## Temario

### Semana 1 — Fundamentos de Docker
- Qué es Docker y por qué se usa.
- Contenedores vs. máquinas virtuales.
- Arquitectura: daemon, cliente, imágenes, contenedores, registries.
- Docker Hub.
- Comandos básicos: `run`, `ps`, `images`, `pull`, `stop`, `rm`, `logs`, `exec -it`.

### Semana 2 — Imágenes y Dockerfile
- `Dockerfile`: `FROM`, `COPY`, `RUN`, `CMD`, `ENTRYPOINT`, `EXPOSE`, `ENV`, `WORKDIR`.
- Construcción de imágenes y caché de capas.
- Buenas prácticas, tags y versionado.
- Publicar imágenes en Docker Hub.
- Volúmenes y redes básicas.

### Semana 3 — Docker Compose
- `docker-compose.yml` y aplicaciones multi-contenedor.
- Redes y volúmenes en Compose.
- Comandos `up`, `down`, `logs`.
- Qué viene después (orquestadores tipo Kubernetes) y relación con el despliegue real de aplicaciones web.

## Entorno de prácticas

Se propone un entorno en la nube (p. ej. [Play with Docker](https://labs.play-with-docker.com/)) para evitar problemas de instalación, pero cada alumno puede usar el entorno que prefiera: Docker Desktop local, una VM Linux propia, WSL2, etc.

## Evaluación

Al final de cada semana (sesión del viernes) se realiza un **cuestionario en papel** de repaso de los contenidos de esa semana, con el mismo formato que los de Git: preguntas tipo test sacadas de un banco de 100 preguntas, con una versión distinta por alumno para evitar copias.

## Estructura de carpetas

Cada carpeta `1.2.N Docker parte N` sigue la misma convención que `1.1 Git`:

- `docker_N_teoria.md` — diapositivas de teoría (Marp).
- `docker_N_practicas.md` — ejercicios guiados + retos.
- `docker_N_test.md` — banco de 100 preguntas de repaso (sin soluciones).
- `docker_N_examen.md` — cuestionario imprimible de cierre de semana (20 versiones).
- `docker_N_examen_sol.md` — soluciones del cuestionario, para uso del profesor.
- `pdf/` y `pptx/` — generados con `python3 build.py` desde la raíz del repo, no se editan a mano.

## Enlaces

- [Documentación oficial de Docker](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Play with Docker](https://labs.play-with-docker.com/)
