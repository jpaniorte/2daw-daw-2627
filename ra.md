# Planificación de contenidos · UD1 a UD5

**Módulo:** Despliegue de Aplicaciones Web (0614) · 2º DAW

Este documento resume qué se ve en cada apartado del módulo, para tener una visión de conjunto antes de preparar la teoría, las diapositivas, las prácticas y los tests de cada semana.

- **UD1 y UD2 ya están impartidas:** aquí se resumen tal como se dieron, a partir de los materiales de `UD1/` y `UD2/`.
- **UD3, UD4 y UD5 son planificación:** cada apartado ocupa una semana de **3 sesiones (2 h de teoría + 1 h de práctica)**. Si algún apartado tiene otra duración, los tiempos se ajustan, pero los contenidos sirven igual.
- **Desde 3.1.1 se trabaja sobre infraestructura real:** cada alumno o alumna tiene su **máquina virtual Ubuntu en Azure** y su **dominio `.me` en Namecheap**, los dos del GitHub Student Developer Pack. Los crea antes, en otra asignatura, siguiendo los dos dosieres de `UD3/3.0 Puesta en marcha/` (ver el apartado 3).

---

## 1. Visión general

Semanas numeradas según el calendario de `index.md`.

| Semana | Apartado                                                            | Idea central                                                       | Práctica                                                  |
| ------ | ------------------------------------------------------------------- | ------------------------------------------------------------------ | --------------------------------------------------------- |
| 2      | **1.1.1** Git en local                                              | Guardar la historia de un proyecto                                 | Primer repositorio, commits, `.gitignore` y `git log`     |
| 3      | **1.1.2** Ramas y resolución de conflictos                          | Trabajar en paralelo sin pisarse                                   | Ramas, *merge*, conflictos, `reset` y `revert`            |
| 4      | **1.1.3** Repositorios remotos                                      | Colaborar a través de GitHub                                       | Push, pull, fork y primer *pull request*                  |
| 5      | **1.2.1** Fundamentos de Docker                                     | «En mi máquina funciona» deja de ser un problema                   | Primeros contenedores y su ciclo de vida                  |
| 6      | **1.2.2** Imágenes y Dockerfile                                     | Empaquetar tu propia aplicación                                    | Dockerfile propio, volúmenes y publicación en Docker Hub  |
| 7      | **1.2.3** Docker Compose                                            | Varias piezas que arrancan juntas                                  | Primer *stack* app + base de datos                        |
| 8      | **2.1** Fundamentos web                                             | Redes, HTTP, sesiones y arquitecturas                              | HTTP por dentro con `curl`: cookies y sesiones            |
| 9      | **2.2** Servidores web y de aplicaciones                            | Servidor web delante, aplicaciones detrás; qué es desplegar        | Nginx como proxy y balanceador, CORS, *rolling* y *rollback* |
| 10     | **3.1.1** Instalación y configuración básica de Nginx (y Apache, en teoría) | Poner en marcha un servidor web, entender su configuración y ampliarlo con módulos | Nginx (imagen oficial) en la VM, servir `<alumno>.me`, cargar módulos dinámicos y leer logs |
| 11     | **3.1.2** Hosts virtuales y redirecciones                           | Un servidor, muchas webs; enviar al cliente a otra URL             | Dos subdominios reales y redirecciones 301/302            |
| 12     | **3.2.1** HTTPS y control de acceso                                 | Cifrar la comunicación y decidir quién entra                       | Let's Encrypt, PositiveSSL, HTTPS obligatorio y `/admin`  |
| 13     | **3.2.2** Proxy inverso, monitorización y rendimiento               | El servidor web como puerta de entrada de otras aplicaciones       | Nginx delante de dos backends, logs y prueba de carga     |
| 14     | **4.1.1** Servidores de aplicaciones                                | Ejecutar aplicaciones Java con Tomcat de forma segura              | Tomcat, despliegue de WAR, Manager y *realms*             |
| 15     | **4.1.2** Aplicaciones con base de datos e integración con el proxy | Aplicación + base de datos + Nginx delante                         | Pila completa con Docker Compose en la VM                 |
| 16     | **4.2.1** FTP, SFTP, SSH, DNS y LDAP                                | Transferir ficheros, administrar en remoto, nombres y usuarios centralizados | Claves SSH, vsftpd, DNS del dominio propio y LDAP |
| 17     | **5.1.1** Fundamentos de DevOps y primer workflow                   | Automatizar lo que hacíamos a mano                                 | Primer workflow de GitHub Actions                         |
| 18     | **5.1.2** Artefactos, imágenes Docker y tests en el pipeline        | Construir y publicar solo lo que pasa los tests                    | Pipeline que prueba, construye y publica una imagen       |
| 19     | **5.2.1** Despliegue por SSH, documentación y proyecto integrador   | El pipeline despliega solo en el servidor y publica la documentación | Despliegue automático en la VM de Azure y documentación |

### Cómo encaja cada unidad

```
UD1: Git     → control de versiones, documentación colaborativa, base de UD5
     Docker  → el entorno de todas las prácticas y la forma de empaquetar
UD2 (teoría) → toda la arquitectura «sobre el papel»: HTTP, servidor web, servidor de aplicaciones, despliegue
UD3          → servidor web real (Apache/Nginx) en la VM: hosts virtuales, HTTPS, proxy inverso
UD4          → servidor de aplicaciones (Tomcat), base de datos y servicios de red (SSH/SFTP/FTP, DNS, LDAP)
UD5          → automatizar todo el despliegue (CI/CD) contra la VM y documentar
```

---

## 2. Dos hilos conductores

### 2.1 La aplicación que crece

Una **misma aplicación** que se va completando semana a semana y que termina siendo la base del proyecto integrador:

| Semana | Estado de la aplicación |
|--------|------------------------|
| 1.1.1 – 1.1.3 | Una web personal en un repositorio Git, con ramas y publicada en GitHub |
| 1.2.1 – 1.2.3 | La misma web en un contenedor, con su `Dockerfile` y un `docker-compose.yml` con base de datos |
| 2.1 – 2.2 | Se estudia cómo viaja por HTTP y cómo se sirve detrás de Nginx (entornos de práctica en local) |
| 3.1.1 – 3.1.2 | Una web estática (HTML/CSS) en **`http://<alumno>.me`**, servida por Nginx, en un contenedor, en la VM de Azure, y un segundo sitio en `tienda.<alumno>.me` |
| 3.2.1 | La misma web, ahora solo por **HTTPS con certificado real** y con una zona `/admin` protegida |
| 3.2.2 | Nginx delante de un backend (puede reutilizarse httpbin o la app de la práctica 2.2) |
| 4.1.1 – 4.1.2 | Una aplicación Java en Tomcat con base de datos, detrás de Nginx |
| 4.2.1 | Se administra y se actualiza en remoto por SSH/SFTP; `/admin` valida contra LDAP |
| 5.1.1 – 5.2.1 | Todo lo anterior se construye, se prueba y se despliega automáticamente en la VM |

Ventaja: el alumnado entiende cada pieza como parte de un todo, y en el proyecto integrador no empieza de cero.

### 2.2 El restaurante

La analogía empieza en las presentaciones de la UD2 y continúa en las siguientes, para que las diapositivas mantengan la coherencia:

| Apartado | Analogía |
|----------|----------|
| 2.1 | **Comensal** (cliente), **cocina** (servidor), **camarero** (HTTP), **comanda** (petición), **plato** (respuesta), **dirección del local** (IP y puerto), **guía de restaurantes** (DNS) y **número de mesa** (cookie de sesión) |
| 2.2 | **Pan y bebidas** (estático) frente a **plato al momento** (dinámico), **la barra** (servidor web), **los cocineros** (servidor de aplicaciones), **locales satélite** (CDN), **jefe de sala** (balanceador), **lote envasado** (artefacto) y **abrir al público** (desplegar) |
| 3.0 | **Alquilar el local** (la VM en Azure) y **poner el rótulo en la calle** (el dominio) |
| 3.1.1 | **Montar la barra**: instalarla en el local, abrirla y apuntar cada comanda en el libro (log de acceso) y cada incidencia en el parte (log de errores); los **módulos** son electrodomésticos que se enchufan a la barra cuando hacen falta; el camarero (`nginx`) sin llave de un armario no puede servir el plato (403) |
| 3.1.2 | **Una cocina, varias marcas** (hosts virtuales) y el cartel de «nos hemos mudado» (301) |
| 3.2.1 | **Hablar en clave** con el camarero (TLS); el certificado es la **licencia colgada en la pared** que expide el ayuntamiento (CA); el **portero** con la lista de invitados (control de acceso) |
| 3.2.2 | **La barra pasa comandas a la cocina** (proxy inverso), el **jefe de sala** las reparte (balanceo), el **libro de reclamaciones** (logs) y los **platos preparados de antemano** (caché) |
| 4.1.1 | **Contratar a los cocineros** (Tomcat) y entregarles la **receta empaquetada** (WAR) |
| 4.1.2 | **La despensa** (base de datos) y el pasillo entre cocina y despensa |
| 4.2.1 | El **sumiller** (FTP/SFTP), la **llave de la puerta trasera** (SSH), la **guía de restaurantes** (DNS) y el **registro de empleados de la cadena** (LDAP: una sola ficha sirve en todos los locales) |
| 5.1.1 | Una **cadena de restaurantes** donde cada receta nueva pasa un control de calidad automático (CI) |
| 5.1.2 | **Lotes envasados y etiquetados** (artefactos) que solo salen si superan la cata (tests) |
| 5.2.1 | **Abrir un local nuevo de forma automática** y el **manual de la franquicia** (documentación); el proyecto integrador es inaugurar tu propio restaurante |

