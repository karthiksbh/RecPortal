import random
from django.core.cache import cache


def send_otp_to_email(mail, user_obj):

    if cache.get(mail):
        return False, cache.ttl(mail)
    try:
        otp_to_send = random.randint(100000, 999999)
        cache.set(mail, otp_to_send, timeout=60)
        user_obj.otp = otp_to_send
        user_obj.save()
        return True, 0

    except Exception as e:
        print(e)
