from django.contrib import admin

from oscar.core.loading import get_model

Invoice = get_model('invoice', 'Invoice')
LegalEntity = get_model('invoice', 'LegalEntity')


admin.site.register(Invoice)
admin.site.register(LegalEntity)
