import hashlib

from django.conf import settings
from rest_framework import status
import requests
from django.db import transaction

from .serializers import ReportSerializer

# FIXME: Set this as an env var
SECRET = "***"
FILES_SRV = "https://carbonara-files.herokuapp.com"

def upload_binary(binary):
    # TODO: Add timeout to every request
    """
    Upload a binary to the file server if it doesn't exist
    """
    content = binary.file.read()
    hasher = hashlib.md5()
    hasher.update(content)
    md5 = hasher.hexdigest()
    print("md5:")
    print(md5)
    # Check if the file is already present with a HEAD request
    res = requests.head(FILES_SRV + '/z/' + md5, params={'key':SECRET})
    # if not upload it performing a POST request
    if res.status_code == 404:
        res = requests.post(FILES_SRV, params={'key':SECRET}, files={"file":(md5, content)})
    return md5
