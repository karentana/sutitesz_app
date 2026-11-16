class Documento:
    def __init__(self, doc_id, usuario_clave, nombre_archivo, fecha):
        self.id = doc_id
        self.usuario_clave = usuario_clave.strip().upper()
        self.nombre_archivo = nombre_archivo.strip()
        self.fecha = fecha

    def to_dict(self):
        return {
            'id': self.id,
            'usuario_clave': self.usuario_clave,
            'nombre_archivo': self.nombre_archivo,
            'fecha': self.fecha
        }