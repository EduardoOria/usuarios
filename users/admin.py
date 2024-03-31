from django.contrib import admin
from .models import defaultUser as user, Area

# Register your models here.

admin.site.register(user)

admin.site.register(Area)