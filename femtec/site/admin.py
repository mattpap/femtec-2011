from django.contrib import admin

from django.contrib.auth.models import User
from femtec.site.models import UserProfile, UserAbstract

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')

    actions_on_top = False
    actions_on_bottom = False

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    def full_name(obj):
        return obj.user.get_full_name()

    full_name.short_description = 'Full Name'

    list_display = (full_name, 'affiliation', 'address', 'city', 'postal_code',
        'country', 'speaker', 'student', 'accompanying', 'vegeterian', 'arrival',
        'departure', 'postconf', 'tshirt')

    actions_on_top = False
    actions_on_bottom = False

admin.site.register(UserProfile, UserProfileAdmin)

class UserAbstractAdmin(admin.ModelAdmin):
    def full_name(obj):
        return obj.user.get_full_name()

    full_name.short_description = 'Full Name'

    list_display = (full_name, 'title', 'submit_date', 'modify_date', 'accepted')

    class Media:
        css = {
            'all': ('css/admin.css',),
        }

        js = ('js/jquery/jquery.js', 'js/admin.js')

    actions_on_top = False
    actions_on_bottom = False

admin.site.register(UserAbstract, UserAbstractAdmin)

