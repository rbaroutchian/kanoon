from django.contrib import admin
from . import models

# Register your models here.
class movieAdmin(admin.ModelAdmin):
    list_display = ['title','capacity']

class movieReserveAdmin(admin.ModelAdmin):
    list_display = ['username','movie','created_at','is_confirmed','tracking_code']
    list_editable = ['is_confirmed']

    def username(self, obj):
        return obj.user.username

    username.short_description = 'نام کاربری'

class showTimeAdmin(admin.ModelAdmin):
    list_display = ['movie','time','date','capacity']



admin.site.register(models.movie, movieAdmin)
admin.site.register(models.MovieReserve, movieReserveAdmin)
admin.site.register(models.ShowTime, showTimeAdmin)
