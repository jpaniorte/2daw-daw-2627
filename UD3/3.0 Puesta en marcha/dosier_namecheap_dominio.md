# Dosier 2 — Tu dominio `.me` con Namecheap

En el dosier 1 dejaste preparado tu servidor en Azure, pero solo se puede llegar a él por su IP (`20.123.45.67`). Nadie recuerda una IP. En este dosier vas a **registrar un nombre de dominio** gratis durante un año y a hacer que **apunte a tu servidor**, para que tu web esté en `http://tunombre.me`.

## Qué vas a conseguir

- Un dominio **`<tunombre>.me`** registrado a tu nombre durante 1 año, a 0 €.
- Los **registros DNS** que hacen que `tunombre.me` y `www.tunombre.me` lleguen a tu VM.
- El **certificado SSL** del Pack reclamado, pero **sin activar** (se activa en clase, en el apartado 3.2.1).

## Lo que NO debes hacer

- ❌ **Pagar nada.** Todo este dosier sale a 0,00 $.
- ❌ **Dejar activada la renovación automática.**
- ❌ **Cambiar los *nameservers* a *Custom DNS*** salvo que el profesor lo pida.
- ❌ **Activar el certificado PositiveSSL** antes del apartado.
- ❌ **Compartir la contraseña de Namecheap.** Quien la tenga puede transferir tu dominio.

## Qué hay que entregar

Nada.

## Antes de empezar: requisitos

| Requisito | Cómo comprobarlo |
|-----------|------------------|
| **VM** | `ssh <user>@<IP_PUBLICA>` funciona|
| **GitHub Student Developer Pack** aprobado | `https://education.github.com/pack` muestra la oferta de **Namecheap** |

## Un poco de teoría 

Cuando escribes `tunombre.me` en el navegador, tu ordenador pregunta al **DNS** (la «guía de restaurantes» de la UD2) qué IP corresponde a ese nombre. Para que la respuesta sea la IP de tu VM:

1. **Registras** el dominio en un **registrador** (Namecheap). Desde ese momento eres su titular.
2. En el registrador, creas **registros DNS**. Los dos que necesitas:

| Tipo | Nombre (*Host*) | Valor | Significa |
|------|-----------------|-------|-----------|
| **A** | `@` (el propio dominio) | `20.123.45.67` | `tunombre.me` está en esta IP |
| **CNAME** | `www` | `tunombre.me.` | `www.tunombre.me` es un alias de `tunombre.me` |

3. Los cambios tardan un poco en verse en todo el mundo (**propagación**), según el **TTL** de cada registro.

## Paso 1 — Elegir el nombre

Antes de entrar en Namecheap, piensa **tres opciones** de nombre, por orden de preferencia. Vas a usarlo todo el curso y lo verá cualquiera, así que:

- ✔ Corto, fácil de escribir y profesional: `jperez.me`, `juanperez-daw.me`, `jpdev.me`.
- ✔ Solo letras minúsculas, números y guiones (sin tildes ni `ñ`).
- ❌ Nada ofensivo ni que imite una marca o a otra persona.
- ❌ Evita poner datos personales de más (fecha de nacimiento, DNI…).

## Paso 2 — Reclamar el dominio gratis

1. Entra en `https://education.github.com/pack`, busca **Namecheap** y pulsa el enlace de la oferta del dominio `.me`. Te llevará a la página de Namecheap para estudiantes (`nc.me`).
2. En el buscador, escribe tu primera opción **sin** `.me` y pulsa **Find** (*Buscar*).
3. Si está libre, aparecerá con el precio tachado y **0,00 $** (o *Free*). Si no, prueba con la siguiente opción.
4. Pulsa **Get it free** (o *Add to cart*) y, cuando lo pida, **conecta tu cuenta de GitHub** (*Authorize with GitHub* / *Sign in with GitHub*) y **autoriza** a Namecheap. Así comprueba que tienes el Pack.
5. **Crea tu cuenta de Namecheap:** usuario, contraseña segura y **correo real** (te llegarán avisos importantes). Rellena los datos de contacto con datos reales: son los del titular del dominio.
6. Revisa el carrito: el **total debe ser 0,00 $**. Si aparece cualquier importe, **no pagues**: quita del carrito lo que sobre (*hosting*, correo, VPN…).
7. Confirma el pedido (*Complete order* / *Confirm order*).

