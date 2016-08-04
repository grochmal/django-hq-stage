from django.views import generic
from django import http
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import json

from . import models, util


class DocView(generic.TemplateView):
    template_name = 'hq_stage/doc.html'


class HqStageListView(generic.ListView):
    template_name = 'hq_main/list.html'
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
    fields  = [ x.name
                for x in models.ExchangeRate._meta.get_fields()
                if x.editable == True and not x.auto_created ]


class OfferUpdateView(generic.edit.UpdateView):
    model = models.Offer
    template_name = 'hq_stage/offer_update.html'
    context_object_name = 'offer'
    fields  = [ x.name
                for x in models.Offer._meta.get_fields()
                if x.editable == True and not x.auto_created ]


@method_decorator(csrf_exempt, name='dispatch')
class UploadView(generic.View):
    '''
    This is an upload API, you can insert data into the staging are through an
    API.  If you have a batch number and that batch has not yet been processed
    you can reuse the batch.

    I really like the idea of an API upload because it is one extra line of
    defence against badly formatted input data.  And an easy way to allow a
    data provider to automate his interaction with us.

    Current issues:

    *   Only a single record can be uploaded at a time.  Adding a list upload
        should not be hard but it will need a lot of checking code to ensure
        that people do not upload mixed lists.

    *   This has not been tested at all, it is probably buggy as hell.

    Example request:

    { 'batch' : 3  // batch is optional
    , 'object_type' : 'currency'
    , 'object_data' :
        { 'external_id' : '3'
        , 'currency_code' : 'GBP'
        , 'currency_name' : 'British Pound'
        }
    }

    And response

    { 'batch' 3 }  // if the batch was reused, otherwise a new number
    '''
    ALLOWED_OBJECTS = {
          'currency' : models.Currency
        , 'exchange-rate' : models.ExchangeRate
        , 'offer' : models.Offer
        }

    def get(self, request, *args, **kwargs):
        return http.HttpResponseForbidden()  # 403

    def post(self, request, *args, **kwargs):
        try:
            json_data = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return http.HttpResponseBadRequest()  # 400
        if not dict == type(json_data):
            return http.HttpResponseBadRequest()  # 400
        batchno = json_data.get('batch')
        object_type = json_data.get('object_type')
        object_data = json_data.get('object_data')
        if not object_data or not object_type:
            return http.HttpResponseBadRequest()  # 400
        if not dict == type(object_data):
            return http.HttpResponseBadRequest()  # 400
        if str == type(object_type):
            return http.HttpResponseBadRequest()  # 400
        if not object_type in self.ALLOWED_OBJECTS:
            return http.HttpResponseBadRequest()  # 400
        batch = util.get_new_model(models.Batch, batchno)
        if not batch:
            return http.HttpResponseBadRequest()  # 400
        try:
            obj = self.ALLOWED_OBJECTS[object_type](
                  batch=batch
                , **object_data
                )
        except TypeError:
            return http.HttpResponseBadRequest()  # 400
        # there are almost no foreign keys here, this is rather safe
        batch.save()
        obj.save()
        return http.JsonResponse({'batch': batch.id})

