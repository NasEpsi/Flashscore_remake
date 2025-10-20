from pathlib import Path
import json, os

# Par défaut: ../open-data/data (dossier frère). Surcharge via STATSBOMB_DATA_DIR.
DATA_DIR = Path(os.getenv("STATSBOMB_DATA_DIR") or Path(__file__).resolve().parents[1] / "open-data" / "data")

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
