# Material del taller 3.1.1 (solo para el docente)

Guion: `../3_1_1_handson.md`.

| Carpeta | Qué es | Uso |
|---------|--------|-----|
| `taller/` | Punto de partida: la web (`html/`), una foto de prueba de 1600 × 1000 y las carpetas `nginx/conf.d/` y `nginx/njs/` vacías | Se copia a la VM antes de clase: `scp -r taller daw:~/` |
| `solucion/` | Cómo quedan `compose.yaml` y `nginx/` al terminar el paso 6 | Chuleta o plan B si algo falla en directo: `scp -r solucion/compose.yaml solucion/nginx daw:~/taller/` |

Cambia `tunombre.me` por tu dominio en `solucion/nginx/conf.d/default.conf` antes de usarla.
