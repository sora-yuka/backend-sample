from django.contrib import admin
from django.db.models import Model
from django.contrib.admin.exceptions import AlreadyRegistered
from django.contrib.auth import get_user_model

# Register your models here.

User = get_user_model()


def admin_register(model: Model, admin_class: admin.ModelAdmin = None) -> None:
    try:
        admin.site.register(model, admin_class)
    except AlreadyRegistered:
        pass
    
admin_register(model=User)