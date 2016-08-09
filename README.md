README for django-hq-stage

## Introduction

Django app for constructing and maintaining the staging area database in the
Hotel Quickly example Warehouse.

The app has two command line tools:

*   `hqs-load-table`: Loads the CSV tables into tables in the staging area.

*   `hqs-print-errors`: After the record in the staging area are uploaded into
    the warehouse the rows that could not be loaded are indicated with errors.
This script prints these errors as links to the web interface of the warehouse,
where they can be corrected or ignored.

Their usage follows:

    hqs-load-table [-h] [-b <batch number>] -f <csv file> -t <table>

      -h  Print usage.
      -b  Batch number to use, if such a batch does not exist yet or has
          already been processed this argument will be ignored.
      -t  The table to load data into, either `currency`, `exchange-rate` or
          `offer`.
      -f  CSV file with relevant data for the table specified with -t.

    ------

    hqs-print-errors [-h] -t <table>

      -h  Print usage.
      -t  Check the table for rows that are in error (and the error has not
          been set to ignored), either `currency`, `exchange-rate` or `offer`.

There is also a data load `API` residing at:

    <url root>/api/

The API is neigh unusable at the moment.

## Loading data

It is preferable to load a self-consistent piece of data into a single batch,
you can specify the batch number to the load script with `-b`.  The script
prints the batch number that it used, which may be different from the one
provided with `-b` if that batch does not exists or has been processed already.
For example:

    $ hqs-load-data -f hq-currency.csv -t currency
    ...
    Batch: [ 3 ]
    $ hqs-load-data -f hq-forex.csv -t exchange-rate -b 3
    $ hqs-load-data -f hq-offer.csv -t offer -b 3

## Copying

Copyright (C) 2016 Michal Grochmal

This file is part of `django-hq-stage`.

`django-hq-stage` is free software; you can redistribute and/or modify all or
parts of it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or (at your
option) any later version.

`django-hq-stage` is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

The COPYING file contains a copy of the GNU General Public License.  If you
cannot find this file, see <http://www.gnu.org/licenses/>.

