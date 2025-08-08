import os
import smtplib
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
CSV_FILE = os.getenv("CSV_FILE")
REMINDER_DAYS = int(os.getenv("REMINDER_DAYS", 3))

LOG_FILE = "enviados.log"

def leer_log():
    enviados = {}
    if not os.path.exists(LOG_FILE):
        return enviados
    with open(LOG_FILE, "r") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            proceso, encargado, fecha_str = linea.split("|")
            fecha_envio = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            enviados[(proceso, encargado)] = fecha_envio
    return enviados

def registrar_envio(proceso, encargado):
    hoy = datetime.now().date()
    with open(LOG_FILE, "a") as f:
        f.write(f"{proceso}|{encargado}|{hoy}\n")

def puede_enviar(proceso, encargado, frecuencia):
    enviados = leer_log()
    hoy = datetime.now().date()

    if (proceso, encargado) not in enviados:
        return True  # Nunca enviado

    ultima_fecha = enviados[(proceso, encargado)]

    if frecuencia == "diaria":
        # Enviar máximo 1 vez al día
        return ultima_fecha < hoy
    elif frecuencia == "semanal":
        return (hoy - ultima_fecha).days >= 7
    elif frecuencia == "mensual":
        mes_actual = hoy.month
        mes_ultimo = ultima_fecha.month
        año_actual = hoy.year
        año_ultimo = ultima_fecha.year
        # Enviar si ya cambió de mes o año
        return (año_actual > año_ultimo) or (mes_actual > mes_ultimo)
    else:
        # Por defecto permitir enviar
        return True

def enviar_correo(destinatario, asunto, cuerpo):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = destinatario
        msg["Subject"] = asunto
        msg.attach(MIMEText(cuerpo, "plain"))

        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"✅ Correo enviado a {destinatario}")
    except Exception as e:
        print(f"❌ Error enviando correo a {destinatario}: {e}")

def verificar_actividades():
    df = pd.read_csv(CSV_FILE)
    hoy = datetime.now().date()

    for _, row in df.iterrows():
        fecha_inicio = datetime.strptime(row["FechaInicio"], "%d/%m/%Y").date()
        fecha_fin = datetime.strptime(row["FechaFin"], "%d/%m/%Y").date()

        dias_restantes = (fecha_inicio - hoy).days

        # Solo actividades pendientes y que empiecen dentro de REMINDER_DAYS
        if 0 <= dias_restantes <= REMINDER_DAYS and row["Estatus"].strip().lower() == "pendiente":
            frecuencia = row["Frecuencia"].strip().lower()
            if puede_enviar(row['Proceso'], row['Encargado'], frecuencia):
                asunto = f"Recordatorio: {row['Actividad']} ({row['Proceso']})"
                cuerpo = (
                    f"Hola,\n\n"
                    f"Esta es una alerta para la actividad '{row['Actividad']}' "
                    f"del proceso '{row['Proceso']}'.\n"
                    f"Fecha de inicio: {row['FechaInicio']} a las {row['Hora']}.\n"
                    f"Frecuencia: {row['Frecuencia']}.\n"
                    f"Estatus: {row['Estatus']}.\n\n"
                    f"Por favor, recuerda realizarla.\n\n"
                    f"Saludos."
                )
                enviar_correo(row["Encargado"], asunto, cuerpo)
                registrar_envio(row['Proceso'], row['Encargado'])
            else:
                print(f"⏩ Ya se envió alerta reciente para {row['Actividad']} ({frecuencia}) a {row['Encargado']}")

if __name__ == "__main__":
    verificar_actividades()
