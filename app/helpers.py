import random
from django.core.cache import cache
import smtplib


def send_otp_to_email(mail, user_obj):

    if cache.get(mail):
        return False, cache.ttl(mail)
    try:
        otp_to_send = random.randint(100000, 999999)
        cache.set(mail, otp_to_send, timeout=60)
        user_obj.otp = otp_to_send
        print(user_obj.email)
        sender_email = "karthiksbh1@gmail.com"
        rec_email = "karthiksbh1@gmail.com"

        otp = str(user_obj.otp)

        # message_type = "OTP is: " + str(user_obj.otp)
        # message_type = str(message_type)

        message = f"""\n

            OTP is: {otp}."""

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, "dummy@1234")

        server.sendmail(sender_email, rec_email, message)
        print("OTP is: " + str(user_obj.otp))
        user_obj.save()
        return True, 0

    except Exception as e:
        print(e)
