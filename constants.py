from pathlib import Path

BASE_DIR: Path = Path(__file__).parent.resolve()

UPLOADS_DIR: Path = BASE_DIR / 'uploads'
SECRET_DIR: Path = BASE_DIR / 'secret'

PIN_FILE: Path = SECRET_DIR / 'pin.txt'

IS_ADMIN_EXECUTABLE: Path = SECRET_DIR / 'is_admin.exe'
