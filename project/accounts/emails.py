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
    
    
def send_otp_for_reset_password(email,otp):
    subject = "Şifrənizin yenilənməsi üçün doğrulama kodu"
    reset_password_otp = otp
    message = f"Şifrə yeniləmə OTP kodunuz: {reset_password_otp}"
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])
    account = Account.objects.get(email=email)
    account.reset_password_otp = reset_password_otp
    account.save()
    