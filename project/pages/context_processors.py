from properties.models import Category,Property
from accounts.models import Account
from django.db.models import Count


def account_info(request):
    if request.user.is_authenticated:
        account = request.user
        # saved_count = account.saveds.count()
    else:
        account = None
        # saved_count = 0

    return {
        "account": account,
        # "saved_count": saved_count,
    }