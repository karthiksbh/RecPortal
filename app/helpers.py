import random
import smtplib
from email.message import EmailMessage


def send_otp_to_email(mail, user_obj):
    try:
        otp_to_send = random.randint(100000, 999999)
        user_obj.otp = otp_to_send
        rec_email = user_obj.email
        sender_email = "iete.vit2021@gmail.com"

        otp = str(user_obj.otp)

        msg = EmailMessage()
        message = "Dear Student, Please use the following OTP " + \
            str(otp) + " to complete the email verification"
        msg.set_content(message)

        msg['Subject'] = 'One Time Password(OTP) Confirmation'
        msg['From'] = sender_email
        msg['To'] = rec_email

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, "Velk@1205")
        server.send_message(msg)
        server.quit()

        print("This is the user obj:======================== " + user_obj)

        print("=======================" + otp_to_send)

        user_obj.save()

        return True, 0

    except Exception as e:
        print(e)
