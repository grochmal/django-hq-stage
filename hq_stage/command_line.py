#!/usr/bin/env python3

import os, sys, getopt, csv, datetime
from pytz import timezone
from . import util

def settings_path():
    '''
    Before we can call django.setup() we need to know the path to the project
    configuration.  If we cannot find the configuration we can do nothing since
    we cannot even connect to the database.
    '''
    project_path = os.environ.get('HQ_DW_CONF_PATH')
    if not project_path:
        print( 'ERROR: You need to set HQ_DW_CONF_PATH environment variable '
             + 'to the path of the main django project (hq-dw).'
             )
        sys.exit(1)
    sys.path.append(project_path)
    settings = os.environ.get('DJANGO_SETTINGS_MODULE')
    if not settings:
        print( 'ERROR: You need to set DJANGO_SETTINGS_MODULE environment '
             + 'variable to the settings module in the main project (hq-dw).'
             )
        sys.exit(1)

def read_unix_csv(csv_file):
    '''
    Iterator over CSV files in the dialect commonly found on UNIX systems:
    delimited by commas (,) and quoted in double quotes (").  This simplifies
    the handling of such a CSV file.
    '''
    with open(csv_file, newline='') as csvf:
        reader = csv.reader(csvf, delimiter=',', quotechar='"')
        for row in reader:
            yield row

def load_currency(csv_file, batch, models, settings):
    '''
    Bulk insert of the Currency model.

    Since we may have a lot of records being inserted firing an insert for each
    would not be quick enough in most warehouses.  Instead we use a bulk insert
    every a certain number of records.
    '''
    infields = util.remove_abstract_fields( models.Currency
                                          , models.DataRow, ['id'] )
    commit_num = settings.HQ_DW_COMMIT_SIZE
    commit_list = []
    iter = read_unix_csv(csv_file)
    next(iter, None)  # ignore header
    next(iter, None)  # ignore dummy row
    # bulk_create does not call save(), we need to add the date manually
    tz = timezone(settings.TIME_ZONE)
    insert_date = tz.localize(datetime.datetime.now())
    for row in iter:
        field_dict = util.zip_default(infields, row)
        cur = models.Currency(
              batch=batch
            , insert_date=insert_date
            , **field_dict
            )
        commit_list.append(cur)
        if len(commit_list) % commit_num == 0:
            models.Currency.objects.bulk_create(commit_list)
            print('commit', commit_num, 'currencies')
            commit_list = []
    models.Currency.objects.bulk_create(commit_list)
    print('final commit, and we are done')

def load_exchange_rate(csv_file, batch, models, settings):
    '''
    Bulk insert of the Exchange Rate model.

    This has a lot of duplicated code from load_currency, someday it will need
    to be refactored.
    '''
    infields = util.remove_abstract_fields( models.ExchangeRate
                                          , models.DataRow, ['id'] )
    commit_num = settings.HQ_DW_COMMIT_SIZE
    commit_list = []
    iter = read_unix_csv(csv_file)
    next(iter, None)  # ignore header
    # bulk_create does not call save(), we need to add the date manually
    tz = timezone(settings.TIME_ZONE)
    insert_date = tz.localize(datetime.datetime.now())
    for row in iter:
        field_dict = util.zip_default(infields, row)
        cur = models.ExchangeRate(
              batch=batch
            , insert_date=insert_date
            , **field_dict
            )
        commit_list.append(cur)
        if len(commit_list) % commit_num == 0:
            models.ExchangeRate.objects.bulk_create(commit_list)
            print('commit', commit_num, 'exchange rates')
            commit_list = []
    models.ExchangeRate.objects.bulk_create(commit_list)
    print('final commit, and we are done')

