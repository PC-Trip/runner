import pytest


@pytest.fixture(autouse=True)
def run_around_tests(request, monkeypatch):
    monkeypatch.chdir(request.fspath.dirname)
    with open('input.txt', 'w') as f:
        f.write(f'x 3')
    with open('output.txt', 'w') as f:
        f.write(f'y 9')
    try:
        yield
    finally:
        with open('input.txt', 'w') as f:
            f.write(f'x 3')
        with open('output.txt', 'w') as f:
            f.write(f'y 9')


@pytest.mark.parametrize("run", ["fixed_best_new_study.yml"], indirect=True)
def test_fixed_best_new_study(run):
    assert run == 0
    with open('input.txt') as f:
        _, x = f.read().strip().split()
    assert '3' == x
    with open('output.txt') as f:
        _, y = f.read().strip().split()
    assert '9' == y


@pytest.mark.parametrize("run", ["optimize.yml"], indirect=True)
def test_optimize(run):
    assert run == 0
    with open('input.txt') as f:
        _, x = f.read().strip().split()
    assert '3' == x
    with open('output.txt') as f:
        _, y = f.read().strip().split()
    assert '9' == y


@pytest.mark.parametrize("run", ["fixed.yml"], indirect=True)
def test_fixed(run):
    assert run == 0
    with open('input.txt') as f:
        _, x = f.read().strip().split()
    assert '3' == x
    with open('output.txt') as f:
        _, y = f.read().strip().split()
    assert '9' == y


@pytest.mark.parametrize("run", ["fixed_default.yml"], indirect=True)
def test_fixed_default(run):
    assert run == 0
    with open('input.txt') as f:
        _, x = f.read().strip().split()
    assert '3' == x
    with open('output.txt') as f:
        _, y = f.read().strip().split()
    assert '9' == y


@pytest.mark.parametrize("run", ["fixed_default_best.yml"], indirect=True)
def test_fixed_default_best(run):
    assert run == 0
    with open('input.txt') as f:
        _, x = f.read().strip().split()
    assert '3' == x
    with open('output.txt') as f:
        _, y = f.read().strip().split()
    assert '9' == y


@pytest.mark.parametrize("run", ["optimize_multi.yml"], indirect=True)
def test_optimize_multi(run):
    assert run == 0
    with open('input.txt') as f:
        _, x = f.read().strip().split()
    assert '3' == x
    with open('output.txt') as f:
        _, y = f.read().strip().split()
    assert '9' == y


@pytest.mark.parametrize("run", ["fixed_default_multi.yml"], indirect=True)
def test_fixed_default_multi(run):
    assert run == 0
    with open('input.txt') as f:
        _, x = f.read().strip().split()
    assert '3' == x
    with open('output.txt') as f:
        _, y = f.read().strip().split()
    assert '9' == y


@pytest.mark.parametrize("run", ["fixed_default_best_multi.yml"], indirect=True)
def test_fixed_default_best_multi(run):
    assert run == 0
    with open('input.txt') as f:
        _, x = f.read().strip().split()
    assert '3' == x
    with open('output.txt') as f:
        _, y = f.read().strip().split()
    assert '9' == y

