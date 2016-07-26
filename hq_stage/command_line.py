#!/usr/bin/env python3

import os, sys, getopt, csv, datetime
from pytz import timezone

def zip_default(keys, values, default=''):
    '''
    Zips two lists into a dictionary.  But, contrary to plain `zip`, if the
    list containing the keys is longer then the list containing the values add
    the `default` value as the value for the remaining keys.
    '''
    while len(keys) > len(values):
        values.append(default)
    return dict(zip(keys, values))

def diff_list(left, right):
    '''
    Compute set difference of lists, but keeps the order of fields in the left
    operand (a real set difference would ignore order).
    '''
    for i in right:
        if i in left:
            left.remove(i)
    return left

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

def load_currency(csv_file, models, settings):
    '''
    Bulk insert of the Currency model.

    Since we may have a lot of records being inserted firing an insert for each
    would not be quick enough in most wareouses.  Instead we use a bulk insert
    every a certain number of records.

    TODO: The number of records commited in bulk should be configurable.
    '''
    fields = list(map(lambda x: x.name, models.Currency._meta.get_fields()))
    ignore = list(map(lambda x: x.name, models.DataRow._meta.get_fields()))
    ignore.append('id')
    infields = diff_list(fields, ignore)

    batch = models.Batch()
    batch.save()
    print('Using new batch [%i]' % batch.id)
    commit_num = 3
    commit_list = []
    iter = read_unix_csv(csv_file)
    next(iter, None)  # ignore header
    next(iter, None)  # ignore dummy row
    # bulk_create does not call save(), we need to add the date manually
    tz = timezone(settings.TIME_ZONE)
    insert_date = tz.localize(datetime.datetime.now())
    for row in iter:
        field_dict = zip_default(infields, row)
        #print(field_dict)
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

def load_exchange_rate(csv_file, models, settings):
    pass

def load_offer(csv_file, models, settings):
    pass

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

    usage = 'hqs-load-table [-h] -f <csv file> -t <table>'
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hf:t:')
    except getopt.GetopetError as e:
        print(e)
        print(usage)
        sys.exit(2)
    infile = None
    table = None
    for o, a in opts:
        if '-h' == o:
            print(usage)
            sys.exit(0)
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

    tables[table](infile, models, settings)

def print_errors():
    settings_path()
    import django
    django.setup()
    from django.conf import settings
    from hq_stage import models

    print(settings.DATABASES)

