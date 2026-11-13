# Azure account

Para desplegar el proyecto en un servidor real necesitas una máquina accesible desde internet. La vamos a montar en **Microsoft Azure**, aprovechando que como alumnos tenéis acceso gratuito a **Azure for Students**: 100 $ de crédito durante 12 meses, **sin necesidad de tarjeta de crédito**.

## Antes de empezar

- Debéis usar vuestra cuenta de alumno **`vuestro.usuario@alu.edu.gva.es`**, con acceso a su bandeja de entrada (Microsoft envía un código de verificación ahí).
- **No hace falta tarjeta de crédito en ningún paso.** Si en algún momento el asistente os la pide, parad y avisad al profesor — no es el proceso normal de Azure for Students y puede ser un indicio de que os habéis metido por la oferta equivocada (la de "Azure gratis" para el público general sí la pide; la de estudiantes no).
- Si ya tenéis una cuenta personal de Microsoft (Outlook, Xbox, etc.) en el navegador, abrid una **ventana de incógnito/privada** para hacer todo el proceso, así evitáis que Azure intente usar esa cuenta personal en vez de la del instituto.

## Fase 1

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

## Fase 2

Crearemos una máquina virtual con Ubuntu Server dentro de Azure y os conectaréis a ella por SSH.

## Antes de empezar

- Tener un par de claves SSH en vuestro equipo. Si no las tenéis, generadlas en una terminal:

```
ssh-keygen -t ed25519 -C "vuestro.usuario@alu.edu.gva.es"
```

Aceptad la ubicación por defecto (`~/.ssh/id_ed25519`) y, si queréis, protegedla con una contraseña (*passphrase*). Esto crea dos ficheros: `id_ed25519` (clave **privada**, no se comparte nunca) e `id_ed25519.pub` (clave **pública**, la que subiremos a Azure).

## Paso 1: Crear la máquina virtual

> **Importante**: no vayáis directamente a "Máquinas virtuales" → "+ Crear". Por defecto Azure os propone tamaños de pago estándar que, en una suscripción de Azure for Students, suelen salir como **"no disponibles"** (cuota a 0 para esa familia/región). Para evitar ese lío, entrad por la puerta de los **servicios gratuitos**, que arranca la VM ya con un tamaño que sí está permitido.

1. Entrad en [portal.azure.com](https://portal.azure.com) con vuestra cuenta `@alu.edu.gva.es`.
2. Desde la página de **"Education"** (la del crédito de 100$), buscad la tarjeta **"Servicios gratuitos"** y pulsad **"Explorar todo"** (o buscad directamente **"Servicios gratuitos"** en la barra de búsqueda superior).
3. Veréis un catálogo de servicios con cuota mensual gratuita durante 12 meses. Buscad la tarjeta **"Máquina virtual con Linux"** (750 horas, usando las VM ampliables **B2pts v2** (Arm) o **B2ats v2** (AMD)) y pulsad su botón **"Crear"**:

   <img src="{{ '/assets/img/proyectos/azure-servicios-gratuitos.png' | relative_url }}" alt="Pantalla Servicios gratuitos de Azure, con la tarjeta Máquina virtual con Linux y su botón Crear" class="screenshot-sm">

   Esto os lleva al mismo formulario **"Crear una máquina virtual"**, pero con el tamaño ya preconfigurado a una opción gratuita — así no tenéis que ir buscando a mano un tamaño disponible.
4. Esta vía abre un formulario **simplificado** (más corto que el genérico de "Máquinas virtuales"):

   <img src="{{ '/assets/img/proyectos/azure-crear-vm.png' | relative_url }}" alt="Formulario simplificado de creación de máquina virtual, llegando desde Servicios gratuitos" class="screenshot-sm">

   - **Suscripción**: ya aparece **"Azure for Students"** seleccionada.
   - **Grupo de recursos**: Azure os propone uno nuevo automáticamente (p. ej. `vm-proyecto_group`, a partir del nombre que le deis a la VM). No hace falta tocarlo — es solo la "carpeta" lógica donde se agrupan todos los recursos de este proyecto.
   - **Nombre de máquina virtual**: por ejemplo `vm-proyecto`.
   - **Región**: Azure os propone una por defecto según disponibilidad (en la captura sale *South Africa North*, nada que ver con España — es normal, simplemente es donde había hueco para el tamaño gratuito en ese momento). Podéis dejarla o cambiarla por una más cercana; si al cambiarla el tamaño gratuito deja de estar disponible, volved a la que os proponía por defecto.
   - **Imagen**: Ubuntu Server 24.04 LTS x64.
   - Veréis un aviso: **"No se le cobrará por hasta 750 horas de uso para máquinas virtuales B1s o B2ats al mes"** — confirma que esta vía os deja ya en el tramo gratuito.
   - **Tamaño**: ya viene fijado a la opción gratuita (en la captura, `Standard_B2ats_v2`, marcada como "servicios gratuitos"). No hace falta cambiarlo.
   - En **"Cuenta de administrador"**:
     - **Tipo de autenticación**: dejad marcada **"Clave pública SSH"** (no "Contraseña").
     - **Nombre de usuario**: el que queráis, por ejemplo vuestro usuario del instituto.
     - **Origen de clave pública SSH**: dejad **"Usar la clave pública existente"** y pegad el contenido de vuestra clave pública. Para verla:
       ```
       cat ~/.ssh/id_ed25519.pub
       ```
       Copiad toda la línea (empieza por `ssh-ed25519 ...`) y pegadla en el campo **"Clave pública SSH"**.
     - (Azure también ofrece generar él mismo un par de claves nuevo y dároslo para descargar — no lo uséis: es preferible que la clave privada la tengáis vosotros desde el principio, generada como en el paso anterior.)
   - En **"Reglas de puerto de entrada"**: dejad **"Permitir los puertos seleccionados"** con **HTTP (80), HTTPS (443) y SSH (22)** — nos vendrán bien los tres más adelante para desplegar la aplicación del proyecto, no solo para conectar por SSH.
5. No hace falta pasar por "Siguiente: Etiquetas". Pulsad directamente **"Revisar y crear"** y, tras la validación, **"Crear"**. Esperad a que el despliegue termine (un par de minutos).
6. Una vez desplegada, entrad en el recurso de la VM y copiad su **dirección IP pública** (aparece en la vista general).

## Paso 2: Conectar por SSH

Desde una terminal de vuestro equipo:

```
ssh azureuser@<IP_PUBLICA>
```

(sustituyendo `azureuser` por el usuario que hayáis puesto y `<IP_PUBLICA>` por la IP copiada en el paso anterior).

- La primera vez os pedirá confirmar la huella (*fingerprint*) del servidor — escribid `yes`.
- Al usar autenticación por clave, deberíais entrar **sin que os pida contraseña**.
- Si protegisteis la clave privada con *passphrase*, os la pedirá a vosotros (es local, no viaja a la VM).

Una vez dentro, actualizad el sistema:

```
sudo apt update && sudo apt upgrade -y
```

