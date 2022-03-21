import pytest
from pathlib import Path


@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    with open('input.txt', 'w') as f:
        f.write(f'x 3')
    with open('output.txt', 'w') as f:
        f.write(f'y 9')


@pytest.mark.parametrize("run", ["optimize.json"], indirect=True)
def test_optimize(run):
    assert run == 0
    with open('input.txt') as f:
        _, x = f.read().strip().split()
    assert '3' == x
    with open('output.txt') as f:
        _, y = f.read().strip().split()
    assert '9' == y


@pytest.mark.parametrize("run", ["optimize_clean_trial.json"], indirect=True)
def test_optimize_clean_trial(run):
    assert run == 0
    with open('input.txt') as f:
        _, x = f.read().strip().split()
    assert '3' == x
    with open('output.txt') as f:
        _, y = f.read().strip().split()
    assert '9' == y
    p = Path('work/clean_trial')
    assert p.exists()
    trials = [x for x in p.glob('[0-9]*') if x.is_dir()]
    assert len(trials) == 0


@pytest.mark.parametrize("run", ["optimize_clean_study.json"], indirect=True)
def test_optimize_clean_study(run):
    assert run == 0
    with open('input.txt') as f:
        _, x = f.read().strip().split()
    assert '3' == x
    with open('output.txt') as f:
        _, y = f.read().strip().split()
    assert '9' == y
    p = Path('work/clean_study')
    assert not p.exists()


@pytest.mark.parametrize("run", ["optimize_clean_work.json"], indirect=True)
def test_optimize_clean_work(run):
    assert run == 0
    with open('input.txt') as f:
        _, x = f.read().strip().split()
    assert '3' == x
    with open('output.txt') as f:
        _, y = f.read().strip().split()
    assert '9' == y
    p = Path('work')
    assert not p.exists()


@pytest.mark.parametrize("run", ["no_optimize.json"], indirect=True)
def test_no_optimize(run):
    assert run == 0
    with open('input.txt') as f:
        _, x = f.read().strip().split()
    assert '3' == x
    with open('output.txt') as f:
        _, y = f.read().strip().split()
    assert '9' == y


@pytest.mark.parametrize("run", ["no_optimize_sub_call.json"], indirect=True)
def test_no_optimize_sub_call(run):
    assert run == 0
    with open('input.txt') as f:
        _, x = f.read().strip().split()
    x = float(x)
    assert -2.0 <= x < 2.0
    with open('output.txt') as f:
        _, y = f.read().strip().split()
    y = float(y)
    assert x ** 2 == pytest.approx(y)


@pytest.mark.parametrize("run", ["optimize_sub_call.json"], indirect=True)
def test_optimize_sub_call(run):
    assert run == 0
    with open('input.txt') as f:
        _, x = f.read().strip().split()
    x = float(x)
    assert -2.0 <= x < 2.0
    with open('output.txt') as f:
        _, y = f.read().strip().split()
    y = float(y)
    print(x, y)
    assert x ** 2 == pytest.approx(y)


@pytest.mark.parametrize("run", ["optimize_sub_call_best.json"], indirect=True)
def test_optimize_sub_call_best(run):
    assert run == 0
    with open('input.txt') as f:
        _, x = f.read().strip().split()
    x = float(x)
    assert -2.0 <= x < 2.0
    with open('output.txt') as f:
        _, y = f.read().strip().split()
    y = float(y)
    print(x, y)
    assert x ** 2 == pytest.approx(y)


@pytest.mark.parametrize("run", ["optimize_sub_call_index.json"], indirect=True)
def test_optimize_sub_call_index(run):
    assert run == 0
    with open('input.txt') as f:
        _, x = f.read().strip().split()
    x = float(x)
    assert -2.0 <= x < 2.0
    with open('output.txt') as f:
        _, y = f.read().strip().split()
    y = float(y)
    print(x, y)
    assert x ** 2 == pytest.approx(y)


@pytest.mark.parametrize("run", ["optimize_sqlite.json"], indirect=True)
def test_optimize_sqlite(run):
    assert run == 0
    with open('input.txt') as f:
        _, x = f.read().strip().split()
    assert '3' == x
    with open('output.txt') as f:
        _, y = f.read().strip().split()
    assert '9' == y


@pytest.mark.parametrize("run", ["no_optimize_sub_call_best_from_sqlite.json"], indirect=True)
def test_no_optimize_sub_call_best_from_sqlite(run):
    assert run == 0
    with open('input.txt') as f:
        _, x = f.read().strip().split()
    x = float(x)
    assert -2.0 <= x < 2.0
    with open('output.txt') as f:
        _, y = f.read().strip().split()
    y = float(y)
    print(x, y)
    assert x ** 2 == pytest.approx(y)


@pytest.mark.parametrize("run", ["no_optimize_sub_call_index_from_sqlite.json"], indirect=True)
def test_no_optimize_sub_call_index_from_sqlite(run):
    assert run == 0
    with open('input.txt') as f:
        _, x = f.read().strip().split()
    x = float(x)
    assert -2.0 <= x < 2.0
    with open('output.txt') as f:
        _, y = f.read().strip().split()
    y = float(y)
    print(x, y)
    assert x ** 2 == pytest.approx(y)
