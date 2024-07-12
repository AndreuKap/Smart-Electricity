from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password, check_password as default_check_password
import os


class Flats(models.Model):
    apartment_number = models.IntegerField(blank=False, null=False, unique=True)
    rooms = models.IntegerField(blank=False, null=False)
    bweller = models.IntegerField(blank=False, null=False)
    power = models.FloatField(blank=False, null=False)

    def __str__(self):
        return f"{self.apartment_number}"

    class Meta:
        ordering = ["number"]
        verbose_name = "Flat"
        verbose_name_plural = "Flats"

class BwellerManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError(_('The Login field must be set'))
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(login, password, **extra_fields)
    

def get_upload_path(instance, filename):
    return os.path.join('static', 'photos', filename)

class Bweller(AbstractBaseUser, PermissionsMixin):
    login = models.CharField(_('login'), max_length=50, unique=True)
    email = models.EmailField(_('email address'), blank=True, null=True)
    phone = models.CharField(_('phone'), max_length=20, blank=True, null=True)
    first_name = models.CharField(_('first name'), max_length=50, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=50, blank=True, null=True)
    photo = models.ImageField(_('photo'), blank=True, null=True, upload_to = get_upload_path)
    identifier = models.CharField(_('identifier'), max_length=64, blank=True, null=True)
    apartment_number = models.OneToOneField('Flats', on_delete=models.CASCADE, related_name='number', primary_key=True)
    is_admin = models.BooleanField(_('admin status'), default=False)
    date_register = models.DateTimeField(_('date registered'), null=True, default=timezone.now)
    language = models.CharField(_('language'), max_length=2, blank=True, null=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    last_login = models.DateTimeField(_('last login'), default=timezone.now)
    time_identifier = models.CharField(_('time identifier'), max_length=64, blank=True, null=True)
    dey_limit = models.FloatField(_('dey limit'), blank=True, default=32)
    naight_limit = models.FloatField(_('night limit'), blank=True, default=11)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name="bweller_set",  
        related_query_name="bweller",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="bweller_set",  
        related_query_name="bweller",
    )

    objects = BwellerManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = _("Bweller")
        verbose_name_plural = _("Bwellers")

    def check_password(self, raw_password):
        return default_check_password(raw_password, self.password)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.login