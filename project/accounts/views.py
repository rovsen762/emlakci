
from .models import Account, Plan, AccountCustomers, AccountFilters, AccountCustomerPreferries,Balance, PreferryPriority, AccountFilterMatch, Subscription, AccountPayments
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AccountCreationForm, LoginForm, ForgotPasswordForm, VerifyForgotPasswordOtpForm, ResetPasswordForm,VerifyRegisterOtpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.utils import timezone
from .emails import send_otp_via_email, send_otp_for_reset_password
from datetime import timedelta
import random
from utils.decorators import redirect_authenticated_user
from datetime import datetime

###############AUTHENTICATION VIEWS################

def generate_otp():
    return str(random.randint(100000, 999999))

MAX_DAILY_RESET_REQUEST = 5
MAX_DAILY_REGISTER_REQUEST = 5
OTP_EXPIRY_MINUTES = 5


# Register view
def register(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            if Account.objects.filter(email=email).exists():
                messages.error(request, "Bu email artıq istifadə olunub.")
                return render(request, 'register.html', {'form': form})

            otp = generate_otp()
            request.session['register_data'] = form.cleaned_data
            request.session['register_otp'] = otp
            request.session['register_otp_created_at'] = timezone.now().isoformat()

            send_otp_via_email(email, otp)  # modela yazma, yalnız email göndər

            messages.success(request, "Email-ə OTP göndərildi. Zəhmət olmasa daxil edin.")
            return redirect('verify-register-otp')
    else:
        form = AccountCreationForm()

    return render(request, 'register.html', {'form': form})



def verify_register_otp(request):
    otp = request.session.get('register_otp')
    otp_created_at = request.session.get('register_otp_created_at')
    register_data = request.session.get('register_data')

    if not otp or not register_data:
        return redirect('register')

    if request.method == 'POST':
        form = VerifyRegisterOtpForm(request.POST)
        if form.is_valid():
            otp_created_at_dt = datetime.fromisoformat(otp_created_at)

            # OTP expiry yoxla
            if timezone.now() > otp_created_at_dt + timedelta(minutes=OTP_EXPIRY_MINUTES):
                messages.error(request, "OTP müddəti bitmişdir. Yenidən göndərin.")
                return redirect('register')

            entered_otp = form.cleaned_data['otp']
            if entered_otp != otp:
                messages.error(request, "OTP yanlışdır.")
                return render(request, 'verify-register-otp.html', {'form': form})

            # OTP düzgündür → hesab yaradılır
            form_data = register_data
            user = Account.objects.create_user(
                username=form_data['username'],
                email=form_data['email'],
                password=form_data['password1'],
            )
            user.is_verified = True
            user.save()

            # Session-u təmizlə
            for key in ['register_otp', 'register_otp_created_at', 'register_data']:
                request.session.pop(key, None)

            messages.success(request, "Hesab uğurla yaradıldı. İndi daxil ola bilərsiniz.")
            return redirect('login')

        else:
            # form invalid olduqda input field görünsün
            return render(request, 'verify-register-otp.html', {'form': form})

    else:
        form = VerifyRegisterOtpForm()

    return render(request, 'verify-register-otp.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            user = authenticate(request, username=username,
                                        password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    if remember_me:
                        request.session.set_expiry(1209600)
                    else:
                        request.session.set_expiry(86400)
                    return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})




def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            account = Account.objects.filter(email=email, is_active=True).first()

            success_message = "Şifrə sıfırlama e-maili göndərildi."

            if account:
                today = timezone.now().date()

                if account.last_reset_password_request_date != today:
                    account.reset_password_request_count = 0

                if account.reset_password_request_count >= MAX_DAILY_RESET_REQUEST:
                    messages.error(request, "Bu gün üçün maksimum şifrə sıfırlama limitinə çatmısınız.")
                    return render(request, 'forgot-password.html', {'form': form})

                otp = generate_otp()
                account.reset_password_otp = otp
                account.reset_password_otp_created_at = timezone.now()
                account.reset_password_request_count += 1
                account.last_reset_password_request_date = today
                account.is_reset_password_otp_verified = False
                account.save()

                send_otp_for_reset_password(email, otp)

                request.session['reset_user_id'] = account.id

                messages.success(request, success_message)
                return redirect('verify-forgot-password-otp')
        
            else:
                messages.error(request, "Bu email adresinə sahib aktiv istifadəçi yoxdur.")
        
        else:
            messages.error(request, "Email daxil edin.")

    else:
        form = ForgotPasswordForm()

    return render(request, 'forgot-password.html', {'form': form})


def verify_forgot_password_otp(request):
    user_id = request.session.get('reset_user_id')

    if not user_id:
        return redirect('forgot-password')

    account = Account.objects.filter(id=user_id).first()
    if not account:
        return redirect('forgot-password')

    if request.method == 'POST':
        form = VerifyForgotPasswordOtpForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']

            if not account.reset_password_otp_created_at or \
               timezone.now() > account.reset_password_otp_created_at + timedelta(minutes=OTP_EXPIRY_MINUTES):
                messages.error(request, "OTP müddəti bitmişdir.")
                return redirect('forgot-password')

            if account.reset_password_otp != otp:
                messages.error(request, "OTP yanlışdır.")
                return render(request, 'verify-forgot-password-otp.html', {'form': form})

            account.reset_password_otp = None
            account.is_reset_password_otp_verified = True
            account.save()

            return redirect('reset-password')

    else:
        form = VerifyForgotPasswordOtpForm()

    return render(request, 'verify-forgot-password-otp.html', {'form': form})



