from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Drug)
admin.site.register(Category)
admin.site.register(Cart)
