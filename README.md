

# **Sigma Security**

---

Este proyecto ofrece una interfaz web interactiva diseñada para gestionar y analizar vulnerabilidades y amenazas en proyectos, incorporando diversas funcionalidades que permiten a los usuarios visualizar, consultar y recibir informes de seguridad de manera personalizada e intuitiva

---

## **Equipo**

### Miembros del equipo y datos de contacto

- **Esteban Sánchez Gámez** (estebansanchezgamez@gmail.com)  
- **Pablo Delgado Muñoz** (pablojesusdelgadomunoz@gmail.com)  
- **Dimitri Morgun** (palmaticdimim@gmail.com)  
- **Álvaro Pastor García** (alvaritopg23@gmail.com)  

### Capacidades y conocimientos del equipo

Nuestro equipo posee una sólida base técnica que abarca ciberseguridad, desarrollo web, inteligencia artificial y gestión de bases de datos. Contamos con experiencia en lenguajes como **Python**, **C**, **SQL** y **JavaScript**, además de herramientas como **LaTeX** y **APIs** de ciberseguridad. En el ámbito del desarrollo web, dominamos **HTML**, **CSS** y frameworks como **Flask**, lo que nos permite implementar un backend eficiente. Además, combinamos conocimientos en seguridad ofensiva y defensiva con habilidades en gestión de proyectos, lo que nos capacita para abordar los desafíos del proyecto de manera estratégica y efectiva.

---

## **Estructura General del Proyecto**

### **Producto**

Nuestro equipo desarrollará el **Sistema de Soporte para Vulnerabilidades y Amenazas basado en IA (SVAIA)**, una plataforma diseñada para identificar vulnerabilidades en los proyectos de los clientes mediante inteligencia artificial. Este sistema abordará la falta de herramientas eficientes para la consulta, monitorización y reporte de vulnerabilidades en entornos web y de software. SVAIA permitirá analizar, reportar y visualizar datos de ciberseguridad en distintos formatos, integrándose con APIs especializadas y ofreciendo un chatbot interactivo que responderá consultas y brindará asesoramiento personalizado a los usuarios.

### **Utilidad**

El **Sistema de Soporte para Vulnerabilidades y Amenazas basado en IA (SVAIA)** ofrece una plataforma eficiente y personalizable para la detección y gestión de vulnerabilidades en proyectos de software. A través de un **dashboard** intuitivo, cada usuario podrá consultar la seguridad de sus proyectos previamente analizados o crear nuevos análisis sin necesidad de repetir información, optimizando el uso de recursos y mejorando la **usabilidad** del sistema.  

Dentro del **dashboard**, los usuarios tendrán acceso a **analíticas detalladas**, podrán interactuar con un **chatbot inteligente** para resolver dudas y generar informes estructurados en **formatos descargables como PDF o CSV**, los cuales pueden enviarse por correo electrónico para auditorías.  

Este sistema está diseñado para facilitar el trabajo de **ingenieros de software y ciberseguridad**, así como de usuarios que inician en el desarrollo, proporcionando información clara y estructurada sobre vulnerabilidades. Al integrar reportes automáticos y consultas optimizadas, SVAIA mejora la eficiencia en la toma de decisiones y la respuesta ante amenazas, contribuyendo a la **seguridad y estabilidad de los proyectos**.

### **Viabilidad**

El proyecto es viable tanto desde una perspectiva académica como comercial. Las tecnologías necesarias (**IA**, **chatbots**, **APIs**, **dashboards personalizados**) están ampliamente disponibles y bien documentadas. Además, la optimización de consultas mediante el almacenamiento de resultados previos es técnica y fácilmente implementable.

El sistema es escalable y mantenible utilizando buenas prácticas de desarrollo, como **microservicios** y plataformas en la **nube**. La generación y envío de reportes también es factible con las herramientas actuales. En resumen, el proyecto puede llevarse a cabo de manera eficiente con los recursos y tecnologías disponibles.