def reset_password(request):
    user_id = request.session.get('reset_user_id')

    if not user_id:
        return redirect('forgot-password')

    account = Account.objects.filter(id=user_id).first()

    if not account or not account.is_reset_password_otp_verified:
        return redirect('forgot-password')

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                messages.error(request, "Şifrələr uyğun gəlmir.")
                return render(request, 'reset-password.html', {'form': form})

            account.set_password(password)
            account.is_reset_password_otp_verified = False
            account.last_reset_password_date = timezone.now().date()
            account.save()

            del request.session['reset_user_id']

            messages.success(request, "Şifrə uğurla dəyişdirildi.")
            return redirect('login')

    else:
        form = ResetPasswordForm()

    return render(request, 'reset-password.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')








######################MEMBERS#################################


@login_required(login_url='login')
def customer_list(request):
    account = request.user
    account_customers = AccountCustomers.objects.filter(account=account)
    context = {
        'account': account,
        'account_customers': account_customers
    }
    return render(request, 'customer-list.html', context)


@login_required(login_url='login')
def customer_grid(request):
    account = request.user
    account_customers = AccountCustomers.objects.filter(account=account)
    context = {
        'account': account,
        'account_customers': account_customers
    }
    return render(request, 'customer-grid.html', context)


@login_required(login_url='login')
def customer_details(request, customer_id):
    account = request.user
    customer = get_object_or_404(AccountCustomers, id=customer_id, account=account)
    context = {
        'account': account,
        'customer': customer
    }
    return render(request, 'customers-details.html', context)



@login_required(login_url='login')
def profile(request):
    account = request.user
    account_payments = AccountPayments.objects.filter(account=account).order_by('-payment_date')
    context = {
        'account': account,
        'account_payments': account_payments
    }
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def settings(request):
    account = request.user
    # if request.method == 'POST':
    #     form = AccountUpdateForm(request.POST, request.FILES, instance=account)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, "Profiliniz uğurla güncellendi.")
    #         return redirect('settings')
    # else:
    #     form = AccountUpdateForm(instance=account)

    context = {
        'account': account,
    }
    return render(request, 'settings.html', context)



@login_required(login_url='login')
def transactions(request):
    account = request.user
    account_payments = AccountPayments.objects.filter(account=account).order_by('-payment_date')
    context = {
        'account': account,
        'account_payments': account_payments
    }
    return render(request, 'transactions.html', context)

















# class WishlistListView(LoginRequiredMixin, ListView):
#     model = Wishlist
#     template_name = 'bookmark.html'
#     context_object_name = 'wishlist_announcements'
#     paginate_by = 1
    
#     def get_queryset(self):
#         customer = self.request.user
#         return super().get_queryset().filter(customer=customer)
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         customer = self.request.user
#         context['customer'] = self.request.user
#         context['customer_announcement_count'] = Announcement.objects.filter(customer=customer).count()
#         return context
    

# def pricing(request):
#     packages = Package.objects.all()
#     context =  {
#         'packages': packages
#     }
#     return render(request, 'price.html',context)


# def dashboard(request,customer_id):
#     customer = get_object_or_404(Account, pk=customer_id)
#     is_own_profile = customer == request.user
#     all_announcements_count = Announcement.objects.filter(customer=customer).count()
#     active_announcements_count = Announcement.objects.filter(customer=customer,is_active=True).count()
#     sale_announcements_count = Announcement.objects.filter(customer=customer,is_rent=False).count()
#     rent_announcements_count = Announcement.objects.filter(customer=customer,is_rent=True).count()
#     context =  {
#         'customer': customer,
#         'all_announcements_count': all_announcements_count,
#         'active_announcements_count': active_announcements_count,
#         'sale_announcements_count': sale_announcements_count,
#         'rent_announcements_count': rent_announcements_count,
#         'is_own_profile': is_own_profile
#     }
#     return render(request, 'dashboard.html',context)


# def customer_announcements(request,customer_id):
#     customer = get_object_or_404(Customer, pk=customer_id)
#     customer_announcements  = Announcement.objects.filter(customer=customer)
#     is_own_profile = customer == request.user
#     context =  {
#         'customer': customer,
#         'customer_announcements': customer_announcements,
#         'is_own_profile': is_own_profile
#     }
#     return render(request, 'my-ads.html', context)

# @login_required
# def profile(request):
#     customer = request.user
#     customer_announcements_count = Announcement.objects.filter(customer=customer).count()
#     customer_soc_medias = CustomerSocMedia.objects.filter(customer=customer)

#     context = {
#         'customer': customer,
#         'customer_announcements_count': customer_announcements_count,
#         'customer_soc_medias': customer_soc_medias
#     }
#     return render(request, 'profile.html',context)


# @login_required
# def setting(request):
#     customer = request.user
#     customer_announcements_count = Announcement.objects.filter(customer=customer).count()

    
#     context = {
#         'customer': customer,
#         'customer_announcements_count': customer_announcements_count
#     }
#     return render(request, 'setting.html',context)