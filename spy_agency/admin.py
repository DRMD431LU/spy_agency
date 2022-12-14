from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import SpyUser, Hit, Assignment, HitmanUser, BossUser,HitmanAssignedBoss
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        "username",
        "is_superuser",
    ]
    list_display_links = ('username',)

admin.site.register(SpyUser, CustomUserAdmin)
admin.site.register(Hit)
admin.site.register(Assignment)
admin.site.register(HitmanUser)
admin.site.register(BossUser)
admin.site.register(HitmanAssignedBoss)