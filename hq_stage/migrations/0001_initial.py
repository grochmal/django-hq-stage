# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-04 16:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(blank=True, editable=False, help_text='creation of the batch', verbose_name='date created')),
                ('processed', models.BooleanField(db_index=True, default=False, help_text='set once the batch is processed', verbose_name='processed')),
            ],
            options={
                'verbose_name_plural': 'batches',
                'verbose_name': 'batch',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insert_date', models.DateTimeField(blank=True, editable=False, help_text='insertion in the stage database', verbose_name='insert date')),
                ('processed', models.BooleanField(db_index=True, default=False, help_text='set if upload to warehouse was attempted', verbose_name='processed')),
                ('in_error', models.BooleanField(default=False, help_text='set if it upload to warehouse failed', verbose_name='in error')),
                ('ignore', models.BooleanField(default=False, help_text='if set the row is considered an ignored error', verbose_name='ignore')),
                ('fields_in_error', models.TextField(blank=True, editable=False, help_text='because of these field the row could not be loaded', null=True, verbose_name='fields in error')),
                ('external_id', models.CharField(blank=True, default=' ', help_text='id provided in the input', max_length=255, verbose_name='external id')),
                ('currency_code', models.CharField(blank=True, default=' ', help_text='iso 4217 currency code', max_length=255, verbose_name='currency code')),
                ('currency_name', models.CharField(blank=True, default=' ', help_text='currency name', max_length=255, verbose_name='currency name')),
                ('batch', models.ForeignKey(help_text='the batch this offer is assigned to', on_delete=django.db.models.deletion.CASCADE, related_name='currency_set', to='hq_stage.Batch', verbose_name='batch')),
            ],
            options={
                'verbose_name_plural': 'currencies',
                'verbose_name': 'currency',
            },
        ),
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insert_date', models.DateTimeField(blank=True, editable=False, help_text='insertion in the stage database', verbose_name='insert date')),
                ('processed', models.BooleanField(db_index=True, default=False, help_text='set if upload to warehouse was attempted', verbose_name='processed')),
                ('in_error', models.BooleanField(default=False, help_text='set if it upload to warehouse failed', verbose_name='in error')),
                ('ignore', models.BooleanField(default=False, help_text='if set the row is considered an ignored error', verbose_name='ignore')),
                ('fields_in_error', models.TextField(blank=True, editable=False, help_text='because of these field the row could not be loaded', null=True, verbose_name='fields in error')),
                ('external_id', models.CharField(blank=True, default=' ', help_text='id provided in the input', max_length=255, verbose_name='external id')),
                ('primary_currency_id', models.CharField(blank=True, default=' ', help_text='original currency', max_length=255, verbose_name='primary currency id')),
                ('secondary_currency_id', models.CharField(blank=True, default=' ', help_text='converted currency', max_length=255, verbose_name='secondary_currency id')),
                ('date_valid', models.CharField(blank=True, default=' ', help_text='date of the forex rate', max_length=255, verbose_name='date valid')),
                ('currency_rate', models.CharField(blank=True, default=' ', help_text='conversion rate', max_length=255, verbose_name='currency rate')),
                ('batch', models.ForeignKey(help_text='the batch this offer is assigned to', on_delete=django.db.models.deletion.CASCADE, related_name='exchangerate_set', to='hq_stage.Batch', verbose_name='batch')),
            ],
            options={
                'verbose_name_plural': 'exchange rates',
                'verbose_name': 'exchange rate',
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insert_date', models.DateTimeField(blank=True, editable=False, help_text='insertion in the stage database', verbose_name='insert date')),
                ('processed', models.BooleanField(db_index=True, default=False, help_text='set if upload to warehouse was attempted', verbose_name='processed')),
                ('in_error', models.BooleanField(default=False, help_text='set if it upload to warehouse failed', verbose_name='in error')),
                ('ignore', models.BooleanField(default=False, help_text='if set the row is considered an ignored error', verbose_name='ignore')),
                ('fields_in_error', models.TextField(blank=True, editable=False, help_text='because of these field the row could not be loaded', null=True, verbose_name='fields in error')),
                ('external_id', models.CharField(blank=True, default=' ', help_text='id provided in the input', max_length=255, verbose_name='external id')),
                ('hotel_id', models.CharField(blank=True, default=' ', help_text='the hotel providing the offer', max_length=255, verbose_name='hotel id')),
                ('currency_id', models.CharField(blank=True, default=' ', help_text='currency the offer is in', max_length=255, verbose_name='currency id')),
                ('source_system_code', models.CharField(blank=True, default=' ', help_text='code form the inventory system', max_length=255, verbose_name='source system code')),
                ('available_cnt', models.CharField(blank=True, default=' ', help_text='number of rooms available', max_length=255, verbose_name='available count')),
                ('selling_price', models.CharField(blank=True, default=' ', help_text='price of the offer', max_length=255, verbose_name='selling price')),
                ('checkin_date', models.CharField(blank=True, default=' ', help_text='date the guest must check in', max_length=255, verbose_name='check-in date')),
                ('checkout_date', models.CharField(blank=True, default=' ', help_text='date the guest must check out', max_length=255, verbose_name='check-out date')),
                ('valid_offer_flag', models.CharField(blank=True, default=' ', help_text='whether the offer is valid', max_length=255, verbose_name='valid offer')),
                ('offer_valid_from', models.CharField(blank=True, default=' ', help_text='when the offer becomes valid', max_length=255, verbose_name='valid from')),
                ('offer_valid_to', models.CharField(blank=True, default=' ', help_text='when the offer becomes invalid', max_length=255, verbose_name='valid to')),
                ('breakfast_included_flag', models.CharField(blank=True, default=' ', help_text='if price includes breakfast', max_length=255, verbose_name='breakfast included')),
                ('external_insert_datetime', models.CharField(blank=True, default=' ', help_text='insert date provided in input', max_length=255, verbose_name='external insert date')),
                ('dummy_field', models.CharField(blank=True, default=' ', help_text='dummy field that may sometimes present in the input', max_length=255, verbose_name='dummy field')),
                ('batch', models.ForeignKey(help_text='the batch this offer is assigned to', on_delete=django.db.models.deletion.CASCADE, related_name='offer_set', to='hq_stage.Batch', verbose_name='batch')),
            ],
            options={
                'verbose_name_plural': 'offers',
                'verbose_name': 'offer',
            },
        ),
        migrations.AlterIndexTogether(
            name='offer',
            index_together=set([('in_error', 'ignore')]),
        ),
        migrations.AlterIndexTogether(
            name='exchangerate',
            index_together=set([('in_error', 'ignore')]),
        ),
        migrations.AlterIndexTogether(
            name='currency',
            index_together=set([('in_error', 'ignore')]),
        ),
    ]