---

## 3. Entorno de trabajo

### 3.1 Recursos del GitHub Student Developer Pack

| Recurso | Oferta | Uso en el módulo |
|---------|--------|------------------|
| **Microsoft Azure** (Azure for Students) | Más de 25 servicios gratuitos y 100 $ de crédito, sin tarjeta. Solo para mayores de 18 años. Se activa con el correo `@alu.edu.gva.es`, sin necesidad del Pack | Una **VM Linux** por alumno, **la misma del Proyecto Intermodular**: el servidor de producción desde 3.1.1 hasta 5.2.1 |
| **Namecheap** | Dominio `.me` gratis 1 año y un certificado SSL (PositiveSSL) gratis 1 año | El **dominio `<alumno>.me`** desde 3.1.1; el certificado se activa en 3.2.1 |

Todo se prepara **antes de 3.1.1**, en el Proyecto Intermodular, con estas guías:

| Guía | Qué se hace |
|------|-------------|
| `proyectos/maquina-remota.md` (Proyecto, fase 1) | Activar Azure for Students con el correo del centro y comprobar los 100 $ |
| `proyectos/vm-ubuntu.md` (Proyecto, fase 2) | Crear la VM Ubuntu desde *Servicios gratuitos* (tamaño gratuito ya preseleccionado) y conectarse por SSH con clave |
| `UD3/3.0 Puesta en marcha/dosier_azure_vm.md` (dosier 1) | Preparar esa VM para DAW: IP estática, puertos 22/80/443, alias `ssh daw`, actualización, zona horaria, Docker, alerta de presupuesto y prueba del puerto 80 |
| `UD3/3.0 Puesta en marcha/dosier_namecheap_dominio.md` (dosier 2) | Reclamar el `.me`, desactivar la renovación automática, crear los registros DNS hacia la VM, comprobar la propagación y reclamar (sin activar) el certificado |

El **GitHub Student Pack** solo hace falta para Namecheap. Se pide con la cuenta de GitHub creada en 1.1.3, y **la verificación puede tardar días**, así que conviene pedirlo cuanto antes.

El usuario de la VM lo elige cada alumno en el Proyecto (`azureuser`, el del centro…). Para que el material sea igual para todos, el dosier 1 crea el alias **`ssh daw`** en `~/.ssh/config`, y todos los comandos de Despliegue empiezan así.

### 3.2 Arquitectura de trabajo

```
PC del alumno (Git Bash, VS Code, Docker local para probar)
   │  ssh daw  (alias → <usuario>@<alumno>.me, solo con clave)
   ▼
VM Ubuntu Server LTS en Azure, la del Proyecto  (tamaño gratuito, IP pública estática, NSG: 22/80/443)
   ├── Apache / Nginx           (UD3)
   ├── Tomcat + base de datos   (UD4, con Docker Compose)
   └── despliegues de GitHub Actions por SSH (UD5)
DNS en Namecheap: <alumno>.me, www, tienda… → IP de la VM
```

- **Docker local** sigue siendo la herramienta para probar antes de llevar los cambios a la VM y para lo que no necesita Internet (OpenLDAP, vsftpd, pruebas de balanceo).
- **Los servidores se ejecutan con Docker, también en la VM.** El servidor web es **Nginx** con la imagen oficial (`nginx:1.30`), o una imagen propia `FROM nginx:1.30` cuando hay que llevar la configuración dentro. **Apache se estudia en la teoría** (arquitectura, MPM, estructura de Debian, `.htaccess`, equivalencias con Nginx), pero no se monta: los RA no obligan a usar un servidor concreto. Tomcat y las bases de datos, con sus imágenes oficiales (UD4).
- **Docker Desktop y la VM no se comportan igual con los *bind mounts*:** en macOS y Windows los permisos se traducen, así que un 403 por permisos solo se ve en la VM Linux.
- **El fichero `hosts`** (bloque 2.1) queda como respaldo para simular dominios cuando no se pueda tocar el DNS real.
- **Cuenta de GitHub** para la UD5 (GitHub Actions y GitHub Container Registry).

### 3.3 Avisos

- **Coste:** la VM de tamaño gratuito tiene 750 h al mes (una VM encendida todo el mes). Una segunda VM o un tamaño mayor gastan crédito, y la IP pública cuesta unos 3,6 $ al mes. **Despliegue usa la misma VM que el Proyecto, no una segunda.** El dosier 1 configura una **alerta de presupuesto** y pide **no activar el apagado automático** (la VM tiene que estar encendida para renovar certificados y recibir despliegues).
- **Tamaño y arquitectura:** la vía de *Servicios gratuitos* propone B2ats v2 (x64) o B2pts v2 (**Arm**). Quien tenga una VM Arm tendrá que construir sus imágenes también para `linux/arm64` en la UD5; el dosier 1 le pide que lo apunte.
- **Caducidad:** el crédito de Azure, el dominio y el certificado duran 12 meses. Hay que **desactivar la renovación automática del dominio** (después del primer año cuesta unos 20 $).
- **Plan B** para quien no pueda usar Azure (menor de 18 años, cuenta de estudiante sin verificar): VM local con Ubuntu Server (VirtualBox o UTM) y dominio simulado en `hosts`. Pierde Let's Encrypt y el despliegue desde GitHub Actions; en 5.2.1 se sustituye por un *self-hosted runner*.

---

## 4. Unidad 1 · Git y Docker *(impartida)*

### 1.1.1 Git en local

**Objetivo:** entender qué es un sistema de control de versiones y guardar la historia de un proyecto con Git.

**Contenidos de teoría**

1. **Sistemas de control de versiones:** qué aportan, cuáles existen (centralizados frente a distribuidos) y por qué Git.
2. **Configuración inicial:** `git config` (`user.name`, `user.email`, niveles `--global` y `--local`) y cómo comprobarla.
3. **Crear un repositorio:** `git init` y la carpeta `.git`.
4. **Los tres estados de un fichero:** modificado, preparado (*staging*) y confirmado. `git status`, `git add` y `git commit`.
5. **`.gitignore`:** logs, dependencias, configuración local con datos sensibles y ficheros del sistema o del editor.
6. **Historial:** `git log`, `git log --oneline` y `git diff`.
7. **Buenas prácticas de commits:** commits pequeños y mensajes descriptivos.

**Práctica:** identificarse, crear el primer repositorio, ignorar lo que no toca, hacer el ciclo completo de commits y revisar el historial. Retos: commit selectivo, todos los estados a la vez, un `.gitignore` que no funciona porque el fichero ya estaba versionado, y reconstruir una historia.

**Conceptos clave para el test:** los tres estados, qué guarda `git add` y qué guarda `git commit`, alcance de `git config`, por qué un fichero ya versionado ignora el `.gitignore`, y lectura de `git log`.

---

### 1.1.2 Ramas y resolución de conflictos

**Objetivo:** trabajar en paralelo con ramas, fusionarlas y resolver conflictos, y saber deshacer cambios con seguridad.

**Contenidos de teoría**

1. **`git commit --amend`** para corregir el último commit.
2. **`HEAD`** y cómo se mueve.
3. **Ramas:** `git branch`, `git checkout` (y `git switch`), nombrar bien las ramas (`feature/…`, `fix/…`) y visualizar el historial.
4. **El *detached HEAD***: qué es, qué puede pasar y cómo salir.
5. **Fusionar:** *fast-forward* frente a fusión de tres vías, y `git merge`.
6. **Conflictos:** por qué aparecen, cómo leer los marcadores y los pasos para resolverlos.
7. **Deshacer:** `git reset` (reescribe la historia) frente a `git revert` (crea un commit nuevo).
8. **Estrategias de ramificación** (introducción) y buenas prácticas.

**Práctica:** ramas `fix/…` y `feature/…`, limpieza de ramas, recuperar un fichero de otra rama, *detached HEAD* controlado, provocar y resolver un conflicto y deshacer con `git revert`. Retos: ramas en cascada, el commit que se pierde, *revert* del *revert* y forzar una fusión de tres vías.

**Conceptos clave para el test:** qué es `HEAD`, *fast-forward* frente a tres vías, marcadores de conflicto, `reset` frente a `revert` y riesgos del *detached HEAD*.

---

### 1.1.3 Repositorios remotos

**Objetivo:** colaborar a través de un repositorio remoto en GitHub.

**Contenidos de teoría**

