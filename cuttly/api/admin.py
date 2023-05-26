from django.contrib import admin

from .models import *
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User

    def save_model(self, request, obj, form, change):
        if obj.pk:
            orig_obj = User.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        obj.save()

admin.site.register(URL)