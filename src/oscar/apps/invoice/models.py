from oscar.apps.invoice.abstract_models import AbstractInvoice, AbstractLegalEntity
from oscar.core.loading import is_model_registered

__all__ = []


if not is_model_registered('invoice', 'Invoice'):
    class Invoice(AbstractInvoice):
        pass

    __all__.append('Invoice')


if not is_model_registered('invoice', 'LegalEntity'):
    class LegalEntity(AbstractLegalEntity):
        pass

    __all__.append('LegalEntity')