1. **Repositorio remoto** y cuenta de GitHub. **Aquí se aprovecha para pedir el GitHub Student Developer Pack**, que da acceso a Azure y Namecheap en UD3.
2. **Autenticación con GitHub:** tokens de acceso personal y claves SSH (se retoma en 4.2.1).
3. **`git clone`, `git remote`, `git fetch`, `git pull` y `git push`** (primera subida con *upstream* y push rechazado).
4. **Ramas remotas:** nomenclatura (`origin/main`), crear, subir y sincronizar.
5. **Fork** y cómo mantenerlo actualizado (`upstream`); diferencia entre copiar y hacer fork.
6. ***Pull requests*** en GitHub o GitLab.
7. **Modelos de ramas:** GitFlow, GitLab Flow y *Trunk-Based Development*.

**Práctica:** crear la cuenta y autenticarse, crear el repositorio remoto y conectarlo, clonarlo en otra carpeta (para simular otro ordenador), `fetch` frente a `pull`, provocar y resolver un push rechazado y abrir el primer *pull request*. Retos: conflicto en remoto, fork con `upstream`, *pull request* cruzado, elegir un modelo de ramas y rotar el token.

**Conceptos clave para el test:** `fetch` frente a `pull`, `origin` frente a `upstream`, por qué se rechaza un push, fork frente a clon y diferencias entre los modelos de ramas.

---

### 1.2.1 Fundamentos de Docker

**Objetivo:** entender por qué hacen falta los contenedores y manejar su ciclo de vida.

**Contenidos de teoría**

1. **El problema:** «en mi máquina funciona», la separación entre equipos y la cultura DevOps (se retoma en 5.1.1).
2. **Contenedores frente a máquinas virtuales:** virtualizar el hardware frente a virtualizar el sistema operativo, y cómo se combinan (que es justo lo que se hará en la VM de Azure).
3. **Imagen frente a contenedor**, y el contenedor como imagen + PID 1.
4. **Arquitectura de Docker:** cliente, *daemon* y registros (Docker Hub). Cuidado con la etiqueta `latest`.
5. **Comandos:** `docker run` (`-d`, `-p`, `--name`, `--rm`, `-it`), `ps`, `logs`, `images`, `pull`, `stop` frente a `kill`, y `exec -it`.

**Práctica:** primer contenedor, explorar una imagen de forma interactiva, contenedores de un solo uso, levantar un servidor web y entrar en un contenedor vivo. Retos: dos webs a la vez, el contenedor que se cae solo, limpieza general y diagnóstico a ciegas.

**Conceptos clave para el test:** imagen frente a contenedor, contenedor frente a VM, qué mantiene vivo un contenedor, publicación de puertos y `stop` frente a `kill`.

---

### 1.2.2 Imágenes y Dockerfile

**Objetivo:** construir imágenes propias, persistir datos y publicar en un registro.

**Contenidos de teoría**

1. **Dockerfile:** `FROM` (y por qué evitar `latest`), `WORKDIR`, `COPY` frente a `ADD`, `.dockerignore`, `RUN`, `CMD` frente a `ENTRYPOINT`, `ENV` y `EXPOSE`.
2. **`docker build`** y la caché de capas: lo que cambia menos va primero.
3. **Buenas prácticas:** imágenes pequeñas, *multi-stage builds* y no meter secretos en la imagen.
4. **Etiquetas y versionado:** `docker tag`.
5. **Volúmenes:** *bind mount* frente a volumen gestionado y el flujo de desarrollo con *bind mount*.
6. **Redes básicas y `-p`**.
7. **Publicar en Docker Hub**.
8. **Organización de los repositorios Git con Docker:** uno o dos repositorios.

**Práctica:** primera imagen, ejecutarla y publicarla, una app con dependencias, aprovechar la caché, variables de entorno, *bind mount*, volúmenes con nombre y Docker Hub. Retos: Dockerfile roto (Node, Python o Java), reducir el tamaño de la imagen, dos contenedores que se hablan y el puerto ocupado.

**Conceptos clave para el test:** `RUN`, `CMD` y `ENTRYPOINT`, orden de las instrucciones y caché, `COPY` frente a `ADD`, *bind mount* frente a volumen y riesgos de `latest`.

---

### 1.2.3 Docker Compose

**Objetivo:** describir y levantar una aplicación de varios servicios con un solo fichero.

**Contenidos de teoría**

1. **El problema de las apps reales:** cuántas imágenes hacen falta y cómo se multiplica.
2. **`docker-compose.yml`:** YAML en 30 segundos, estructura mínima, `image` frente a `build`, `ports`, `environment` y ficheros `.env`.
3. **Volúmenes** y *bind mount* para desarrollo.
4. **Redes:** la red por defecto de Compose y la comunicación entre servicios por nombre.
5. **`depends_on`** y el problema de «arrancado pero no listo» (se resuelve con `healthcheck` en 4.1.2).
6. **Ciclo de vida:** `up`/`down`, `stop`/`start`/`restart`, `ps`, `logs` y `exec`.
7. **Ejemplo completo app + base de datos**, buenas prácticas y para qué sirve en un despliegue real.

**Práctica:** primer `docker-compose.yml`, un segundo servicio, comunicación por nombre, persistencia con volúmenes, `depends_on` y logs, y la app propia con base de datos. Retos: variables desde `.env`, exponer solo lo necesario, migración puntual y *stack* completo desde cero.

**Conceptos clave para el test:** `image` frente a `build`, resolución por nombre de servicio, volúmenes y persistencia, `.env`, `depends_on` y lo que no garantiza, y `down` frente a `stop`.

---

## 5. Unidad 2 · Arquitecturas web *(impartida)*

### 2.1 Fundamentos web: redes, HTTP y arquitecturas

**Objetivo:** entender cómo viaja una petición web, qué hay en un mensaje HTTP, cómo se mantiene el estado y cómo se organizan las arquitecturas web.

**Contenidos de teoría**

1. **Redes y modelos de comunicación:** OSI y TCP/IP.
2. **Cliente-servidor, URL y DNS:** anatomía de una URL y resolución de nombres básica (se amplía en 4.2.1).
3. **El protocolo HTTP:** métodos, códigos de estado (incluidos 301/302/304/401/502/504) y cabeceras (`Host`, `User-Agent`, `Accept-Encoding`, `WWW-Authenticate`…).
4. **HTTP no tiene estado:** cookies y sesiones; robo de sesión.
5. **Arquitecturas en capas:** 1, 2, 3 y N capas.
6. **Arquitecturas a gran escala:** monolito, SOA, microservicios, orientada a eventos, *serverless* y P2P.
7. **Arquitecturas de diseño interno:** MVC, MVP, MVVM, hexagonal y *Clean/Onion*.
8. **Panorama general:** cuándo usar cada una.

**Práctica:** el protocolo HTTP por dentro con `curl` sobre un entorno de Docker Compose: anatomía de los mensajes, métodos y envío de datos (formulario y JSON), códigos de estado, redirecciones, autenticación básica (401), petición condicional (304), cookies y *cookie jar*, y sesiones (iniciar, usar, robar y cerrar).

**Conceptos clave para el test:** capas de TCP/IP, partes de una URL, estructura de una petición y una respuesta, familias de códigos de estado, cookie frente a sesión, y ventajas e inconvenientes de cada arquitectura.

---

### 2.2 Servidores web, servidores de aplicaciones y despliegue

**Objetivo:** distinguir el servidor web del servidor de aplicaciones, ver el patrón «servidor web delante, aplicaciones detrás» y entender qué significa desplegar.

**Contenidos de teoría**

1. **Contenido estático frente a dinámico.**
2. **Renderizado, CDN y SEO:** CSR, SSR, hidratación, SSG y *cache busting*.
3. **Servidor web (Apache/Nginx) frente a servidor de aplicaciones** (Tomcat, Node.js, Gunicorn, PHP-FPM…): compresión, modelos de concurrencia y *frameworks* de frontend y backend.
4. **CORS:** orígenes, cabeceras `Access-Control-Allow-*` y *preflight*.
5. **Servidor web delante y aplicaciones detrás:** proxy inverso, 502 y 504, balanceo, escalado y *health checks*.
6. **Qué significa desplegar:** dominio, DNS, alojamiento (compartido, VPS, dedicado, IaaS y PaaS), entornos, artefactos versionados (SemVer), y configuración y secretos fuera del artefacto. *La VM de Azure es un IaaS y Namecheap es el registrador del dominio: lo que aquí se ve en teoría se monta en UD3.*
7. **Despliegue con contenedores y estrategias sin corte:** *rolling*, *blue-green*, *canary* y *feature flags* (sin CI/CD todavía, que es la UD5).

**Práctica:** entorno de Compose con Nginx delante de dos instancias de una app Node.js: estático frente a dinámico, CSR frente a SSR, compresión y caché, balanceo, provocar 502 y 504, un fallo de CORS desde otro origen, y desplegar un artefacto versionado con actualización *rolling* y *rollback*.

**Conceptos clave para el test:** estático frente a dinámico, CSR frente a SSR, servidor web frente a servidor de aplicaciones, CORS y *preflight*, 502 frente a 504, tipos de alojamiento, SemVer y estrategias de despliegue.

