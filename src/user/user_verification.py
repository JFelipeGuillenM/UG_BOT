import pyotp
import smtplib
from email.mime.text import MIMEText
from config import EMAIL_SENDER, EMAIL_PASSWORD

def generate_otp():
    """Genera un OTP con una duración de 5 minutos."""
    secret = pyotp.random_base32()  # Esto debe ser una cadena en base32
    totp = pyotp.TOTP(secret, interval=300)  # 300 segundos = 5 minutos
    return totp.now(), secret

def send_otp_email(recipient_email, otp):
    """Envía el OTP al correo electrónico del usuario."""
    # Configura el mensaje
    msg = MIMEText("Tu código de verificación es: " + otp)
    msg['Subject'] = 'Código de Verificación'
    msg['From'] = EMAIL_SENDER
    msg['To'] = recipient_email

    # Conecta al servidor SMTP y envía el correo
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, recipient_email, msg.as_string())

def verify_otp(otp, user_input):
    """Verifica si el OTP ingresado por el usuario es correcto."""
    totp = pyotp.TOTP(otp, interval=300)  # 300 segundos = 5 minutos
    return totp.verify(user_input)