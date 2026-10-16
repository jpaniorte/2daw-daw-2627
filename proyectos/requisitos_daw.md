---
layout: default
title: "Proyecto Intermodular — Requisitos DAW"
permalink: /proyectos/requisitos-daw/
---

# Requisitos — Despliegue de Aplicaciones Web (0614)

Docente: José Pérez Aniorte

El proyecto debe demostrar, mediante un despliegue real, lo trabajado a lo largo de las 5 UD del módulo: Git y Docker (UD1), arquitecturas web (UD2), administración de servidores web (UD3), implantación de aplicaciones en servidores (UD4) y DevOps/CI-CD (UD5).

## Requisitos Mínimos

- El despliegue se debe realizar en un **servidor real accesible desde internet**: una VPS o instancia cloud de cualquier proveedor (AWS, Azure, Oracle Cloud, DigitalOcean, Hetzner...) o un servidor del centro. No se exige ningún proveedor concreto: lo importante es que sea una máquina de verdad, no un entorno de desarrollo local.
- Al menos un **servidor web y/o de aplicaciones** con todos los recursos integrados (lenguaje de programación, base de datos, servidor web) funcionando de forma conjunta.
- El servidor debe tener una **IP fija** asignada y ser **accesible por SSH**.
- La aplicación debe funcionar en **HTTPS**, con un certificado válido (p. ej. generado con Let's Encrypt).
- Al menos la aplicación (o uno de sus componentes) debe estar **empaquetada y ejecutándose en un contenedor Docker** — es contenido central del módulo (UD1) y, a diferencia de otros planteamientos de este mismo proyecto en otros módulos, aquí es obligatorio.
- Se debe **automatizar el despliegue con un pipeline de GitHub Actions** (UD5) que, como mínimo, construya la aplicación y la despliegue al servidor con cada cambio relevante.

Para alcanzar una calificación superior en el módulo de Despliegue de Aplicaciones Web se debe implementar alguno de los requisitos adicionales.

## Requisitos adicionales

Adicionalmente se podrá hacer uso de:

- Alojar la base de datos en un **contenedor Docker dedicado**, con los datos persistidos en un volumen.
- Colocar **Nginx o Apache como proxy inverso** delante del servidor de aplicaciones (UD3), en vez de exponerlo directamente.
- Orquestar todo el stack (aplicación, base de datos, proxy...) con **Docker Compose** (UD1, bloque 1.2.3).
- Ampliar el pipeline de CI/CD para que **ejecute tests automáticos** antes de desplegar (UD5).
- Instalar un **servidor FTP/SFTP** asegurado para la transferencia de ficheros (UD4.2.1).
- Configurar un **dominio propio** con su DNS apuntando al servidor, en vez de usar solo la IP.
- Añadir **medidas de seguridad adicionales**: cortafuegos, `fail2ban`, cabeceras de seguridad HTTP, o un WAF (UD3.2).
- Implementar **balanceo de carga** entre varias instancias o contenedores de la aplicación.
- Añadir **monitorización básica** del servidor (logs centralizados, métricas de uso, comprobación de disponibilidad) — UD3.2.2.

---

Departamento de Informática · Curso 2026/27

*Nota: no se ha concretado el nombre del centro en este pie — dime cuál es y lo añado.*
