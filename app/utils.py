import random
from email.message import EmailMessage
import os


class Util:
    @staticmethod
    def send_otp_to_email(mail, user_obj):
        try:
            otp_to_send = random.randint(100000, 999999)
            user_obj.otp = otp_to_send
            rec_email = user_obj.email
            user_obj.save()

            otp = str(user_obj.otp)
            message = "Dear Student, Please use the following OTP " + \
                str(otp) + " to complete the email verification"

            data = {
                'subject': 'One Time Password(OTP) Confirmation',
                'body': message
            }

            subject, from_email, to = data['subject'], os.environ.get(
                'EMAIL_FROM'), rec_email
            body = data['body']

            email = EmailMessage(subject, body,
                                 from_email, [to])
            email.send()
            return True, 0

        except Exception as e:
            print(e)
