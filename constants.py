import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOADS_DIR = os.path.join(BASE_DIR, 'uploads')
SECRET_DIR = os.path.join(BASE_DIR, 'secret')

PIN_FILE = os.path.join(SECRET_DIR, 'pin.txt')

IS_ADMIN_EXECUTABLE = os.path.join(SECRET_DIR, 'is_admin.exe')
