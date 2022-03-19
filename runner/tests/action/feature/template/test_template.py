import pytest


@pytest.mark.parametrize("run", ["value_template.json"], indirect=True)
def test_value_template(run):
    assert run == 0
    with open("value_template_string.txt") as f:
        assert f.read() == '42 42'
    with open("value_template_file.txt") as f:
        assert f.read() == '42\n42'
    with open("value_template_empty_string.txt") as f:
        assert f.read() == ''
    with open("value_template_empty_file.txt") as f:
        assert f.read() == ''


@pytest.mark.parametrize("run", ["variable.json"], indirect=True)
def test_variable(run):
    assert run == 0
    with open("variable_continuous.txt") as f:
        assert -2 <= float(f.read()) < 2
    with open("variable_discrete.txt") as f:
        assert int(f.read()) in range(-42, 43)
    with open("variable_discrete_float.txt") as f:
        assert float(f.read()) in [-1.5, -0.5, 0.5, 1.5]
    with open("variable_categorical.txt") as f:
        assert f.read() in ['red', 'green', 'blue']
    with open("variable_file.txt") as f:
        lines = [x.strip() for x in f]
        assert -2 <= float(lines[0]) < 2
        i, f = lines[1].split()
        assert int(i) in range(-42, 43)
        assert float(f) in [-1.5, -0.5, 0.5, 1.5]
        assert lines[2] in ['red', 'green', 'blue']
