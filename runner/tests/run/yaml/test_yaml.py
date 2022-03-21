import pytest


@pytest.mark.parametrize("plot", ["action.yml"], indirect=True)
def test_plot(plot):
    assert plot == 0


@pytest.mark.parametrize("run", ["action.yml"], indirect=True)
def test_run(run):
    assert run == 0
