from django.contrib import admin
from .models import Client, Lawyer, File, CASE


# Register your models here.


class LawyerAdmin(admin.ModelAdmin):
    list_display = ['username', 'license_verify_status']
    actions = ['approve_license']
    def approve_license(self, request, queryset):
        queryset.update(license_verify_status=True)
    approve_license.short_description = "Approve selected lawyers' license"

admin.site.register(Client)
admin.site.register(Lawyer,LawyerAdmin)

# admin.site.register(Lawyer)
# admin.site.register(License)
admin.site.register(File)
admin.site.register(CASE)
# admin.site.register(Academic)