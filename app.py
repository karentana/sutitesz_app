
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from viewmodels.usuario_vm import UsuarioViewModel
from viewmodels.documento_vm import DocumentoViewModel
from viewmodels.calculadora_vm import CalculadoraViewModel
from services.datos_service import noticias_db, eventos_db

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'sutitesz_clave_secreta_2026')

# Configuración para la carga de archivos
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ==========================================
# RUTAS GENERALES (Noticias, Eventos, Formatos)
# ==========================================

@app.route('/')
def index():
    return render_template('index.html', noticias=noticias_db)


@app.route('/eventos')
def eventos():
    return render_template('eventos.html', eventos=eventos_db)


@app.route('/formatos')
def descargar_formatos():
    return render_template('formatos.html')


# ==========================================
# CALCULADORA DE ESCALAFÓN (Conectada a ViewModel)
# ==========================================

@app.route('/calculadora-escalafon', methods=['GET', 'POST'])
def calculadora_escalafon():
    resultado = None
    if request.method == 'POST':
        try:
            antiguedad_base = float(request.form.get('antiguedad_base', 0))
            antiguedad_sindical = float(request.form.get('antiguedad_sindical', 0))

            puntos_base = antiguedad_base * 5
            puntos_sindical = antiguedad_sindical * 5
            total_puntos = CalculadoraViewModel.calcular_puntos_antiguedad(antiguedad_base, antiguedad_sindical)

            resultado = {
                'base_anos': antiguedad_base,
                'sindical_anos': antiguedad_sindical,
                'puntos_base': puntos_base,
                'puntos_sindical': puntos_sindical,
                'total_puntos': total_puntos
            }
            flash("Cálculo de escalafón realizado con éxito.", "success")
        except ValueError:
            flash("Por favor, ingresa números válidos para los años.", "danger")

    return render_template('calculadora_escalafon.html', resultado=resultado)


# ==========================================
# GESTIÓN DE USUARIOS Y ROLES (T... y S...)
# ==========================================

@app.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    if request.method == 'POST':
        clave = request.form.get('clave', '').strip().upper()
        exito, es_admin, nombre_sesion, mensaje = UsuarioViewModel.autenticar(clave)

        if exito:
            session['es_admin'] = es_admin
            session['usuario_actual'] = nombre_sesion
            flash(mensaje, "success")
        else:
            flash(mensaje, "danger")

        return redirect(url_for('usuarios'))

    es_admin = session.get('es_admin', False)
    usuario_actual = session.get('usuario_actual', 'No identificado')
    return render_template('usuarios.html', es_admin=es_admin, usuario_actual=usuario_actual, resultado_busqueda=None)


@app.route('/usuarios/cerrar-sesion', methods=['POST'])
def cerrar_sesion():
    session.pop('es_admin', None)
    session.pop('usuario_actual', None)
    flash("Has cerrado sesión correctamente.", "info")
    return redirect(url_for('index'))


@app.route('/usuarios/agregar', methods=['POST'])
def agregar_usuario():
    if not session.get('es_admin', False):
        flash("Acceso denegado.", "danger")
        return redirect(url_for('usuarios'))

    exito, mensaje = UsuarioViewModel.registrar_usuario(
        request.form.get('clave_acceso', ''),
        request.form.get('nombre_completo', ''),
        request.form.get('area_adscripcion', ''),
        request.form.get('correo_electronico', ''),
        request.form.get('telefono', ''),
        request.form.get('area_trabajo', '')
    )
    flash(mensaje, "success" if exito else "danger")
    return redirect(url_for('usuarios'))


@app.route('/usuarios/buscar', methods=['POST'])
def buscar_usuario():
    if not session.get('es_admin', False):
        flash("Acceso denegado.", "danger")
        return redirect(url_for('usuarios'))

    criterio = request.form.get('criterio_busqueda', '')
    encontrado = UsuarioViewModel.buscar_usuario(criterio)

    if not encontrado:
        flash("No se encontró ningún usuario con ese criterio.", "warning")

    es_admin = session.get('es_admin', False)
    usuario_actual = session.get('usuario_actual', 'No identificado')
    return render_template('usuarios.html', es_admin=es_admin, usuario_actual=usuario_actual, resultado_busqueda=encontrado)


