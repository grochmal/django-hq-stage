from django.conf.urls import url

from . import views


app_name = 'hq_stage'
urlpatterns = [
      url( r'^batch/(?P<pk>\d+)/'
         , views.BatchView.as_view()
         , name='batch'
         )
    , url( r'^batch/$'
         , views.BatchListView.as_view()
         , name='batch_list'
         )
    , url( r'^currency/(?P<pk>\d+)/'
         , views.CurrencyUpdateView.as_view()
         , name='currency'
         )
    , url( r'^currency/$'
         , views.CurrencyListView.as_view()
         , name='currency_list'
         )
    , url( r'^exchange/(?P<pk>\d+)/'
         , views.ExchangeUpdateView.as_view()
         , name='exchange'
         )
    , url( r'^exchange/$'
         , views.ExchangeListView.as_view()
         , name='exchange_list'
         )
    , url( r'^offer/(?P<pk>\d+)/'
         , views.OfferUpdateView.as_view()
         , name='offer'
         )
    , url( r'^offer/$'
         , views.OfferListView.as_view()
         , name='offer_list'
         )
    , url( r'^upload-api/$'
         , views.UploadView.as_view()
         , name='api'
         )
    , url( r''
         , views.DocView.as_view()
         , name='doc'
         )
]