> **Si te ofrecen conectar el dominio con GitHub Pages o con otro servicio**, de momento **no** lo hagas: el dominio tiene que apuntar a tu VM.

> **Correo de verificación:** puede que Namecheap (o ICANN) te envíe un correo para **verificar tu dirección de contacto**. **Ábrelo y pulsa el enlace en los próximos 15 días**: si no lo haces, el dominio se suspende.

✅ **Comprobación:** entra en `https://ap.www.namecheap.com` (o pulsa **Account → Dashboard**). En **Domain List** aparece tu dominio con estado **Active**.

## Paso 3 — Proteger la cuenta y el dominio

En **Domain List**, junto a tu dominio:

| Opción | Qué poner | Por qué |
|--------|-----------|---------|
| **Auto-Renew** | **Desactivado** (interruptor en gris) | Después del primer año, el `.me` cuesta unos **20 $ al año**. Si lo dejas activado y tienes una tarjeta guardada, se cobrará solo |
| **Domain Privacy** (*Withheld for Privacy*) | **Activado** (suele venir activado y es gratis) | Oculta tu nombre, dirección y teléfono en la base de datos pública WHOIS |

Además, activa la **verificación en dos pasos** de la cuenta de Namecheap: **Profile → Security → 2-Factor Authentication**. Quien entre en tu cuenta puede llevarse tu dominio.

> Si al año quieres conservar el dominio, podrás renovarlo a mano antes de que caduque. Namecheap te avisará por correo.

✅ **Comprobación:** **Auto-Renew** está en gris y **Domain Privacy** está activo.

## Paso 4 — Comprobar que usas el DNS de Namecheap

1. En **Domain List**, pulsa **Manage** junto a tu dominio.
2. En la pestaña **Domain**, busca la sección **NAMESERVERS**.
3. Debe poner **Namecheap BasicDNS**. Si pone otra cosa (*Custom DNS*), cámbialo a **Namecheap BasicDNS** y pulsa el ✔ verde.

> **¿Qué es esto?** Los *nameservers* son los servidores que responden por tu dominio. Con *Namecheap BasicDNS*, los registros que crees en el paso siguiente los sirve Namecheap. Si eligieras *Custom DNS*, los registros de Namecheap dejarían de tener efecto.

## Paso 5 — Crear los registros DNS

1. Dentro de **Manage**, abre la pestaña **Advanced DNS**.
2. En **HOST RECORDS** verás los registros que Namecheap crea por defecto para mostrar su página de «dominio aparcado». Normalmente son estos dos:

| Type | Host | Value |
|------|------|-------|
| CNAME Record | `www` | `parkingpage.namecheap.com.` |
| URL Redirect Record | `@` | `http://www.tunombre.me/` |

3. **Bórralos los dos** con el icono de la papelera 🗑 de cada fila.
4. Pulsa **ADD NEW RECORD** y crea este registro:

| Campo | Valor |
|-------|-------|
| Type | **A Record** |
| Host | `@` |
| Value | **La IP pública de tu VM** (dosier 1), por ejemplo `20.123.45.67` |
| TTL | **5 min** |

   Pulsa el ✔ verde de la fila para guardarlo.

5. Pulsa otra vez **ADD NEW RECORD** y crea:

| Campo | Valor |
|-------|-------|
| Type | **CNAME Record** |
| Host | `www` |
| Value | `tunombre.me.` (tu dominio **con un punto al final**) |
| TTL | **5 min** |

   Pulsa el ✔ verde.

6. Al final, en **HOST RECORDS** debe haber **solo** estos dos registros:

| Type | Host | Value | TTL |
|------|------|-------|-----|
| A Record | `@` | `20.123.45.67` | 5 min |
| CNAME Record | `www` | `tunombre.me.` | 5 min |

---

> **¿Por qué un punto al final?** `tunombre.me.` es un nombre **completo**. Sin el punto, algunos sistemas lo interpretan como relativo y lo convierten en `tunombre.me.tunombre.me`.

