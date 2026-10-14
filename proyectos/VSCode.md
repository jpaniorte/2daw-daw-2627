---
layout: default
title: "Proyecto Intermodular — VSCode + Copilot CLI"
permalink: /proyectos/vscode/
---

# VSCode + GitHub Copilot CLI

> **Alcance de esta guía**: trabajamos con **Copilot en el terminal** (la herramienta `copilot`). **No** instalamos ni usamos el panel lateral de chat ("GitHub Copilot Chat"): todo pasa por comandos, igual que ya haces con `git` o `docker`. 

## 0. Vivecoding responsable: la mentalidad antes que la herramienta

"Vivecoding" no es "aceptar todo lo que proponga la IA sin mirar". Es un ciclo corto y disciplinado:

```
1. Pide algo concreto y acotado (no "hazme la app entera")
2. Revisa el plan antes de que toque nada (Shift+Tab, ver más abajo)
3. Deja que ejecute, aprobando cada acción con criterio
4. Mira el diff en el panel de Git de VS Code antes de aceptarlo del todo
5. Haz commit de lo que funciona, en pasos pequeños
6. Si algo no cuadra, pídele que lo corrija — no lo arregles a mano "por rapidez"
```

Git es tu red de seguridad: si commiteas a menudo, siempre puedes volver atrás. Si no commiteas nunca, un solo paso en falso del agente (o tuyo) puede tirar horas de trabajo.

## 1. Instalación

```bash
# npm (macOS, Linux, Windows) — requiere Node.js
npm install -g @github/copilot

# Homebrew (macOS y Linux)
brew install copilot-cli

# Script de instalación (macOS y Linux)
curl -fsSL https://gh.io/copilot-install | bash

# WinGet (Windows)
winget install GitHub.Copilot
```

