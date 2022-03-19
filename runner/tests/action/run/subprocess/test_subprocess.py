import pytest


@pytest.mark.parametrize("run", ["echo.json"], indirect=True)
def test_echo(run):
    assert run == 0
    with open('good_echo.err') as f:
        assert f.read() == ''
    with open('good_echo.out') as f:
        assert f.read().strip() == '"Hello world!"'
