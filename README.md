# Sistema de Envío Automático de Correos de Alertas

Este proyecto es un script en Python para enviar correos electrónicos de alerta basados en actividades programadas, leyendo los datos desde un archivo CSV. Cuenta con un sistema simple para evitar enviar correos repetidos según la frecuencia (diaria, semanal, mensual) definida para cada actividad.

---

## Características principales

- Lee las actividades desde un archivo CSV con columnas:  
  `Proceso, FechaInicio, FechaFin, Hora, Actividad, Encargado, Estatus, Frecuencia`.
- Envía correos a los encargados de cada actividad usando SMTP.
- Controla los envíos para no repetir correos antes de tiempo según la frecuencia:  
  - Diario: máximo 1 correo por día.  
  - Semanal: máximo 1 correo por semana.  
  - Mensual: máximo 1 correo por mes.
- Registra los envíos en un archivo `enviados.log` para mantener el control.
- Fácil configuración mediante archivo `.env` para datos SMTP y rutas.

---

## Requisitos

- Python 3.7 o superior  
- Paquetes Python:
  - pandas  
  - python-dotenv

---

## Instalación

1. Clona este repositorio:

   ```bash
   git clone [https://github.com/tu_usuario/tu_repositorio.git](https://github.com/DenzelRdz/demo-emails.git)
   cd demo-emails

2. Instala las dependencias

    pip install -r requirements.txt

3. Crea un archivo .env con tus datos SMTP y configuración, por ejemplo:

    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_USER=tu_correo@gmail.com
    EMAIL_PASSWORD=tu_token_o_contraseña
    CSV_FILE=actividades.csv
    REMINDER_DAYS=3

4. Prepara tu archivo actividades.csv con el formato esperado

    Proceso,FechaInicio,FechaFin,Hora,Actividad,Encargado,Estatus,Frecuencia
    App1,08/08/2025,15/08/2025,09:00,Prueba QA,correo@ejemplo.com,Pendiente,Diaria

## Uso

Para ejecutar el script manualmente:
    ```bash
    python enviar_alertas.py

El script verificará las actividades próximas a iniciar según REMINDER_DAYS, enviará alertas a los encargados, y controlará los envíos para no repetir correos innecesarios.


## Notas
- Para pruebas rápidas, puedes modificar el archivo enviados.log para simular fechas de envío pasadas y permitir reenvíos.

- Para producción, considera automatizar la ejecución con un scheduler o migrar a un entorno en la nube como Azure Functions.

- El log enviados.log puede crecer con el tiempo; puedes implementar rotación o migrar el control a una base de datos.