Necesitas una **suscripción de Copilot activa** (gratis como estudiante con el [GitHub Student Developer Pack](https://education.github.com/pack)). En Windows, PowerShell v6 o superior.

## 2. Arranque, login y conexión con VS Code

```bash
copilot
```

La primera vez, autentícate con:

```
/login
```

Para abrirlo integrado en VS Code tienes tres caminos equivalentes (todos terminan en una pestaña de **terminal**, no de chat):

1. Terminal integrado (`` Ctrl+` ``) y escribes `copilot`.
2. Perfil de terminal dedicado **"GitHub Copilot CLI"** (desplegable "+" del panel Terminal).
3. Paleta de comandos → **"Chat: New Copilot CLI Session"** (el nombre lleva "Chat" por catalogación interna de VS Code, pero abre una sesión de terminal normal).

Si lo abres desde una carpeta que coincide con el workspace abierto en VS Code, se conecta solo a ese contexto.

## 3. El superpoder real: dale contexto persistente de tu proyecto

Esto es lo que más diferencia "usarlo a ciegas" de "exprimirlo": Copilot CLI lee automáticamente, al arrancar, ficheros de instrucciones si existen en tu repositorio. No tienes que repetir el contexto en cada prompt.

Los sitios donde busca (por orden, de más general a más específico):

| Fichero | Alcance |
| --- | --- |
| `$HOME/.copilot/copilot-instructions.md` | Tus preferencias personales, en **todos** tus proyectos |
| `.github/copilot-instructions.md` | Todo este repositorio |
| `AGENTS.md` (en la raíz) | Todo este repositorio (formato abierto, también lo leen otras IAs) |
| `.github/instructions/**/*.instructions.md` | Reglas específicas por ruta, con `applyTo` |

**Para el proyecto del Hito 1, cread un `AGENTS.md` en la raíz del repo** con algo como esto (adaptadlo a vuestro stack real):

```markdown
# AGENTS.md

## Stack
- Backend: Laravel 11 (PHP 8.3), en `backend/`
- Frontend: Vue 3 + Vite, en `frontend/`
- Base de datos: MySQL (ver `docker-compose.yml`)

## Cómo arrancar en local
- Backend: `cd backend && composer install && php artisan serve`
- Frontend: `cd frontend && npm install && npm run dev`

## Convenciones del equipo
- Commits en español, en imperativo ("añade", no "añadido").
- No tocar `main` directamente: trabajamos en ramas `feature/...`.
- Nunca subir `.env` ni secretos reales (usar `.env.example`).

## Qué NO debe hacer el agente sin preguntar
- No ejecutar `git push`, `git push --force` ni borrar ramas.
- No instalar dependencias nuevas sin decirlo explícitamente en el prompt.
```

Con esto, cualquier miembro del equipo que abra `copilot` en el repo recibe automáticamente el mismo contexto — no hace falta que cada uno lo explique de nuevo.

Puedes comprobar qué ficheros se han cargado con `/instructions`, y ver de un vistazo todo lo que Copilot tiene activo (agentes, hooks, servidores MCP) con `/env`.

## 4. Referenciar código concreto en el prompt

En vez de describir un fichero con palabras, nómbralo directamente con `@` y autocompleta la ruta:

```
Revisa @backend/app/Http/Controllers/AuthController.php y añade validación del email
```

También puedes arrastrar un fichero a la ventana, o pegar una captura de pantalla (p. ej. un error de consola, o un diseño a replicar).

## 5. El modo Plan: piensa antes de tocar código

Antes de que escriba una sola línea, pulsa **`Shift+Tab`** para entrar en **modo Plan**: Copilot te propone los pasos que va a seguir y puedes discutirlos, recortarlos o ampliarlos *antes* de que ejecute nada. Para tareas de más de "un par de líneas", úsalo siempre — es la diferencia entre dirigir el trabajo y simplemente mirar lo que pasa.

## 6. Aprobaciones: el control real sobre lo que hace

Cada vez que Copilot quiere ejecutar algo (un comando, crear/editar un fichero), te pregunta y te da tres opciones:

1. **Yes** — lo aprueba solo esta vez; la próxima vuelve a preguntar.
2. **Yes, and approve `<tool>` for the rest of the running session** — a partir de ahora, esa herramienta concreta no vuelve a preguntar en esta sesión.
3. **No (Esc)** — lo rechaza y termina la operación actual.

⚠️ **Cuidado con la opción 2** en comandos destructivos: aprobar `rm` "para el resto de la sesión" significa que a partir de ahí puede borrar lo que quiera en esa carpeta sin volver a preguntarte. Apruébalo "para siempre" solo en comandos inofensivos (`ls`, `cat`, `npm run dev`...), no en `rm`, `git push`, `docker rm`, etc.

Existe también `--allow-all` (alias `--yolo`) para arrancar `copilot` sin pedir ningún permiso. **No lo uséis en el proyecto de equipo**: es cómodo para una prueba rápida y personal, pero en un repo compartido es la forma más rápida de que algo salga mal sin que nadie lo revise.

Si quieres aislar lo que hace en una caja más controlada, activa `/sandbox enable`.

## 7. Comandos de sesión que vale la pena conocer

- **`/resume`** — retoma una sesión anterior con todo su contexto (no empieces de cero cada vez que cierras la terminal).
- **`--continue`** (al arrancar `copilot`) — retoma directamente la última sesión cerrada.
- **`/compact`** — comprime el historial de la conversación cuando se hace muy largo (lo notarás porque empieza a "olvidar" cosas de hace rato).
- **`/context`** — cuánto contexto (tokens) estás usando ahora mismo.
- **`/usage`** — cuántos créditos de IA has consumido.
- **`/model`** — cambiar de modelo para la sesión.
- **`/mcp add`** — conectar servidores MCP (herramientas externas: por ejemplo, para que el agente pueda leer/crear issues de GitHub él mismo).
- **`/agent`** — elegir entre agentes personalizados, si vuestro equipo define alguno.

### Qué modelos puedes usar gratis

**Modelos gratis en OpenRouter**

OpenRouter mantiene una colección en vivo de modelos con precio **$0** por token: [openrouter.ai/collections/free-models](https://openrouter.ai/collections/free-models). Importante: ahí **no** vas a encontrar gratis a Claude, GPT o Gemini de gama alta — los gratuitos son modelos de pesos abiertos o de proveedores más pequeños. Esta es la lista a fecha de esta guía (entre 17 y 19 modelos según el día):

| Modelo | Para qué sirve |
| --- | --- |
| `nvidia/nemotron-3-ultra-550b-a55b:free` | Modelo grande (550B, 55B activos) para razonamiento con contexto largo, orquestación de agentes y tareas de nivel empresarial |
| `nvidia/nemotron-3.5-lightning:free` | Versión ligera (30B, 3B activos) pensada para cargas de trabajo agénticas de alto rendimiento |
| `nvidia/nemotron-3-super-120b-a12b:free` | Modelo intermedio (120B, 12B activos) con hasta 1M de contexto, para aplicaciones multi-agente |
| `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` | Modelo multimodal pequeño, pensado como "sub-agente" que procesa entradas con imágenes u otros formatos |
| `nvidia/nemotron-3.5-content-safety:free` | No es un asistente general: es un clasificador para moderación/filtrado de contenido |
| `poolside/laguna-s-2.1:free` | Modelo especializado en programación (118B, 8B activos), pensado como agente de ingeniería de software |
| `poolside/laguna-xs-2.1:free` | Versión compacta (33B, 3B activos) del anterior, también con *tool calling*, para tareas de código más ligeras |
| `dots-studio/dots-3-note-preview:free` | Modelo grande (280B, 16B activos) multimodal: razonamiento, código y contexto largo |
| `thinkingmachines/inkling:free` | Modelo grande multimodal (975B, 41B activos) de propósito general: razonamiento, código, agentes, RAG |
| `thinkingmachines/inkling-small:free` | Versión más pequeña y eficiente (276B, 12B activos) del anterior |
| `cohere/north-mini-code:free` | Modelo pequeño (30B, 3B activos) especializado en generación de código y tareas agénticas de desarrollo |
| `inception/mercury-decide:free` | No genera texto libre: devuelve probabilidades calibradas para tareas de decisión/puntuación |
| `liquid/lfm-2.5-2.6b:free` | Modelo muy compacto (2.6B), para razonamiento ligero en flujos de agentes, extracción de datos y RAG |
| `google/gemma-4-26b-a4b-it:free` | Gemma 4 de Google, variante de 26B, uso general (chat, instrucciones), contexto largo |
| `google/gemma-4-31b-it:free` | Gemma 4 de Google, variante de 31B, algo más capaz que la anterior, mismo uso general |
| `inclusionai/ling-3.1-flash` *(sin sufijo `:free`, pero a coste $0 en el momento de escribir esto)* | Modelo híbrido de razonamiento (560B, 25B activos) de InclusionAI |

Esta tabla **envejece rápido**: he comprobado que el catálogo de modelos gratis de OpenRouter cambia casi a diario (altas, bajas y modelos que dejan de ser gratis de un día para otro). Antes de confiar en un nombre concreto, comprobadlo en el enlace de arriba.

Son perfectamente válidos para practicar prompting, resolver dudas o prototipos pequeños. Un aviso de privacidad real: varios de los proveedores que ofrecen estos modelos gratis **pueden entrenar con tus prompts** — no son aptos para pegar código o datos sensibles del proyecto.

**Modelos gratis con el GitHub Student Developer Pack (plan "Copilot Student")**

Si activáis el [Student Developer Pack](https://education.github.com/pack), GitHub os da acceso a Copilot bajo un plan específico para estudiantes (distinto del Pro de pago). Lo que incluye de verdad:

- Finalización de código (autocompletado) **ilimitada**.
- **300 "premium requests" al mes** para usar el chat/agente (donde entra Copilot CLI).
- La selección de modelo es **automática ("Auto") únicamente**: Copilot elige por vosotros qué modelo usar según la tarea, sin que podáis forzar manualmente con `/model` un modelo concreto de gama alta (esto cambió durante 2026; antes sí se podía elegir a mano).

No os extrañéis, por tanto, si `/model` no os deja escoger entre una lista larga: con la cuenta de estudiante es normal, y no significa que algo esté mal configurado.

**¿Da igual elegir Intelligence, Balance o Efficiency?** No exactamente, pero tampoco es tan simple como "una gasta más que otra siempre". Las tres opciones **no fijan un modelo concreto**: cambian el objetivo con el que Auto decide, para cada petición, qué modelo usar de ese mismo conjunto disponible:

- **Efficiency** prioriza mantener el coste bajo — para tareas rápidas y sencillas.
- **Balance** pondera coste, calidad y velocidad a la vez — el valor por defecto razonable para el trabajo normal del día a día.
- **Intelligence** prioriza la calidad — para tareas complejas, aunque **no garantiza** que siempre use el modelo más grande disponible.

## 8. Atajos que ahorran tiempo de verdad

| Atajo / sintaxis | Qué hace |
| --- | --- |
| `Shift+Tab` | Entrar en modo Plan antes de ejecutar |
| `!comando` | Ejecuta ese comando de shell **directamente**, sin pasar por el modelo (para cosas que ya sabes hacer tú) |
| `Esc` `Esc` (en menos de medio segundo) | Interrumpe a Copilot mientras está "pensando" o ejecutando |
| `Ctrl+T` | Muestra u oculta el razonamiento interno del modelo |
| Dictado por voz | Alternativa a escribir el prompt |

## 9. Atajos de VS Code (generales, más allá de Copilot)

Estos no son específicos de Copilot: son atajos de VS Code que usarás constantemente durante todo el proyecto.

| Acción | Windows / Linux | macOS |
| --- | --- | --- |
| Paleta de comandos | `Ctrl+Shift+P` | `Cmd+Shift+P` |
| Abrir fichero rápido (Quick Open) | `Ctrl+P` | `Cmd+P` |
| Ir a una línea concreta | `Ctrl+G` | `Cmd+G` |
| Buscar en todo el proyecto | `Ctrl+Shift+F` | `Cmd+Shift+F` |
| Mostrar/ocultar terminal integrado | `` Ctrl+` `` | `` Cmd+` `` |
| Mostrar/ocultar el explorador de ficheros | `Ctrl+Shift+E` | `Cmd+Shift+E` |
| Ir al panel de Control de versiones (Git) | `Ctrl+Shift+G` | `Cmd+Shift+G` |
| Ir al panel de Extensiones | `Ctrl+Shift+X` | `Cmd+Shift+X` |
| Ir a la definición de un símbolo | `F12` | `F12` |
| Vista previa de la definición (sin saltar) | `Alt+F12` | `Option+F12` |
| Buscar todos los usos de un símbolo | `Shift+F12` | `Shift+F12` |
| Renombrar un símbolo en todo el proyecto | `F2` | `F2` |
| Acciones rápidas / quick fix | `Ctrl+.` | `Cmd+.` |
| Comentar/descomentar la línea actual | `Ctrl+/` | `Cmd+/` |
| Duplicar la línea hacia abajo | `Shift+Alt+Down` | `Shift+Option+Down` |
| Mover la línea actual arriba/abajo | `Alt+Up` / `Alt+Down` | `Option+Up` / `Option+Down` |
| Seleccionar la siguiente aparición igual (multi-cursor) | `Ctrl+D` | `Cmd+D` |
| Añadir un cursor en la línea de arriba/abajo | `Ctrl+Alt+Up` / `Ctrl+Alt+Down` | `Cmd+Option+Up` / `Cmd+Option+Down` |
| Dividir el editor (ver dos ficheros a la vez) | `Ctrl+\` | `Cmd+\` |
| Cerrar la pestaña actual | `Ctrl+W` | `Cmd+W` |
| Reabrir la última pestaña cerrada | `Ctrl+Shift+T` | `Cmd+Shift+T` |

## 10. Plugins populares que os van a hacer falta

No todo el trabajo lo hace Copilot: estas extensiones cubren huecos que la IA no sustituye (formateo consistente, avisos en tiempo real, ver el historial de Git, gestionar contenedores desde el propio editor...).

Imprescindibles para cualquier proyecto:

- **GitLens** — amplía el panel de Git: ves quién cambió cada línea, cuándo y por qué (el `blame` directamente en el editor). Muy útil para repartir trabajo en equipo y entender código que no escribiste tú.
- **Prettier** — formateador automático para JS/TS/Vue/CSS/HTML/JSON/Markdown. Configurad "formatear al guardar" para que todo el equipo entregue el mismo estilo, sin discutirlo a mano.
- **ESLint** — avisa de errores y malas prácticas de JavaScript/TypeScript mientras escribes, antes de que lleguen a ejecutarse.
- **Error Lens** — pinta los errores y avisos directamente al final de la línea donde ocurren, en vez de obligarte a mirar el panel de "Problemas" aparte.
- **Container Tools** (de Microsoft, sucesora de la antigua extensión "Docker") — gestiona contenedores, imágenes y servicios de `docker-compose` desde una pestaña del propio VS Code, sin salir a la terminal para mirar qué hay en marcha.
- **GitHub Pull Requests and Issues** — revisa y comenta Pull Requests de GitHub sin salir del editor; útil para la revisión cruzada entre equipos del Hito 1.
- **Bruno** — cliente de API basado en ficheros (en vez de en la nube), pensado para vivir dentro del repositorio y versionarse con Git. Es justo lo que usamos en `docs/bruno/` para documentar y probar los endpoints del backend.
- **Mini Browser** — un navegador embebido dentro de VS Code, útil para comprobar el frontend sin cambiar de ventana mientras programas.

Específicos según vuestro stack:

- **Backend en PHP/Laravel**: **PHP Intelephense** (autocompletado y análisis de PHP) + **Laravel Extension Pack** (soporte de Blade, rutas y comandos Artisan).
- **Frontend en Vue 3**: **Vue - Official (Volar)** — soporte oficial del lenguaje, imprescindible en Vue 3.
- **Si usáis Tailwind CSS** (backend o frontend): **Tailwind CSS IntelliSense**, autocompleta las clases de utilidad y te avisa de las que no existen.

No instaléis extensiones "por si acaso": cada una consume recursos y, en equipo, es mejor que todos tengáis las mismas instaladas para evitar comportamientos distintos entre máquinas.

### Mostrar/ocultar los paneles de Container Tools, Bruno y Mini Browser

Estas tres extensiones añaden su propio icono a la barra de actividad (el lateral izquierdo), pero **ninguna trae un atajo de teclado por defecto** para abrir o cerrar su panel — hay que asignarlo vosotros mismos.

Cómo asignarlo, paso a paso:

1. Abre la paleta de comandos y ejecuta **"Preferences: Open Keyboard Shortcuts"** (o el atajo `Ctrl+K Ctrl+S` / `Cmd+K Cmd+S`).
2. Busca el nombre exacto del comando del panel que quieres controlar (tabla abajo).
3. Haz clic en el icono de lápiz (o doble clic sobre el resultado) y pulsa la combinación de teclas que quieras usar.
4. Si esa combinación ya está en uso, VS Code te avisará y te dejará decidir si la reasignas.

| Plugin | Comando a buscar | Atajo de ejemplo |
| --- | --- | --- |
| Bruno | `workbench.view.extension.bruno` | elige uno libre, p. ej. `Cmd+Shift+H` / `Ctrl+Shift+H` |
| Container Tools | `workbench.view.extension.containersView` | elige uno libre, p. ej. `Cmd+Shift+K` / `Ctrl+Shift+K` |
| Mini Browser | `workbench.view.extension.miniBrowser` | elige uno libre, p. ej. `Cmd+Shift+M` / `Ctrl+Shift+M` |

Los "atajos de ejemplo" son solo sugerencias: lo importante es el nombre del comando, no la combinación concreta — cada uno puede elegir la que le resulte más cómoda.

## 11. Flujo recomendado para el equipo en el Hito 1

1. Cada persona autentica **su propia cuenta** (nunca compartáis tokens entre compañeros).
2. Trabajad en ramas (`feature/backend-auth`, `feature/frontend-login`...), nunca directamente en `main`.
3. Un terminal con `copilot` por tarea/rama, no todo mezclado en una sesión gigante.
4. Modo Plan para cualquier cosa que no sea trivial.
5. Antes de aceptar, mirad el diff en la pestaña **Source Control** de VS Code — exactamente igual que revisaríais el código de un compañero humano.
6. Commits pequeños y frecuentes, con mensaje descriptivo (lo puede proponer el propio Copilot, pero el commit lo decides tú).
7. Un Pull Request se revisa igual lo haya escrito una persona o un agente: nadie mergea sin que otro del equipo lo mire.

## 12. Ejemplo real: así evoluciona una conversación de vivecoding

Esto es un extracto real de los prompts usados para construir un proyecto de demostración (Laravel + Vue + Docker + documentación de API), con otro asistente en terminal — el asistente concreto cambia, pero la forma de pedir las cosas es exactamente la misma que haréis con Copilot CLI. Fijaos en el patrón: cada prompt es concreto, dice el "qué" con detalle (formato de respuesta, puertos, casos límite) y, cuando algo no sale bien, se pide ayuda para diagnosticar en vez de insistir a ciegas.

**1. Arrancar la aplicación Laravel y Vue**

> quiero iniciar una app, en una carpeta backend debe de existir una aplicación laravel, con un endpoint hello world listo que devuelva un 200 "hello world" en JSON. En otro lado, quiero un frontend con vuejs que sea capaz de lanzar un apeticion a ese endpoint y mostrar hello world. El endpoint /hello-world puede aceptar parámetros, de manera que si le paso name="jose" me devuelve Hello Wolrd Jose. En el frontend, añade un text box de manera que me permita editar y enviar este parametro. Al pulsar sobre enviar, mostrará la respuesta con el nombre

Fíjate en que el prompt ya deja claras varias decisiones de diseño (formato de la respuesta, nombre del endpoint, caso sin parámetro) para que el agente no tenga que adivinarlas.

**2. Levantar los servicios de desarrollo con Docker Compose**

> Crea un fichero start-services.sh con un script de bash para levantar todos los servicios de desarrollo en local. Estos servicios deben estar montados en docker compose, ten en cuenta que debe tener un bd de mariadb. Al finalizar, dime las variables de conexión para que pueda configurarlas en mi aplicación y guiame para hacerlo en vuejs. Ten en cuenta que es desarrollo, quiero que tenga hotreloading

**3. Documentar las peticiones HTTP con Bruno**

> Crea la carpeta docs si no existe en la raiz de proyecto y dentro una carpeta con el nombre bruno. De momento, quiero tener un entorno develop con la baseURL de mi app: http://localhost:8080. Crea las peticiones a las rutas helloWorld con y sin parámetros

Fíjate en que, igual que en el primer prompt, aquí también se fija de entrada un dato concreto (la `baseURL`) y qué peticiones exactas hacen falta, en vez de pedir algo vago como "documenta la API".

## Enlaces oficiales

- [Using GitHub Copilot CLI (guía de uso completa)](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/overview)
- [Custom instructions para Copilot CLI (AGENTS.md y similares)](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions)
- [GitHub Copilot CLI — repositorio oficial](https://github.com/github/copilot-cli)
- [Copilot CLI en VS Code](https://code.visualstudio.com/docs/copilot/agents/copilot-cli)
- [GitHub Student Developer Pack](https://education.github.com/pack)
