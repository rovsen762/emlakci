from django.core.mail import send_mail
import random
from django.conf import settings
from .models import Account


def send_otp_via_email(email):
    subject = "Hesabınızın email doğrulanması"
    otp = random.randint(100000, 999999)
    message = f"Sizin OTP kodunuz: {otp}"
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])
    customer = Account.objects.get(email=email)
    customer.otp = otp
    customer.save()
    
    
def send_otp_for_reset_password(email):
    subject = "Şifrənizin yenilənməsi üçün doğrulama kodu"
    reset_password_otp = random.randint(100000, 999999)
    message = f"Şifrə yeniləmə OTP kodunuz: {reset_password_otp}"
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])
    customer = Account.objects.get(email=email)
    customer.reset_password_otp = reset_password_otp
    customer.save()
    