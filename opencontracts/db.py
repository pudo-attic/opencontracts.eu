import dataset
from opencontracts.core import DATABASE

engine = dataset.connect(DATABASE)

documents_table = engine['documents']
contracts_table = engine['contracts']
references_table = engine['references']
cpvs_table = engine['cpvs']