@app.route('/usuarios/actualizar/<clave_usuario>', methods=['POST'])
def actualizar_usuario(clave_usuario):
    if not session.get('es_admin', False):
        flash("Acceso denegado.", "danger")
        return redirect(url_for('usuarios'))

    exito, mensaje = UsuarioViewModel.actualizar_usuario(
        clave_usuario,
        request.form.get('nombre_completo', ''),
        request.form.get('area_adscripcion', ''),
        request.form.get('correo_electronico', ''),
        request.form.get('telefono', ''),
        request.form.get('area_trabajo', '')
    )
    if exito:
        flash(mensaje, "success")
    return redirect(url_for('usuarios'))


@app.route('/usuarios/restringir/<clave_usuario>', methods=['POST'])
def restringir_usuario(clave_usuario):
    if not session.get('es_admin', False):
        flash("Acceso denegado.", "danger")
        return redirect(url_for('usuarios'))

    exito, mensaje = UsuarioViewModel.alternar_restriccion(clave_usuario)
    if exito:
        flash(mensaje, "info")
    return redirect(url_for('usuarios'))


@app.route('/usuarios/eliminar/<clave_usuario>', methods=['POST'])
def eliminar_usuario(clave_usuario):
    if not session.get('es_admin', False):
        flash("Acceso denegado.", "danger")
        return redirect(url_for('usuarios'))

    exito, mensaje = UsuarioViewModel.eliminar_usuario(clave_usuario)
    if exito:
        flash(mensaje, "success")
    return redirect(url_for('usuarios'))


# ==========================================
# GESTIÓN DE DOCUMENTOS POR USUARIO
# ==========================================

@app.route('/documentos', methods=['GET', 'POST'])
def documentos():
    if not session.get('usuario_actual'):
        flash("Debes iniciar sesión con tu clave (T... o S...) para acceder a tus documentos.", "warning")
        return redirect(url_for('usuarios'))

    clave_actual = DocumentoViewModel.extraer_clave_sesion(session.get('usuario_actual', ''))

    if request.method == 'POST':
        archivo = request.files.get('archivo_subido')
        nombre_archivo = archivo.filename if archivo else ''
        exito, mensaje = DocumentoViewModel.agregar_documento(clave_actual, nombre_archivo)
        flash(mensaje, "success" if exito else "danger")
        return redirect(url_for('documentos'))

    documentos_usuario = DocumentoViewModel.obtener_por_usuario(clave_actual)
    return render_template('documentos.html', documentos=documentos_usuario, clave_actual=clave_actual)


@app.route('/documentos/eliminar/<int:doc_id>', methods=['POST'])
def eliminar_documento(doc_id):
    if not session.get('usuario_actual'):
        flash("Inicia sesión para realizar esta acción.", "danger")
        return redirect(url_for('usuarios'))

    if DocumentoViewModel.eliminar_documento(doc_id):
        flash("Documento eliminado correctamente.", "info")
    return redirect(url_for('documentos'))


# --- RUTA TEMPORAL APP MOVIL ---
@app.route('/vista-movil')
def vista_movil():
    return render_template('mobile_preview.html')


# ==========================================
# ENDPOINTS API REST (JSON)
# ==========================================

@app.route('/api/usuarios', methods=['GET'])
def api_listar_usuarios():
    return jsonify({
        'status': 'ok',
        'total': len(UsuarioViewModel.obtener_todos()),
        'usuarios': UsuarioViewModel.obtener_todos()
    }), 200


@app.route('/api/escalafon/calcular', methods=['POST'])
def api_calcular_escalafon():
    datos = request.get_json() or {}
    try:
        base = float(datos.get('anios_base', 0))
        empresa = float(datos.get('anios_empresa', 0))
        puntos = CalculadoraViewModel.calcular_puntos_antiguedad(base, empresa)
        return jsonify({'status': 'ok', 'puntos_totales': puntos}), 200
    except ValueError as e:
        return jsonify({'status': 'error', 'mensaje': str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)