---

## 6. Unidad 3 · Servidores web

### 3.0 Puesta en marcha *(se hace en el Proyecto Intermodular, antes de 3.1.1)*

Cada alumno o alumna sigue las guías del Proyecto (`proyectos/maquina-remota.md` y `proyectos/vm-ubuntu.md`) y después los dos dosieres de `UD3/3.0 Puesta en marcha/`, y llega a 3.1.1 con:

- una VM Ubuntu Server LTS en Azure (la del Proyecto), accesible con el alias `ssh daw` (clave ed25519, sin contraseña) y con Docker instalado;
- los puertos 22, 80 y 443 abiertos en el grupo de seguridad de red (NSG);
- el dominio `<alumno>.me` con registros A para `@` y `www` apuntando a la IP estática de la VM;
- el certificado PositiveSSL reclamado, pero sin activar.

**Comprobación el primer día de 3.1.1** (5 minutos): `ssh daw 'hostname; docker --version'` y `dig +short <alumno>.me` devuelve la IP de la VM. Quien no lo tenga trabaja ese día con el plan B (apartado 3.3).

---

### 3.1.1 Instalación y configuración básica de Nginx (y Apache, en teoría)

**Objetivo:** conocer los dos servidores web más usados, poner en marcha Nginx en un contenedor en la VM, entender cómo se organiza su configuración, ampliarlo con módulos dinámicos, cambiarlo sin romper el servicio y diagnosticar un problema con sus logs.

**Material:** `UD3/3.1 Configuración de servidores web/3.1.1 Apache y Nginx/3_1_1_teoria.md`

**Contenidos de teoría**

1. **Apache y Nginx frente a frente** (repaso del bloque 2.2): historia, modelo de procesos (MPM *prefork*, *worker* y *event* en Apache; maestro y *workers* con eventos en Nginx), **Apache en una página** (módulos, estructura `*-available` / `*-enabled` de Debian, `.htaccess`, tabla de equivalencias de directivas con Nginx), cuándo elegir cada uno y por qué el curso usa Nginx. Solo descriptivo: Apache no se instala.
2. **Cómo lo ejecutamos: Docker**
   - Tres formas de instalar: paquete del sistema, imagen oficial (`nginx:1.30`) e imagen propia `FROM nginx:1.30`.
   - Sin systemd: Nginx es el **proceso principal** del contenedor (`nginx -g 'daemon off;'`; enlace con el PID 1 de la UD1). Equivalencias entre `systemctl` y `docker`.
   - `reload` (`nginx -s reload`) frente a `restart` (`docker restart`).
   - Un puerto, cuatro capas: NSG de Azure, `ufw` (que Docker se salta), `-p host:contenedor` y `listen`.
3. **Nginx con la imagen oficial:** `nginx.conf`, `conf.d/`, `mime.types`, `modules/`; contextos `main`, `events`, `http`, `server` y `location`, en qué contexto va cada directiva y la herencia. Directivas básicas: `listen`, `server_name`, `root`, `index`, `location`, `error_page`.
4. **Módulos: ampliar la funcionalidad** (RA2 b)
   - Módulos estáticos (`nginx -V`) frente a dinámicos (`.so` cargados con `load_module` en el contexto `main`); `nginx -T` para ver la configuración efectiva.
   - Los más populares: los oficiales que trae la imagen (`njs`, `image_filter`, `acme`, `geoip`, `xslt`) y los de terceros (brotli, headers-more, geoip2, ModSecurity, lua/OpenResty, fancyindex, cache-purge, rtmp), cómo se obtienen (paquetes `libnginx-mod-*` de Debian o compilación) y por qué un `.so` tiene que ser de la misma versión.
   - Ejemplos: miniaturas al vuelo con `image_filter` y una respuesta en JavaScript con `njs`.
5. **Cambiar la configuración sin romper nada:** en la imagen (`Dockerfile` con `COPY nginx.conf`), montada (*bind mount* de `conf.d/`, no de ficheros sueltos) o con `docker exec` (solo para probar). Comprobar con `nginx -t` antes de recargar, y por qué una configuración rota tumba el servicio en el **siguiente reinicio**.
6. **Logs**
   - Ubicación (`/var/log/nginx/`) y, en la imagen oficial, enlaces a `/dev/stdout` y `/dev/stderr`; leerlos con `docker logs` (`-f`, `--tail`, `--since`, separar acceso y errores).
   - Leer una línea del log de acceso (formato `main`: IP, fecha, petición, código de estado, tamaño, *referer*, *user-agent* y `X-Forwarded-For`) y del log de errores.
   - En un servidor público aparecen enseguida peticiones de bots y escáneres (`/wp-login.php`, `/.env`…).
7. **Permisos y usuario del servicio** (`nginx`, UID 101): por qué un 403 suele ser un problema de permisos o de una carpeta sin índice, y por qué en Docker Desktop no se ve y en la VM sí.
8. **Primeras medidas de seguridad:** ocultar la versión (`server_tokens off;`) y no activar `autoindex` donde no toca.
9. **Todo junto:** `compose.yaml` con Nginx en el 80 de la VM, `nginx.conf` y `njs/` en la imagen, `conf.d/` y la web montados.

**Práctica (1 h):** en la VM, con Docker Compose: levantar Nginx con la imagen oficial en el puerto 80 para servir una web propia en `http://<alumno>.me`; crear una imagen propia `FROM nginx:1.30` que cargue `image_filter` y `njs`, y probar miniaturas de una foto propia con distintos anchos y el endpoint `/hola`; romper a propósito la configuración (un `;` olvidado, `load_module` dentro de `http`, una directiva sin su módulo) y detectarlo con `nginx -t`; provocar un 403 (permisos y carpeta sin índice) y un 404 y localizarlos con `docker logs`; buscar peticiones de bots en el log de acceso; y comprobar la cabecera `Server` con `curl -I` antes y después de `server_tokens off`.

**Conceptos clave para el test:** MPM de Apache, `.htaccess`, equivalencias Apache ↔ Nginx, proceso principal del contenedor, `reload` frente a `restart`, capas de un puerto (NSG, `-p`, `listen`), contextos de Nginx y herencia de directivas, módulo estático frente a dinámico, `load_module` en `main`, compatibilidad de versión de un `.so`, `nginx -t` y `nginx -T`, dónde cambiar la configuración de un contenedor, formato del log de acceso, `docker logs` y relación entre permisos y error 403.

---

### 3.1.2 Hosts virtuales y redirecciones

**Objetivo:** alojar varias webs en un mismo servidor y saber redirigir al cliente con el código adecuado.

**Contenidos de teoría**

1. **Hosts virtuales**
   - Por nombre (el más habitual), por IP y por puerto.
   - Cómo decide el servidor qué web servir: la **cabecera `Host`** (enlace directo con el bloque 2.1).
   - Apache: `<VirtualHost *:80>`, `ServerName`, `ServerAlias`. Nginx: bloques `server` con `server_name`.
   - El **servidor por defecto**: qué web responde cuando el `Host` no coincide con ninguna (`000-default` en Apache, `default_server` en Nginx). Es un error típico; en la VM se ve al entrar por la IP en vez de por el nombre.
   - **Subdominios reales:** crear `tienda.<alumno>.me` en *Advanced DNS* de Namecheap (registro A o CNAME). El fichero `hosts` queda como respaldo.
2. **Organización de varias webs:** un `DocumentRoot` y unos logs por sitio.
3. **Redirecciones**
   - Repaso de códigos: 301, 302, 303, 307 y 308 (bloque 2.1), y su efecto en buscadores y cachés.
   - Apache: `Redirect`, `RedirectMatch` y `mod_rewrite` (`RewriteEngine`, `RewriteCond`, `RewriteRule`), con nociones básicas de expresiones regulares.
   - Nginx: `return 301`, `rewrite` y cuándo usar cada uno.
   - Casos típicos: de `www` a sin `www` (o al revés), página movida y cambio de estructura de URLs.
   - El peligro de los **bucles de redirección** y de cachear un 301 equivocado en el navegador.
4. **Páginas de error personalizadas:** `ErrorDocument` / `error_page`.
5. **`Alias` y `location`:** servir una carpeta fuera del `DocumentRoot` (por ejemplo, `/docs`).
6. **`.htaccess` en Apache:** qué es, `AllowOverride` y por qué penaliza el rendimiento. Nginx no tiene equivalente.

**Práctica (1 h):** dos webs (`<alumno>.me` y `tienda.<alumno>.me`) en la misma VM, cada una con sus logs; crear el subdominio en Namecheap y comprobarlo con `dig`; redirección 301 de `www.<alumno>.me` a `<alumno>.me`; una 302 temporal por mantenimiento; una página 404 propia; y verificar todo con `curl -I` y `curl -L`, también entrando por la IP para ver el servidor por defecto.

**Conceptos clave para el test:** cabecera `Host` y hosts virtuales, servidor por defecto, registro A frente a CNAME para un subdominio, diferencia entre los tipos de redirección, `Redirect` frente a `RewriteRule`, `return` frente a `rewrite`, `AllowOverride` y bucles de redirección.

