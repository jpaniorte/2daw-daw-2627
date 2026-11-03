---
marp: true
theme: a4-print
paginate: false
backgroundColor: white
---

<style>
section { place-content: flex-start !important; padding: 9mm 11mm; }
.cab { display: flex; justify-content: space-between; align-items: baseline; border-bottom: 2px solid #333; padding-bottom: 4px; margin-bottom: 6px; }
.cab h1 { font-size: 16px; margin: 0; }
.cab .cara { font-size: 12px; font-weight: 700; }
.alumno { display: flex; gap: 18px; font-size: 12px; margin-bottom: 4px; }
.alumno span { border-bottom: 1px solid #555; padding-bottom: 2px; }
.alumno .nombre { flex: 1; }
.alumno .grupo { width: 90px; }
.ayuda { font-size: 9.5px; color: #444; margin-bottom: 8px; }
.rejilla { display: grid; grid-template-columns: 1fr 1fr; gap: 14px 12px; }
.bloque { border: 1.5px solid #333; border-radius: 5px; padding: 8px 10px 10px; }
.bloque .num { font-size: 9px; color: #666; float: right; }
.campos { display: flex; align-items: center; gap: 8px; font-size: 12px; margin-bottom: 10px; }
.campos .lbl { font-weight: 700; }
.casillas { display: inline-flex; gap: 2px; }
.casillas i { display: inline-block; width: 20px; height: 24px; border: 1.3px solid #333; }
.fecha { flex: 1; border-bottom: 1px solid #555; height: 14px; font-size: 9px; color: #777; }
.respuestas { display: grid; grid-template-columns: 1fr 1fr; column-gap: 12px; }
.fila { display: flex; align-items: center; gap: 6px; height: 54px; font-size: 13px; }
.fila b { width: 20px; text-align: right; }
.fila span { display: inline-flex; align-items: center; justify-content: center; width: 27px; height: 27px; border: 1.3px solid #333; border-radius: 4px; font-size: 10px; color: #666; }
.prof { margin-top: 8px; border-top: 1px dashed #888; padding-top: 6px; font-size: 11px; display: flex; justify-content: space-between; color: #444; }
.prof .caja { border: 1px solid #888; padding: 1px 6px; }
</style>

<div class="cab"><h1>Digitalización — Hoja de respuestas de las píldoras</h1><span class="cara">Cara 1/2</span></div>
<div class="alumno"><span class="nombre">Nombre y apellidos:</span><span class="grupo">Grupo:</span></div>
<div class="ayuda">Marca con una <strong>X</strong> la casilla elegida. Para corregir, rellena entera la casilla equivocada y marca otra. Antes de empezar, escribe el número de <strong>píldora</strong> y la <strong>versión</strong> que figuran en tu cuadernillo (no escribas en el cuadernillo). Un bloque por control.</div>
<div class="rejilla">
<div class="bloque">
<span class="num">Bloque 1</span>
<div class="campos"><span class="lbl">Píldora</span><span class="casillas"><i></i><i></i></span>
<span class="lbl">Versión</span><span class="casillas"><i></i><i></i></span>
<span class="lbl">Fecha</span><span class="fecha"></span></div>
<div class="respuestas"><div class="fila"><b>1</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>2</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>3</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>4</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>5</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>6</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>7</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>8</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>9</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>10</b><span>A</span><span>B</span><span>C</span><span>D</span></div></div>
<div class="prof"><span>Profesor:</span><span class="caja">Aciertos ____ / 10</span><span class="caja">APTO &nbsp;·&nbsp; NO APTO</span></div>
</div>
<div class="bloque">
<span class="num">Bloque 2</span>
<div class="campos"><span class="lbl">Píldora</span><span class="casillas"><i></i><i></i></span>
<span class="lbl">Versión</span><span class="casillas"><i></i><i></i></span>
<span class="lbl">Fecha</span><span class="fecha"></span></div>
<div class="respuestas"><div class="fila"><b>1</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>2</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>3</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>4</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>5</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>6</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>7</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>8</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>9</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>10</b><span>A</span><span>B</span><span>C</span><span>D</span></div></div>
<div class="prof"><span>Profesor:</span><span class="caja">Aciertos ____ / 10</span><span class="caja">APTO &nbsp;·&nbsp; NO APTO</span></div>
</div>
<div class="bloque">
<span class="num">Bloque 3</span>
<div class="campos"><span class="lbl">Píldora</span><span class="casillas"><i></i><i></i></span>
<span class="lbl">Versión</span><span class="casillas"><i></i><i></i></span>
<span class="lbl">Fecha</span><span class="fecha"></span></div>
<div class="respuestas"><div class="fila"><b>1</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>2</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>3</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>4</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>5</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>6</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>7</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>8</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>9</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>10</b><span>A</span><span>B</span><span>C</span><span>D</span></div></div>
<div class="prof"><span>Profesor:</span><span class="caja">Aciertos ____ / 10</span><span class="caja">APTO &nbsp;·&nbsp; NO APTO</span></div>
</div>
<div class="bloque">
<span class="num">Bloque 4</span>
<div class="campos"><span class="lbl">Píldora</span><span class="casillas"><i></i><i></i></span>
<span class="lbl">Versión</span><span class="casillas"><i></i><i></i></span>
<span class="lbl">Fecha</span><span class="fecha"></span></div>
<div class="respuestas"><div class="fila"><b>1</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>2</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>3</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>4</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>5</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>6</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>7</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>8</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>9</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>10</b><span>A</span><span>B</span><span>C</span><span>D</span></div></div>
<div class="prof"><span>Profesor:</span><span class="caja">Aciertos ____ / 10</span><span class="caja">APTO &nbsp;·&nbsp; NO APTO</span></div>
</div>
</div>

---

<div class="cab"><h1>Digitalización — Hoja de respuestas de las píldoras</h1><span class="cara">Cara 2/2</span></div>
<div class="alumno"><span class="nombre">Nombre y apellidos:</span><span class="grupo">Grupo:</span></div>
<div class="ayuda">Marca con una <strong>X</strong> la casilla elegida. Para corregir, rellena entera la casilla equivocada y marca otra. Antes de empezar, escribe el número de <strong>píldora</strong> y la <strong>versión</strong> que figuran en tu cuadernillo (no escribas en el cuadernillo). Un bloque por control.</div>
<div class="rejilla">
<div class="bloque">
<span class="num">Bloque 5</span>
<div class="campos"><span class="lbl">Píldora</span><span class="casillas"><i></i><i></i></span>
<span class="lbl">Versión</span><span class="casillas"><i></i><i></i></span>
<span class="lbl">Fecha</span><span class="fecha"></span></div>
<div class="respuestas"><div class="fila"><b>1</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>2</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>3</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>4</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>5</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>6</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>7</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>8</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>9</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>10</b><span>A</span><span>B</span><span>C</span><span>D</span></div></div>
<div class="prof"><span>Profesor:</span><span class="caja">Aciertos ____ / 10</span><span class="caja">APTO &nbsp;·&nbsp; NO APTO</span></div>
</div>
<div class="bloque">
<span class="num">Bloque 6</span>
<div class="campos"><span class="lbl">Píldora</span><span class="casillas"><i></i><i></i></span>
<span class="lbl">Versión</span><span class="casillas"><i></i><i></i></span>
<span class="lbl">Fecha</span><span class="fecha"></span></div>
<div class="respuestas"><div class="fila"><b>1</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>2</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>3</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>4</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>5</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>6</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>7</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>8</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>9</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>10</b><span>A</span><span>B</span><span>C</span><span>D</span></div></div>
<div class="prof"><span>Profesor:</span><span class="caja">Aciertos ____ / 10</span><span class="caja">APTO &nbsp;·&nbsp; NO APTO</span></div>
</div>
<div class="bloque">
<span class="num">Bloque 7</span>
<div class="campos"><span class="lbl">Píldora</span><span class="casillas"><i></i><i></i></span>
<span class="lbl">Versión</span><span class="casillas"><i></i><i></i></span>
<span class="lbl">Fecha</span><span class="fecha"></span></div>
<div class="respuestas"><div class="fila"><b>1</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>2</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>3</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>4</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>5</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>6</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>7</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>8</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>9</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>10</b><span>A</span><span>B</span><span>C</span><span>D</span></div></div>
<div class="prof"><span>Profesor:</span><span class="caja">Aciertos ____ / 10</span><span class="caja">APTO &nbsp;·&nbsp; NO APTO</span></div>
</div>
<div class="bloque">
<span class="num">Bloque 8</span>
<div class="campos"><span class="lbl">Píldora</span><span class="casillas"><i></i><i></i></span>
<span class="lbl">Versión</span><span class="casillas"><i></i><i></i></span>
<span class="lbl">Fecha</span><span class="fecha"></span></div>
<div class="respuestas"><div class="fila"><b>1</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>2</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>3</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>4</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>5</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>6</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>7</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>8</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>9</b><span>A</span><span>B</span><span>C</span><span>D</span></div><div class="fila"><b>10</b><span>A</span><span>B</span><span>C</span><span>D</span></div></div>
<div class="prof"><span>Profesor:</span><span class="caja">Aciertos ____ / 10</span><span class="caja">APTO &nbsp;·&nbsp; NO APTO</span></div>
</div>
</div>
