import sys
import subprocess
from pathlib import Path

import pytest


@pytest.fixture()
def run(request, monkeypatch):
    monkeypatch.chdir(request.fspath.dirname)
    python = sys.executable
    cfd = Path(__file__).parent.resolve()
    root = cfd.parent
    script = root / "run.py"
    p = Path(request.param).resolve()
    args = [python, str(script), str(p)]
    result = subprocess.run(args)
    return result.returncode


@pytest.fixture()
def plot(request, monkeypatch):
    monkeypatch.chdir(request.fspath.dirname)
    python = sys.executable
    cfd = Path(__file__).parent.resolve()
    root = cfd.parent
    script = root / "plot.py"
    p = Path(request.param).resolve()
    args = [python, str(script), str(p)]
    result = subprocess.run(args)
    return result.returncode
