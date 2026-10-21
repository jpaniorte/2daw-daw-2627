---
layout: default
title: "Proyecto Intermodular — Azure account"
permalink: /proyectos/maquina-remota/
---

# Azure account

Para desplegar vuestro proyecto en un servidor real (requisito del proyecto, ver [Requisitos de proyecto](https://github.com/jpaniorte/2daw-tfc-2627/wiki)) necesitáis una máquina accesible desde internet. La vamos a montar en **Microsoft Azure**, aprovechando que como alumnos tenéis acceso gratuito a **Azure for Students**: 100 $ de crédito durante 12 meses, **sin necesidad de tarjeta de crédito**.

Esta guía tiene dos fases:

- **Fase 1 (esta página)**: crear la cuenta de Azure for Students con vuestro correo `@alu.edu.gva.es` y comprobar que tenéis los 100 $ de crédito activos.
- **Fase 2 (más adelante)**: crear una máquina virtual con Ubuntu Server dentro de esa cuenta. Todavía no está disponible; se publicará cuando toda la clase haya completado la Fase 1.

---

## Objetivo de la Fase 1

Al terminar esta fase debéis llegar a una pantalla como esta, dentro del portal de Azure (`portal.azure.com`), mostrando **100 US$ de 100 US$** de crédito disponible:

<img src="/assets/img/proyectos/azure-students-credito.jpg" alt="Pantalla de Azure Education con 100$ de crédito disponible" class="screenshot-sm">


Fijaos en dos datos concretos de esa pantalla, porque son los que tenéis que comprobar al final:

- **Créditos disponibles**: `100 US$ de 100 US$`
- **Días hasta que expire el crédito**: `365`

---

## Antes de empezar

- Debéis usar vuestra cuenta de alumno **`vuestro.usuario@alu.edu.gva.es`**, con acceso a su bandeja de entrada (Microsoft envía un código de verificación ahí).
- **No hace falta tarjeta de crédito en ningún paso.** Si en algún momento el asistente os la pide, parad y avisad al profesor — no es el proceso normal de Azure for Students y puede ser un indicio de que os habéis metido por la oferta equivocada (la de "Azure gratis" para el público general sí la pide; la de estudiantes no).
- Si ya tenéis una cuenta personal de Microsoft (Outlook, Xbox, etc.) en el navegador, abrid una **ventana de incógnito/privada** para hacer todo el proceso, así evitáis que Azure intente usar esa cuenta personal en vez de la del instituto.

---

## Paso a paso

### 1. Abrir la oferta de Azure for Students

Entrad en:

```
https://azure.microsoft.com/es-es/free/students/
```

Pulsad el botón **"Empezar gratis"** (o "Activate now" / "Comenzar ahora", el texto exacto puede variar).

### 2. Iniciar sesión con vuestra cuenta del instituto

Cuando os pida iniciar sesión, usad vuestro correo completo:

```
vuestro.usuario@alu.edu.gva.es
```

con la misma contraseña que usáis para Aules / el correo del centro.

### 3. Verificación de estudiante

Azure os pedirá confirmar que sois estudiantes. Normalmente esto se hace enviando un **código de verificación al propio correo `@alu.edu.gva.es`**:

1. Revisad la bandeja de entrada de ese correo (y la carpeta de spam/no deseado si no llega en un par de minutos).
2. Copiad el código y pegadlo en el formulario de Azure.

### 4. Rellenar vuestros datos

El formulario pedirá nombre, apellidos, país (España) y, en algunos casos, un número de teléfono para un segundo código por SMS. Rellenadlo con vuestros datos reales.

### 5. Aceptar las condiciones de la oferta

Revisad y aceptad las condiciones del programa "Azure for Students". En ningún punto de este formulario se pide tarjeta de crédito.

### 6. Comprobar el crédito activado

Al terminar, Azure os llevará al portal (`portal.azure.com`) dentro de la sección **"Education"**. Buscad en el menú lateral u "Inicio" → **Education** y comprobad que veis la pantalla del objetivo de arriba, con:

- Créditos disponibles: **100 US$ de 100 US$**
- Días hasta que expire el crédito: **365**

---

## Si algo falla

- **El código no llega**: revisad spam/no deseado y esperad unos minutos; si sigue sin llegar, probad a reenviarlo desde el propio formulario.
- **Azure dice que el correo no es válido como cuenta académica**: avisad al profesor antes de insistir — puede ser necesario comprobar algo a nivel de centro.
- **Ya tenéis una cuenta de Azure/Microsoft personal asociada a otro correo**: aseguraos de estar en una ventana de incógnito y de iniciar sesión específicamente con `@alu.edu.gva.es`, no con una cuenta personal.
- **En algún paso os piden tarjeta de crédito**: parad inmediatamente y avisad al profesor; no es parte del proceso normal de esta oferta.

---

## Próximos pasos (Fase 2)

Con la cuenta activa y el crédito disponible, continuad con la [Fase 2: VM Ubuntu Server](/proyectos/vm-ubuntu/), donde crearemos juntos una máquina virtual con Ubuntu Server dentro de Azure y os conectaréis a ella por SSH.
