from django.contrib import admin
from .models import Client, Lawyer, File, CASE

# Register your models here.


admin.site.register(Client)
admin.site.register(Lawyer)
# admin.site.register(License)
admin.site.register(File)
admin.site.register(CASE)
# admin.site.register(Academic)