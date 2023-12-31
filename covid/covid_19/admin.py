from django.contrib import admin
from .models import CustomUser  # Import your model here

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    ordering = ('-date_joined',)

# Register your custom user model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)
# Register your models here.
