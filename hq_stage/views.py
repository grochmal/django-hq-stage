from django.shortcuts import render
from django.views import generic

from . import models


class HqStageListView(generic.ListView):
    template_name = 'hq_stage/list.html'
    context_object_name = 'object_list'
    paginate_by = 12  # I just like the number 12


class BatchListView(HqStageListView):
    model = models.Batch


class CurrencyListView(HqStageListView):
    model = models.Currency


class ExchangeListView(HqStageListView):
    model = models.ExchangeRate


class OfferListView(HqStageListView):
    model = models.Offer


class BatchView(generic.DetailView):
    model = models.Batch
    template_name = 'hq_stage/batch.html'
    context_object_name = 'batch'


class CurrencyUpdateView(generic.edit.UpdateView):
    model = models.Currency
    template_name = 'hq_stage/currency_update.html'
    context_object_name = 'currency'
    fields  = [ x.name
                for x in models.Currency._meta.get_fields()
                if x.editable == True and not x.auto_created ]


class ExchangeUpdateView(generic.edit.UpdateView):
    model = models.ExchangeRate
    template_name = 'hq_stage/exchange_update.html'
    context_object_name = 'exchange'


class OfferUpdateView(generic.edit.UpdateView):
    model = models.Offer
    template_name = 'hq_stage/offer_update.html'
    context_object_name = 'offer'

