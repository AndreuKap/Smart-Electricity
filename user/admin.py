from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import BwellerAdminCreationForm, BwellerAdminChangeForm, PasswordResetForm
from .models import Bweller, Flats

class BwellerAdmin(BaseUserAdmin):
    # Формы для добавления и изменения экземпляров пользователя
    form = BwellerAdminChangeForm
    add_form = BwellerAdminCreationForm

    # Поля, которые будут использоваться при отображении модели пользователя.
    # Они переопределяют определения базового UserAdmin, которые ссылается на модель пользователя по умолчанию.
    list_display = ('login', 'email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email', 'phone', 'photo', 'identifier', 'apartment_number', 'date_register', 'language')}),
        ('Права доступа', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login', 'email', 'password1', 'password2', 'apartment_number')}
        ),
    )
    search_fields = ('login', 'email')
    ordering = ('login',)
    filter_horizontal = ('groups', 'user_permissions')

@admin.register(Flats)
class FlatsAdmin(admin.ModelAdmin):
    list_display = ('apartment_number', 'rooms', 'bweller', 'power')
    search_fields = ('apartment_number', 'bweller')

admin.site.register(Bweller, BwellerAdmin)