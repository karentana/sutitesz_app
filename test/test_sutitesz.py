import pytest
from viewmodels.usuario_vm import UsuarioViewModel
from viewmodels.documento_vm import DocumentoViewModel
from viewmodels.calculadora_vm import CalculadoraViewModel


# CASO 1: Validación de autenticación por prefijo de rol (Admin T vs Estándar S)
def test_autenticacion_roles():
    exito_admin, es_admin, sesion_admin, _ = UsuarioViewModel.autenticar('T101')
    assert exito_admin is True
    assert es_admin is True
    assert sesion_admin == 'Administrador (T101)'

    exito_invalido, _, _, msg = UsuarioViewModel.autenticar('X999')
    assert exito_invalido is False
    assert "comenzar únicamente con 'T' o 'S'" in msg


# CASO 2: Regla de negocio de registro y prevención de claves duplicadas
def test_registro_usuario_y_duplicados():
    exito, _ = UsuarioViewModel.registrar_usuario(
        'S099', 'Carlos Ruiz', 'Docente', 'carlos@sutitesz.edu.mx', '3530001122', 'Industrial'
    )
    assert exito is True

    # Intentar registrar la misma clave debe fallar
    exito_dup, msg_dup = UsuarioViewModel.registrar_usuario(
        'S099', 'Carlos Ruiz', 'Docente', 'carlos@sutitesz.edu.mx', '3530001122', 'Industrial'
    )
    assert exito_dup is False
    assert "ya está registrada" in msg_dup


# CASO 3: Bloqueo y restricción de acceso de usuario
def test_restriccion_acceso_usuario():
    UsuarioViewModel.alternar_restriccion('S002')  # Restringir acceso a S002
    exito, _, _, mensaje = UsuarioViewModel.autenticar('S002')
    assert exito is False
    assert "restringida" in mensaje

    # Restaurar su acceso para mantener estado limpio
    UsuarioViewModel.alternar_restriccion('S002')


# CASO 4: Cálculo de puntos de antigüedad en escalafón (factor x 5)
def test_calculo_puntos_antiguedad():
    puntos = CalculadoraViewModel.calcular_puntos_antiguedad(4, 6)
    assert puntos == 50

    with pytest.raises(ValueError):
        CalculadoraViewModel.calcular_puntos_antiguedad(-2, 5)


# CASO 5: Vinculación privada de documentos por clave de sesión
def test_documentos_por_usuario():
    exito, _ = DocumentoViewModel.agregar_documento('S001', 'Constancia_Curso.pdf')
    assert exito is True
    docs = DocumentoViewModel.obtener_por_usuario('S001')
    assert any(d['nombre_archivo'] == 'Constancia_Curso.pdf' for d in docs)