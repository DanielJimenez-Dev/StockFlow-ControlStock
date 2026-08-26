# 📦 StockFlow - Inventory & Stock Control System

**Developed by:** Daniel Jiménez  
**Status:** Active Development (v1.6 - Production Ready)  
**LinkedIn:** https://www.linkedin.com/in/jimenezvalderramadaniel/  
**🚀 Live Demo / Web App:** https://stockflow-controlstock.onrender.com

---

## 🛠️ Tech Stack & Architecture

### Backend
- **Language:** Python 3.12+
- **Primary Framework:** Django 5.2.11
- **API & Integrations:** Django REST Framework 3.17.1 (`djangorestframework`) & Django CORS Headers 4.9.0 (`django-cors-headers`) for decoupled frontend integration.
- **Authentication & Security:** Django Auth System (Sessions, Cookies, Decorators, and Role-Based Access Control - RBAC).

### Frontend & UI
- **Structure & Styling:** HTML5, Tailwind CSS (CDN).
- **Logic & Interactivity:** Vanilla JavaScript / TypeScript logic (Modals, DOM event handling, keyboard shortcuts).
- **Data Visualization:** Chart.js (Dynamic and interactive charts).
- **Branding:** Official corporate logotype integrated across headers, login UI, and browser favicon.

### Database & Persistence
- **Engine:** SQLite3 (Local Development) / Configured for PostgreSQL (Production).
- **ORM:** Django ORM.
- **Image Management:** Pillow 12.3.0 (`Pillow`).

### Libraries & Reporting
- **openpyxl (v3.1.5):** Tabular report export/import in Microsoft Excel (.xlsx).
- **ReportLab (v5.0.0):** Dynamic PDF document generation (.pdf).

---

## 🔐 Live Demo Test Credentials

To evaluate the system under different access hierarchies:

### 🛠️ Admin User (Superuser)
- **Username:** `admin`
- **Password:** `administradorcerouno`
- **Permissions:** Full access to product management (Create/Read/Update/Delete), category administration, executive metrics on Dashboard, and Django `/admin/` panel.

### 👤 Employee User (Standard Operator)
- **Username:** `operador1`
- **Password:** `operador1`
- **Permissions:** Restricted catalog access (Read-Only mode), recording stock in/out movements, and viewing operation history.

---

## 🚀 Key Features Implemented

### 1. 🔐 Authentication, Session & Visual Identity
- Optimized login screen with vector branding and zero typographic redundancy.
- Global route protection using `@login_required` decorators across all critical views.
- Active user indicator and logout functionality in navigation header.

### 2. 👥 Role-Based Access Control (RBAC)
- Dynamic UI element hiding (*+ New Product*, *Categories*, *Dashboard*) based on user roles (`user.is_staff`).
- Employee-level restriction enforcing "Read-Only" labels on administrative actions.

### 3. 📦 Inventory & Product Module
- Full CRUD operations for products and categories (Admin restricted).
- Interactive table with processed thumbnail images.
- Low-stock dynamic badge alerts when current stock meets or drops below minimum thresholds.
- Advanced filtering: SKU/name search, category selection, and "Low stock only" conditional toggle.

### 4. 📋 Audit History & Movement Logs
- Inbound (`IN`) and Outbound (`OUT`) stock transactions automatically tied to authenticated users.
- Multi-criteria filtering by date range, product, movement type, and free search.
- **Report Exports:** Download filtered history in **PDF** (ReportLab) and **Excel** (openpyxl) formats.

### 5. 📊 Dashboard & Stock Turnover Analytics
- **KPI Metrics Panel:** Total inventory valuation ($), registered products count, low stock alerts, and active categories.
- **Dynamic Charts (Chart.js):** Product category distribution (Doughnut) and Top 5 items by outbound volume (Bar Chart).
- **Executive Turnover Report:** Timeframe analysis (7, 30, 90, 365 days) calculating Turnover Index, Dispatched Units, Capital in Stock, and deadstock identification.

# 📦 StockFlow - Sistema de Control de Inventario y Stock

**Desarrollado por:** Daniel Jiménez  
**Estado:** En desarrollo activo (v1.6 - Listo para Deploy)  
**LinkedIn:** https://www.linkedin.com/in/jimenezvalderramadaniel/  
**🚀 Demo en vivo / Web App:** https://stockflow-controlstock.onrender.com
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
- **Contraseña:** `administradorcerouno`
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