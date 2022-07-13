#!/usr/bin/env python 
from evernote.api.client import EvernoteClient
from evernote.edam.error.ttypes import EDAMSystemException

import dotenv


if __name__ == '__main__':
    variables = dotenv.get_variables('.env')
    client = EvernoteClient(
        token=variables['EVERNOTE_PERSONAL_TOKEN'],
        sandbox=False
    )
    try:
        note_store = client.get_note_store()

        notebooks = note_store.listNotebooks()
        for notebook in notebooks:
            print('%s - %s' % (notebook.guid, notebook.name))
    except EDAMSystemException as err:
        print("Error: {}".format(err._message))
