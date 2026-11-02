# UD2 · Arquitecturas Web

Segunda Unidad Didáctica del módulo **Despliegue de Aplicaciones Web (0614)**, 2º CFGS DAW.

A diferencia de UD1 (Git y Docker, con 3 "partes" por bloque), UD2 tiene solo **2 bloques independientes** (2.1 y 2.2), cada uno equivalente a una semana de 3 sesiones.

## Calendario

2 semanas, 3h/semana repartidas en dos sesiones:

| Bloque | Carpeta | Miércoles (2h) | Viernes (1h) | Tema |
| --- | --- | --- | --- | --- |
| 2.1 | `2.1 Fundamentos web` | 28 oct | 30 oct | Fundamentos web |
| 2.2 | `2.2 Servidores web y de aplicaciones` | 4 nov | 6 nov | Servidores web y de aplicaciones |

Reparto semanal: **1h de teoría + 2h de práctica** (teoría y arranque de la práctica el miércoles, cierre de la práctica y cuestionario el viernes).

## Temario

### Bloque 2.1 — Fundamentos web
- Arquitectura cliente-servidor, protocolo HTTP (métodos, códigos de estado, cabeceras).
- Anatomía de una URL y DNS básico.
- HTTP sin estado: cookies y sesiones.
- Arquitecturas en capas (1/2/3/N capas).
- Arquitecturas a gran escala: monolito, SOA, microservicios, event-driven, serverless, P2P.
- Patrones de diseño interno: MVC/MVP/MVVM, arquitectura Hexagonal, Clean/Onion Architecture.

### Bloque 2.2 — Servidores web y de aplicaciones
- Contenido estático vs. dinámico.
- Renderizado (CSR, SSR, hidratación, SSG), SEO, CDN y *cache busting*.
- Servidor web (Apache/Nginx) vs. servidor de aplicaciones (Tomcat, Node.js, Gunicorn, PHP-FPM...): compresión, modelos de concurrencia y frameworks frontend/backend.
- CORS: orígenes, cabeceras `Access-Control-Allow-*` y preflight.
- El patrón servidor web + servidores de aplicaciones detrás: proxy inverso, 502/504, balanceo, escalado, health checks.
- Qué significa desplegar: dominio, DNS, hosting (compartido, VPS, dedicado, IaaS/PaaS), entornos, artefactos versionados (SemVer), configuración y secretos.
- Despliegue con contenedores Docker y estrategias sin corte (rolling, blue-green, canary, feature flags), sin entrar todavía en CI/CD, que es UD5.

## Entorno de prácticas

Las dos prácticas se hacen con `curl` (en Windows, desde Git Bash) y un entorno de Docker Compose que el alumnado descarga como zip desde la página de la práctica (`web_N_practica_entorno.zip`). Cada zip trae un `README.md` con un plan B por si Docker no funciona.

- **2.1:** httpbin (un "espejo" de HTTP) y una mini aplicación PHP con login y sesiones.
- **2.2:** Nginx delante de dos instancias de una app Node.js, más una segunda web en otro puerto para la parte de CORS. Se toca la configuración de Nginx solo lo justo (balanceo, compresión, caché); Apache/Nginx a fondo se ve en la UD3.

## Evaluación

Al final de cada bloque (sesión del viernes) se realiza un **cuestionario en papel** de repaso, con el mismo formato que en UD1: preguntas tipo test sacadas de un banco de 80 preguntas, con una versión distinta por alumno para evitar copias.

## Estructura de carpetas

Cada carpeta `2.N <nombre del bloque>` sigue la misma convención que UD1, con prefijo `web_N_` (al no haber "partes" dentro de cada bloque):

- `web_N_teoria.md` — diapositivas de teoría (Marp).
- `web_N_teoria_presentacion.pdf` — presentación de la teoría (botón «Presentación» de la web).
- `web_N_practica.md` — práctica guiada con preguntas ❓ para entregar.
- `web_N_practica_entorno.zip` — entorno de Docker Compose de la práctica.
- `web_N_practica_sol.md` — solucionario de la práctica, para uso del profesor (no se sube).
- `web_N_test.md` — banco de 80 preguntas de repaso (sin soluciones).
- `web_N_test_sol.md` — soluciones del banco con explicación de cada pregunta (no se sube).
- `web_N_simulacro.html` — simulacro interactivo (20 preguntas al azar del banco, con las explicaciones del solucionario).
- `web_N_examen.md` / `web_N_examen_sol.md` y `pdf/` — cuestionario imprimible (20 versiones de 20 preguntas) y sus soluciones. No se suben: se generan desde el banco con `examenes.py` en la raíz del repo:

  ```bash
  python3 examenes.py "UD2/2.2 Servidores web y de aplicaciones" web_2 \
    --titulo "web bloque 2.2: Servidores web y de aplicaciones" --pie "UD2: Arquitecturas Web"
  ```
