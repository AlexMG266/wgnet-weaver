from pathlib import Path

BASE_DIR = Path.home() / ".wgnet-weaver"

DB_DIR = BASE_DIR / "db"
DB_FILE = DB_DIR / "wgnet-weaver.db"
INVENTORIES_DIR = BASE_DIR / "inventories"
PLAYHOOKS_DIR = BASE_DIR / "playhooks"
LOGS_DIR = BASE_DIR / "logs"
STATE_FILE = BASE_DIR / "state.json"

def init_directories():
    for d in [INVENTORIES_DIR, PLAYHOOKS_DIR, LOGS_DIR, DB_DIR]:
        d.mkdir(parents=True, exist_ok=True)
