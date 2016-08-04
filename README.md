README for django-hq-stage

## Introduction

Django app for constructing and maintaining the staging area database in the
Hotel Quickly example Warehouse.

The app has two command line tools:

*   `hqs-load-table`

*   `hqs-print-errors`

And a data load `API` residing at:

    <url root>/api/

## Loading data

It is preferable to load a self-consistent piece of data into a single batch,
you can specify the batch number to the load script with `-b`.  The script
prints the batch number that it used, which may be different from the one
provided with `-b` if that batch does not exists or has been processed already.
For example:

    $ hqs-load-data -f hq-currency.csv -t currency
    ...
    Batch: [ 1 ]
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

