Back-end Gimnasio y Rutina 🏋️‍♂️💪

Proyecto de gestión de gimnasio, rutinas e integración con desarrollo de backend y soluciones 

👥 Integrantes y Distribución de Hitos

Hito 1: Configuración del Proyecto y Modelado Base
Responsable: Javiera
Descripción: Creación del proyecto Django (gimnasio_project) y la aplicación website. 
Definición de los modelos iniciales de la base de datos, ejecución de migraciones en SQLite y 
configuración del panel de administración (admin.py).

📌 Hito 2: Vistas, Rutas y Plantillas Web
Responsable: Alejandro
Descripción: Desarrollo e integración de la interfaz de usuario. Creación de vistas en views.py, 
enrutamiento de URLs en urls.py, y diseño de plantillas HTML/CSS para la visualización del gimnasio y
rutinas públicas.

📌 Hito 3: Aplicación Móvil, Autenticación y Seguridad IoT
Responsable: Javiera
Descripción: Desarrollo de la aplicación móvil en Android Studio (Kotlin), 
implementación del sistema de autenticación (Login), comunicación inalámbrica (Wi-Fi/Bluetooth/MQTT) 
con sensores IoT y aplicación de la norma ISO 27400 para la protección de datos.

📌 Hito 4: Integración del Sistema y Pruebas
Responsables: Angel
Descripción: Interconexión entre la aplicación móvil Android y el backend Django. 
Pruebas integrales de flujo de datos en tiempo real, consumo de API/base de datos y validación de comunicación 
entre múltiples dispositivos.

📌 Hito 5: Despliegue, Documentación y Entrega Final
Responsable: Ángel
Descripción: Despliegue final del sistema, refinamiento de la interfaz de usuario, 
pruebas de estabilidad, documentación técnica detallada en el repositorio y presentación del proyecto final.

1. Requisitos de Instalación y Ejecución
- Repositorio: https://github.com/andre-nyx/Back-end_Gimnasio-y-Rutina.git
- cd Back-end_Gimnasio-y-Rutina

2. Crear y activar el entorno virtual
- python -m venv env
- Set-ExecutionPolicy Unrestricted -Scope Process
- .\env\Scripts\Activate

3. Instalar dependencias
- pip install django

4. Aplicar migraciones e iniciar servidor
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver
