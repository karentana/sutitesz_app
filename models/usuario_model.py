class Usuario:
    def __init__(self, clave, nombre_completo, area_adscripcion, correo, telefono, area_trabajo, activo=True):
        self.clave = clave.strip().upper()
        self.nombre_completo = nombre_completo.strip()
        self.area_adscripcion = area_adscripcion.strip()
        self.correo = correo.strip()
        self.telefono = telefono.strip()
        self.area_trabajo = area_trabajo.strip()
        self.activo = activo

    def es_clave_valida(self):
        return self.clave.startswith('T') or self.clave.startswith('S')

    def to_dict(self):
        return {
            'clave': self.clave,
            'nombre_completo': self.nombre_completo,
            'area_adscripcion': self.area_adscripcion,
            'correo': self.correo,
            'telefono': self.telefono,
            'area_trabajo': self.area_trabajo,
            'activo': self.activo
        }