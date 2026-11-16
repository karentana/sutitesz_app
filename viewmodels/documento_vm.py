from datetime import date
from models.documento_model import Documento
from services.datos_service import documentos_db


class DocumentoViewModel:
    @staticmethod
    def extraer_clave_sesion(usuario_actual_str):
        if '(' in usuario_actual_str and ')' in usuario_actual_str:
            return usuario_actual_str.split('(')[1].replace(')', '').strip()
        return usuario_actual_str.replace('Usuario', '').strip()

    @staticmethod
    def agregar_documento(clave_usuario, nombre_archivo):
        if not nombre_archivo or nombre_archivo.strip() == '':
            return False, "Por favor, selecciona un archivo válido."
        nuevo_id = max([d.id for d in documentos_db], default=0) + 1
        nuevo_doc = Documento(nuevo_id, clave_usuario, nombre_archivo, str(date.today()))
        documentos_db.append(nuevo_doc)
        return True, f"Documento '{nombre_archivo}' subido y vinculado a tu cuenta exitosamente."

    @staticmethod
    def obtener_por_usuario(clave_usuario):
        return [d.to_dict() for d in documentos_db if d.usuario_clave == clave_usuario]

    @staticmethod
    def eliminar_documento(doc_id):
        inicial = len(documentos_db)
        documentos_db[:] = [d for d in documentos_db if d.id != doc_id]
        return len(documentos_db) < inicial