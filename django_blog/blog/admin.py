from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_date']  # ✅ Correct field names
    list_filter = ['published_date', 'author']           # ✅ Correct field names
    search_fields = ['title', 'content']
    readonly_fields = ['published_date']                 # ✅ Now works!

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
