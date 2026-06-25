import os
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- BASE DE DATOS DE PRODUCTOS (Solo lectura para el catálogo) ---
productos_db = [
    # Bebidas
    {"id": 1,  "nombre": "Agua San Luis 625ml",       "tipo": "Bebidas",   "precio": 1.00,  "descripcion": "Agua mineral sin gas, tamaño personal"},
    {"id": 2,  "nombre": "Agua San Luis 1.5L",         "tipo": "Bebidas",   "precio": 2.00,  "descripcion": "Agua mineral sin gas, tamaño familiar"},
    {"id": 3,  "nombre": "Coca Cola 500ml",             "tipo": "Bebidas",   "precio": 2.50,  "descripcion": "La clásica Coca Cola bien fría"},
    {"id": 4,  "nombre": "Coca Cola 1.5L",              "tipo": "Bebidas",   "precio": 5.00,  "descripcion": "Coca Cola tamaño familiar"},
    {"id": 5,  "nombre": "Inka Cola 500ml",             "tipo": "Bebidas",   "precio": 2.50,  "descripcion": "La bebida de sabor nacional"},
    {"id": 6,  "nombre": "Inka Cola 1.5L",              "tipo": "Bebidas",   "precio": 5.00,  "descripcion": "Inka Cola tamaño familiar"},
    {"id": 7,  "nombre": "Guaraná 500ml",               "tipo": "Bebidas",   "precio": 2.50,  "descripcion": "Guaraná con sabor a frutas tropicales"},
    {"id": 8,  "nombre": "Sprite 500ml",                "tipo": "Bebidas",   "precio": 2.50,  "descripcion": "Sprite lima-limón bien helada"},
    # Snacks
    {"id": 9,  "nombre": "Papas Lays Clásicas",        "tipo": "Snacks",    "precio": 2.00,  "descripcion": "Bolsa mediana de papas fritas saladas"},
    {"id": 10, "nombre": "Papas Lays Queso",            "tipo": "Snacks",    "precio": 2.00,  "descripcion": "Papas fritas con sabor a queso"},
    {"id": 11, "nombre": "Piqueo 3 Ositos",             "tipo": "Snacks",    "precio": 3.50,  "descripcion": "Mix de maíz, habas y camote frito"},
    {"id": 12, "nombre": "Inkachips Natural",            "tipo": "Snacks",    "precio": 2.50,  "descripcion": "Chips de camote al natural, sin gluten"},
    {"id": 13, "nombre": "Inkachips BBQ",                "tipo": "Snacks",    "precio": 2.50,  "descripcion": "Chips de camote sabor BBQ"},
    # Galletas
    {"id": 14, "nombre": "Galletas Oreo",               "tipo": "Galletas",  "precio": 1.50,  "descripcion": "Pack de galletas Oreo rellenas de crema"},
    {"id": 15, "nombre": "Galletas Vainilla Field",     "tipo": "Galletas",  "precio": 2.00,  "descripcion": "Galletas de vainilla crujientes"},
    {"id": 16, "nombre": "Galletas Casino Chocolate",   "tipo": "Galletas",  "precio": 1.80,  "descripcion": "Galletas sándwich de chocolate Casino"},
    {"id": 17, "nombre": "Galletas Morochas",            "tipo": "Galletas",  "precio": 1.50,  "descripcion": "Galletas de chocolate clásicas peruanas"},
    # Caramelos
    {"id": 18, "nombre": "Caramelos Halls Menta",       "tipo": "Caramelos", "precio": 0.50,  "descripcion": "Caramelos de menta refrescante, unidad"},
    {"id": 19, "nombre": "Caramelos Halls Cereza",      "tipo": "Caramelos", "precio": 0.50,  "descripcion": "Caramelos de cereza y mentol, unidad"},
    {"id": 20, "nombre": "Chupetín Bonobon",             "tipo": "Caramelos", "precio": 0.50,  "descripcion": "Chupetín relleno de crema de maní"},
    {"id": 21, "nombre": "Chicles Trident Menta",       "tipo": "Caramelos", "precio": 1.00,  "descripcion": "Pack de chicles sin azúcar sabor menta"},
    {"id": 22, "nombre": "Caramelos Surtidos x10",      "tipo": "Caramelos", "precio": 1.00,  "descripcion": "Bolsita surtida de caramelos varios"},
    # Otros
    {"id": 23, "nombre": "Detergente Ace Bolsa 500g",   "tipo": "Otros",     "precio": 3.50,  "descripcion": "Detergente en polvo para ropa blanca y color"},
    {"id": 24, "nombre": "Jabón Bolívar 180g",           "tipo": "Otros",     "precio": 2.00,  "descripcion": "Jabón de tocador clásico"},
    {"id": 25, "nombre": "Papel Higiénico Elite x4",    "tipo": "Otros",     "precio": 5.50,  "descripcion": "Pack de 4 rollos doble hoja"},
    {"id": 26, "nombre": "Fósforos Nacional",            "tipo": "Otros",     "precio": 0.50,  "descripcion": "Cajita de fósforos de 50 unidades"},
    {"id": 27, "nombre": "Vela de Cera Blanca",          "tipo": "Otros",     "precio": 1.00,  "descripcion": "Vela blanca para uso doméstico"},
]

