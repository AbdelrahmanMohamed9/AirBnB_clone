#!/usr/bin/python3
"""__init__ Magic Method For Models Directory."""
from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
