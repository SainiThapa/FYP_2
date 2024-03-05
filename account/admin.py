from django.contrib import admin
from .models import Client, Lawyer, File, CASE


# Register your models here.

def approve_lawyer(modeladmin, request, queryset):
    queryset.update(license_verify_status=True)

approve_lawyer.short_description = "Approve selected lawyers"

class LawyerAdmin(admin.ModelAdmin):
    list_display = ['username', 'license_verify_status']
    actions = [approve_lawyer]

admin.site.register(Client)
admin.site.register(Lawyer,LawyerAdmin)

# admin.site.register(Lawyer)
# admin.site.register(License)
admin.site.register(File)
admin.site.register(CASE)
# admin.site.register(Academic)