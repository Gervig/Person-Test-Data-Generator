import json
from pathlib import Path

# Path(__file__) points to data_loader.py.
# The repository-level data directory is next to the backend directory.
DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def load_person_names() -> list[dict]:
    path = DATA_DIR / "person-names.json"

    with path.open(encoding="utf-16") as file:
        data = json.load(file)

    return data["persons"]
