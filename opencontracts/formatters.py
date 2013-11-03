import csv
import locale

from opencontracts.core import app

COUNTRIES = {}

def country_name_formatter(column, row):
    if not len(COUNTRIES):
        with app.open_resource('countries.csv', 'rb') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                COUNTRIES[row.get('ISO-2')] = row
    country_code = row.get(column.name)
    return COUNTRIES.get(country_code, {}).get('Country', country_code)


def format_number(column, row):
    locale.setlocale(locale.LC_ALL, 'en_US')
    value = row.get(column.name)
    try:
        value = float(value)
        if value == 0:
            return '-'
        return locale.format("%d", value, grouping=True)
    except TypeError:
        return '-'