---

### 3.2.1 HTTPS y control de acceso

**Objetivo:** obtener e instalar certificados reales, servir las webs de forma cifrada y restringir el acceso a las partes privadas.

**Contenidos de teoría**

1. **Por qué HTTPS:** confidencialidad, integridad y autenticidad. Enlace con la práctica 2.1, donde la autenticación básica viajaba en Base64 legible y la cookie no podía llevar `Secure`.
2. **Cómo funciona TLS (simplificado):** cifrado simétrico y asimétrico, el *handshake*, el certificado X.509 y la cadena de confianza (autoridades raíz, intermedias y certificado del servidor).
3. **Tipos de certificado y cómo se obtienen**
   - **Autofirmado** con `openssl` (para pruebas: el navegador avisa).
   - **mkcert** para tener certificados de confianza en local.
   - **Let's Encrypt y certbot** (protocolo ACME): gratuitos, automáticos, de 90 días y con renovación automática (`certbot renew`, *timer* de systemd). Necesitan un dominio público y el puerto 80 accesible, **que ya tenemos**.
   - **Certificado comercial (PositiveSSL de Namecheap, incluido en el Pack):** el proceso «clásico» de una CA. Generar la clave privada y la **CSR** con `openssl req` (clave de 2048 bits o más), activarlo en Namecheap, **validar el dominio (DCV)** por fichero HTTP, por registro CNAME o por correo, y descargar el certificado y la **cadena intermedia**. Validación DV frente a OV y EV.
   - Comparar los dos: quién lo emite, duración, automatización y coste.
4. **Configuración**
   - Apache: `mod_ssl`, `SSLEngine`, `SSLCertificateFile`, `SSLCertificateKeyFile` (y la cadena).
   - Nginx: `listen 443 ssl`, `ssl_certificate` (con la cadena concatenada), `ssl_certificate_key`.
   - Protocolos: solo TLS 1.2 y 1.3.
   - Redirección de HTTP a HTTPS con 301.
   - **HSTS** (`Strict-Transport-Security`): qué es y su riesgo si se activa mal.
   - Activar HTTP/2.
5. **Inspeccionar un certificado:** `curl -v`, `openssl s_client -connect <alumno>.me:443 -servername …`, el candado del navegador y una prueba externa (SSL Labs).
6. **Control de acceso**
   - **Autenticación básica:** `htpasswd`; Apache con `AuthType Basic` y `Require valid-user`; Nginx con `auth_basic` y `auth_basic_user_file`. Enlace con el 401 y `WWW-Authenticate`.
   - **Restricción por IP:** `Require ip` en Apache; `allow` y `deny` en Nginx.
   - Combinar ambos: por ejemplo, la IP del centro sin contraseña y el resto con ella.
   - Por qué la autenticación básica solo es aceptable sobre HTTPS.
   - Avance: en 4.2.1 la misma zona se validará contra un directorio LDAP.
7. **Cabeceras de seguridad (introducción):** `X-Content-Type-Options`, `X-Frame-Options` y nociones de `Content-Security-Policy`.

**Práctica (1 h):** obtener con certbot un certificado de Let's Encrypt para `<alumno>.me` y `www`; generar la CSR y activar el PositiveSSL para `tienda.<alumno>.me` (la validación DCV puede tardar: se lanza al principio y se instala al final o como tarea); HTTPS obligatorio con redirección desde HTTP; proteger `/admin` con usuario y contraseña; y comprobar con `curl -v` y `openssl s_client` la cadena, el emisor y los códigos 301, 401 y 200.

**Conceptos clave para el test:** cadena de confianza, autofirmado frente a CA, CSR y clave privada, métodos de DCV, Let's Encrypt frente a certificado comercial, requisitos de Let's Encrypt, HSTS, redirección a HTTPS, `htpasswd`, autenticación básica frente a restricción por IP y por qué la básica requiere HTTPS.

---

### 3.2.2 Proxy inverso, monitorización y rendimiento

**Objetivo:** usar el servidor web como puerta de entrada de otras aplicaciones, vigilar su funcionamiento y medir y mejorar su rendimiento.

**Contenidos de teoría**

1. **Proxy inverso**
   - Proxy directo frente a proxy inverso.
   - Nginx: `proxy_pass`. Apache: `mod_proxy`, `ProxyPass`, `ProxyPassReverse` y `ProxyPreserveHost`.
   - Cabeceras que hay que reenviar: `Host`, `X-Real-IP`, `X-Forwarded-For` y `X-Forwarded-Proto`. Por qué sin ellas la aplicación cree que todas las peticiones vienen del proxy.
   - **Terminación TLS:** HTTPS hasta Nginx y HTTP interno hasta la aplicación.
   - Diagnóstico de los errores **502** y **504** (bloque 2.1).
2. **Balanceo de carga**
   - Nginx: bloque `upstream`, estrategias *round robin*, `least_conn`, `ip_hash` y pesos (`weight`).
   - Comprobaciones de salud **pasivas** en Nginx de código abierto (`max_fails`, `fail_timeout`). Las activas son de la versión comercial NGINX Plus.
   - El problema de la sesión cuando hay varios backends (enlace con las sesiones del bloque 2.1).
3. **Monitorización**
   - Logs de acceso y de error, formatos personalizados (`log_format` / `LogFormat`) y el tiempo de respuesta (`$request_time`).
   - Análisis rápido con `tail -f`, `grep` y `awk` (por ejemplo, contar códigos de estado) y con **GoAccess**.
   - Páginas de estado: `mod_status` y `stub_status` (restringidas por IP).
   - Qué vigilar: errores 5xx, tiempo de respuesta y peticiones por segundo. Las métricas de la VM en el portal de Azure (CPU, red).
4. **Rendimiento**
   - **Compresión:** `gzip` en Nginx y `mod_deflate` en Apache (enlace con `Accept-Encoding` y `Content-Encoding`).
   - **Caché del navegador:** `Cache-Control`, `Expires` y `ETag`, y su relación con el código 304.
   - **Caché en el proxy:** `proxy_cache`, como introducción.
   - Ajustes básicos: `worker_processes`, `worker_connections` y `keepalive`.
   - **Pruebas de carga** con `ab` (ApacheBench): medir antes y después de cada cambio. *Lanzarlas contra la propia VM o en local, nunca contra servidores ajenos; la VM gratuita es pequeña y los créditos de CPU de la serie B se agotan.*

**Práctica (1 h):** Nginx como proxy inverso, con HTTPS, de dos backends idénticos en contenedores en la VM (httpbin o la app de la práctica 2.2). El alumnado comprueba el balanceo, apaga un backend y observa el comportamiento, provoca un 502 y lo localiza en el log, activa la compresión y compara tamaños, y mide con `ab` antes y después de activar la caché.

**Conceptos clave para el test:** proxy directo frente a inverso, cabeceras `X-Forwarded-*`, terminación TLS, estrategias de balanceo, comprobaciones de salud pasivas, 502 frente a 504, compresión, `Cache-Control` y lectura de resultados de `ab`.

---

## 7. Unidad 4 · Servidores de aplicaciones y servicios de red

### 4.1.1 Instalación, configuración y despliegue en servidores de aplicaciones

**Objetivo:** instalar un servidor de aplicaciones Java, entender su estructura, desplegar aplicaciones en él y configurar su seguridad.

**Contenidos de teoría**

1. **Repaso:** servidor web frente a servidor de aplicaciones (bloque 2.2) y el panorama de servidores (Tomcat, Jetty, WildFly, GlassFish; Gunicorn, PHP-FPM y Node.js en otros lenguajes).
2. **Tomcat**
   - Requisitos: Java (JDK o JRE) y versiones compatibles.
   - **Aviso importante:** Tomcat 10 y posteriores usan Jakarta EE (`jakarta.*`). Las aplicaciones antiguas (`javax.*`) necesitan Tomcat 9 o una migración. Es un error muy frecuente.
   - Instalación por paquete, desde el archivo oficial o con la imagen Docker `tomcat`.
   - Componentes: *Server*, *Service*, *Connector*, *Engine*, *Host* y *Context*, y cómo se reflejan en `server.xml`.
   - Estructura: `bin/`, `conf/` (`server.xml`, `tomcat-users.xml`, `web.xml`, `context.xml`), `webapps/`, `logs/` (`catalina.out`), `lib/` (**bibliotecas compartidas**, como los *drivers* JDBC), `work/`.
   - Puertos y conectores: 8080 (HTTP) y 8005 (apagado); el conector AJP viene desactivado por defecto.
3. **Aplicaciones web Java:** el formato **WAR** y su estructura (`WEB-INF/`, `web.xml` como **descriptor de despliegue**, `lib/`, `classes/`) frente al **JAR ejecutable de Spring Boot**, con Tomcat embebido (bloque 2.2). Componentes web: *servlets*, JSP y filtros.
4. **Formas de desplegar**
   - Copiar el WAR en `webapps/` (*autoDeploy*).
   - Con la aplicación **Manager** (`/manager/html`), que exige definir roles en `tomcat-users.xml`.
   - Rutas de contexto: el nombre del WAR determina la URL.
