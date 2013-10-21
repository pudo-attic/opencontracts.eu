from flask.ext.script import Manager
from flask.ext.assets import ManageAssets

from opencontracts.core import app, assets
from opencontracts.extract.download import make_ecas_session, download_latest
from opencontracts.extract.parse import ted_documents, parse

manager = Manager(app)
manager.add_command("assets", ManageAssets(assets))


@manager.command
def download():
    """ Download the latest TED XML files. """
    session = make_ecas_session()
    download_latest(session)


@manager.command
def extract():
    """ Extract data from the latest TED XML files. """
    for file_name, file_content in ted_documents():
        parse(file_name, file_content)


if __name__ == "__main__":
    manager.run()
