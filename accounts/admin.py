from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Address, Profile


# Register your models here.

admin.site.register(User, UserAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'house_number_name', 'street', 'town', 'postcode']


admin.site.register(Address, AddressAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phonenumber', 'avatar',
                    'birthday', 'gender', 'created_at', 'updated_at']


admin.site.register(Profile, ProfileAdmin)
