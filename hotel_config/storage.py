"""Custom Django storage backend backed by Vercel Blob.

Used for user-uploaded media (e.g. room images), because Vercel's serverless
filesystem is ephemeral and read-only. The full public blob URL is stored as
the file's name (i.e. the value persisted in the model's ImageField).

Requires the BLOB_READ_WRITE_TOKEN environment variable, which Vercel injects
automatically when a Blob store is connected to the project.
"""

import urllib.request

from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

import vercel_blob


@deconstructible
class VercelBlobStorage(Storage):
    def _save(self, name, content):
        content.seek(0)
        result = vercel_blob.put(name, content.read(), {"addRandomSuffix": "true"})
        # Persist the absolute public URL as the file name.
        return result["url"]

    def _open(self, name, mode="rb"):
        with urllib.request.urlopen(name) as resp:
            return ContentFile(resp.read())

    def delete(self, name):
        if name:
            try:
                vercel_blob.delete(name)
            except Exception:
                pass

    def exists(self, name):
        # Random suffix guarantees unique names, so never report a collision.
        return False

    def get_available_name(self, name, max_length=None):
        return name

    def url(self, name):
        return name

    def size(self, name):
        try:
            return int(vercel_blob.head(name)["size"])
        except Exception:
            return 0
