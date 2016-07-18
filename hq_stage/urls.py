from django.conf.urls import url

app_name = 'hq_stage'
urlpatterns = [
      url( r'batch/(P<batch_id>\d+)/'
         , #TODO
         , name='batch'
         )
    , url( r'offer/(P<offer_id>\d+)/'
         , #TODO
         , name='offer'
         )
    , url( r'currecny/(P<currency_id>\d+)/'
         , #TODO
         , name='currency'
         )
    , url( r'exchnage/(P<exhcnage_id>\d+)/'
         , #TODO
         , name='exchange'
         )
]
