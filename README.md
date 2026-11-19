# SUTITESZ - Sistema Integral de Gestión Sindical y Escalafón

Aplicación web desarrollada en **Python (Flask)** bajo el patrón arquitectónico **MVVM (Model - View - ViewModel)** para la gestión de agremiados, control de acceso basado en roles (RBAC), repositorio documental y cálculo automatizado de puntos escalafonarios del Sindicato Único de Trabajadores del Instituto Tecnológico de Estudios Superiores de Zamora (SUTITESZ).

---

## 🏗️ Arquitectura del Proyecto (MVVM)

El sistema implementa una separación estricta de responsabilidades:

* **`models/`**: Definición de entidades de dominio y esquemas de datos (`usuario.py`, `documento.py`).
* **`viewmodels/`**: Lógica de negocio, reglas de validación de roles (`T101` Administrador vs `S*` Agremiados) y motor de cálculo de antigüedad (`calculadora_vm.py`).
* **`services/`**: Capa de persistencia, gestión de sesiones y almacenamiento seguro de archivos.
* **`templates/` & `static/`**: Vistas HTML dinámicas y recursos visuales institucionales.
* **`test/`**: Suite de pruebas unitarias automatizadas con `pytest`.

---

## 🚀 Despliegue con Docker

El proyecto cuenta con contenedorización completa para garantizar portabilidad entre entornos:

1. Configurar variables de entorno tomando como base `.env.example`:
   ```bash
   cp .env.example .env

   - **Integración Continua (CI/CD):** Validación automática ejecutada con GitHub Actions (`pytest` y `flake8`) en cada integración hacia `main`.