### **Productos similares**

- **Darktrace**: Se enfoca en detectar comportamientos anómalos dentro de redes y sistemas en tiempo real utilizando IA. A diferencia de este proyecto, que se centra en la seguridad de proyectos específicos con un **dashboard** personalizado, Darktrace opera en un contexto más amplio, centrado en la seguridad de la infraestructura de TI.

- **Cortex XSOAR**: Automatiza la respuesta a incidentes y gestiona vulnerabilidades, con una fuerte integración de inteligencia de amenazas y flujos de trabajo automatizados. Mientras que el proyecto Sigma Security ofrece una consulta más personalizada y visualización de analíticas, Cortex XSOAR se enfoca más en la automatización de respuestas y acciones de mitigación.

- **IBM QRadar**: Es un sistema de gestión de eventos e información de seguridad (SIEM) que se centra en la recopilación y análisis de eventos de seguridad. A diferencia del proyecto Sigma Security, que prioriza la interacción con un **chatbot** y la personalización de reportes, IBM QRadar está más orientado a la detección de amenazas en tiempo real.

- **Qualys VMDR**: Detecta vulnerabilidades y gestiona el ciclo completo de parches. Aunque ofrece algunas funciones de informes y visualización, se enfoca principalmente en la gestión técnica de vulnerabilidades. El proyecto Sigma Security, por su parte, pone más énfasis en la experiencia del usuario y la interacción con el **chatbot**.


---

## **Restricciones e Información Adicional**

El Sistema de Soporte para Vulnerabilidades y Amenazas basado en IA (SVAIA) hará uso de diversas APIs de ciberseguridad, como ChatGPT, CVE y NIST, para obtener información actualizada sobre vulnerabilidades y amenazas. 

Sin embargo, el proyecto podría enfrentar ciertas limitaciones, principalmente relacionadas con la dependencia de estas APIs externas, que pueden imponer restricciones en el acceso a ciertos datos sensibles o en la disponibilidad de información en tiempo real.

Además, la integración de múltiples APIs requiere un manejo seguro de la información y una optimización en el número de consultas para garantizar el rendimiento del sistema.



---

## **Entrada de datos para el sistema**

**SVAIA** busca separar aplicaciones **web** de aplicaciones de **escritorio**, la entrada de datos debe adaptarse a cada tipo, ya que los riesgos y análisis son diferentes.

El formato de SBOM utilizado para este proyecto sigue el formato CycloneDX versión 1.4 y describe los componentes de software utilizados en una aplicación, junto con metadatos sobre la herramienta que generó el SBOM y las dependencias externas. Este SBOM se utilizará como una herramienta para extraer información detallada sobre los componentes de software y sus dependencias. La información contenida en el SBOM se integrará en una base de datos, donde será almacenada y organizada para su posterior análisis o modificación. Este análisis permitirá identificar posibles vulnerabilidades, gestionar licencias de uso, y evaluar la seguridad y compatibilidad de las librerías utilizadas. Al centralizar estos datos, se podrá realizar un seguimiento eficiente de los componentes de software y facilitar la toma de decisiones informadas para mejorar la seguridad y la gestión de los proyectos de desarrollo.

Una vez que el usuario eliga, si la aplicacion es web o desktop, se introducirá el sbom, siguiendo el siguiente formato.

### **Ejemplo SBOM**

