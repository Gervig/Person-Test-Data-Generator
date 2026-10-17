import json
from pathlib import Path

# Path(__file__) points to data_loader.py.
# .parent goes up to the app folder.
# .parent.parent goes up to the backend folder.
# / "data" points to the data folder inside backend.
DATA_DIR = Path(__file__).parent.parent / "data"


def load_person_names() -> list[dict]:
    path = DATA_DIR / "person-names.json"

    with path.open(encoding="utf-8") as file:
        data = json.load(file)

    return data["persons"]