> **¿Por qué TTL de 5 min?** El TTL indica cuánto tiempo pueden guardar en caché la respuesta los demás servidores DNS. Con un TTL bajo, si te equivocas y lo corriges, el cambio se ve antes. En producción se suele subir (por ejemplo, a 1 hora).

> **Más adelante** (apartado 3.1.2) añadirás aquí más registros para tus subdominios, como `tienda.tunombre.me`. No los crees todavía.

## Paso 6 — Comprobar la propagación

Espera **unos 5 minutos** después de guardar. Luego comprueba que el nombre se resuelve a tu IP.

**6.1 Desde tu VM** (funciona igual en Windows, macOS y Linux, porque el comando se ejecuta en Ubuntu):

```bash
ssh daw 'dig +short tunombre.me; dig +short www.tunombre.me'
```

Debe salir:

```
20.123.45.67
tunombre.me.
20.123.45.67
```

La segunda consulta devuelve primero el alias (`tunombre.me.`) y luego su IP.

**6.2 Desde tu ordenador:**

```bash
nslookup tunombre.me
```

En la parte **Respuesta no autoritativa** (*Non-authoritative answer*) debe aparecer tu IP. En macOS y Linux también puedes usar `dig +short tunombre.me`.

**6.3 Desde todo el mundo:** abre `https://www.whatsmydns.net`, escribe `tunombre.me`, elige el tipo **A** y pulsa **Search**. Poco a poco irán apareciendo ✔ verdes con tu IP en distintos países.

**6.4 La prueba de verdad:** abre en el navegador

- `http://tunombre.me`
- `http://www.tunombre.me`

Las dos deben mostrar **Welcome to nginx!**, el contenedor de prueba de tu VM. Y desde la terminal:

```bash
curl -I http://tunombre.me
```

> **Ojo:** escribe `http://` delante. Muchos navegadores intentan `https://` primero y todavía no tienes certificado. Si te sale un aviso de conexión no segura, es normal: lo resolverás en el apartado 3.2.1.

**6.5 Actualiza tu alias SSH.** En tu ordenador, edita `~/.ssh/config` (dosier 1, paso 4) y cambia la IP por el dominio:

```
Host daw
    HostName tunombre.me
    ...
```

Comprueba que sigue funcionando con `ssh daw 'hostname'`. Si te pide aceptar la huella otra vez (porque ahora el nombre es otro), responde `yes`.

## Paso 7 — Reclamar el certificado SSL (sin activarlo)

El Pack también incluye **un certificado SSL (PositiveSSL) gratis durante 1 año**. Lo vas a **reclamar** ahora, pero **no lo actives**:

> **¿Por qué no activarlo todavía?** Para activarlo hay que generar en el servidor una **clave privada** y una **petición de firma (CSR)**, demostrar que el dominio es tuyo e instalar el certificado en Apache o Nginx. Es justo lo que harás en clase en el apartado 3.2.1. Además, el año de validez empieza a contar cuando se emite.

1. En `https://education.github.com/pack`, en la oferta de **Namecheap**, busca la del **certificado SSL** y sigue su enlace. Inicia sesión con la **misma cuenta de Namecheap** del paso 2.
2. Añade al carrito el **PositiveSSL** que aparece a 0,00 $ y confirma el pedido. **El total tiene que ser 0,00 $.**
3. Comprueba que aparece en tu cuenta: **Account → Dashboard → Product List** (o **SSL Certificates**). Debe verse **PositiveSSL** con el estado **Issue now** / **Activate** / **Not activated**.
4. **No pulses Activate.** Ya está.

> Si al registrar el dominio en el paso 2 ya te apareció el certificado en la cuenta, no hace falta repetir nada: solo compruébalo en el punto 3.

> Si no consigues reclamarlo, no pasa nada: anótalo en la entrega. En el apartado 3.2.1 también usarás **Let's Encrypt**, que es gratuito para todo el mundo.

📸 **E6:** captura del certificado PositiveSSL en tu cuenta, **sin activar**.

---

## Paso 8 — Limpieza

Cuando hayas hecho todas las capturas, borra el contenedor de prueba de la VM:

```bash
ssh daw 'docker rm -f prueba'
```

A partir de ahora, `http://tunombre.me` no responderá hasta que instales tu propio servidor web en el apartado 3.1.1. **Es lo esperado.**
