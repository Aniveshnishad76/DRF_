from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from application.models import UserInfo, paypal_payment, UserOTP

#
admin.site.register(UserInfo)
admin.site.register(UserOTP)

class paypal_paymentAdmin(admin.ModelAdmin):
    list_display = ('email', 'pay_id', 'amount', 'currency', 'datetime',)
    search_fields = ('email',)
    list_per_page = 10
    list_editable = ('amount', 'currency', 'datetime',)
    list_filter = ('datetime',)
    ordering = ('amount',)


# admin.site.register(paypal_payment, paypal_paymentAdmin)
# admin.site.register(PartnerInfo)

admin.site.site_title = 'Wood House'
admin.site.site_url = '#'
admin.site.index_title = 'Wood House Admin Panel'
admin.empty_value_display = '**Empty**'
admin.site.site_header = "Wood House"