```json 
   {
   "bomFormat": "CycloneDX",
   "specVersion": "1.4",
   "serialNumber": "urn:uuid:123e4567-e89b-12d3-a456-426614174000",
   "metadata": {
      "timestamp": "2024-02-25T12:00:00Z",
      "tools": [
         { "vendor": "SVAIA", "name": "SBOM Analyzer", "version": "1.0" }
      ],
      "component": {
         "type": "application",
         "name": "MiAplicacion",
         "version": "1.0",
         "description": "this app is for algorithmic trading",
         "licenses": [{ "id": "MIT" }],
         "externalReferences": [
         {
            "type": "VCS",       // (VCS / website) (github / repositorio descargable)
            "url": "https://github.com/miusuario/miaplicacion",
            "comment": "Código fuente del proyecto en GitHub"
         }
         ]
      }
   },
   "components": [
      {
         "type": "library",
         "name": "flask",
         "version": "2.1.3",
         "purl": "pkg:pypi/flask@2.1.3",
         "licenses": [{ "id": "BSD-3-Clause" }]
      },
      {
         "type": "library",
         "name": "requests",
         "version": "2.27.1",
         "purl": "pkg:pypi/requests@2.27.1",
         "licenses": [{ "id": "Apache-2.0" }]
      }
   ]
   }
```

### **Explicación SBOM**

1. bomFormat:
```json
"bomFormat": "CycloneDX"
```

**Descripción:** Especifica que el formato de este SBOM es CycloneDX, que es un estándar abierto para describir la composición de un software.

2. specVersion:
```json
"specVersion": "1.4"
```

**Descripción:** Indica la versión de la especificación CycloneDX que se está utilizando. En este caso, es la 1.4.

3. serialNumber:
```json
"serialNumber": "urn:uuid:123e4567-e89b-12d3-a456-426614174000"
```

**Descripción:** Es un identificador único universal (UUID) para este SBOM, lo que permite que cada archivo SBOM sea único e identificable

4. metadata:
```json
"metadata": {
      "timestamp": "2024-02-25T12:00:00Z",
      "tools": [
         { "vendor": "SVAIA", "name": "SBOM Analyzer", "version": "1.0" }
      ],
      "component": {
         "type": "application",
         "name": "MiAplicacion",
         "version": "1.0",
         "description": "this app is for algorithmic trading",
         "licenses": [{ "id": "MIT" }],
         "externalReferences": [
         {
            "type": "VCS",       // (VCS / website) (github / repositorio descargable)
            "url": "https://github.com/miusuario/miaplicacion",
            "comment": "Código fuente del proyecto en GitHub"
         }
         ]
      }
   }
```

**Descripción:** Aquí se incluyen metadatos sobre el SBOM y el componente que se está describiendo (la aplicación).

5. components

```json
"components": [
   {
      "type": "library",
      "name": "flask",
      "version": "2.1.3",
      "purl": "pkg:pypi/flask@2.1.3",
      "licenses": [{ "id": "BSD-3-Clause" }]
   },
   {
      "type": "library",
      "name": "requests",
      "version": "2.27.1",
      "purl": "pkg:pypi/requests@2.27.1",
      "licenses": [{ "id": "Apache-2.0" }]
   }
]
```

**Descripción:** Aquí se describen los componentes utilizados por la aplicación, que en este caso son librerías externas necesarias para el funcionamiento del software.

## **Salida de datos del sistema**

**Opciones de salida**

- Interfaz visual: Un dashboard con reportes interactivos.
- Reportes en archivos: Exportación en JSON, CSV, PDF para auditorías.
- Notificaciones: Alertas vía email o Telegram sobre vulnerabilidades críticas.

## **Diseño y Seguridad de la Página Web (por definir)**

### **HTML**

- `main.html`: Página principal de la aplicación web.

### **CSS**

- `login.css`: Estilos para la página de inicio de sesión.

### **JavaScript**

- `login.js`: Funcionalidades para la página de inicio de sesión.

---

## **Bases de Datos (por definir)**

---

## **Sistemas de Seguridad (por definir)**

---

## **Instalación**

Para ejecutar el proyecto, sigue estos pasos:

1. Clona este repositorio:
   ```bash
   git clone https://github.com/Sauvageduck24/sigma-security
   ```

2. Dirígete a la carpeta del proyecto y, una vez dentro, ejecuta el archivo `app.py` (es necesario estar dentro de la carpeta para que las rutas relativas funcionen correctamente).
   ```bash
   python app.py
   ```
---