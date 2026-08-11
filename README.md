# 📦 StockFlow - Sistema de Control de Inventario y Stock

**Desarrollado por:** Daniel Jiménez  
**Estado:** En desarrollo activo (v1.6 - Listo para Deploy)
**Linkedin:** https://www.linkedin.com/in/jimenezvalderramadaniel/

---

## 🛠️ Stack Tecnológico & Arquitectura

### Backend
- **Lenguaje:** Python 3.12+
- **Framework Principal:** Django 5.2.11
- **API & Integraciones:** Django REST Framework 3.17.1 (`djangorestframework`) & Django CORS Headers 4.9.0 (`django-cors-headers`) para integración con frontends desacoplados.
- **Autenticación & Permisos:** Django Auth System (Sesiones, Cookies, Decoradores y Control de Acceso Basado en Roles - RBAC).

### Frontend & UI
- **Estructura y Estilos:** HTML5, Tailwind CSS (CDN).
- **Lógica e Interactividad:** JavaScript Vanilla (Modales, manejo de eventos DOM, atajos de teclado ESC).
- **Visualización de Datos:** Chart.js (Gráficos dinámicos e interactivos).
- **Branding & Identidad:** Isotipo corporativo oficial integrado en la cabecera principal, pantalla de autenticación y favicon para la pestaña del navegador.

### Base de Datos & Persistencia
- **Motor Actual:** SQLite3 (Entorno local) / Preparado para PostgreSQL (Producción).
- **ORM:** Django ORM.
- **Gestión de Imágenes:** Pillow 12.3.0 (`Pillow`).

### Librerías & Generación de Reportes
- **openpyxl (v3.1.5):** Exportación e importación de reportes tabulares en Microsoft Excel (.xlsx).
- **ReportLab (v5.0.0):** Generación dinámica de documentos en formato PDF (.pdf).

---

## 🔐 Credenciales de Prueba / Demo Credentials

Para evaluar el sistema bajo distintas jerarquías de acceso:

### 🛠️ Usuario Administrador (Superusuario)
- **Usuario:** `admin`
- **Contraseña:** `admin1234`
- **Permisos:** Acceso total a gestión de productos (Alta/Baja/Modificación), administración de categorías, métricas ejecutivas en el Dashboard y acceso al panel `/admin/`.

### 👤 Usuario Empleado (Operador Estándar)
- **Usuario:** `operador1`
- **Contraseña:** `operador1`
- **Permisos:** Acceso restringido exclusivamente a consulta de catálogo (modo solo lectura), registro de movimientos de entrada/salida de stock e historial de operaciones.

---

## 🚀 Funcionalidades Implementadas

### 1. 🔐 Módulo de Autenticación, Sesiones e Identidad Visual
- **Portal de Acceso Limpio:** Pantalla de login optimizada con isotipo vectorial integrado y eliminación de redundancias tipográficas.
- **Favicon & Branding:** Identificación visual unificada en la pestaña del navegador y barra superior de navegación.
- **Seguridad en Rutas:** Protección global mediante el decorador `@login_required` en todas las vistas críticas.
- **Gestión de Sesión:** Indicador de usuario activo y botón de cierre de sesión ubicado en el encabezado.

### 2. 👥 Control de Acceso y Roles (RBAC)
- **Diferenciación de Interfaz:** Ocultamiento dinámico de botones de gestión (*+ Nuevo Producto*, *Categorías*, *Dashboard*) según el rol (`user.is_staff`).
- **Nivel Empleado:** Restricción de acciones de edición y eliminación a la etiqueta "Solo lectura".
- **Gestión Centralizada:** Creación y modificación de usuarios administrada únicamente desde el panel de administración de Django.

### 3. 📦 Módulo de Inventario y Productos
- **CRUD Completo:** Alta, lectura, edición y eliminación de productos y categorías (restringido a Administradores).
- **Visualización Pro:** Tabla interactiva con miniaturas de imágenes procesadas.
- **Modal de Detalle:** Vista ampliada con ficha técnica completa (SKU, categoría, descripción, precio y stock actual).
- **Control de Stock Bajo:** Alertas dinámicas tipo badge cuando el stock actual es igual o inferior al mínimo requerido.
- **Filtros Avanzados:** Búsqueda por SKU/nombre, selección por categoría y selector condicional "Solo stock bajo".

### 4. 📋 Módulo de Historial y Movimientos Comerciales
- **Registro Auditado:** Movimientos de entrada (`IN`) y salida (`OUT`) asignados automáticamente al usuario autenticado.
- **Trazabilidad Comercial:** Campo opcional de **Razón Social / Proveedor / Cliente**.
- **Filtrado Multicriterio:** Por rango de fechas, producto, tipo de movimiento y búsqueda libre.
- **Modal "Generar Total":** Resumen monetario y de unidades acumuladas en tiempo real según filtros aplicados.
- **📄 Exportación de Reportes:** Descarga del historial filtrado en formatos **PDF** (ReportLab) y **Excel** (openpyxl).

### 5. 📊 Módulo Dashboard y Análisis de Rotación (Métricas Avanzadas)
- **Panel de Métricas (KPIs):** Valorización total del inventario ($), total de productos registrados, alertas de stock bajo y categorías activas.
- **Gráficos Dinámicos (Chart.js):**
  - Distribución de productos por categoría (Gráfico de Dona).
  - Top 5 de productos con más salidas (Gráfico de Barras).
- **📈 Reporte Ejecutivo de Rotación:**
  - Análisis condicional por períodos de tiempo (7, 30, 90 y 365 días).
  - Cálculo dinámico de Índice de Rotación, Unidades Despachadas, Capital en Stock e Identificación de SKUs inmovilizados.
  - Indicadores visuales de Nivel de Rotación (Alta, Media, Baja).
  - Exportación dedicada del reporte ejecutivo a formatos **PDF** y **Excel**.

---

## 📌 Plan de Trabajo & Próximas Actividades

1. **🚀 Despliegue a Producción (Deploy Final)**
   - Configuración de servidores WSGI con `gunicorn`.
   - Gestión eficiente de archivos estáticos con `whitenoise`.
   - Publicación en plataforma Cloud (Render / Railway).