5. **Seguridad del servidor de aplicaciones**
   - **Realms (dominios de seguridad):** `UserDatabaseRealm` (`tomcat-users.xml`), `DataSourceRealm` y `JNDIRealm` (LDAP, se usa en 4.2.1); roles y `security-constraint` en `web.xml`.
   - **Válvulas como filtros de solicitudes:** `RemoteAddrValve` (restringir por IP) y `AccessLogValve` (log de acceso).
   - **SSL/TLS en Tomcat:** conector HTTPS con *keystore* (`keytool`) frente a terminar TLS en Nginx (3.2.2). Cuándo tiene sentido cada uno.
   - No exponer el Manager, eliminar las aplicaciones de ejemplo en producción y no ejecutar Tomcat como `root`.
6. **Trampas habituales con Docker:** la imagen oficial trae `webapps/` vacía (las aplicaciones de ejemplo están en `webapps.dist/`), y el Manager solo admite conexiones desde `localhost` por defecto (válvula `RemoteAddrValve` en `context.xml`).
7. **Logs y diagnóstico:** `catalina.out`, logs de acceso y errores típicos de despliegue.

**Práctica (1 h):** levantar Tomcat con Docker en la VM (sin publicar el 8080 a Internet: se accede por un túnel SSH, `ssh -L 8080:localhost:8080 daw`), desplegar el WAR de ejemplo oficial copiándolo a `webapps/`, configurar un usuario y un rol para el Manager y desplegar un segundo WAR desde la interfaz, proteger una ruta de la aplicación con `security-constraint`, y localizar en los logs un despliegue fallido.

**Conceptos clave para el test:** componentes y estructura de Tomcat, ficheros de configuración y su función, `lib/` compartida, WAR frente a JAR ejecutable, descriptor de despliegue, `javax` frente a `jakarta`, roles del Manager, *realms*, válvulas, ruta de contexto y puertos por defecto.

---

### 4.1.2 Aplicaciones con base de datos e integración con el proxy

**Objetivo:** desplegar una aplicación completa (aplicación, base de datos y proxy), hacer que las piezas se comuniquen de forma segura y medir su rendimiento.

**Contenidos de teoría**

1. **La arquitectura de tres capas montada de verdad:** Nginx → Tomcat → base de datos (enlace con las capas del bloque 2.1).
2. **Conexión de la aplicación con la base de datos**
   - JDBC, cadenas de conexión, *pool* de conexiones y `DataSource` en `context.xml` (el *driver* va en `lib/`).
   - **Configuración y secretos fuera del artefacto** (bloque 2.2): variables de entorno y ficheros `.env` (que no se suben al repositorio).
3. **Sesiones en el servidor de aplicaciones**
   - Cómo gestiona Tomcat las sesiones (`JSESSIONID`, *timeout* en `web.xml`).
   - **Sesiones persistentes:** `PersistentManager` con almacenamiento en fichero o en base de datos, para que sobrevivan a un reinicio.
   - Varias instancias detrás del balanceador: sesiones pegajosas (`ip_hash`) frente a sesiones compartidas (enlace con 3.2.2).
4. **La base de datos en Docker**
   - Imágenes `mysql`, `mariadb` o `postgres` y sus variables de inicialización.
   - Scripts de arranque en `/docker-entrypoint-initdb.d/`.
   - **Persistencia con volúmenes:** qué pasa si se borra el contenedor sin volumen.
5. **Docker Compose para la pila completa**
   - Redes internas: la base de datos no se publica al exterior (y en la VM, además, el NSG solo deja pasar 22/80/443).
   - Orden de arranque: `depends_on` con `healthcheck` (`condition: service_healthy`).
6. **Integración con el proxy:** Nginx delante de Tomcat, con HTTPS en Nginx (3.2.1), cabeceras reenviadas (3.2.2), `RemoteIpValve` para que Tomcat vea la IP real, y estáticos servidos por Nginx y lo dinámico por Tomcat.
7. **Pruebas de funcionamiento y rendimiento de la aplicación desplegada:** una ruta `/health`, `ab` contra una página dinámica frente a una estática y lectura de los tiempos en los logs.
8. **Copias de seguridad:** `mysqldump` y `pg_dump`, cómo restaurar y la relación con las migraciones y el *rollback* (bloque 2.2).
9. **Diagnóstico de la pila:** 502 si la aplicación no arranca, errores de conexión a la base de datos y `docker compose logs`.

**Práctica (1 h):** en la VM, un `docker-compose.yml` con Nginx, la aplicación y la base de datos, servido en `https://app.<alumno>.me`; credenciales en `.env`; volumen persistente; comprobar que los datos y las sesiones sobreviven a un `docker compose down` y `up`; medir con `ab` lo estático frente a lo dinámico; hacer una copia con `mysqldump`; y provocar y diagnosticar un 502 parando la aplicación.

**Conceptos clave para el test:** volúmenes y persistencia, `depends_on` frente a `healthcheck`, redes internas de Compose, secretos en variables de entorno, sesiones persistentes, terminación TLS en el proxy, `RemoteIpValve` y copias de seguridad.

---

### 4.2.1 FTP, SFTP, SSH, DNS y LDAP

**Objetivo:** conocer los servicios de red que intervienen en un despliegue: transferir ficheros, administrar servidores en remoto, gestionar el dominio y centralizar la autenticación de usuarios.

> Es el apartado más amplio, pero tiene **4 sesiones** en el calendario. Reparto propuesto: **sesión 1** SSH y SFTP (los usarán en 5.2.1); **sesión 2** FTP con vsftpd; **sesión 3** DNS sobre el dominio propio; **sesión 4** LDAP. Si hace falta recortar, FTP se queda en lo imprescindible para el RA4 (anónimo, activo/pasivo, FTPS) y LDAP en el ejemplo de autenticación.

**Contenidos de teoría**

1. **SSH**
   - Arquitectura cliente-servidor (OpenSSH) y huella del servidor (`known_hosts`).
   - **Autenticación con claves:** repaso de la clave creada en el dosier (`ssh-keygen -t ed25519`), `ssh-copy-id`, `authorized_keys` y sus permisos. Crear un segundo usuario y darle acceso.
   - Endurecer `sshd_config`: `PasswordAuthentication no` y `PermitRootLogin no`. **En la VM de Azure se ven ataques reales:** `journalctl -u ssh` o `/var/log/auth.log`, y `fail2ban` bloqueándolos.
   - Transferir ficheros: `scp`, `sftp` y `rsync`.
   - Fichero `~/.ssh/config` y túneles (`ssh -L`), ya usados en 4.1.1.
2. **FTP**
   - Funcionamiento: canal de control (21) y canal de datos; modo **activo** frente a **pasivo**, y por qué el pasivo es el habitual con cortafuegos y NAT (en Azure habría que abrir el rango pasivo en el NSG: por eso se monta en Docker en local).
   - Problema principal: credenciales y datos **sin cifrar**.
   - Servidor de referencia `vsftpd`: usuarios y **grupos locales**, enjaular en el directorio personal (`chroot_local_user`), **acceso anónimo** (`anonymous_enable`, carpeta de solo lectura y de subida), **permisos** (`umask`, `write_enable`) y **cuotas** de disco (`quota`, `setquota`) y de ancho de banda.
   - Clientes: en línea de comandos (`ftp`, `lftp`, `curl ftp://…`) y gráficos (FileZilla).
   - **El navegador como cliente:** Chrome y Firefox retiraron el soporte de FTP en 2021. Hoy se cubre con clientes web o con servicios de transferencia integrados en el servidor web.
   - **Transferencia integrada en el servidor web:** **WebDAV** con `mod_dav` en Apache (o `dav` en Nginx), protegido con HTTPS y autenticación, y accesible desde el navegador y desde el explorador de archivos.
   - Uso de la transferencia de ficheros en el despliegue: subir una web estática (y su automatización en 5.2.1).
3. **FTPS frente a SFTP**
   - FTPS: FTP sobre TLS (explícito por el 21 o implícito por el 990); `ssl_enable` en vsftpd.
   - SFTP: un protocolo distinto, que funciona **sobre SSH** (puerto 22).
4. **DNS en la práctica** (amplía el bloque 2.1)
   - Sistema de nombres jerárquico: raíz, TLD (`.me`), dominio y subdominio, y el proceso de resolución (resolutor recursivo, servidores autoritativos y caché).
   - Registros: A, AAAA, CNAME, MX, TXT, NS, SOA, PTR y CAA.
   - TTL y propagación.
   - Consultas con `dig` y `nslookup`, incluido `dig +trace <alumno>.me`.
   - **Sobre el dominio propio:** qué registros ha hecho falta crear para el despliegue (A de `@`, CNAME de `www`, subdominios de 3.1.2, CNAME de la DCV de 3.2.1), qué son los NS de Namecheap y por qué un registro CAA puede bloquear a Let's Encrypt.
   - Opcional: un servidor DNS sencillo en local (`dnsmasq` o `bind9`).
