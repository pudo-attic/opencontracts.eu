import dataset
from sqlalchemy import func, select, and_
from sqlalchemy.dialects.postgresql import FLOAT
from opencontracts.core import DATABASE

engine = dataset.connect(DATABASE)

documents_table = engine['documents']
contracts_table = engine['contracts']
references_table = engine['references']
cpvs_table = engine['cpvs']



def aggregate(group_by=[], order_by=[('count', 'desc'),], **filters):
    contract_alias = contracts_table.table.alias('contract')
    document_alias = documents_table.table.alias('document')
    _tables = [contract_alias, document_alias]

    def field(name):
        table, column = name.split('_', 1)
        for alias in _tables:
            if alias.name == table:
               return alias.c[column]

    _fields = [
        func.count(func.distinct(contract_alias.c.id)).label('count'),
        func.sum(func.cast(contract_alias.c.total_value_cost, FLOAT)).label('contract_total_value_cost'),
        func.sum(func.cast(contract_alias.c.initial_value_cost, FLOAT)).label('contract_initial_value_cost'),
        func.sum(func.cast(contract_alias.c.contract_value_cost, FLOAT)).label('contract_contract_value_cost')
        ]

    _filters = contract_alias.c.doc_no == document_alias.c.doc_no
    if len(filters):
        _filters = [_filters]
        for f, value in filters.items():
            _filters.append(field(f)==value)
        _filters = and_(*_filters)

    _group_by = []
    for group in group_by:
        f = field(group)
        _group_by.append(f)
        _fields.append(f)

    _order_by = []
    for field in _fields:
        for name, direction in order_by:
            if field._label == name:
                _order_by.append(field.desc() if direction == 'desc' else field.asc())

    q = select(_fields, _filters, _tables, use_labels=True,
        group_by=_group_by, order_by=_order_by)
    return engine.query(q)
