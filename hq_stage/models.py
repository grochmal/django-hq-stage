from django.db import models
from django.code.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

import datetime
from pytz import timezone


class Batch(models.Model):
    '''
    The batch separates data loads into pieces that are meant to be uploaded to
    the warehouse together.  Operations on a single batch simplify several
    procedures:

    *   If an entire file was wrongly loaded the entire batch can be used to
    invalidate all relevant rows.
    *   Data can be loaded from several sources into the same batch and then
    processed together.

    A batch ID is not recyclable, once a batch has been processed no new items
    can be included in the batch.
    '''
    date_created = models.DateTimeField(
          _('date created')
        , blank=True
        , help_text=_('creation of the batch')
        )
    processed = modles.BooleanField(
          _('processed')
        , db_index=True
        , default=False
        , help_text=_('set once the batch is processed')
        )

    def __str__(self):
        return '[' + str(self.date_created) + '] ' + str(self.id)

    def get_absolute_url(self):
        reverse('hq_stage:batch', kwargs={ 'batch_id' : self.id })

    class Meta:
        verbose_name = _('batch')
        verbose_name_plural = _('batches')


class DataRow(models.Model):
    '''
    Abstract class that deals with the state of the rows in the staging
    database.  All rows in the staging database are awaiting cleansing and
    upload to the actual warehouse.  Therefore any row can only be in one of
    the following states:

    1. processed=0, in_error=0, ignore=0
       The row has been inserted in the staging database but the procedure to
       upload it to the warehouse has not been started.  Since all data columns
       in the staging database are VARCHAR(255) the data must be terribly dirty
       to not enter the staging database.  Given that we input a single space
       even for missing data we assume that all data is inserted into the
       staging database.

    2. processed=1, in_error=0, ignore=0
       The row has been uploaded successfully to the warehouse.  Not issues
       with the data have been found.  The row does not require any more
       processing in the staging database.

    3. processed=1, in_error=1, ignore=0
       The row could not be uploaded to the warehouse.  The data must be
       reviewed by an operator and the upload of the batch repeated.  The batch
       upload will only attempt to upload rows that are in state 1 and 3.

    4. processed=1, in_error=1, ignored=1
       The row is complete garbage and no amount of editing by an operator can
       save this data.  The row has been marked as an ignored error by an
       operator.
    '''
    insert_date = models.DateTimeField(
          _('insert date')
        , blank=True
        , help_text=_('insertion in the stage database')
        )
    batch = models.ForeignKey(
          Batch
        , verbose_name=_('batch')
        , related_name='%(app_label)s_%(class)s_set'
        , help_text=_('the batch this offer is assigned to')
        )
    processed = models.BooleanField(
          _('processed')
        , db_index=True
        , default=False
        , help_text=_('set if upload to warehouse was attempted')
        )
    in_error = models.BooleanField(
          _('in error')
        , default=False
        , help_text=_('set if it upload to warehouse failed')
        )
    ignore = models.BooleanField(
          _('ignore')
        , default=False
        , help_text=_('if set the row is considered an ignored error')
        )

    def __str__(self):
        return '[' + str(self.insert_date) + '] ' + str(self.batch.id)

    class Meta:
        abstarct = True


class Offer(DataRow):
    external_id = models.CharField(
          _('external id')
        , max_length=255
        , help_text=_('id provided in the input')
        )
    hotel_id = models.CharField(
          _('hotel id')
        , max_length=255
        , help_text=_('the hotel providing the offer')
        )
    currency_id = models.CharField(
          _('currency id')
        , max_length=255
        , help_text=_('currency the offer is in')
        )
    source_system_code = models.CharField(
          _('source system code')
        , max_length=255
        , help_text=_('code form the inventory system')
        )
    available_cnt = models.CharField(
          _('available count')
        , max_length=255
        , help_text=_('number of rooms available')
        )
    selling_price = models.CharField(
          _('selling price')
        , max_length=255
        , help_text=_('price of the offer')
        )
    checkin_date = models.CharField(
          _('check-in date')
        , max_length=255
        , help_text=_('date the guest must check in')
        )
    checkout_date = models.CharField(
          _('check-out date')
        , max_length=255
        , help_text=_('date the guest must check out')
        )
    valid_offer_flag = models.CharField(
          _('valid offer')
        , max_length=255
        , help_text=_('whether the offer is valid')
        )
    offer_valid_from = models.CharField(
          _('valid from')
        , max_length=255
        , help_text=_('when the offer becomes valid')
        )
    offer_valid_to = models.CharField(
          _('valid to')
        , max_length=255
        , help_text=_('when the offer becomes invalid')
        )
    breakfast_included_flag = models.CharField(
          _('breakfast included')
        , max_length=255
        , help_text=_('if price includes breakfast')
        )
    external_insert_datetime = models.CharField(
          _('external insert date')
        , max_length=255
        , help_text=_('insert date provided in input')
        )

    def get_absolute_url(self):
        reverse('hq_stage:offer', kwargs={ 'offer_id' : self.id })

    class Meta:
        index_together = [ ( 'in_error' , 'ignore' ) ]
        verbose_name = _('offer')
        verbose_name_plural = _('offers')


class Currency(DataRow):
    external_id = models.CharField(
          _('external id')
        , max_length=255
        , help_text=_('id provided in the input')
        )
    currency_code = models.CharField(
          _('currency code')
        , max_length=255
        , help_text=_('iso 4217 currency code')
        )
    currency_name = models.CharField(
          _('currency name')
        , max_length=255
        , help_text=_('currency name')
        )

    def get_absolute_url(self):
        reverse('hq_stage:currency', kwargs={ 'currency_id' : self.id })

    class Meta:
        index_together = [ ( 'in_error' , 'ignore' ) ]
        verbose_name = _('currency')
        verbose_name_plural = _('currencies')


class ExchangeRate(DataRow):
    external_id = models.CharField(
          _('external id')
        , max_length=255
        , help_text=_('id provided in the input')
        )
    primary_currency_id = models.CharField(
          _('primary currency id')
        , max_length=255
        , help_text=_('original currency')
        )
    secondary_currency_id = models.CharField(
          _('secondary_currency id')
        , max_length=255
        , help_text=_('converted currency')
        )
    date_valid = models.CharField(
          _('date valid')
        , max_length=255
        , help_text=_('date of the forex rate')
        )
    currency_rate = models.CharField(
          _('currency rate')
        , max_length=255
        , help_text=_('conversion rate')
        )

    def get_absolute_url(self):
        reverse('hq_stage:exchange', kwargs={ 'exchange_id' : self.id })

    class Meta:
        index_together = [ ( 'in_error' , 'ignore' ) ]
        verbose_name = _('exchange rate')
        verbose_name_plural = _('exchange rates')

