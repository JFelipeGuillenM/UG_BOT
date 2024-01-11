from config import *
from user.user_verification import generate_otp, send_otp_email
from config.database import connect_to_db
import re

def is_user_registered(chat_id):
    # Aquí se conecta a la base de datos y verifica si el usuario está registrado
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios WHERE tele_chat_id = %s", (chat_id,))
    user_exists = cur.fetchone() is not None
    cur.close()
    conn.close()
    return user_exists

def register_user(correo, chat_id):
    # Aquí se conecta a la base de datos y registra el nuevo usuario
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO usuarios (correo_electronico, tele_chat_id, fecha_registro) VALUES (%s, %s, NOW());", (correo, chat_id))
    conn.commit()
    cur.close()
    conn.close()

def unregister_user(chat_id):
    # Código para eliminar el usuario de la base de datos
    conn = connect_to_db()
    cur = conn.cursor()
    # Primero, eliminar las interacciones del usuario
    cur.execute("DELETE FROM interacciones_usuario WHERE id_usuario = (SELECT id FROM usuarios WHERE tele_chat_id = %s);", (chat_id,))
    cur.execute("DELETE FROM usuarios WHERE tele_chat_id = %s;", (chat_id,))
    conn.commit()
    cur.close()
    conn.close()

""" Solicita el correo al usuario """    
def get_mail_from_user(message, bot, estado):
    chat_id = message.chat.id
    correo = message.text
    if re.match(r"^[a-zA-Z0-9._%+-]+@ug\.edu\.ec$", correo):
        otp, secret = generate_otp()
        send_otp_email(correo, otp)
        bot.send_message(chat_id, "Se ha enviado un código de verificación a tu correo electrónico...")
        return secret  # Devuelve y almacena el secreto en base32
    else:
        bot.send_message(chat_id, "Correo inválido, asegúrate de que termine en @ug.edu.ec")
        return None

