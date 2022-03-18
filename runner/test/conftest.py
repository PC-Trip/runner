import sys
import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def run(request):
    python = sys.executable
    cfd = Path(__file__).parent.resolve()
    root = cfd.parent
    script = root / "run.py"
    p = Path(request.param).resolve()
    args = [python, str(script), str(p)]
    result = subprocess.run(args)
    return result.returncode
