from flask import render_template, make_response

from opencontracts.core import app
from opencontracts.db import aggregate
from opencontracts.formatters import country_name_formatter, format_number

class Column(object):

    def __init__(self, type_, name, title):
        self.type = type_
        self.name = name
        self.title = title
        self.text_formatter = lambda c, r: r.get(c.name)
        self.link_generator = None

    def text(self, row):
        return self.text_formatter(self, row)


class AggregatePager(object):

    def __init__(self, name, page_size=20, page=1):
        self.name = name
        self._dimensions = []
        self._measures = []
        self._filters = {}
        self._aggregate = None
        self.page_size = page_size
        self.page = page

    def add_dimension(self, name, title, text_formatter=None, link_generator=None):
        col = Column('dimension', name, title)
        if text_formatter is not None:
            col.text_formatter = text_formatter
        if link_generator is not None:
            col.link_generator = link_generator
        self._dimensions.append(col)

    def add_measure(self, name, title, text_formatter=None):
        col = Column('measure', name, title)
        if text_formatter is not None:
            col.text_formatter = text_formatter
        else:
            col.text_formatter = lambda c, r: r.get(c.name) or 0
        self._measures.append(col)

    def add_filter(self, dimension, value):
        self._filters[dimension] = value

    @property
    def aggregate(self):
        if self._aggregate is None:
            self._aggregate = aggregate(group_by=[d.name for d in self._dimensions],
                **self._filters)
        return self._aggregate

    @property
    def headers(self):
        return self._dimensions + self._measures
        
    @property
    def rows(self):
        for row in self.aggregate:
            cells = []
            for col in self._dimensions:
                cells.append((col, row))
            for col in self._measures:
                cells.append((col, row))
            yield cells


@app.route("/")
@app.route("/index.html")
@app.route("/index.<pager>.<sort>-<direction>.html")
def index(**kw):
    by_country = AggregatePager('by_country')
    by_country.add_dimension('contract_authority_country', 'Authority Country',
        text_formatter=country_name_formatter)
    by_country.add_measure('count', 'Count',
        text_formatter=format_number)
    by_country.add_measure('contract_contract_value_cost_eur', 'Contract value (EUR)',
        text_formatter=format_number)
    #by_country.add_filter('contract_authority_country', 'DE')
    res = make_response(render_template('index.html', by_country=by_country))
    #print type(template)
    res.headers.add_header('Link', '/test/1')
    res.headers.add_header('Link', '/test/2')
    return res
