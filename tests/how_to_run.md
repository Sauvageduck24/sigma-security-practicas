# Pruebas unitarias y de integración para Sigma Security

Este directorio contiene las pruebas automáticas para la API, la base de datos y el endpoint de chat de la aplicación.

## Estructura de los tests

- **conftest.py**: Define fixtures reutilizables para pytest, incluyendo la creación de una app Flask de prueba y una base de datos SQLite en memoria para aislar los tests.
- **test_api.py**: Pruebas unitarias para los endpoints REST principales:
  - `/api/usuarios`: creación, consulta y borrado de usuarios.
  - `/api/proyectos`: creación y consulta de proyectos.
  - `/api/mensajes`: creación y consulta de mensajes.
- **test_chat.py**: Pruebas para el endpoint `/chat/send-message`, usando mocks para simular la respuesta del backend externo.

## Cómo ejecutar los tests

1. **Instala las dependencias necesarias:**

   Asegúrate de tener un entorno virtual activo y ejecuta:
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecuta los tests:**

   Desde la raíz del proyecto, ejecuta:
   ```bash
   pytest
   ```
   Esto buscará automáticamente todos los archivos que comiencen con `test_` en la carpeta `tests/` y ejecutará las pruebas.

3. **Opcional: Ver reporte detallado**

   Para ver un reporte más detallado, puedes usar:
   ```bash
   pytest -v
   ```

## Notas profesionales
- Los tests usan una base de datos en memoria, por lo que no afectan tus datos reales.
- Se recomienda ejecutar los tests antes de cada despliegue o cambio importante.
- Puedes ampliar los tests agregando más casos en los archivos existentes o creando nuevos archivos `test_*.py`.
