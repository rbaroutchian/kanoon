from django.contrib import admin
from . import models

# Register your models here.
class productAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher']

class pishsabtAdmin(admin.ModelAdmin):
    list_display = ['std_name','mobile','is_read']
    list_editable = ['is_read']
    list_filter = ['is_read']

admin.site.register(models.product, productAdmin)
admin.site.register(models.pish_sabt, pishsabtAdmin)