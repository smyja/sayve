from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import Profile, wallet

from .models import User
# Regis
admin.site.register(Profile)
admin.site.register(wallet)

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ( 'email', 'is_staff')
    list_filter = ('is_staff',)
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
   
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        
        ('Permissions', {'fields': ('is_staff',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)