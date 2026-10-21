---
layout: default
title: "Proyecto Intermodular — VM Ubuntu Server"
permalink: /proyectos/vm-ubuntu/
---

# VM Ubuntu Server

Con la cuenta de [Azure for Students](/proyectos/maquina-remota/) activa y el crédito disponible, toca crear la máquina virtual que será vuestro servidor: una **Ubuntu Server** a la que os conectaréis por **SSH**.

---

## Antes de empezar

- Haber completado la [Fase 1: Azure account](/proyectos/maquina-remota/) (crédito de 100$ activo).
- Tener un par de claves SSH en vuestro equipo. Si no las tenéis, generadlas en una terminal:

```
ssh-keygen -t ed25519 -C "vuestro.usuario@alu.edu.gva.es"
```

Aceptad la ubicación por defecto (`~/.ssh/id_ed25519`) y, si queréis, protegedla con una contraseña (*passphrase*). Esto crea dos ficheros: `id_ed25519` (clave **privada**, no se comparte nunca) e `id_ed25519.pub` (clave **pública**, la que subiremos a Azure).

---

## Paso 1: Crear la máquina virtual

> **Importante**: no vayáis directamente a "Máquinas virtuales" → "+ Crear". Por defecto Azure os propone tamaños de pago estándar que, en una suscripción de Azure for Students, suelen salir como **"no disponibles"** (cuota a 0 para esa familia/región). Para evitar ese lío, entrad por la puerta de los **servicios gratuitos**, que arranca la VM ya con un tamaño que sí está permitido.

1. Entrad en [portal.azure.com](https://portal.azure.com) con vuestra cuenta `@alu.edu.gva.es`.
2. Desde la página de **"Education"** (la del crédito de 100$), buscad la tarjeta **"Servicios gratuitos"** y pulsad **"Explorar todo"** (o buscad directamente **"Servicios gratuitos"** en la barra de búsqueda superior).
3. Veréis un catálogo de servicios con cuota mensual gratuita durante 12 meses. Buscad la tarjeta **"Máquina virtual con Linux"** (750 horas, usando las VM ampliables **B2pts v2** (Arm) o **B2ats v2** (AMD)) y pulsad su botón **"Crear"**:

   <img src="/assets/img/proyectos/azure-servicios-gratuitos.png" alt="Pantalla Servicios gratuitos de Azure, con la tarjeta Máquina virtual con Linux y su botón Crear" class="screenshot-sm">

   Esto os lleva al mismo formulario **"Crear una máquina virtual"**, pero con el tamaño ya preconfigurado a una opción gratuita — así no tenéis que ir buscando a mano un tamaño disponible.
4. Esta vía abre un formulario **simplificado** (más corto que el genérico de "Máquinas virtuales"):

   <img src="/assets/img/proyectos/azure-crear-vm.png" alt="Formulario simplificado de creación de máquina virtual, llegando desde Servicios gratuitos" class="screenshot-sm">

   - **Suscripción**: ya aparece **"Azure for Students"** seleccionada.
   - **Grupo de recursos**: Azure os propone uno nuevo automáticamente (p. ej. `vm-proyecto_group`, a partir del nombre que le deis a la VM). No hace falta tocarlo — es solo la "carpeta" lógica donde se agrupan todos los recursos de este proyecto.
   - **Nombre de máquina virtual**: por ejemplo `vm-proyecto`.
   - **Región**: Azure os propone una por defecto según disponibilidad (en la captura sale *South Africa North*, nada que ver con España — es normal, simplemente es donde había hueco para el tamaño gratuito en ese momento). Podéis dejarla o cambiarla por una más cercana; si al cambiarla el tamaño gratuito deja de estar disponible, volved a la que os proponía por defecto.
   - **Imagen**: ya viene seleccionada una Ubuntu Server LTS (en la captura, *Ubuntu Server 22.04 LTS*; puede que a vosotros os proponga otra versión LTS más reciente, como 24.04 — cualquiera de las dos es válida).
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

---

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

---

## Comprobación final

Si veis un prompt parecido a `azureuser@vm-proyecto:~$`, la conexión funciona correctamente. Guardad en un lugar accesible:

- La **IP pública** de la VM.
- El **usuario** (`azureuser` o el que hayáis elegido).

Los necesitaréis en los siguientes pasos del despliegue del proyecto.

---

## Si algo falla

- **"Permission denied (publickey)"**: comprobad que estáis usando la misma clave privada que corresponde a la pública que subisteis a Azure (`ssh -i ~/.ssh/id_ed25519 azureuser@<IP>` para indicarla explícitamente).
- **La conexión se queda colgada o da timeout**: revisad en Azure que la regla de red permite el puerto 22 de entrada y que la VM está en estado "en ejecución".
- **Os pide contraseña en vez de usar la clave**: puede que hayáis creado la VM con autenticación por contraseña en vez de por clave pública; revisad la configuración o recread la VM con la opción correcta.
