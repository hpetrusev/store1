import os

DATABASE = os.environ.get("DB", "jsondb")
FORMATTER = os.environ.get("FORMAT", "PoundFormatter")
LOGLEVEL = os.environ.get("LOGLEVEL", "INFO")
