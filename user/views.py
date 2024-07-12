from django.views import View
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import LoginUserForm, BwellerRegistrationForm, PasswordResetForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from .models import Bweller
from homecounter.models import Languages
from datetime import datetime, date
import hashlib


def get_language(leng='ua'):
    queryset = Languages.objects.all()
    leng_dict = {}
    if leng == 'ua':
        for obj in queryset:
            leng_dict[obj.key] = obj.ua
    return leng_dict

class LoginUserView(View):
    form_class = LoginUserForm
    template_name = 'index.html'  # Укажите здесь путь к вашему шаблону логина

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'leng': get_language()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            ip_address = request.META.get('REMOTE_ADDR')
            user = self.authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                user.time_identifier = hashlib.sha256(f'{user.login}2jk6lo{ip_address}{date.today()}'.encode()).hexdigest()
                user.save()
                if user.is_admin:
                    return redirect('profile/profile_admin/?time_identifier=' + str(user.time_identifier))
                else:
                    return redirect('profile/profile_user/?time_identifier=' + str(user.time_identifier))
            else:
                messages.error(request, 'Неправильный логин или пароль')
        else:
            messages.error(request, 'Форма заполнена некорректно')

        return render(request, self.template_name, {'form': form, 'leng': get_language()})

    def authenticate(self, request, username, password):
        try:
            user = Bweller.objects.get(login=username)
            if user.check_password(password):
                return user
        except Bweller.DoesNotExist:
            return None
        


class BwellerRegistrationView(View):
    form_class = BwellerRegistrationForm
    template_name = 'register.html'  # Укажите путь к вашему шаблону регистрации

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'leng': get_language()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # После регистрации перенаправляем пользователя
            return redirect(reverse_lazy('user:index')) 
        return render(request, self.template_name, {'form': form, 'leng': get_language()})
    



def password_reset_request_view(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_link = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))

            subject = "Password Reset Requested"
            message = render_to_string('password_reset_email.html', {
                'user': user,
                'reset_link': reset_link,
            })

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

            messages.success(request, "Password reset email has been sent.")
            return redirect('password_reset_done')

    else:
        form = PasswordResetForm()

    return render(request, 'password_reset_form.html', {'form': form, 'leng': get_language()})

def password_reset_confirm_view(request, uidb64=None, token=None):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Bweller.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Bweller.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password has been reset successfully.")
                return redirect('password_reset_complete')
            else:
                messages.error(request, "Passwords do not match.")

        return render(request, 'password_reset_confirm.html', {'validlink': True})

    else:
        return render(request, 'password_reset_confirm.html', {'validlink': False})

def password_reset_done_view(request):
    return render(request, 'password_reset_done.html')

def password_reset_complete_view(request):
    return render(request, 'password_reset_complete.html')