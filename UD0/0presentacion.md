---
marp: true
theme: default
paginate: true
size: 16:9
---

# Despliegue de Aplicaciones Web
### Módulo 0614 · CFGS Desarrollo de Aplicaciones Web

**José Pérez Aniorte**
j.perezaniorte@edu.gva.es

IES Severo Ochoa (Elche) · Curso 2026-2027

---

## ¿Qué es este módulo?

El módulo **Despliegue de Aplicaciones Web** cubre todo lo necesario para llevar una aplicación web desde el desarrollo hasta un entorno real:

- Instalar y configurar servidores Web y de aplicaciones
- Asegurar el acceso y las comunicaciones
- Transferir y desplegar aplicaciones de forma fiable
- Configurar los servicios de red implicados (DNS, directorio)
- Documentar y versionar todo el proceso

---

## Resultados de aprendizaje (RA)

1. **RA1** — Implanta arquitecturas Web
2. **RA2** — Gestiona servidores Web (acceso seguro)
3. **RA3** — Implanta aplicaciones en servidores de aplicaciones
4. **RA4** — Administra servidores de transferencia de archivos
5. **RA5** — Verifica la ejecución de aplicaciones Web (servicios de red)
6. **RA6** — Elabora la documentación de la aplicación Web

---

## RA1 — Implanta arquitecturas Web

Criterios de evaluación (CE):

- a) Aspectos generales de arquitecturas Web, características, ventajas e inconvenientes
- b) Fundamentos y protocolos del funcionamiento de un servidor Web
- c) Instalación y configuración básica de servidores Web
- d) Clasificación y descripción de los principales servidores de aplicaciones
- e) Instalación y configuración básica de servidores de aplicaciones
- f) Pruebas de funcionamiento de servidores Web y de aplicaciones
- g) Estructura y recursos que componen una aplicación Web
- h) Requerimientos del proceso de implantación de una aplicación Web
- i) Documentación de los procesos de instalación y configuración

---

## RA2 — Gestiona servidores Web

Criterios de evaluación (CE):

- a) Parámetros de administración más importantes del servidor Web
- b) Ampliación de la funcionalidad del servidor mediante módulos
- c) Creación y configuración de sitios virtuales
- d) Configuración de mecanismos de autenticación y control de acceso
- e) Obtención e instalación de certificados digitales
- f) Mecanismos para asegurar las comunicaciones cliente-servidor
- g) Pruebas de funcionamiento y rendimiento del servidor Web
- h) Documentación de configuración, administración segura y recomendaciones de uso
- i) Ajustes necesarios para la implantación de aplicaciones en el servidor Web

---

## RA3 — Implanta aplicaciones Web en servidores de aplicaciones

Criterios de evaluación (CE):

- a) Componentes y funcionamiento de los servicios del servidor de aplicaciones
- b) Principales archivos de configuración y bibliotecas compartidas
- c) Configuración del servidor de aplicaciones para cooperar con el servidor Web
- d) Configuración y activación de mecanismos de seguridad
- e) Configuración y uso de los componentes web del servidor de aplicaciones
- f) Ajustes necesarios para el despliegue de aplicaciones sobre el servidor
- g) Pruebas de funcionamiento y rendimiento de la aplicación Web desplegada
- h) Documentación de administración y recomendaciones de uso del servidor
- i) Documentación relativa al despliegue de aplicaciones sobre el servidor

---

## RA4 — Administra servidores de transferencia de archivos

Criterios de evaluación (CE):

- a) Instalación y configuración de servidores de transferencia de archivos
- b) Creación de usuarios y grupos para el acceso remoto
- c) Configuración del acceso anónimo
- d) Comprobación del acceso al servidor en modo activo y pasivo
- e) Pruebas con clientes en línea de comandos y en modo gráfico
- f) Uso del protocolo seguro de transferencia de archivos
- g) Configuración y uso de servicios de transferencia integrados en servidores web
- h) Uso del navegador como cliente del servicio de transferencia de archivos
- i) Documentación de configuración y administración del servicio

---

## RA5 — Verifica la ejecución de aplicaciones Web

Criterios de evaluación (CE):

- a) Estructura, nomenclatura y funcionalidad de los sistemas de nombres jerárquicos
- b) Necesidades de configuración del servidor de nombres (DNS)
- c) Función, elementos y estructuras lógicas del servicio de directorio
- d) Configuración y personalización del servicio de directorio
- e) Capacidad del servicio de directorio como autenticación centralizada
- f) Parámetros de configuración del servicio de directorios para validación de usuarios
- g) Documentación de las adaptaciones realizadas en los servicios de red

---

## RA6 — Elabora la documentación de la aplicación Web

Criterios de evaluación (CE):

- a) Identificación de herramientas de generación de documentación
- b) Documentación de componentes software con generadores específicos
- c) Uso de diferentes formatos para la documentación
- d) Uso de herramientas colaborativas para la documentación
- e) Instalación, configuración y uso de un sistema de control de versiones
- f) Accesibilidad y seguridad de la documentación en el sistema de control de versiones
- g) Documentación de la instalación, configuración y uso del sistema de control de versiones

---

## Organización del curso

| | |
|---|---|
| **Duración total** | 50 horas |
| **Sesiones semanales** | Miércoles (2) + Viernes (1) |
| **Nº de unidades didácticas** | 5 |


---

## Unidades didácticas

**UD1 — Git y Docker**
→ RA6 (control de versiones) + parte de RA1

**UD2 — Arquitecturas Web**
→ RA1 (arquitecturas, servidores, descriptor de despliegue)

**UD3 — Administración de servidores Web**
→ RA2 (completo)

**UD4 — Implantación de aplicaciones en servidores Web**
→ RA3, RA4 y RA5 (servidor de aplicaciones, FTP, servicios de red)

**UD5 — DevOps, CI/CD y GitHub Actions**
→ Unidad integradora: automatiza y refuerza RA1, RA2, RA3 y RA6 con un pipeline real

---

## Evaluación

- 50% de los CE de un RA superados -> RA superados
- 100% de los RA superados -> Módulo superado.

---

## Instrumentos de evaluación

- **Prácticas y proyectos de despliegue** — Durante una UD
- **Pruebas teórico-prácticas** — Al final de una UD
- **Repositorio Git y documentación** — Diario

---

## Herramientas de trabajo

- **Git / GitHub** — control de versiones y colaboración
- **Docker** — contenedores para servidores y entornos reproducibles
- **Servidor Web** (Apache / Nginx) y **servidor de aplicaciones**
- **Terminal** — administración de servicios
- **GitHub Actions** — integración y despliegue continuo (CI/CD)

---

# ¡Bienvenidos al módulo!

Regla 20-50-90 de retención del aprendizaje (Pirámide del Aprendizaje de Cody Blair):

- **Retienes el 20% cuando escuchas**: El aprendizaje pasivo retiene un porcentaje bajo de la información a largo plazo.

- **Retienes el 50% cuando escribes**: Tomar notas, resumir o transcribir activa la memoria cinestésica y visual, duplicando la retención.

- **Retienes el 90% cuando explicas**: Enseñar a otros o explicar el concepto con tus propias palabras (Técnica Feynman) obliga al cerebro a estructurar, simplificar y consolidar el conocimiento de forma profunda.

### ¿Dudas? 