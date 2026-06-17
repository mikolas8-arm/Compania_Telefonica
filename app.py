import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- BASE DE DATOS DE SERVICIOS (Solo lectura para el catálogo) ---
servicios_db = [
    # Móvil
    {"id": 1,  "nombre": "Plan Postpago Max",        "tipo": "Móvil",    "precio": 29.90, "descripcion": "Llamadas ilimitadas + 15 GB"},
    {"id": 2,  "nombre": "Plan Postpago Básico",     "tipo": "Móvil",    "precio": 19.90, "descripcion": "Llamadas ilimitadas + 5 GB"},
    {"id": 3,  "nombre": "Plan Postpago Pro",        "tipo": "Móvil",    "precio": 49.90, "descripcion": "Llamadas ilimitadas + 40 GB + Roaming"},
    {"id": 4,  "nombre": "Plan Prepago Flexible",    "tipo": "Móvil",    "precio": 9.90,  "descripcion": "Recarga y usa cuando quieras"},
    # Hogar
    {"id": 5,  "nombre": "Internet Fibra 200 Mbps",  "tipo": "Hogar",    "precio": 79.90, "descripcion": "Fibra óptica simétrica 200 Mbps"},
    {"id": 6,  "nombre": "Internet Fibra 500 Mbps",  "tipo": "Hogar",    "precio": 99.90, "descripcion": "Fibra óptica simétrica 500 Mbps"},
    {"id": 7,  "nombre": "Dúo Cable + Telefonía",    "tipo": "Hogar",    "precio": 55.00, "descripcion": "TV Cable HD + Línea fija ilimitada"},
    {"id": 8,  "nombre": "Trío Fibra + TV + Fijo",   "tipo": "Hogar",    "precio": 129.90,"descripcion": "Internet 300 Mbps + TV HD + Línea fija"},
    {"id": 9,  "nombre": "TV Cable Básico",          "tipo": "Hogar",    "precio": 39.90, "descripcion": "80 canales HD + 10 canales premium"},
    # Empresas
    {"id": 10, "nombre": "Plan Corporativo Starter", "tipo": "Empresas", "precio": 89.90, "descripcion": "5 líneas móviles + Internet 100 Mbps"},
    {"id": 11, "nombre": "Plan Corporativo Business","tipo": "Empresas", "precio": 159.90,"descripcion": "15 líneas móviles + Internet 300 Mbps"},
    {"id": 12, "nombre": "Internet Dedicado 1 Gbps", "tipo": "Empresas", "precio": 299.90,"descripcion": "Fibra dedicada + SLA 99.9% + Soporte 24/7"},
    {"id": 13, "nombre": "Central Telefónica IP",    "tipo": "Empresas", "precio": 199.90,"descripcion": "50 anexos + llamadas ilimitadas + nube"},
]

