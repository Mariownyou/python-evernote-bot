#
# A simple Evernote API demo script that lists all notebooks in the user's
# account and creates a simple test note in the default notebook.
#
# Before running this sample, you must fill in your Evernote developer token.
#
# To run (Unix):
#   export PYTHONPATH=../../lib; python EDAMTest.py
#

import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
import os
from utils import list_folder, delete_files, EVERNOTE_TOKEN

from evernote.api.client import EvernoteClient

# Real applications authenticate with Evernote using OAuth, but for the
# purpose of exploring the API, you can get a developer token that allows
# you to access your own Evernote account. To get a developer token, visit
# https://sandbox.evernote.com/api/DeveloperToken.action
auth_token = EVERNOTE_TOKEN

if auth_token == "your developer token":
    print("Please fill in your developer token")
    print("To get a developer token, visit " \
          "https://sandbox.evernote.com/api/DeveloperToken.action")
    exit(1)

# Initial development is performed on our sandbox server. To use the production
# service, change sandbox=False and replace your
# developer token above with a token from
# https://www.evernote.com/api/DeveloperToken.action
# To access Sandbox service, set sandbox to True
# To access production (International) service, set both sandbox and china to False
# To access production (China) service, set sandbox to False and china to True

sandbox=False
china=False
client = EvernoteClient(token=auth_token, sandbox=sandbox,china=china)
user_store = client.get_user_store()
note_store = client.get_note_store()


def add_img(note, image_path):
    # To include an attachment such as an image in a note, first create a Resource
    # for the attachment. At a minimum, the Resource contains the binary attachment
    # data, an MD5 hash of the binary data, and the attachment MIME type.
    # It can also include attributes such as filename and location.
    # image_path = constants_path = os.path.join(os.path.dirname(__file__), "enlogo.png")
    image_path = 'photos/' + image_path
    with open(image_path, 'rb') as image_file:
        image = image_file.read()
    md5 = hashlib.md5()
    md5.update(image)
    hash = md5.digest()

    data = Types.Data()
    data.size = len(image)
    data.bodyHash = hash
    data.body = image

    resource = Types.Resource()
    resource.mime = 'image/png'
    resource.data = data

    # Now, add the new Resource to the note's list of resources
    note.resources.append(resource)
    print(len(note.resources))
    # To display the Resource as part of the note's content, include an <en-media>
    # tag in the note's ENML content. The en-media tag identifies the corresponding
    # Resource using the MD5 hash.
    hash_hex = binascii.hexlify(hash)
    hash_str = hash_hex.decode("UTF-8")
    content = '<br/>'
    content += '<en-media type="image/png" hash="{}"/>'.format(hash_str)
    content += '<br/>'
    return content


def create_note(text, title=None):
    note = Types.Note()
    note.resources = []
    note.title = "Test note from EDAMTest.py" if title == None else title
    files = list_folder()
    # The content of an Evernote note is represented using Evernote Markup Language
    # (ENML). The full ENML specification can be found in the Evernote API Overview
    # at http://dev.evernote.com/documentation/cloud/chapters/ENML.php
    note.content = '<?xml version="1.0" encoding="UTF-8"?>'
    note.content += '<!DOCTYPE en-note SYSTEM ' \
                    '"http://xml.evernote.com/pub/enml2.dtd">'
    note.content += '<en-note>'
    note.content += f'{text}<br/>'
    if len(files) > 0:
        for file in files:
            print(file)
            note.content += add_img(note, file)
            print(note.content)
    note.content += '</en-note>'

    # Finally, send the new note to Evernote using the createNote method
    # The new Note object that is returned will contain server-generated
    # attributes such as the new note's unique GUID.
    created_note = note_store.createNote(note)
    delete_files()

    print("Successfully created a new note with GUID: ", created_note.guid)
