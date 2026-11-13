---
marp: true
theme: default
paginate: true
backgroundColor: white
footer: 'Despliegue de Aplicaciones Web (0614) · UD3: Servidores web'
layout: default
title: "Servidores Web — Bloque 3.1.1: Nginx (Presentación)"
permalink: /servidores-web/semana-1/presentacion/
---

<!-- _class: lead -->
# servidores web
## 3.1.1 · Instalación y configuración básica de Nginx

---

## Hoy

| Qué | Tiempo |
|-----|--------|
| **Lo importante**, en estas diapositivas | 15 min |
| **Taller:** lo hago yo en directo, en mi VM | 15–20 min |
| **Práctica:** lo hacéis vosotros, en vuestra VM, con evidencias | resto de la clase |

Al final de la clase: **`http://tunombre.me` servido por tu Nginx**, con módulos cargados y sabiendo leer sus logs.

---

## En el restaurante: montamos la barra

| Restaurante | Servidor web |
|-------------|--------------|
| El local alquilado | Tu **VM** de Azure |
| La barra | **Nginx** |
| Los electrodomésticos que se enchufan | Los **módulos** |
| El libro de comandas | El **log de acceso** |
| El parte de incidencias | El **log de errores** |
| El camarero sin llave de un armario | Un **403** |

---

## Apache y Nginx

| | Apache | Nginx |
|--|--------|-------|
| Nace | 1995 | 2004, para atender **10 000 conexiones** a la vez |
| Cómo trabaja | Un proceso o hilo por conexión (**MPM**) | Un maestro + pocos *workers* con **eventos** |
| Su punto fuerte | Módulos y `.htaccess` (alojamiento compartido) | Estático, **proxy inverso**, mucha concurrencia |

**En el curso usamos Nginx:** es el más usado y el que está casi siempre **delante de las aplicaciones**. Con Apache, las ideas son las mismas; solo cambian los nombres.

---

## Nginx en Docker

```bash
docker run -d --name web -p 80:80 nginx:1.30
```

- **No hay systemd:** Nginx es el **proceso principal** del contenedor (`nginx -g 'daemon off;'`). Si muere, el contenedor se para.
- El **maestro** corre como `root` (abre el puerto 80); los **workers**, como el usuario `nginx`.

**Un puerto, cuatro capas** (todas abiertas o no llega nada):

```
navegador ─▶ NSG de Azure ─▶ docker -p 80:80 ─▶ listen 80;
             (22, 80, 443)    host:contenedor
```

---

## Dónde está la configuración

```
/etc/nginx/
├── nginx.conf          ← global: incluye conf.d/*.conf
├── conf.d/default.conf ← el sitio
└── modules/            ← módulos dinámicos (.so)
/usr/share/nginx/html/  ← la web
```

```nginx
server {
    listen 80;
    server_name tunombre.me;
    root  /usr/share/nginx/html;
    index index.html;
}
```

Directivas terminadas en **`;`**, dentro de bloques que se anidan:
`main` → `events` / `http` → `server` → `location`. Lo de fuera **se hereda** dentro.

---

## Cambiar sin romper nada

```
editar ─▶ nginx -t ─▶ nginx -s reload ─▶ curl ─▶ docker logs
```

| | `nginx -s reload` | `docker restart` |
|--|-------------------|------------------|
| Conexiones en curso | Terminan bien | Se cortan |
| Configuración rota | **La rechaza** y sigue con la anterior | **No arranca:** web caída |

⚠️ Una configuración rota que nadie comprobó **tumba la web en el siguiente reinicio**, quizá horas después.

---

## Módulos: ampliar Nginx

| Estáticos | Dinámicos |
|-----------|-----------|
| Dentro del binario (`nginx -V`) | Ficheros `.so` en `/etc/nginx/modules` |
| Siempre disponibles | Se cargan con **`load_module`** |

```nginx
load_module modules/ngx_http_image_filter_module.so;   # al principio de nginx.conf
```

**Ya vienen en la imagen:** `image_filter` (miniaturas), `njs` (JavaScript), `acme` (Let's Encrypt), `geoip`, `xslt`.
**De terceros, muy usados:** brotli, headers-more, ModSecurity (WAF), lua…

⚠️ Un `.so` tiene que ser **de la misma versión** de Nginx.

---

## Logs: el libro de comandas

```bash
docker logs -f web                  # en directo
docker logs web 2>&1 >/dev/null     # solo errores
```

```
81.45.12.200 - - [12/Nov/2026:10:15:32 +0100] "GET /index.html HTTP/1.1" 200 10958 "-" "Mozilla/5.0 ..."
   IP cliente           fecha y hora                petición           código  bytes  referer  user-agent
```

En cuanto abras el puerto 80 verás **bots** pidiendo `/wp-login.php`, `/.env`, `/phpmyadmin/`… Que les dé **404** es buena señal.

---

## 403, 404 y seguridad mínima

| Respuesta | Causa habitual | Lo dice el log de errores |
|-----------|----------------|---------------------------|
| **404** | El fichero no existe | `(2: No such file or directory)` |
| **403** | El usuario `nginx` no puede leer el fichero | `(13: Permission denied)` |
| **403** | Carpeta sin `index.html` | `directory index of … is forbidden` |

**Seguridad mínima:**
- `server_tokens off;` → `Server: nginx` en vez de `Server: nginx/1.30.6`
- `autoindex on;` **solo** donde quieras listar ficheros

---

## Lo que tienes que llevarte

1. Nginx en Docker: **proceso principal**, puertos en **cuatro capas**.
2. `nginx.conf` + `conf.d/`, **bloques** anidados y directivas con **`;`**.
3. **`nginx -t` antes de `reload`**, siempre.
4. Módulos **dinámicos** con `load_module`, de la **misma versión**.
5. **Logs:** acceso (qué ha pasado) y errores (por qué ha fallado).
6. **403** = permisos o carpeta sin índice. **`server_tokens off`**.

---

<!-- _class: lead -->
# Al taller
## `ssh daw`
