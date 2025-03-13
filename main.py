import time
import socket
import datetime
import os

def check_internet(host="8.8.8.8", port=53, timeout=3):
    """Verifica si hay conexión a Internet intentando conectarse a un servidor DNS de Google."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

def get_log_file():
    """Devuelve el nombre del archivo de registro diario en la carpeta actual."""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    return f"internet_log_{today}.txt"

def log_event(message):
    """Registra un evento en el archivo de log."""
    with open(get_log_file(), "a") as log_file:
        log_file.write(message + "\n")

def get_monthly_log_file():
    """Devuelve el nombre del archivo de registro mensual en la carpeta actual."""
    month = datetime.datetime.now().strftime("%Y-%m")
    return f"internet_log_monthly_{month}.txt"

def log_monthly_event(message):
    """Registra un evento en el archivo de log mensual."""
    with open(get_monthly_log_file(), "a") as log_file:
        log_file.write(message + "\n")

def main():
    internet_status = check_internet()
    last_status = internet_status
    start_downtime = None
    total_downtime_daily = 0
    total_downtime_monthly = 0
    last_day = datetime.datetime.now().day
    last_month = datetime.datetime.now().month
    log_file = get_log_file()

    # Asegurar que el archivo de log tenga el encabezado del día
    if not os.path.exists(log_file):
        log_event("Registro de Internet para " + datetime.datetime.now().strftime("%Y-%m-%d"))
        log_event("-------------------------------------------")

    while True:
        internet_status = check_internet()
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        current_day = datetime.datetime.now().day
        current_month = datetime.datetime.now().month

        if internet_status and not last_status:
            # Internet ha vuelto
            downtime_duration = (datetime.datetime.now() - start_downtime).total_seconds() // 60
            total_downtime_daily += downtime_duration
            total_downtime_monthly += downtime_duration
            log_event(f"Internet volvió a las {current_time} después de {int(downtime_duration)} minutos de caída.")
            start_downtime = None
        elif not internet_status and last_status:
            # Internet se ha caído
            start_downtime = datetime.datetime.now()
            log_event(f"Internet se cayó a las {current_time}.")

        # Guardar el estado actual para la próxima iteración
        last_status = internet_status

        # Cada día, actualizar el resumen de tiempo sin Internet y resetear el contador diario
        if current_day != last_day:
            log_event(f"Resumen del día: {int(total_downtime_daily)} minutos sin Internet.")
            total_downtime_daily = 0
            last_day = current_day

        # Cada mes, actualizar el resumen de tiempo sin Internet y resetear el contador mensual
        if current_month != last_month:
            log_monthly_event(f"Resumen del mes: {int(total_downtime_monthly)} minutos sin Internet.")
            total_downtime_monthly = 0
            last_month = current_month

        time.sleep(60)  # Espera un minuto antes de la siguiente verificación

if __name__ == "__main__":
    main()
