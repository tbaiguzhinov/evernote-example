#!/usr/bin/env python 
import argparse

import dotenv

from evernote.api.client import EvernoteClient
from evernote.api.client import NoteStore
from bs4 import BeautifulSoup

    
def get_notebook_list(note_store, notebook_guid, number=10, offset=0):
    _filter = NoteStore.NoteFilter(notebookGuid=notebook_guid)
    resultSpec = NoteStore.NotesMetadataResultSpec(
        includeTitle=True,
        includeContentLength=True,
        includeCreated=True,
        includeUpdated=True,
        includeDeleted=False,
        includeUpdateSequenceNum=True,
        includeNotebookGuid=False,
        includeTagGuids=True,
        includeAttributes=True,
        includeLargestResourceMime=True,
        includeLargestResourceSize=True,
    )

    # this determines which info you'll get for each note
    return note_store.findNotesMetadata(_filter, offset, number, resultSpec);


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=u'Dumps notes from Evernote inbox to console')
    parser.add_argument('number',
                        nargs='?',
                        type=int,
                        default=10,
                        help='number of records to dump')
    args = parser.parse_args()

    variables = dotenv.get_variables('.env')

    client = EvernoteClient(
        token=variables["EVERNOTE_PERSONAL_TOKEN"],
        sandbox=False
    )
    note_store = client.get_note_store()

    notes = get_notebook_list(note_store, variables["INBOX_NOTEBOOK_GUID"], args.number).notes

    # print('Notes', notes)
    
    for counter, note in enumerate(notes, start=1):
        print('\n--------- %s ---------' % counter)
        content = note_store.getNoteContent(note.guid)  # kwargs will be skipped by api because of bug
        soup = BeautifulSoup(content, "html.parser")
        print(soup.get_text())
