from models.usuario_model import Usuario
from models.documento_model import Documento

# Base de datos simulada en memoria
usuarios_db = [
    Usuario('S001', 'Ana María Torres', 'Docente', 'ana_maria@sutitesz.edu.mx', '3531234567', 'Sistemas y Computación', True),
    Usuario('S002', 'María López Hernández', 'Administrativo', 'maria.lopez@sutitesz.edu.mx', '3539876543', 'Recursos Humanos', True)
]

documentos_db = [
    Documento(1, 'S001', 'Comprobante_Estudios.pdf', '2026-10-28')
]

noticias_db = [
    {
        "titulo": "Asamblea General Ordinaria 2026",
        "fecha": "2026-10-25",
        "contenido": "Se convoca a todos los miembros del SUTITESZ a la asamblea anual en el auditorio principal.",
        "imagen": "asamblea.jpg"
    },
    {
        "titulo": "Toma de instalaciones de la Secretaría de Educación Pública",
        "fecha": "2026-10-15",
        "contenido": "Agremiados del SUTITESZ junto con otros sindicatos piden incremento salarial y pagos de adeudos",
        "imagen": "evento.jpeg"
    }
]

eventos_db = [
    {
        "titulo": "Torneo Anual de Fútbol SUTITESZ",
        "fecha": "2026-11-10",
        "lugar": "Canchas Deportivas",
        "descripcion": "Torneo interdepartamental de fútbol rápido."
    }
]