PAGINA_WEB = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bodega El Gringo</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }

        body { background-color: #f4f4f6; color: #333; display: flex; flex-direction: column; min-height: 100vh; }

        /* NAVBAR */
        .navbar { background-color: #ffffff; border-bottom: 1px solid #e0e0e0; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .nav-contenedor { max-width: 1300px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; padding: 0 20px; height: 60px; }
        .logo { font-size: 22px; font-weight: bold; color: #2e7d32; letter-spacing: -0.5px; }
        .navbar nav ul { display: flex; list-style: none; height: 100%; }
        .navbar nav ul li { padding: 19px 15px; font-size: 14px; font-weight: 600; color: #555; cursor: pointer; transition: all 0.3s ease; }
        .navbar nav ul li.activo { background-color: #2e7d32; color: #ffffff; }
        .navbar nav ul li:hover:not(.activo) { background-color: #f4f4f6; }

        .contenedor-principal { flex: 1; display: flex; justify-content: center; padding: 30px 20px; }

        .vista { width: 100%; max-width: 1300px; display: none; }
        .vista.visible { display: block; }

        /* LOGIN */
        .login-wrapper { display: flex; justify-content: center; align-items: flex-start; padding-top: 20px; }
        .acceso-sesion { background: #ffffff; padding: 40px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 100%; max-width: 420px; text-align: center; }
        .acceso-sesion h2 { color: #111; margin-bottom: 8px; font-size: 24px; }
        .acceso-sesion p { color: #666; font-size: 14px; margin-bottom: 24px; }
        .grupo-entrada { margin-bottom: 18px; text-align: left; }
        .grupo-entrada label { display: block; margin-bottom: 6px; font-size: 14px; font-weight: 600; color: #444; }
        .grupo-entrada input, .grupo-entrada select { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 4px; font-size: 15px; }
        .mensaje-alerta { min-height: 20px; font-size: 14px; font-weight: 500; margin-bottom: 15px; }

        /* CUENTA (cuando ya inició sesión) */
        .cuenta-box { background: #ffffff; padding: 40px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 100%; max-width: 420px; text-align: center; margin: 0 auto; }
        .cuenta-box .avatar-circulo { width: 70px; height: 70px; border-radius: 50%; background: #2e7d32; color: #fff; font-size: 28px; font-weight: 800; display: flex; align-items: center; justify-content: center; margin: 0 auto 18px; }
        .cuenta-box h2 { font-size: 20px; margin-bottom: 6px; }
        .cuenta-box .dato-cuenta { text-align: left; background: #f8f8f9; padding: 10px 14px; border-radius: 6px; margin-bottom: 10px; font-size: 13px; }
        .cuenta-box .dato-cuenta b { color: #444; }

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
        .filtro-btn:hover { background: #2e7d32; color: #fff; border-color: #2e7d32; }
        .filtro-btn.activo { background: #2e7d32; color: #fff; border-color: #2e7d32; }

        .grid-servicios { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 14px; }

        .tarjeta-servicio { border: 1.5px solid #e8e8e8; border-radius: 8px; padding: 18px; transition: all 0.2s; cursor: pointer; position: relative; background: #fff; }
        .tarjeta-servicio:hover { border-color: #2e7d32; box-shadow: 0 4px 12px rgba(46,125,50,0.12); transform: translateY(-2px); }
        .tarjeta-servicio.en-carrito { border-color: #28a745; background: #f6fff8; }

        .tag-tipo { display: inline-block; font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 12px; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px; }
        .tag-Bebidas   { background: #cfe2ff; color: #084298; }
        .tag-Snacks    { background: #fff3cd; color: #856404; }
        .tag-Galletas  { background: #f8d7da; color: #842029; }
        .tag-Caramelos { background: #fce4ec; color: #880e4f; }
        .tag-Otros     { background: #e8f5e9; color: #1b5e20; }

        .tarjeta-servicio h4 { font-size: 15px; font-weight: 700; margin-bottom: 6px; color: #111; }
        .tarjeta-servicio .descripcion { font-size: 12px; color: #777; margin-bottom: 14px; line-height: 1.4; }
        .tarjeta-servicio .precio-grande { font-size: 22px; font-weight: 800; color: #2e7d32; }
        .tarjeta-servicio .precio-grande span { font-size: 13px; font-weight: 500; color: #888; }

        .btn-agregar-carrito { width: 100%; margin-top: 14px; background: #2e7d32; color: #fff; border: none; padding: 10px; font-size: 13px; font-weight: 700; border-radius: 4px; cursor: pointer; transition: background 0.2s; }
        .btn-agregar-carrito:hover { background: #1b5e20; }
        .btn-agregar-carrito.agregado { background: #28a745; }
        .btn-agregar-carrito.agregado:hover { background: #218838; }

        /* CARRITO */
        .carrito-box { background: #ffffff; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); padding: 25px; position: sticky; top: 20px; }
        .carrito-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px; border-bottom: 2px solid #f4f4f6; padding-bottom: 14px; }
        .carrito-header h3 { font-size: 18px; }
        .badge-carrito { background: #2e7d32; color: #fff; border-radius: 50%; width: 24px; height: 24px; font-size: 13px; font-weight: 700; display: flex; align-items: center; justify-content: center; }

        .carrito-vacio { text-align: center; padding: 30px 10px; color: #aaa; font-size: 13px; }
        .carrito-vacio .icono-vacio { font-size: 40px; margin-bottom: 10px; }

        .lista-carrito { list-style: none; }
        .item-carrito { display: flex; justify-content: space-between; align-items: flex-start; padding: 12px 0; border-bottom: 1px solid #f0f0f0; gap: 10px; }
        .item-carrito:last-child { border-bottom: none; }
        .item-info { flex: 1; }
        .item-nombre { font-size: 13px; font-weight: 700; color: #222; }
        .item-tipo { font-size: 11px; color: #999; margin-top: 2px; }
        .item-precio { font-size: 14px; font-weight: 700; color: #2e7d32; white-space: nowrap; }

        .btn-quitar { background: none; border: none; color: #ccc; font-size: 18px; cursor: pointer; padding: 0 2px; line-height: 1; transition: color 0.2s; }
        .btn-quitar:hover { background: none; color: #2e7d32; }

        .carrito-total { border-top: 2px solid #2e7d32; margin-top: 15px; padding-top: 14px; }
        .fila-total { display: flex; justify-content: space-between; align-items: center; }
        .fila-total .label-total { font-size: 16px; font-weight: 700; }
        .fila-total .monto-total { font-size: 22px; font-weight: 800; color: #2e7d32; }
        .fila-total .igv-nota { font-size: 11px; color: #999; margin-top: 3px; }

        .btn-contratar { width: 100%; margin-top: 16px; background: #2e7d32; color: #fff; border: none; padding: 13px; font-size: 15px; font-weight: 700; border-radius: 4px; cursor: pointer; transition: background 0.2s; }
        .btn-contratar:hover { background: #1b5e20; }
        .btn-contratar:disabled { background: #ccc; cursor: not-allowed; }

        /* CONTACTO */
        .contacto-box { background: #ffffff; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); padding: 35px; max-width: 600px; margin: 0 auto; }
        .contacto-box h2 { font-size: 22px; margin-bottom: 8px; }
        .contacto-box > p.subtitulo { color: #666; font-size: 14px; margin-bottom: 26px; }
        .item-contacto { display: flex; align-items: flex-start; gap: 16px; padding: 16px 0; border-bottom: 1px solid #f0f0f0; }
        .item-contacto:last-child { border-bottom: none; }
        .item-contacto .icono { font-size: 26px; width: 44px; height: 44px; background: #e8f5e9; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
        .item-contacto .texto-contacto .titulo-contacto { font-size: 13px; font-weight: 700; color: #888; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
        .item-contacto .texto-contacto .valor-contacto { font-size: 16px; font-weight: 600; color: #222; }

        /* BOTONES GENERALES */
        button { transition: background 0.2s; }
        .boton-Salir { background-color: #555; color: #fff; border: none; padding: 10px 15px; font-size: 14px; font-weight: bold; border-radius: 4px; cursor: pointer; }
        .boton-Salir:hover { background-color: #333; }
        .btn-login { background-color: #2e7d32; color: white; border: none; padding: 12px; font-size: 15px; font-weight: bold; border-radius: 4px; cursor: pointer; width: 100%; }
        .btn-login:hover { background-color: #1b5e20; }

        /* MODAL DE PAGO */
        .modal-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.5); align-items: center; justify-content: center; z-index: 1000; padding: 20px; }
        .modal-overlay.visible { display: flex; }
        .modal-pago { background: #fff; border-radius: 8px; width: 100%; max-width: 440px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.25); }
        .modal-pago h2 { font-size: 20px; margin-bottom: 4px; }
        .modal-pago p.subtitulo { color: #666; font-size: 13px; margin-bottom: 20px; }
        .resumen-pago { background: #f8f8f9; border-radius: 6px; padding: 14px 16px; margin-bottom: 20px; }
        .resumen-pago .fila-resumen { display: flex; justify-content: space-between; font-size: 13px; color: #555; padding: 3px 0; }
        .resumen-pago .fila-resumen.total-resumen { border-top: 1px solid #ddd; margin-top: 8px; padding-top: 8px; font-weight: 700; color: #111; font-size: 15px; }
        .opciones-pago { display: flex; flex-direction: column; gap: 10px; margin-bottom: 22px; }
        .opcion-pago { display: flex; align-items: center; gap: 10px; border: 1.5px solid #e0e0e0; border-radius: 6px; padding: 12px 14px; cursor: pointer; font-size: 14px; font-weight: 600; color: #444; }
        .opcion-pago:has(input:checked) { border-color: #2e7d32; background: #e8f5e9; color: #2e7d32; }
        .opcion-pago input { accent-color: #2e7d32; }
        .modal-botones { display: flex; gap: 10px; }
        .modal-botones button { flex: 1; padding: 12px; border-radius: 4px; font-size: 14px; font-weight: 700; border: none; cursor: pointer; }
        .btn-cancelar-pago { background: #eee; color: #555; }
        .btn-cancelar-pago:hover { background: #ddd; }
        .btn-confirmar-pago { background: #2e7d32; color: #fff; }
        .btn-confirmar-pago:hover { background: #1b5e20; }

        /* MODAL DE CONFIRMACIÓN */
        .modal-confirmacion { background: #fff; border-radius: 8px; width: 100%; max-width: 420px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.25); text-align: left; }
        .modal-confirmacion .icono-exito { width: 54px; height: 54px; border-radius: 50%; background: #e6f7ec; color: #28a745; font-size: 28px; display: flex; align-items: center; justify-content: center; margin-bottom: 16px; }
        .modal-confirmacion h2 { font-size: 20px; margin-bottom: 4px; }
        .modal-confirmacion p.subtitulo { color: #666; font-size: 13px; margin-bottom: 18px; }
        .resumen-confirmacion { background: #f8f8f9; border-radius: 6px; padding: 14px 16px; margin-bottom: 16px; }
        .resumen-confirmacion .fila-resumen { display: flex; justify-content: space-between; font-size: 13px; color: #555; padding: 3px 0; }
        .resumen-confirmacion .fila-metodo { font-size: 13px; color: #444; margin-top: 10px; padding-top: 10px; border-top: 1px solid #ddd; }
        .resumen-confirmacion .fila-metodo b { color: #111; }
        .nota-confirmacion { font-size: 13px; color: #666; margin-bottom: 22px; }
        .btn-aceptar-confirmacion { width: 100%; background: #2e7d32; color: #fff; border: none; padding: 12px; font-size: 14px; font-weight: 700; border-radius: 4px; cursor: pointer; }
        .btn-aceptar-confirmacion:hover { background: #1b5e20; }
    </style>
</head>
<body>
    <header class="navbar">
        <div class="nav-contenedor">
            <div class="logo">🛒 BODEGA EL GRINGO</div>
            <nav>
                <ul>
                    <li class="activo" id="nav-servicios" onclick="irA('servicios')">Catálogo de Productos</li>
                    <li id="nav-login" onclick="irA('login')">Iniciar Sesión</li>
                    <li id="nav-contacto" onclick="irA('contacto')">Contacto</li>
                </ul>
            </nav>
        </div>
    </header>

    <main class="contenedor-principal">

        <!-- VISTA: CATÁLOGO (vista inicial) -->
        <div class="vista visible" id="vista-servicios">
            <div class="panel-wrapper">
                <div class="encabezado-panel">
                    <div>
                        <h1>¡Bienvenido a la Bodega El Gringo!</h1>
                        <p>Selecciona los productos que deseas comprar y agrégalos a tu carrito.</p>
                    </div>
                </div>

                <div class="layout-catalogo-carrito">
                    <!-- CATÁLOGO -->
                    <div class="catalogo-box">
                        <h3>Productos Disponibles</h3>
                        <p class="subtitulo">Haz clic en un producto para agregarlo a tu carrito.</p>
                        <div class="filtros">
                            <button class="filtro-btn activo" onclick="filtrar('Todos', this)">Todos</button>
                            <button class="filtro-btn" onclick="filtrar('Bebidas', this)">🥤 Bebidas</button>
                            <button class="filtro-btn" onclick="filtrar('Snacks', this)">🍟 Snacks</button>
                            <button class="filtro-btn" onclick="filtrar('Galletas', this)">🍪 Galletas</button>
                            <button class="filtro-btn" onclick="filtrar('Caramelos', this)">🍬 Caramelos</button>
                            <button class="filtro-btn" onclick="filtrar('Otros', this)">📦 Otros</button>
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
                                <p>Tu carrito está vacío.<br>Agrega productos del catálogo.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- VISTA: LOGIN / CUENTA -->
        <div class="vista" id="vista-login">
            <div class="login-wrapper">
                <!-- Formulario de inicio de sesión -->
                <div class="acceso-sesion" id="acceso-sesion">
                    <h2>Iniciar Sesión</h2>
                    <p>Ingresa tus datos para acceder a tu cuenta</p>
                    <div class="grupo-entrada">
                        <label>Correo</label>
                        <input type="email" id="correo" placeholder="Correo electrónico">
                    </div>
                    <div class="grupo-entrada">
                        <label>Nombres completos</label>
                        <input type="text" id="usuario" placeholder="Usuario">
                    </div>
                    <div class="grupo-entrada">
                        <label>DNI</label>
                        <input type="text" id="dni" placeholder="N° DNI" maxlength="8">
                    </div>
                    <div class="grupo-entrada">
                        <label>Contraseña</label>
                        <input type="password" id="contraseña" placeholder="••••••••••" onkeydown="if(event.key==='Enter') validarAcceso()">
                    </div>
                    <div id="mensaje" class="mensaje-alerta"></div>
                    <button class="btn-login" onclick="validarAcceso()">Ingresar</button>
                </div>

                <!-- Cuenta ya iniciada -->
                <div class="cuenta-box" id="cuenta-box" style="display:none;">
                    <div class="avatar-circulo" id="avatar-inicial">M</div>
                    <h2 id="cuenta-nombre">Cliente</h2>
                    <p style="color:#666; font-size:13px; margin-bottom:20px;">Sesión iniciada correctamente</p>
                    <div class="dato-cuenta"><b>Correo:</b> <span id="cuenta-correo"></span></div>
                    <div class="dato-cuenta"><b>DNI:</b> <span id="cuenta-dni"></span></div>
                    <button class="boton-Salir" style="width:100%; margin-top:10px;" onclick="cerrarSesion()">Cerrar Sesión</button>
                </div>
            </div>
        </div>

        <!-- VISTA: CONTACTO -->
        <div class="vista" id="vista-contacto">
            <div class="contacto-box">
                <h2>Contáctanos</h2>
                <p class="subtitulo">Estamos para ayudarte. Encuéntranos o escríbenos.</p>
                <div class="item-contacto">
                    <div class="icono">📍</div>
                    <div class="texto-contacto">
                        <div class="titulo-contacto">Dirección</div>
                        <div class="valor-contacto">Jiron Pedro Gutierrez Blanco Mz. T12 - Lt. 8, Lima Metropolitana 15446, Lima, Perú</div>
                    </div>
                </div>
                <div class="item-contacto">
                    <div class="icono">📞</div>
                    <div class="texto-contacto">
                        <div class="titulo-contacto">Teléfono</div>
                        <div class="valor-contacto">+51 912 345 678</div>
                    </div>
                </div>
                <div class="item-contacto">
                    <div class="icono">✉️</div>
                    <div class="texto-contacto">
                        <div class="titulo-contacto">Correo</div>
                        <div class="valor-contacto">elgringo.bodega@gmail.com</div>
                    </div>
                </div>
                <div class="item-contacto">
                    <div class="icono">🕒</div>
                    <div class="texto-contacto">
                        <div class="titulo-contacto">Horario de atención</div>
                        <div class="valor-contacto">Todos los días, 7:00 am - 11:00 pm</div>
                    </div>
                </div>
            </div>
        </div>

    </main>

    <!-- MODAL: MÉTODO DE PAGO -->
    <div class="modal-overlay" id="modal-pago">
        <div class="modal-pago">
            <h2>Método de pago</h2>
            <p class="subtitulo">Selecciona cómo deseas pagar tu pedido.</p>

            <div class="resumen-pago" id="resumen-pago"></div>

            <div class="opciones-pago">
                <label class="opcion-pago">
                    <input type="radio" name="metodoPago" value="Tarjeta de crédito/débito" checked>
                    💳 Tarjeta de crédito / débito
                </label>
                <label class="opcion-pago">
                    <input type="radio" name="metodoPago" value="Transferencia bancaria">
                    🏦 Transferencia bancaria
                </label>
                <label class="opcion-pago">
                    <input type="radio" name="metodoPago" value="Yape / Plin">
                    📲 Yape / Plin
                </label>
                <label class="opcion-pago">
                    <input type="radio" name="metodoPago" value="Pago en efectivo">
                    💵 Pago en efectivo
                </label>
            </div>

            <div class="modal-botones">
                <button class="btn-cancelar-pago" onclick="cerrarModalPago()">Cancelar</button>
                <button class="btn-confirmar-pago" onclick="confirmarPago()">Confirmar pago</button>
            </div>
        </div>
    </div>

    <!-- MODAL: CONFIRMACIÓN DE COMPRA -->
    <div class="modal-overlay" id="modal-confirmacion">
        <div class="modal-confirmacion">
            <div class="icono-exito">✓</div>
            <h2>¡Gracias por tu compra!</h2>
            <p class="subtitulo">Tu pedido fue registrado con éxito.</p>

            <div class="resumen-confirmacion" id="resumen-confirmacion"></div>

            <p class="nota-confirmacion">Pasa por la bodega o espera tu delivery. ¡Que lo disfrutes!</p>

            <button class="btn-aceptar-confirmacion" onclick="cerrarModalConfirmacion()">Aceptar</button>
        </div>
    </div>

    <script>
        let todosLosProductos = [];
        let carrito = [];
        let filtroActual = 'Todos';
        let usuarioActual = null;

        /* NAVEGACIÓN ENTRE VISTAS */
        function irA(vista) {
            document.querySelectorAll('.vista').forEach(v => v.classList.remove('visible'));
            document.getElementById('vista-' + vista).classList.add('visible');
            document.querySelectorAll('.navbar nav ul li').forEach(li => li.classList.remove('activo'));
            document.getElementById('nav-' + vista).classList.add('activo');
        }

        /* Cargar catálogo apenas se abre la página */
        document.addEventListener('DOMContentLoaded', cargarProductos);

        /* AUTH */
        function validarAcceso() {
            const correo = document.getElementById('correo').value.trim();
            const usuario = document.getElementById('usuario').value.trim();
            const dni = document.getElementById('dni').value.trim();
            const contrasena = document.getElementById('contraseña').value;
            const caja = document.getElementById('mensaje');

            if (!correo || !usuario || !dni || !contrasena) {
                caja.style.color = '#c62828';
                caja.textContent = 'Por favor completa todos los campos.';
                return;
            }

            const correoValido = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(correo);
            if (!correoValido) {
                caja.style.color = '#c62828';
                caja.textContent = 'Ingresa un correo válido.';
                return;
            }

            if (!/^\\d{8}$/.test(dni)) {
                caja.style.color = '#c62828';
                caja.textContent = 'El DNI debe tener 8 dígitos.';
                return;
            }

            if (contrasena.length < 6) {
                caja.style.color = '#c62828';
                caja.textContent = 'La contraseña debe tener al menos 6 caracteres.';
                return;
            }

            fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ correo, usuario, dni, contrasena })
            })
            .then(r => r.json())
            .then(data => {
                if (data.valido) {
                    caja.style.color = '#28a745';
                    caja.textContent = data.mensaje;
                    usuarioActual = { correo, usuario, dni };
                    setTimeout(() => {
                        mostrarCuenta();
                    }, 700);
                } else {
                    caja.style.color = '#c62828';
                    caja.textContent = data.mensaje;
                }
            });
        }

        function mostrarCuenta() {
            document.getElementById('acceso-sesion').style.display = 'none';
            document.getElementById('cuenta-box').style.display = 'block';
            document.getElementById('cuenta-nombre').textContent = usuarioActual.usuario;
            document.getElementById('cuenta-correo').textContent = usuarioActual.correo;
            document.getElementById('cuenta-dni').textContent = usuarioActual.dni;
            document.getElementById('avatar-inicial').textContent = usuarioActual.usuario.charAt(0).toUpperCase();
            document.getElementById('nav-login').textContent = '👤 ' + usuarioActual.usuario;
        }

        function cerrarSesion() {
            usuarioActual = null;
            document.getElementById('correo').value = '';
            document.getElementById('usuario').value = '';
            document.getElementById('dni').value = '';
            document.getElementById('contraseña').value = '';
            document.getElementById('mensaje').textContent = '';
            document.getElementById('acceso-sesion').style.display = 'block';
            document.getElementById('cuenta-box').style.display = 'none';
            document.getElementById('nav-login').textContent = 'Iniciar Sesión';
            irA('servicios');
        }

        /* CATÁLOGO */
        function cargarProductos() {
            fetch('/servicios')
            .then(r => r.json())
            .then(data => {
                todosLosProductos = data;
                renderGrid(data);
            });
        }

        function filtrar(tipo, btn) {
            filtroActual = tipo;
            document.querySelectorAll('.filtro-btn').forEach(b => b.classList.remove('activo'));
            btn.classList.add('activo');
            const lista = tipo === 'Todos' ? todosLosProductos : todosLosProductos.filter(s => s.tipo === tipo);
            renderGrid(lista);
        }

        function renderGrid(lista) {
            const grid = document.getElementById('grid-servicios');
            grid.innerHTML = '';
            lista.forEach(prod => {
                const enCarrito = carrito.some(c => c.id === prod.id);
                grid.innerHTML += `
                    <div class="tarjeta-servicio ${enCarrito ? 'en-carrito' : ''}" id="card-${prod.id}">
                        <span class="tag-tipo tag-${prod.tipo}">${prod.tipo}</span>
                        <h4>${prod.nombre}</h4>
                        <p class="descripcion">${prod.descripcion}</p>
                        <div class="precio-grande">S/. ${prod.precio.toFixed(2)} <span>/ unidad</span></div>
                        <button class="btn-agregar-carrito ${enCarrito ? 'agregado' : ''}" onclick="toggleCarrito(${prod.id})">
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
                const prod = todosLosProductos.find(s => s.id === id);
                if (prod) carrito.push(prod);
            } else {
                carrito.splice(idx, 1);
            }
            const lista = filtroActual === 'Todos' ? todosLosProductos : todosLosProductos.filter(s => s.tipo === filtroActual);
            renderGrid(lista);
            renderCarrito();
        }

        function quitarDelCarrito(id) {
            carrito = carrito.filter(c => c.id !== id);
            const lista = filtroActual === 'Todos' ? todosLosProductos : todosLosProductos.filter(s => s.tipo === filtroActual);
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
                        <p>Tu carrito está vacío.<br>Agrega productos del catálogo.</p>
                    </div>`;
                return;
            }

            const total = carrito.reduce((acc, s) => acc + s.precio, 0);

            let html = '<ul class="lista-carrito">';
            carrito.forEach(prod => {
                html += `
                    <li class="item-carrito">
                        <div class="item-info">
                            <div class="item-nombre">${prod.nombre}</div>
                            <div class="item-tipo">${prod.tipo}</div>
                        </div>
                        <div style="display:flex;align-items:center;gap:8px;">
                            <div class="item-precio">S/. ${prod.precio.toFixed(2)}</div>
                            <button class="btn-quitar" onclick="quitarDelCarrito(${prod.id})" title="Quitar">✕</button>
                        </div>
                    </li>`;
            });
            html += '</ul>';

            html += `
                <div class="carrito-total">
                    <div class="fila-total">
                        <span class="label-total">Total</span>
                        <span class="monto-total">S/. ${total.toFixed(2)}</span>
                    </div>
                    <div class="igv-nota">Incluye IGV · Precios en soles</div>
                </div>
                <button class="btn-contratar" onclick="contratar()">Pagar ahora →</button>`;

            cont.innerHTML = html;
        }

        /* MODAL DE PAGO */
        function contratar() {
            if (carrito.length === 0) return;
            const total = carrito.reduce((acc, s) => acc + s.precio, 0);
            let html = '';
            carrito.forEach(prod => {
                html += `<div class="fila-resumen"><span>${prod.nombre}</span><span>S/. ${prod.precio.toFixed(2)}</span></div>`;
            });
            html += `<div class="fila-resumen total-resumen"><span>Total</span><span>S/. ${total.toFixed(2)}</span></div>`;
            document.getElementById('resumen-pago').innerHTML = html;
            document.getElementById('modal-pago').classList.add('visible');
        }

        function cerrarModalPago() {
            document.getElementById('modal-pago').classList.remove('visible');
        }

        function confirmarPago() {
            const metodo = document.querySelector('input[name="metodoPago"]:checked').value;

            let html = '';
            carrito.forEach(prod => {
                html += `<div class="fila-resumen"><span>${prod.nombre}</span><span>S/. ${prod.precio.toFixed(2)}</span></div>`;
            });
            html += `<div class="fila-metodo">Método de pago: <b>${metodo}</b></div>`;
            document.getElementById('resumen-confirmacion').innerHTML = html;

            cerrarModalPago();
            document.getElementById('modal-confirmacion').classList.add('visible');

            carrito = [];
            const lista = filtroActual === 'Todos' ? todosLosProductos : todosLosProductos.filter(s => s.tipo === filtroActual);
            renderGrid(lista);
            renderCarrito();
        }

        function cerrarModalConfirmacion() {
            document.getElementById('modal-confirmacion').classList.remove('visible');
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
    datos = request.get_json() or {}
    correo = (datos.get('correo') or '').strip()
    usuario = (datos.get('usuario') or '').strip()
    dni = (datos.get('dni') or '').strip()
    contrasena = datos.get('contrasena') or ''

    if not correo or not usuario or not dni or not contrasena:
        return jsonify({"valido": False, "mensaje": "Por favor completa todos los campos."})

    if '@' not in correo or '.' not in correo.split('@')[-1]:
        return jsonify({"valido": False, "mensaje": "Ingresa un correo válido."})

    if not (dni.isdigit() and len(dni) == 8):
        return jsonify({"valido": False, "mensaje": "El DNI debe tener 8 dígitos."})

    if len(contrasena) < 6:
        return jsonify({"valido": False, "mensaje": "La contraseña debe tener al menos 6 caracteres."})

    return jsonify({"valido": True, "mensaje": f"¡Bienvenido, {usuario}!"})

@app.route('/servicios', methods=['GET'])
def listar_productos():
    return jsonify(productos_db)

if __name__ == '__main__':
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=puerto, debug=False)
