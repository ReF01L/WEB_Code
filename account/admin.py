from django.contrib import admin

from account.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'position', 'post_code')

admin.site.register(Profile, ProfileAdmin)