5. **Servicio de directorio (LDAP)**
   - Qué es un servicio de directorio y para qué sirve: **autenticación centralizada** de usuarios en una red. Ejemplos: OpenLDAP, Active Directory y Microsoft Entra ID (el que usa la cuenta de Azure).
   - Estructura lógica: árbol (DIT), entradas, `dn`, `dc`, `ou`, `cn`, `uid`, `objectClass` y atributos; esquemas `inetOrgPerson` y `posixAccount`.
   - Ficheros básicos: formato **LDIF** y configuración del servidor (`cn=config`).
   - Herramientas: `ldapsearch`, `ldapadd` y `ldapmodify`; un cliente gráfico (phpLDAPadmin o Apache Directory Studio).
   - **Adaptarlo al despliegue:** una `ou=usuarios` y un grupo `cn=admins` para la aplicación; la cuenta de servicio que usa el servidor web para buscar; y LDAPS o StartTLS para que las contraseñas no viajen en claro.
   - Integración: Apache con `mod_authnz_ldap` (`AuthLDAPURL`, `Require ldap-group`) protegiendo `/admin` (retoma 3.2.1) y Tomcat con `JNDIRealm` (retoma 4.1.1).

**Práctica (sesiones de 1 h):**
- *SSH/SFTP:* crear un segundo usuario en la VM con su clave, desactivar el acceso por contraseña, revisar los intentos de acceso en los logs, instalar `fail2ban`, y subir la web estática por SFTP y con `rsync`.
- *FTP (en local, con Docker):* vsftpd con un usuario enjaulado y acceso anónimo de solo lectura; probar el modo activo y el pasivo con `curl`/`lftp` y con FileZilla; activar FTPS; y publicar una carpeta por WebDAV y abrirla desde el navegador.
- *DNS:* consultar con `dig` los registros A, CNAME, NS, MX y TXT del dominio propio y de uno real, bajar y subir un TTL y medir la propagación, y seguir una resolución con `+trace`.
- *LDAP:* OpenLDAP en Docker, cargar usuarios y grupos con LDIF, buscar con `ldapsearch` y proteger `/admin` de Apache con `Require ldap-group`.

**Conceptos clave para el test:** puertos de cada protocolo, FTP activo frente a pasivo, acceso anónimo y enjaulado, FTPS frente a SFTP, WebDAV, clave pública frente a privada, `authorized_keys`, endurecimiento de SSH, jerarquía y proceso de resolución DNS, tipos de registro DNS con su uso, estructura de un `dn`, LDIF y autenticación centralizada.

---

## 8. Unidad 5 · Integración y despliegue continuos (CI/CD)

### 5.1.1 Fundamentos de DevOps y primer workflow

**Objetivo:** entender qué es DevOps y crear una primera automatización con GitHub Actions.

**Contenidos de teoría**

1. **Qué es DevOps:** cultura y prácticas (colaboración entre desarrollo y operaciones, automatización, medición y mejora continua; se planteó en 1.2.1). El ciclo planificar → programar → construir → probar → publicar → desplegar → operar → monitorizar.
2. **CI y CD, sin confusiones**
   - **Integración continua:** cada cambio se compila y se prueba automáticamente.
   - **Entrega continua:** el artefacto siempre queda listo para desplegar, pero el paso a producción es manual.
   - **Despliegue continuo:** cada cambio que supera el pipeline llega solo a producción.
   - Enlace con el bloque 2.2: despliegue continuo no es lo mismo que despliegue *rolling*.
3. **GitHub Actions**
   - Conceptos: *workflow*, evento (*trigger*), *job*, *step*, *runner* y *action*.
   - Estructura de un fichero en `.github/workflows/*.yml` y sintaxis YAML básica (vista en 1.2.3).
   - Eventos: `push`, `pull_request`, `workflow_dispatch` y `schedule`.
   - Actions del Marketplace (`actions/checkout`) y la importancia de **fijar versiones**.
   - Variables y **secretos** del repositorio.
   - Leer los logs de una ejecución y entender por qué falla.
4. **Buenas prácticas:** ramas, *pull requests* (1.1.3) y proteger la rama principal para que no se pueda fusionar si el pipeline falla.

**Práctica (1 h):** crear un repositorio con la web del proyecto, un primer workflow que se ejecute en cada `push` y valide el HTML (o ejecute un *linter*), provocar un fallo y corregirlo, y lanzar el workflow a mano con `workflow_dispatch`.

**Conceptos clave para el test:** diferencia entre CI, entrega continua y despliegue continuo; elementos de un workflow; eventos; uso de secretos; y por qué fijar versiones de las actions.

---

### 5.1.2 Artefactos, imágenes Docker y tests en el pipeline

**Objetivo:** que el pipeline pruebe la aplicación, construya un artefacto versionado y lo publique solo si los tests pasan.

**Contenidos de teoría**

1. **Repaso del artefacto** (bloque 2.2): inmutable, versionado y el mismo en todos los entornos.
2. **Tests en el pipeline**
   - Tipos: unitarios, de integración y *end-to-end* (concepto).
   - Ejecutarlos según el lenguaje: `mvn test`, `npm test`, `pytest` o `phpunit`.
   - **Fallar rápido:** si un test falla, el pipeline se detiene y no se genera el artefacto.
3. **Construir y publicar imágenes Docker**
   - Actions oficiales de Docker: `docker/login-action`, `docker/metadata-action` y `docker/build-push-action`.
   - Registros: Docker Hub (1.2.2) y **GitHub Container Registry** (`ghcr.io`).
   - **Etiquetado:** SemVer, *hash* del commit y por qué evitar `latest` en producción (UD1 y bloque 2.2).
   - Arquitectura de la imagen: si la VM es Arm (B2pts v2), hay que construir para `linux/arm64` (`docker/setup-qemu-action` y `platforms`).
4. **Otros artefactos:** subir ficheros generados con `actions/upload-artifact` (un WAR, un informe de tests).
5. **Pipelines con varios jobs:** dependencias entre jobs (`needs`) y caché de dependencias para acelerar.

**Práctica (1 h):** ampliar el workflow para que ejecute los tests, construya la imagen Docker de la aplicación y la publique en `ghcr.io` etiquetada con la versión y el commit; romper un test a propósito y comprobar que la imagen ya no se publica.

**Conceptos clave para el test:** orden lógico del pipeline, *fail fast*, etiquetado de imágenes, `needs`, registros de contenedores y diferencia entre artefacto e imagen.

---

### 5.2.1 Despliegue por SSH, documentación y proyecto integrador

**Objetivo:** cerrar el ciclo con un despliegue automático en la VM de Azure, publicar la documentación del proyecto y presentar el proyecto integrador.

**Contenidos de teoría**

1. **El job de despliegue**
   - Depende de los anteriores: solo se despliega lo que se ha probado y construido.
   - **Usuario de despliegue** en la VM (`deploy`, en el grupo `docker`, sin `sudo`) con su propia clave; la clave privada se guarda como **secreto** del repositorio y la huella del servidor como variable (`known_hosts`), sin desactivar la comprobación de la huella (4.2.1).
   - Dos estrategias:
     - **Con contenedores:** conectar por SSH y ejecutar `docker compose pull` y `docker compose up -d` con la nueva etiqueta.
     - **Sin contenedores:** copiar ficheros con `rsync` o SFTP (por ejemplo, una web estática) y recargar el servicio.
   - El puerto 22 de la VM tiene que aceptar conexiones de los *runners* de GitHub, cuyas IP cambian; se compensa con solo clave, `fail2ban` y un usuario sin privilegios.
2. **Entornos en GitHub:** `staging` y `production`, con aprobación manual para producción (entrega continua).
3. **Comprobar después de desplegar:** una petición a `https://<alumno>.me/health` y fallar si no responde con 200 (bloque 2.2).
4. **Rollback:** volver a desplegar la etiqueta anterior.
5. **Seguridad del pipeline:** mínimo privilegio para la clave de despliegue, no imprimir secretos y usuario sin permisos de `root` en el servidor.
6. **Documentación de la aplicación web**
   - Herramientas para generar documentación: a partir del código (Javadoc, JSDoc, phpDocumentor, Sphinx) y sitios de documentación (MkDocs, Docusaurus).
   - Formatos: Markdown, HTML y PDF; plantillas (por ejemplo, la plantilla del `README.md` de las prácticas y las de *issues* y *pull requests* de GitHub).
   - Herramientas colaborativas: el propio repositorio, *pull requests*, wiki de GitHub y GitHub Pages.
   - Un job del pipeline que genera la documentación y la publica en GitHub Pages (o en `docs.<alumno>.me`).
   - Accesibilidad y seguridad de la documentación en el control de versiones: qué es público y qué no, y no publicar secretos (1.1.1).

**Práctica (1 h):** crear el usuario `deploy` en la VM, completar el pipeline con un job que despliegue por SSH, comprobar que un cambio en el repositorio llega solo a `https://<alumno>.me`, hacer un rollback a la versión anterior y añadir un job que publique la documentación con MkDocs.

