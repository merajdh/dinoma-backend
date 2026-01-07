from django.contrib import admin
from userauths.models import Profile , User

class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name' , "phone" , "email" ]


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name' , "gender" , "date" ]
    list_filter = ["date"]

admin.site.register(User , UserAdmin)
admin.site.register(Profile , ProfileAdmin)

# Register your models here.
