from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CheckoutConfig(AppConfig):
    label = 'invoice'
    name = 'oscar.apps.invoice'
    verbose_name = _('Invoice')