**Proyecto integrador (propuesta):** desplegar la aplicación del curso en la VM y el dominio propios, con todos los elementos vistos:

| Requisito | Unidad |
|-----------|--------|
| Repositorio Git con ramas, *pull requests* y rama principal protegida | UD1 y UD5 |
| Nginx como proxy inverso con HTTPS (certificado real) y redirección desde HTTP | UD3 |
| Al menos un host virtual adicional (subdominio) y una zona con acceso restringido | UD3 |
| Aplicación en un servidor de aplicaciones con base de datos persistente | UD4 |
| Configuración y secretos fuera del código | UD2 y UD4 |
| Acceso al servidor solo por clave SSH | UD4 |
| Pipeline con tests, imagen versionada y despliegue automático | UD5 |
| Documentación generada y publicada: arquitectura, cómo desplegar y cómo hacer rollback | Todas |

> **Infraestructura:** con la VM de Azure accesible desde Internet, GitHub Actions entra por SSH sin más. Quien siga el plan B (VM local) usa un *self-hosted runner* instalado en su equipo, que ejecuta el pipeline desde dentro de la red.
>
> **Antes de que caduque:** el crédito, el dominio y el certificado duran un año. Al acabar el curso, el alumnado decide si borra el grupo de recursos y deja caducar el dominio, o si los mantiene pagando.

**Conceptos clave para el test:** dependencias entre jobs, gestión de claves en el pipeline, entornos y aprobaciones, comprobación después de desplegar, estrategia de rollback y herramientas de generación de documentación.

---

## 9. Correspondencia con los resultados de aprendizaje

Resultados de aprendizaje y criterios de evaluación del módulo 0614 (RD 686/2010, BOE de 12 de junio de 2010), resumidos.

### RA1 · Implanta arquitecturas web analizando y aplicando criterios de funcionalidad

| Criterio | Apartados |
|----------|-----------|
| a) Arquitecturas web: características, ventajas e inconvenientes | 2.1, 2.2 |
| b) Fundamentos y protocolos de un servidor web | 2.1, 3.1.1 |
| c) Instalación y configuración básica de servidores web | 2.2 (práctica), 3.1.1 |
| d) Clasificación de los principales servidores de aplicaciones | 2.2, 4.1.1 |
| e) Instalación y configuración básica de servidores de aplicaciones | 4.1.1 |
| f) Pruebas de funcionamiento de servidores web y de aplicaciones | 3.1.1, 3.2.2, 4.1.2 |
| g) Estructura y recursos de una aplicación web | 2.2, 4.1.1 (WAR y descriptor de despliegue) |
| h) Requerimientos del proceso de implantación | 2.2, 3.0, 4.1.2 |
| i) Documentación de la instalación y configuración | `README.md` de cada práctica, 5.2.1 |

### RA2 · Gestiona servidores web con criterios de acceso seguro

| Criterio | Apartados |
|----------|-----------|
| a) Parámetros de administración más importantes | 3.1.1 |
| b) Módulos: activación y configuración | 3.1.1 (módulos dinámicos de Nginx con `load_module`: `image_filter`, `njs`), 3.1.2 (`mod_rewrite`), 3.2.1 (`mod_ssl`), 3.2.2 (`mod_proxy`, `mod_deflate`, `mod_status`), 4.2.1 (`mod_dav`, `mod_authnz_ldap`) |
| c) Sitios virtuales | 3.1.2 |
| d) Autenticación y control de acceso | 3.2.1, 4.2.1 (LDAP) |
| e) Obtención e instalación de certificados digitales | 3.2.1 (Let's Encrypt y PositiveSSL) |
| f) Comunicaciones seguras entre cliente y servidor | 3.2.1 (TLS, HSTS, redirección a HTTPS) |
| g) Pruebas de funcionamiento y rendimiento | 3.2.2 (`ab`, logs, GoAccess) |
| h) Documentación de configuración, administración segura y recomendaciones | `README.md` de las prácticas de UD3 |
| i) Ajustes para implantar aplicaciones en el servidor web | 3.2.2 (proxy inverso), 4.1.2 |

### RA3 · Implanta aplicaciones web en servidores de aplicaciones de forma segura

| Criterio | Apartados |
|----------|-----------|
| a) Componentes y servicios del servidor de aplicaciones | 4.1.1 |
| b) Archivos de configuración y bibliotecas compartidas | 4.1.1 (`conf/`, `lib/`), 4.1.2 (*driver* JDBC) |
| c) Cooperación con el servidor web | 4.1.2 (Nginx delante de Tomcat, `RemoteIpValve`) |
| d) Mecanismos de seguridad | 4.1.1 (*realms*, válvulas, conector TLS, Manager) |
| e) Componentes web | 4.1.1 (*servlets*, JSP, filtros) |
| f) Ajustes para el despliegue | 4.1.1, 4.1.2 |
| g) Pruebas de funcionamiento y rendimiento de la aplicación desplegada | 4.1.2 (`/health`, `ab`) |
| h) Documentación de administración del servidor de aplicaciones | `README.md` de las prácticas de 4.1 |
| i) Documentación del despliegue | 4.1.2, 5.2.1 |

### RA4 · Administra servidores de transferencia de archivos

| Criterio | Apartados |
|----------|-----------|
| a) Instalación y configuración | 4.2.1 (vsftpd) |
| b) Usuarios y grupos para el acceso remoto | 4.2.1 (vsftpd y usuarios SSH) |
| c) Acceso anónimo | 4.2.1 |
| d) Modo activo y pasivo | 4.2.1 |
| e) Clientes en línea de comandos y gráficos | 4.2.1 (`lftp`/`curl`, FileZilla, `sftp`) |
| f) Protocolo seguro de transferencia | 4.2.1 (SFTP y FTPS), 5.2.1 |
| g) Transferencia integrada en servidores web | 4.2.1 (WebDAV) |
| h) El navegador como cliente | 4.2.1 (WebDAV y cliente web; FTP retirado de los navegadores) |
| i) Documentación del servicio | `README.md` de la práctica de 4.2.1 |

### RA5 · Verifica la ejecución de aplicaciones web comprobando los servicios de red

| Criterio | Apartados |
|----------|-----------|
| a) Sistemas de nombres jerárquicos | 2.1, 4.2.1 |
| b) Configuración del servidor de nombres según la aplicación | 3.0, 3.1.2, 3.2.1 (DCV), 4.2.1 (sobre el dominio propio) |
| c) Función, elementos y estructura del servicio de directorio | 4.2.1 |
| d) Configuración y personalización del servicio de directorio | 4.2.1 (LDIF, `ou` y grupos) |
| e) El directorio como autenticación centralizada | 4.2.1 |
| f) Parámetros del directorio para validar usuarios de la aplicación | 4.2.1 (`mod_authnz_ldap`, `JNDIRealm`) |
| g) Documentación de las adaptaciones en los servicios de red | `README.md` de la práctica de 4.2.1 |

### RA6 · Elabora la documentación de la aplicación web con herramientas de documentación y control de versiones

| Criterio | Apartados |
|----------|-----------|
| a) Herramientas de generación de documentación | 5.2.1 |
| b) Documentar componentes con los generadores de cada plataforma | 5.2.1 (Javadoc y similares) |
| c) Diferentes formatos | 5.2.1 (Markdown, HTML y PDF) |
| d) Herramientas colaborativas | 1.1.3 (*pull requests*), 5.2.1 (wiki, GitHub Pages) |
| e) Instalar, configurar y usar un sistema de control de versiones | 1.1.1 – 1.1.3 |
| f) Accesibilidad y seguridad de lo almacenado en el control de versiones | 1.1.1 (`.gitignore`), 1.1.3 (tokens y repositorios privados), 5.2.1 |
| g) Documentar la instalación y uso del control de versiones | 1.1.3, `README.md` del repositorio del proyecto |

> **Criterios de documentación** (RA1 i, RA2 h, RA3 h–i, RA4 i, RA5 g, RA6 g): cada práctica de UD3 y UD4 se entrega con un `README.md` en el repositorio del alumno que explique qué se ha instalado, cómo se ha configurado y qué recomendaciones de uso seguro se aplican. Ese conjunto de `README.md` es la base de la documentación del proyecto integrador.

---

## 10. Material que se puede preparar para cada semana

Siguiendo el formato de la UD2:

| Material | Formato |
|----------|---------|
| Dosieres de puesta en marcha (preparar la VM y dominio) | Markdown, en `UD3/3.0 Puesta en marcha/` (ya preparados; continúan las guías de `proyectos/`) |
| Teoría desarrollada | Markdown (`ud3_1_1_teoria.md`, …) |
| Diapositivas | PowerPoint editable, con el hilo del restaurante |
| Práctica de 1 h con entorno preparado | Markdown y `docker-compose.yml`, con los pasos sobre la VM y la alternativa en local |
| Plantilla de `README.md` de entrega | Markdown, la misma para todas las prácticas de UD3 y UD4 |
| Solucionario de la práctica | Markdown, solo para el docente |
| Test tipo test | Markdown, con solucionario explicado |
