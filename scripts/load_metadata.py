import json
import sys
from pathlib import Path


def load_metadata(path):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    data = json.loads(p.read_text())
    print('Loaded metadata:', data)
    return data


if __name__ == '__main__':
    meta = load_metadata(sys.argv[1])
    print(meta)