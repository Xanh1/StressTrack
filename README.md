# Proyecto de Test de Estrés

Este es un proyecto para gestionar y realizar tests de estrés en estudiantes. El sistema permite a los profesores crear y asignar tests, mientras que los estudiantes pueden realizar estos tests y revisar su progreso.

## Requisitos

- Django 4.x o superior
- Python 3.x
- Base de datos (SQLite, PostgreSQL, etc.)
- Bootstrap 5 (opcional para el diseño)
- Otras dependencias: `django-crispy-forms`, `django-messages`, etc.

---

## Funcionalidades Implementadas

A continuación se muestra una lista de las características implementadas y las que faltan por hacer.

### Funcionalidades Completadas ✅

- [x] **Sistema de autenticación de usuarios** (Login, Logout, Registro de usuarios)
- [x] **Vista de lista de tests**: Muestra una lista de los tests disponibles y permite que los estudiantes los realicen.
- [x] **Creación de tests** (para profesores): Permite a los profesores crear un test con preguntas y respuestas.
- [x] **Asignación de tests a grupos**: Los profesores pueden asignar tests a los grupos de estudiantes.
- [x] **Respuesta a los tests** (para estudiantes): Los estudiantes pueden responder a los tests asignados.
- [x] **Visualización de los resultados** (para estudiantes): Los estudiantes pueden ver si han completado un test y el estado de sus respuestas.
- [x] **Sistema de mensajes**: Permite mostrar mensajes al usuario (éxito, error, etc.).
- [x] **Tag personalizado** para verificar si un grupo está asignado a un test.

### Funcionalidades Pendientes ⏳

- [ ] **Modificación de tests**: Los profesores deberían poder modificar un test después de haberlo creado (agregar/eliminar preguntas, cambiar el título).
- [ ] **Eliminación de tests**: Los profesores deben poder eliminar tests que ya no sean necesarios.
- [ ] **Respuestas y resultados de los tests**: Implementar la lógica para almacenar y mostrar las respuestas correctas de los estudiantes.
- [ ] **Página de detalles de un test**: Los estudiantes deberían poder ver más detalles sobre un test antes de realizarlo.
- [ ] **Notificaciones para los estudiantes**: Los estudiantes deberían recibir notificaciones cuando se les asignen nuevos tests.
- [ ] **Interfaz de usuario (UI)**: Mejorar la interfaz de usuario para hacerla más amigable y atractiva.
- [ ] **Pruebas unitarias**: Agregar pruebas unitarias para validar el correcto funcionamiento de las vistas, modelos y lógica de negocio.


---

## Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/Xanh1/StressTrack.git

### 2.asdasd

