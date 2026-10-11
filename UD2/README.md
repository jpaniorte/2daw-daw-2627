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
- Servidor web (Apache/Nginx) vs. servidor de aplicaciones (Tomcat, Node.js, PHP-FPM...).
- El patrón servidor web + servidor de aplicaciones detrás.
- Qué significa desplegar: dominio, DNS, tipos de hosting (compartido, VPS, dedicado, cloud).
- Despliegue con contenedores Docker (sin entrar todavía en CI/CD, que es UD5).

## Entorno de prácticas

El bloque 2.1 no necesita ningún entorno especial: navegador con herramientas de desarrollador y una terminal con `curl`/`nslookup`. El bloque 2.2 usa Docker (ya conocido de la UD1) de forma ligera, lanzando contenedores ya construidos sin entrar en la configuración real de Apache/Nginx, que se reserva para la UD3.

## Evaluación

Al final de cada bloque (sesión del viernes) se realiza un **cuestionario en papel** de repaso, con el mismo formato que en UD1: preguntas tipo test sacadas de un banco de 100 preguntas, con una versión distinta por alumno para evitar copias.

## Estructura de carpetas

Cada carpeta `2.N <nombre del bloque>` sigue la misma convención que UD1, con prefijo `web_N_` (al no haber "partes" dentro de cada bloque):

- `web_N_teoria.md` — diapositivas de teoría (Marp).
- `web_N_practicas.md` — ejercicios guiados + retos.
- `web_N_test.md` — banco de 100 preguntas de repaso (sin soluciones).
- `web_N_examen.md` — cuestionario imprimible de cierre de bloque (20 versiones).
- `web_N_examen_sol.md` — soluciones del cuestionario, para uso del profesor.
- `web_N_simulacro.html` — simulacro interactivo (20 preguntas al azar del banco de 100).
- `pdf/` y `pptx/` — generados con `python3 build.py` desde la raíz del repo, no se editan a mano.
