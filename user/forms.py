from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Bweller
from django.utils.translation import gettext_lazy as _
import hashlib

class LoginUserForm(forms.Form):
    username = forms.CharField(label='Логін', widget = forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget = forms.PasswordInput(attrs={'class': 'form-input'}))



from .models import Bweller

def generate_identifier(login, apartment_number):
    return hashlib.sha256(f'{login}{apartment_number}htEf5rg'.encode()).hexdigest()

class BwellerAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Підтвердження паролю', widget=forms.PasswordInput)

    class Meta:
        model = Bweller
        fields = ('login', 'email', 'phone', 'first_name', 'last_name', 'photo', 'apartment_number', 'is_admin', 'date_register', 'language')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Паролі не співпадають")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # Вычисляем identifier
        if user.login and user.apartment_number:
            user.identifier = generate_identifier(user.login, user.apartment_number)
        if commit:
            user.save()
        return user

class BwellerAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Bweller
        fields = ('login', 'password', 'email', 'phone', 'first_name', 'last_name', 'photo', 'identifier', 'apartment_number', 'is_admin', 'date_register', 'language')

    def clean_password(self):
        return self.initial["password"]



class BwellerRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )
    password2 = forms.CharField(
        label=_('Підтвердження паролю'),
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = Bweller
        fields = ('login', 'email', 'phone', 'first_name', 'last_name', 'photo', 'apartment_number', 'language')
        labels = {
            'login': _('Логін'),
            'email': _('Email'),
            'phone': _('Телефон'),
            'first_name': _("Ім'я"),
            'last_name': _('Прізвищє'),
            'photo': _('Фотографія'),
            'apartment_number': _('Номер квартири'),
            'language': _('Мова')
        }
        widgets = {
            'login': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'photo': forms.FileInput(attrs={'class': 'form-input'}),
            'language': forms.Select(
                choices=[('ua', _('Українська')), ('en', _('English'))],
                attrs={'class': 'form-input'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(BwellerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['language'].initial = 'ua'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Пароли не совпадают"))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if user.login and user.apartment_number:
            user.identifier = generate_identifier(user.login, user.apartment_number)
        if commit:
            user.save()
        return user



class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Email')
    apartment_number = forms.IntegerField(label='Номер квартири')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        apartment_number = cleaned_data.get('apartment_number')

        try:
            self.user = Bweller.objects.get(email=email, apartment_number=apartment_number)
        except Bweller.DoesNotExist:
            raise forms.ValidationError("Користувача із вказаною адресою електронної пошти та номером квартири не існує.")
        return cleaned_data
    

    def get_user(self):
        return self.user



class BwellerRedactionFormUA(forms.ModelForm):
    password1 = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )
    password2 = forms.CharField(
        label=_('Підтвердження паролю'),
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = Bweller
        fields = ('login', 'email', 'phone', 'first_name', 'last_name', 'photo', 'language',  'dey_limit', 'naight_limit')
        labels = {
            'login': _('Логін'),
            'email': _('Email'),
            'phone': _('Телефон'),
            'first_name': _("Ім'я"),
            'last_name': _('Прізвище'),
            'photo': _('Фотографія'),
            'language': _('Мова'),
            'dey_limit': _('Денний ліміт'),
            'naight_limit': _('Ночний ліміт')

        }
        widgets = {
            'login': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'photo': forms.FileInput(attrs={'class': 'form-input'}),
            'language': forms.Select(
                choices=[('ua', _('Україньска')), ('en', _('English'))],
                attrs={'class': 'form-input'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(BwellerRedactionFormUA, self).__init__(*args, **kwargs)
        self.fields['language'].initial = 'ua'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Паролі не збігаються"))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    


class BwellerRedactionFormEN(forms.ModelForm):
    password1 = forms.CharField(
    label=_('Password'),
    widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )
    password2 = forms.CharField(
    label=_('Password confirmation'),
    widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = Bweller
        fields = ('login', 'email', 'phone', 'first_name', 'last_name', 'photo', 'language',  'dey_limit', 'naight_limit')
        labels = {
            'login': _('Login'),
            'email': _('Email'),
            'phone': _('Phone'),
            'first_name': _("First Name"),
            'last_name': _('Last Name'),
            'photo': _('Photo'),
            'language': _('Language'),
            'dey_limit': _('Day Limit'),
            'naight_limit': _('Night Limit')
        }
        widgets = {
            'login': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'photo': forms.FileInput(attrs={'class': 'form-input'}),
            'language': forms.Select(
                choices=[('ua', _('Україньска')), ('en', _('English'))],
                attrs={'class': 'form-input'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(BwellerRedactionFormEN, self).__init__(*args, **kwargs)
        self.fields['language'].initial = 'ua'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

class BwellerRedactionFormUAAdmin(forms.ModelForm):
    password1 = forms.CharField(
    label=_('Пароль'),
    widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )
    password2 = forms.CharField(
    label=_('Підтвердження паролю'),
    widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = Bweller
        fields = ('login', 'email', 'phone', 'first_name', 'last_name', 'photo', 'language')
        labels = {
            'login': _('Логін'),
            'email': _('Email'),
            'phone': _('Телефон'),
            'first_name': _("Ім'я"),
            'last_name': _('Прізвище'),
            'photo': _('Фотографія'),
            'language': _('Мова'),

        }
        widgets = {
            'login': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'photo': forms.FileInput(attrs={'class': 'form-input'}),
            'language': forms.Select(
                choices=[('ua', _('Україньска')), ('en', _('English'))],
                attrs={'class': 'form-input'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(BwellerRedactionFormUAAdmin, self).__init__(*args, **kwargs)
        self.fields['language'].initial = 'ua'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Паролі не збігаються"))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    


class BwellerRedactionFormENAdmin(forms.ModelForm):
    password1 = forms.CharField(
    label=_('Password'),
    widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )
    password2 = forms.CharField(
    label=_('Password confirmation'),
    widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = Bweller
        fields = ('login', 'email', 'phone', 'first_name', 'last_name', 'photo', 'language')
        labels = {
            'login': _('Login'),
            'email': _('Email'),
            'phone': _('Phone'),
            'first_name': _("First Name"),
            'last_name': _('Last Name'),
            'photo': _('Photo'),
            'language': _('Language'),

        }
        widgets = {
            'login': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'photo': forms.FileInput(attrs={'class': 'form-input'}),
            'language': forms.Select(
                choices=[('ua', _('Україньска')), ('en', _('English'))],
                attrs={'class': 'form-input'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(BwellerRedactionFormENAdmin, self).__init__(*args, **kwargs)
        self.fields['language'].initial = 'ua'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user