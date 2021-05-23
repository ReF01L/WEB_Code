from django.contrib import admin

from account.models import Profile, Cell


class ProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'position', 'post_code')


class CellAdmin(admin.ModelAdmin):
    fields = ('date', 'post_code', 'vacancy')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Cell, CellAdmin)
