from django.contrib import admin

from customers.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'get_email', 'phone_number', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'phone_number']

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    get_full_name.short_description = 'Name'

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = 'Email'
