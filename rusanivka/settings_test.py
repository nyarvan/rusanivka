"""
Settings for running the test suite locally.

Replaces PostgreSQL and S3 with in-memory SQLite and the local file system,
so tests need no environment variables or network access.
"""
import atexit
import os
import shutil
import tempfile

os.environ.setdefault('SECRET_KEY', 'test-secret-key')
os.environ.setdefault('AWS_URL', '')

from .settings import *  # noqa: E402,F401,F403

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = tempfile.mkdtemp(prefix='rusanivka-test-media-')
atexit.register(shutil.rmtree, MEDIA_ROOT, ignore_errors=True)

PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
