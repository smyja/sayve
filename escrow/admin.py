from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import Profile, wallet,MoneyDeposit,Verification,sendcoin,Log

from .models import User
# Regis
admin.site.register(Profile)
admin.site.register(wallet)
admin.site.register(MoneyDeposit)
admin.site.register(Verification)
admin.site.register(Log)


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ( 'email', 'first_name','last_name','full_name','is_staff')
    list_filter = ('is_staff',)
    # def get_fullname(self,obj):
    #     """
    #     Returns the first_name plus the last_name and middle_name, with a space in between.
    #     """
    #     full_name = '%s %s %s' % ( obj.last_name, self.middle_name)
    #     return full_name.strip()    
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
   
    fieldsets = (
        (None, {'fields': ('email', 'password','first_name','last_name','middle_name')}),
        
        ('Permissions', {'fields': ('is_staff','is_active')}),
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
class sendcoinAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)
admin.site.register(sendcoin, sendcoinAdmin)

