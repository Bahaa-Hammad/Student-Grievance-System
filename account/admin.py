from django.contrib import admin
from .models import Account
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Account
from .forms import UserCreationForm


class AccountAdmin(BaseUserAdmin):
    add_form = UserCreationForm

    list_display = ('email', 'is_staff',  'is_superuser')
    list_filter = ('is_superuser',)

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(Account, AccountAdmin)
