from models.usuario_model import Usuario
from services.datos_service import usuarios_db


class UsuarioViewModel:
    @staticmethod
    def autenticar(clave):
        clave = clave.strip().upper()
        if clave.startswith('T'):
            return True, True, f"Administrador ({clave})", "¡Acceso de Administrador concedido!"
        elif clave.startswith('S'):
            usuario = next((u for u in usuarios_db if u.clave == clave), None)
            if usuario and not usuario.activo:
                return False, False, None, "Acceso denegado. Su cuenta ha sido restringida por el Administrador."
            return True, False, f"Usuario {clave}", f"Bienvenido usuario {clave}"
        return False, False, None, "Clave no válida. Debe comenzar únicamente con 'T' o 'S'."

    @staticmethod
    def registrar_usuario(clave, nombre, adscripcion, correo, telefono, area_trabajo):
        nuevo = Usuario(clave, nombre, adscripcion, correo, telefono, area_trabajo)
        if not nuevo.es_clave_valida():
            return False, "La clave debe comenzar únicamente con 'T' o 'S'."
        if any(u.clave == nuevo.clave for u in usuarios_db):
            return False, f"La clave {nuevo.clave} ya está registrada."
        usuarios_db.append(nuevo)
        return True, "Usuario registrado correctamente."

    @staticmethod
    def buscar_usuario(criterio):
        criterio = criterio.strip().upper()
        for u in usuarios_db:
            if u.clave == criterio or criterio in u.nombre_completo.upper():
                return u.to_dict()
        return None

    @staticmethod
    def actualizar_usuario(clave, nombre, adscripcion, correo, telefono, area_trabajo):
        for u in usuarios_db:
            if u.clave == clave:
                u.nombre_completo = nombre.strip()
                u.area_adscripcion = adscripcion.strip()
                u.correo = correo.strip()
                u.telefono = telefono.strip()
                u.area_trabajo = area_trabajo.strip()
                return True, f"Usuario {clave} modificado exitosamente."
        return False, "Usuario no encontrado."

    @staticmethod
    def alternar_restriccion(clave):
        for u in usuarios_db:
            if u.clave == clave:
                u.activo = not u.activo
                estado = "habilitado" if u.activo else "restringido"
                return True, f"El acceso para el usuario {clave} ha sido {estado}."
        return False, "Usuario no encontrado."

    @staticmethod
    def eliminar_usuario(clave):
        global usuarios_db
        inicial = len(usuarios_db)
        usuarios_db[:] = [u for u in usuarios_db if u.clave != clave]
        if len(usuarios_db) < inicial:
            return True, f"Usuario {clave} eliminado permanentemente."
        return False, "Usuario no encontrado."

    @staticmethod
    def obtener_todos():
        return [u.to_dict() for u in usuarios_db]