def load_offer(csv_file, batch, models, settings):
    '''
    Bulk insert of the Offer model.

    Again, duplicated code.  The main difficulty in making a generic function
    is the fact that the files are not consistent:

    *   currency has a header and a dummy row
    *   exchange rate has a header only
    *   and offer has a dummy row only

    I could edit the files, but that would be cheating.
    '''
    infields = util.remove_abstract_fields( models.Offer
                                          , models.DataRow, ['id'] )
    commit_num = settings.HQ_DW_COMMIT_SIZE
    commit_list = []
    iter = read_unix_csv(csv_file)
    next(iter, None)  # ignore header
    # bulk_create does not call save(), we need to add the date manually
    tz = timezone(settings.TIME_ZONE)
    insert_date = tz.localize(datetime.datetime.now())
    for row in iter:
        field_dict = util.zip_default(infields, row)
        cur = models.Offer(
              batch=batch
            , insert_date=insert_date
            , **field_dict
            )
        commit_list.append(cur)
        if len(commit_list) % commit_num == 0:
            models.Offer.objects.bulk_create(commit_list)
            print('commit', commit_num, 'offers')
            commit_list = []
    models.Offer.objects.bulk_create(commit_list)
    print('final commit, and we are done')

def load_table():
    '''
    Set up the needed environment, scrutinise the parameters, and, if
    everything went alright call the actual function that will load the table
    data from a file.

    We check that the file exists but it is the responsibility of the called
    function to verify if the file is in the correct format.
    '''
    settings_path()
    import django
    django.setup()
    from django.conf import settings
    from hq_stage import models

    tables = {
          'currency' : load_currency
        , 'exchange-rate' : load_exchange_rate
        , 'offer' : load_offer
        }

    usage = 'hqs-load-table [-h] [-b <batch>] -f <csv file> -t <table>'
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hb:f:t:')
    except getopt.GetoptError as e:
        print(e)
        print(usage)
        sys.exit(2)
    batchno = None
    infile = None
    table = None
    for o, a in opts:
        if '-h' == o:
            print(usage)
            sys.exit(0)
        elif '-b' == o:
            batchno = a
        elif '-f' == o:
            infile = a
        elif '-t' == o:
            table = a
        else:
            assert False, 'unhandled option [%s]' % o
    if not infile or not table:
        print(usage)
        sys.exit(1)
    if not os.path.isfile(infile):
        print(usage)
        print('%s: No such file' % infile)
        sys.exit(1)
    if not table in tables:
        print(usage)
        print('No such table to load.  Available tables:')
        print(', '.join(sorted(tables.keys())))
        sys.exit(1)

    batch = util.get_new_model(models.Batch, batchno)
    if not batch:
        # we got rubbish, build a new one
        batch = models.Batch()
    batch.save()
    print('Using batch [%i]' % batch.id)
    tables[table](infile, batch, models, settings)
    print('Batch: [ %i ]' % batch.id)

def print_errors():
    '''
    Print the current rows in error from the command line.

    TODO:

    *   This should receive a batch argument and then print errors from all
        tables in that batch.
    '''
    settings_path()
    import django
    django.setup()
    from django.conf import settings
    from hq_stage import models

    tables = {
          'currency' : models.Currency.objects
        , 'exchange-rate' : models.ExchangeRate.objects
        , 'offer' : models.Offer.objects
        }

    usage = 'hqs-print-errors [-h] -t <table>'
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'ht:')
    except getopt.GetoptError as e:
        print(e)
        print(usage)
        sys.exit(2)
    table = None
    for o, a in opts:
        if '-h' == o:
            print(usage)
            sys.exit(0)
        elif '-t' == o:
            table = a
        else:
            assert False, 'unhandled option [%s]' % o
    if not table:
        print(usage)
        sys.exit(1)
    if not table in tables:
        print(usage)
        print('No such table.  Available tables:')
        print(', '.join(sorted(tables.keys())))
        sys.exit(1)

    q = tables[table].filter(in_error=True).exclude(ignore=True)
    # This is horrible code, but there is no time to make proper views
    domain = (settings.ALLOWED_HOSTS[0:1] or 'localhost')
    if settings.DEBUG:
        domain += ':8000'
    for obj in q:
        print('http://%s%s' % (domain, obj.get_absolute_url()))

