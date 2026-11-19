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

   ---

## Cierre Técnico del Proyecto (SUTITESZ)

### 1. Arquitectura Implementada (MVVM)
El sistema está desarrollado en **Python 3 + Flask** bajo el patrón arquitectónico **MVVM (Modelo-Vista-VistaModelo)** para desacoplar la interfaz gráfica de la lógica de negocio y la persistencia:
* **Vista (`templates/` y `static/`):** Interfaces web dinámicas con Jinja2 y estilos institucionales.
* **VistaModelo / Lógica (`app.py` y `viewmodels/`):** Enrutamiento, control de sesiones, validación de permisos por rol y motor de cálculo escalafonario (`calculadora_vm.py`).
* **Modelo (`models/`):** Entidades del dominio sindical (`usuario.py`, `documento.py`).
* **Servicios y Persistencia (`services/`):** Gestión de sesiones, reglas de acceso y resguardo de registros.
* **Contenedores y Calidad (`Dockerfile`, `compose.yaml`, `.github/workflows/ci.yml`):** Empaquetado portable con Docker y validación automatizada con `pytest` y `flake8` en cada `push`.

### 2. Módulos Terminados y Demostrables
* **Autenticación y Control de Roles:** Validación diferenciada entre Administrador (`T101`) y Agremiado (`S*`) mediante sesiones protegidas.
* **Gestión CRUD de Usuarios:** Alta, búsqueda por clave o nombre, actualización de datos, restricción de acceso y eliminación de registros.
* **Calculadora Escalafonaria:** Cálculo automatizado de puntaje por antigüedad laboral y sindical bajo la fórmula `(años_base + años_empresa) * 5`.
* **Gestión de Formatos Sindicales:** Consulta y descarga de documentación institucional según perfil.
* **Integración Continua (CI/CD):** Pipeline funcional en GitHub Actions que ejecuta pruebas unitarias y análisis de estilo automáticamente.

### 3. Funcionalidades Pendientes (Siguiente Incremento)
* **Persistencia Relacional Externa (ID `7.4` en Azure Boards):** Integrar el contenedor de base de datos **MySQL** con el script `init.sql` dentro de `compose.yaml` para migrar el almacenamiento local ligero hacia un motor relacional persistente.
* **Auditoría de Movimientos:** Incorporar una bitácora histórica de modificaciones realizadas por usuarios administradores.
* FUNCIONALIDADES DE CALCULADORA ESCALAFONARIA*

### 4. Instrucciones de Requisitos y Ejecución Local
**Requisitos previos:** Python 3.10+ (o Docker Desktop).

**Opción A — Ejecución con Python local:**
1. Clonar el repositorio:
   `git clone https://github.com/karentana/sutitesz_app.git`
2. Entrar al directorio del proyecto e instalar dependencias:
   `pip install -r requirements.txt`
3. Ejecutar la aplicación:
   `python app.py`
4. Abrir en el navegador: `http://localhost:5000` (Claves de prueba: `T101` para Administrador / `S001` para Agremiado).

**Opción B — Ejecución con Docker:**
1. Construir y levantar el contenedor:
   `docker compose up --build`
2. Acceder en el navegador a `http://localhost:5000`.

**Ejecución de pruebas unitarias:**
`pytest`

### 5. Dificultades Encontradas y Soluciones
* **Desacoplamiento de lógica para pruebas automatizadas:** Inicialmente las validaciones estaban ligadas a las rutas de Flask; se resolvió extrayendo las reglas de cálculo hacia `viewmodels/calculadora_vm.py` para permitir pruebas unitarias directas con `pytest`.
* **Configuración del entorno en GitHub Actions (`ci.yml`):** Se ajustaron las rutas de importación (`PYTHONPATH=.`) y los estándares de formato (`flake8`) para lograr la ejecución limpia del pipeline sin errores.
* **Alcance de base de datos en contenedor:** Debido a los tiempos del Sprint, se priorizó la estabilidad funcional del backend y las pruebas automatizadas, documentando la conexión completa con MySQL como brecha controlada para el siguiente incremento.
