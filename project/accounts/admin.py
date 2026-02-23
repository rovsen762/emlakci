from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account, Plan, AccountCustomers, AccountFilters, AccountCustomerPreferries

admin.site.register(Plan)
admin.site.register(AccountCustomers)
admin.site.register(AccountFilters) 
admin.site.register(AccountCustomerPreferries)




@admin.register(Account)
class AccountAdmin(UserAdmin):
    model = Account

    list_display = (
        "username",
        "email",
        "phone",
        "city",
        "gender",
        "is_verified",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "gender",
        "is_verified",
        "is_staff",
        "is_active",
        "private_account",
    )

    search_fields = ("username", "email", "phone")
    ordering = ("-date_joined",)

    fieldsets = UserAdmin.fieldsets + (
        ("Profile Information", {
            "fields": (
                "image",
                "phone",
                "birth_date",
                "city",
                "gender",
                "bio",
            )
        }),
        ("Verification & Privacy", {
            "fields": (
                "is_verified",
                "private_account",
                "rank",
            )
        }),
        ("Password Reset System", {
            "classes": ("collapse",),
            "fields": (
                "otp",
                "reset_password_otp",
                "is_reset_password_otp_verified",
                "reset_password_request_count",
                "last_reset_password_request_date",
                "last_password_reset_date",
                "reset_password_otp_created_at",
                "reset_password_otp_expires_at",
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Profile Information", {
            "fields": (
                "email",
                "image",
                "phone",
                "birth_date",
                "city",
                "gender",
            )
        }),
    )