PAGINA_WEB = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portal Compañía Telefónica</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }

        body { background-color: #f4f4f6; color: #333; display: flex; flex-direction: column; min-height: 100vh; }

        /* NAVBAR */
        .navbar { background-color: #ffffff; border-bottom: 1px solid #e0e0e0; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .nav-contenedor { max-width: 1300px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; padding: 0 20px; height: 60px; }
        .logo { font-size: 22px; font-weight: bold; color: #da291c; letter-spacing: -0.5px; }


        .contenedor-principal { flex: 1; display: flex; justify-content: center; align-items: center; padding: 20px; }

        /* LOGIN */
        .acceso-sesion { background: #ffffff; padding: 40px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center; }
        .acceso-sesion h2 { color: #111; margin-bottom: 8px; font-size: 24px; }
        .acceso-sesion p { color: #666; font-size: 14px; margin-bottom: 24px; }
        .grupo-entrada { margin-bottom: 20px; text-align: left; }
        .grupo-entrada label { display: block; margin-bottom: 6px; font-size: 14px; font-weight: 600; color: #444; }
        .grupo-entrada input, .grupo-entrada select { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 4px; font-size: 15px; }
        .mensaje-alerta { min-height: 20px; font-size: 14px; font-weight: 500; margin-bottom: 15px; }

        /* PANEL PRINCIPAL */
        .panel-wrapper { width: 100%; max-width: 1300px; }
        .encabezado-panel { background: #ffffff; padding: 20px 30px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .encabezado-panel h1 { font-size: 22px; }
        .encabezado-panel p { color: #666; font-size: 14px; margin-top: 4px; }

        /* LAYOUT CATÁLOGO + CARRITO */
        .layout-catalogo-carrito { display: grid; grid-template-columns: 1fr 340px; gap: 20px; align-items: start; }

        /* CATÁLOGO */
        .catalogo-box { background: #ffffff; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); padding: 25px; }
        .catalogo-box h3 { font-size: 18px; margin-bottom: 5px; }
        .catalogo-box .subtitulo { color: #666; font-size: 13px; margin-bottom: 18px; }

        .filtros { display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }
        .filtro-btn { background: #f4f4f6; color: #555; border: 1px solid #ddd; padding: 7px 16px; font-size: 13px; font-weight: 600; border-radius: 20px; cursor: pointer; transition: all 0.2s; }
        .filtro-btn:hover { background: #da291c; color: #fff; border-color: #da291c; }
        .filtro-btn.activo { background: #da291c; color: #fff; border-color: #da291c; }

        .grid-servicios { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 14px; }

        .tarjeta-servicio { border: 1.5px solid #e8e8e8; border-radius: 8px; padding: 18px; transition: all 0.2s; cursor: pointer; position: relative; background: #fff; }
        .tarjeta-servicio:hover { border-color: #da291c; box-shadow: 0 4px 12px rgba(218,41,28,0.12); transform: translateY(-2px); }
        .tarjeta-servicio.en-carrito { border-color: #28a745; background: #f6fff8; }

        .tag-tipo { display: inline-block; font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 12px; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px; }
        .tag-Móvil { background: #fff3cd; color: #856404; }
        .tag-Hogar { background: #cfe2ff; color: #084298; }
        .tag-Empresas { background: #f8d7da; color: #842029; }

        .tarjeta-servicio h4 { font-size: 15px; font-weight: 700; margin-bottom: 6px; color: #111; }
        .tarjeta-servicio .descripcion { font-size: 12px; color: #777; margin-bottom: 14px; line-height: 1.4; }
        .tarjeta-servicio .precio-grande { font-size: 22px; font-weight: 800; color: #da291c; }
        .tarjeta-servicio .precio-grande span { font-size: 13px; font-weight: 500; color: #888; }

        .btn-agregar-carrito { width: 100%; margin-top: 14px; background: #da291c; color: #fff; border: none; padding: 10px; font-size: 13px; font-weight: 700; border-radius: 4px; cursor: pointer; transition: background 0.2s; }
        .btn-agregar-carrito:hover { background: #b51f15; }
        .btn-agregar-carrito.agregado { background: #28a745; }
        .btn-agregar-carrito.agregado:hover { background: #218838; }

        /* CARRITO */
        .carrito-box { background: #ffffff; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); padding: 25px; position: sticky; top: 20px; }
        .carrito-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px; border-bottom: 2px solid #f4f4f6; padding-bottom: 14px; }
        .carrito-header h3 { font-size: 18px; }
        .badge-carrito { background: #da291c; color: #fff; border-radius: 50%; width: 24px; height: 24px; font-size: 13px; font-weight: 700; display: flex; align-items: center; justify-content: center; }

        .carrito-vacio { text-align: center; padding: 30px 10px; color: #aaa; font-size: 13px; }
        .carrito-vacio .icono-vacio { font-size: 40px; margin-bottom: 10px; }

        .lista-carrito { list-style: none; }
        .item-carrito { display: flex; justify-content: space-between; align-items: flex-start; padding: 12px 0; border-bottom: 1px solid #f0f0f0; gap: 10px; }
        .item-carrito:last-child { border-bottom: none; }
        .item-info { flex: 1; }
        .item-nombre { font-size: 13px; font-weight: 700; color: #222; }
        .item-tipo { font-size: 11px; color: #999; margin-top: 2px; }
        .item-precio { font-size: 14px; font-weight: 700; color: #da291c; white-space: nowrap; }

        .btn-quitar { background: none; border: none; color: #ccc; font-size: 18px; cursor: pointer; padding: 0 2px; line-height: 1; transition: color 0.2s; }
        .btn-quitar:hover { background: none; color: #da291c; }

        .carrito-total { border-top: 2px solid #da291c; margin-top: 15px; padding-top: 14px; }
        .fila-total { display: flex; justify-content: space-between; align-items: center; }
        .fila-total .label-total { font-size: 16px; font-weight: 700; }
        .fila-total .monto-total { font-size: 22px; font-weight: 800; color: #da291c; }
        .fila-total .igv-nota { font-size: 11px; color: #999; margin-top: 3px; }

        .btn-contratar { width: 100%; margin-top: 16px; background: #da291c; color: #fff; border: none; padding: 13px; font-size: 15px; font-weight: 700; border-radius: 4px; cursor: pointer; transition: background 0.2s; }
        .btn-contratar:hover { background: #b51f15; }
        .btn-contratar:disabled { background: #ccc; cursor: not-allowed; }

        /* BOTONES GENERALES */
        button { transition: background 0.2s; }
        .boton-Salir { background-color: #555; color: #fff; border: none; padding: 10px 15px; font-size: 14px; font-weight: bold; border-radius: 4px; cursor: pointer; }
        .boton-Salir:hover { background-color: #333; }
        .btn-login { background-color: #da291c; color: white; border: none; padding: 12px; font-size: 15px; font-weight: bold; border-radius: 4px; cursor: pointer; width: 100%; }
        .btn-login:hover { background-color: #b51f15; }
    </style>
</head>
<body>
    <header class="navbar">
        <div class="nav-contenedor">
            <div class="logo">COMPAÑÍA TELEFÓNICA</div>

        </div>
    </header>

    <main class="contenedor-principal">
        <!-- LOGIN -->
        <div class="acceso-sesion" id="acceso-sesion">
            <h2>Portal Corporativo</h2>
            <p>Ingresa tus credenciales para explorar el catálogo</p>
            <div class="grupo-entrada">
                <label>Usuario o Correo</label>
                <input type="text" id="usuario" placeholder="Completar usuario/correo">
            </div>
            <div class="grupo-entrada">
                <label>Contraseña</label>
                <input type="password" id="contraseña" placeholder="••••••••" onkeydown="if(event.key==='Enter') validarAcceso()">
            </div>
            <div id="mensaje" class="mensaje-alerta"></div>
            <button class="btn-login" onclick="validarAcceso()">Ingresar</button>
        </div>

        <!-- PANEL PRINCIPAL -->
        <div class="panel-wrapper" id="seccionBienvenida" style="display:none;">
            <div class="encabezado-panel">
                <div>
                    <h1>¡Bienvenido al Catálogo!</h1>
                    <p>Selecciona los servicios que deseas contratar y agrégalos a tu carrito.</p>
                </div>
                <button class="boton-Salir" onclick="cerrarSesion()">Cerrar Sesión</button>
            </div>

            <div class="layout-catalogo-carrito">
                <!-- CATÁLOGO -->
                <div class="catalogo-box">
                    <h3>Servicios Disponibles</h3>
                    <p class="subtitulo">Haz clic en un servicio para agregarlo a tu carrito.</p>
                    <div class="filtros">
                        <button class="filtro-btn activo" onclick="filtrar('Todos', this)">Todos</button>
                        <button class="filtro-btn" onclick="filtrar('Móvil', this)">📱 Móvil</button>
                        <button class="filtro-btn" onclick="filtrar('Hogar', this)">🏠 Hogar</button>
                        <button class="filtro-btn" onclick="filtrar('Empresas', this)">🏢 Empresas</button>
                    </div>
                    <div class="grid-servicios" id="grid-servicios"></div>
                </div>

                <!-- CARRITO -->
                <div class="carrito-box">
                    <div class="carrito-header">
                        <h3>🛒 Mi Carrito</h3>
                        <div class="badge-carrito" id="badge-count">0</div>
                    </div>
                    <div id="carrito-contenido">
                        <div class="carrito-vacio">
                            <div class="icono-vacio">🛒</div>
                            <p>Tu carrito está vacío.<br>Agrega servicios del catálogo.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <script>
        let todosLosServicios = [];
        let carrito = [];
        let filtroActual = 'Todos';

        /* AUTH */
        function validarAcceso() {
            const usuario = document.getElementById('usuario').value.trim();
            const contrasena = document.getElementById('contraseña').value;
            const caja = document.getElementById('mensaje');

            fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ usuario, contrasena })
            })
            .then(r => r.json())
            .then(data => {
                if (data.valido) {
                    caja.style.color = '#28a745';
                    caja.textContent = data.mensaje;
                    setTimeout(() => {
                        document.getElementById('acceso-sesion').style.display = 'none';
                        document.getElementById('seccionBienvenida').style.display = 'block';
                        cargarServicios();
                    }, 900);
                } else {
                    caja.style.color = '#da291c';
                    caja.textContent = data.mensaje;
                }
            });
        }

        function cerrarSesion() {
            document.getElementById('usuario').value = '';
            document.getElementById('contraseña').value = '';
            document.getElementById('mensaje').textContent = '';
            document.getElementById('acceso-sesion').style.display = 'block';
            document.getElementById('seccionBienvenida').style.display = 'none';
            carrito = [];
            todosLosServicios = [];
        }

        /* CATÁLOGO */
        function cargarServicios() {
            fetch('/servicios')
            .then(r => r.json())
            .then(data => {
                todosLosServicios = data;
                renderGrid(data);
            });
        }

        function filtrar(tipo, btn) {
            filtroActual = tipo;
            document.querySelectorAll('.filtro-btn').forEach(b => b.classList.remove('activo'));
            btn.classList.add('activo');
            const lista = tipo === 'Todos' ? todosLosServicios : todosLosServicios.filter(s => s.tipo === tipo);
            renderGrid(lista);
        }

        function renderGrid(lista) {
            const grid = document.getElementById('grid-servicios');
            grid.innerHTML = '';
            lista.forEach(srv => {
                const enCarrito = carrito.some(c => c.id === srv.id);
                grid.innerHTML += `
                    <div class="tarjeta-servicio ${enCarrito ? 'en-carrito' : ''}" id="card-${srv.id}">
                        <span class="tag-tipo tag-${srv.tipo}">${srv.tipo}</span>
                        <h4>${srv.nombre}</h4>
                        <p class="descripcion">${srv.descripcion}</p>
                        <div class="precio-grande">S/. ${srv.precio.toFixed(2)} <span>/ mes</span></div>
                        <button class="btn-agregar-carrito ${enCarrito ? 'agregado' : ''}" onclick="toggleCarrito(${srv.id})">
                            ${enCarrito ? '✓ Agregado' : '+ Agregar al carrito'}
                        </button>
                    </div>
                `;
            });
        }

        /* CARRITO */
        function toggleCarrito(id) {
            const idx = carrito.findIndex(c => c.id === id);
            if (idx === -1) {
                const srv = todosLosServicios.find(s => s.id === id);
                if (srv) carrito.push(srv);
            } else {
                carrito.splice(idx, 1);
            }
            // Re-render solo el grid filtrado y el carrito
            const lista = filtroActual === 'Todos' ? todosLosServicios : todosLosServicios.filter(s => s.tipo === filtroActual);
            renderGrid(lista);
            renderCarrito();
        }

        function quitarDelCarrito(id) {
            carrito = carrito.filter(c => c.id !== id);
            const lista = filtroActual === 'Todos' ? todosLosServicios : todosLosServicios.filter(s => s.tipo === filtroActual);
            renderGrid(lista);
            renderCarrito();
        }

        function renderCarrito() {
            const cont = document.getElementById('carrito-contenido');
            document.getElementById('badge-count').textContent = carrito.length;

            if (carrito.length === 0) {
                cont.innerHTML = `
                    <div class="carrito-vacio">
                        <div class="icono-vacio">🛒</div>
                        <p>Tu carrito está vacío.<br>Agrega servicios del catálogo.</p>
                    </div>`;
                return;
            }

            const total = carrito.reduce((acc, s) => acc + s.precio, 0);

            let html = '<ul class="lista-carrito">';
            carrito.forEach(srv => {
                html += `
                    <li class="item-carrito">
                        <div class="item-info">
                            <div class="item-nombre">${srv.nombre}</div>
                            <div class="item-tipo">${srv.tipo}</div>
                        </div>
                        <div style="display:flex;align-items:center;gap:8px;">
                            <div class="item-precio">S/. ${srv.precio.toFixed(2)}</div>
                            <button class="btn-quitar" onclick="quitarDelCarrito(${srv.id})" title="Quitar">✕</button>
                        </div>
                    </li>`;
            });
            html += '</ul>';

            html += `
                <div class="carrito-total">
                    <div class="fila-total">
                        <span class="label-total">Total mensual</span>
                        <span class="monto-total">S/. ${total.toFixed(2)}</span>
                    </div>
                    <div class="igv-nota">Incluye IGV · Facturación mensual</div>
                </div>
                <button class="btn-contratar" onclick="contratar()">Contratar ahora →</button>`;

            cont.innerHTML = html;
        }

        function contratar() {
            const nombres = carrito.map(s => '• ' + s.nombre).join('\\n');
            alert('¡Gracias por tu interés!\\n\\nHas seleccionado:\\n' + nombres + '\\n\\nUn asesor se pondrá en contacto contigo para finalizar la contratación.');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def inicio():
    return render_template_string(PAGINA_WEB)

@app.route('/login', methods=['POST'])
def verificar_credenciales():
    datos = request.get_json()
    if datos.get('usuario') == "Mikolas" and datos.get('contrasena') == "upn1234":
        return jsonify({"valido": True, "mensaje": "¡Ingreso correcto! Cargando catálogo..."})
    return jsonify({"valido": False, "mensaje": "Usuario o contraseña incorrectos."})

@app.route('/servicios', methods=['GET'])
def listar_servicios():
    return jsonify(servicios_db)

if __name__ == '__main__':
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=puerto, debug=False)
