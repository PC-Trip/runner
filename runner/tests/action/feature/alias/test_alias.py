import pytest
import json

import yaml


@pytest.mark.parametrize("run", ["categorical.json"], indirect=True)
def test_categorical(run):
    assert run == 0
    with open('categorical.txt') as f:
        value = f.read().strip()
    assert value in ["red", "green", "blue"]


@pytest.mark.parametrize("run", ["continuous.json"], indirect=True)
def test_continuous(run):
    assert run == 0
    with open('continuous.txt') as f:
        value = float(f.read().strip())
    assert -1.0 <= value < 1.0


@pytest.mark.parametrize("run", ["discrete_int.json"], indirect=True)
def test_discrete_int(run):
    assert run == 0
    with open('discrete_int.txt') as f:
        value = f.read().strip()
    assert value.isdigit() or value.startswith('-') and value[1:].isdigit()
    assert int(value) in [-1, 0, 1]


@pytest.mark.parametrize("run", ["discrete_int_num.json"], indirect=True)
def test_discrete_int_num(run):
    assert run == 0
    with open('discrete_int_num.txt') as f:
        value = f.read().strip()
    assert value.isdigit() or value.startswith('-') and value[1:].isdigit()
    assert int(value) in [-2, 0, 2]


@pytest.mark.parametrize("run", ["discrete_float.json"], indirect=True)
def test_discrete_float(run):
    assert run == 0
    with open('discrete_float.txt') as f:
        value = f.read().strip()
    assert not value.isdigit()
    assert float(value) in [-1.0, 0.0, 1.0]


@pytest.mark.parametrize("run", ["discrete_float_num.json"], indirect=True)
def test_discrete_float_num(run):
    assert run == 0
    with open('discrete_float_num.txt') as f:
        value = f.read().strip()
    assert not value.isdigit()
    assert float(value) in [-1.0, -0.5, 0.0, 0.5, 1.0]


@pytest.mark.parametrize("run", ["continuous_file.json"], indirect=True)
def test_continuous_file(run):
    assert run == 0
    with open('continuous_file.txt') as f:
        value = float(f.read().strip())
    assert -1.0 <= value < 1.0


@pytest.mark.parametrize("run", ["continuous_file_template.json"], indirect=True)
def test_continuous_file_template(run):
    assert run == 0
    with open('continuous_file_template.txt') as f:
        value = float(f.read().strip().split(':')[1].strip())
    assert -1.0 <= value < 1.0


@pytest.mark.parametrize("run", ["continuous_json.json"], indirect=True)
def test_continuous_json(run):
    assert run == 0
    with open('continuous_json_out.json') as f:
        data = json.load(f)
    assert -1.0 <= data['value'] < 1.0


@pytest.mark.parametrize("run", ["continuous_json_input.json"], indirect=True)
def test_continuous_json_input(run):
    assert run == 0
    with open('continuous_json_input_out.json') as f:
        data = json.load(f)
    assert -1.0 <= data['value'] < 1.0
    assert data['value2'] == 42
    assert data['list'] == [1, 2, 3]
    assert data['dict'] == {"a": 1, "b":  2, "c":  3}


@pytest.mark.parametrize("run", ["continuous_yaml.json"], indirect=True)
def test_continuous_yaml(run):
    assert run == 0
    with open('continuous_yaml_out.yaml') as f:
        data = yaml.safe_load(f)
    assert -1.0 <= data['value'] < 1.0


@pytest.mark.parametrize("run", ["continuous_yaml_input.json"], indirect=True)
def test_continuous_yaml_input(run):
    assert run == 0
    with open('continuous_yaml_input_out.yaml') as f:
        data = yaml.safe_load(f)
    assert -1.0 <= data['value'] < 1.0
    assert data['value2'] == 42
    assert data['list'] == [1, 2, 3]
    assert data['dict'] == {"a": 1, "b":  2, "c":  3}


@pytest.mark.parametrize("run", ["discrete_file.json"], indirect=True)
def test_discrete_file(run):
    assert run == 0
    with open('discrete_file.txt') as f:
        value = f.read().strip()
    assert value.isdigit() or value.startswith('-') and value[1:].isdigit()
    assert int(value) in [-1, 0, 1]


@pytest.mark.parametrize("run", ["discrete_file_template.json"], indirect=True)
def test_discrete_file_template(run):
    assert run == 0
    with open('discrete_file_template.txt') as f:
        value = f.read().strip().split(':')[1].strip()
    assert value.isdigit() or value.startswith('-') and value[1:].isdigit()
    assert int(value) in [-1, 0, 1]


@pytest.mark.parametrize("run", ["discrete_json.json"], indirect=True)
def test_discrete_json(run):
    assert run == 0
    with open('discrete_json_out.json') as f:
        data = json.load(f)
    assert data['value'] in [-1, 0, 1]


@pytest.mark.parametrize("run", ["discrete_json_input.json"], indirect=True)
def test_discrete_json_input(run):
    assert run == 0
    with open('discrete_json_input_out.json') as f:
        data = json.load(f)
    assert data['value'] in [-1, 0, 1]
    assert data['value2'] == 42
    assert data['list'] == [1, 2, 3]
    assert data['dict'] == {"a": 1, "b":  2, "c":  3}


@pytest.mark.parametrize("run", ["discrete_yaml.json"], indirect=True)
def test_discrete_yaml(run):
    assert run == 0
    with open('discrete_yaml_out.yaml') as f:
        data = yaml.safe_load(f)
    assert data['value'] in [-1, 0, 1]


@pytest.mark.parametrize("run", ["discrete_yaml_input.json"], indirect=True)
def test_discrete_yaml_input(run):
    assert run == 0
    with open('discrete_yaml_input_out.yaml') as f:
        data = yaml.safe_load(f)
    assert data['value'] in [-1, 0, 1]
    assert data['value2'] == 42
    assert data['list'] == [1, 2, 3]
    assert data['dict'] == {"a": 1, "b":  2, "c":  3}


@pytest.mark.parametrize("run", ["categorical_file.json"], indirect=True)
def test_categorical_file(run):
    assert run == 0
    with open('categorical_file.txt') as f:
        value = f.read().strip()
    assert value in ["red", "green", "blue"]


@pytest.mark.parametrize("run", ["categorical_file_template.json"], indirect=True)
def test_categorical_file_template(run):
    assert run == 0
    with open('categorical_file_template.txt') as f:
        value = f.read().strip().split(':')[1].strip()
    assert value in ["red", "green", "blue"]


@pytest.mark.parametrize("run", ["categorical_json.json"], indirect=True)
def test_categorical_json(run):
    assert run == 0
    with open('categorical_json_out.json') as f:
        data = json.load(f)
    assert data['value'] in ["red", "green", "blue"]


@pytest.mark.parametrize("run", ["categorical_json_input.json"], indirect=True)
def test_categorical_json_input(run):
    assert run == 0
    with open('categorical_json_input_out.json') as f:
        data = json.load(f)
    assert data['value'] in ["red", "green", "blue"]
    assert data['value2'] == 42
    assert data['list'] == [1, 2, 3]
    assert data['dict'] == {"a": 1, "b":  2, "c":  3}


@pytest.mark.parametrize("run", ["categorical_yaml.json"], indirect=True)
def test_categorical_yaml(run):
    assert run == 0
    with open('categorical_yaml_out.yaml') as f:
        data = yaml.safe_load(f)
    assert data['value'] in ["red", "green", "blue"]


@pytest.mark.parametrize("run", ["categorical_yaml_input.json"], indirect=True)
def test_categorical_yaml_input(run):
    assert run == 0
    with open('categorical_yaml_input_out.yaml') as f:
        data = yaml.safe_load(f)
    assert data['value'] in ["red", "green", "blue"]
    assert data['value2'] == 42
    assert data['list'] == [1, 2, 3]
    assert data['dict'] == {"a": 1, "b":  2, "c":  3}


@pytest.mark.parametrize("run", ["regex.json"], indirect=True)
def test_regex(run):
    assert run == 0
    values = [4, 52.706986632, 0.885797144782, 3.8595430149, 248.889829489,
              0.0463496945413, 3.74712588231, 247.483437342, 0.399518064935,
              4.56903994962, 50.5971768535, 0.958371135622, -4.28812108518]
    with open("output_float_all.txt") as f:
        actual = [float(x) for x in f.read().strip()[1:-1].split(',')]
        expected = values[1:]
        assert len(actual) == len(expected)
        assert all([x == y for x, y in zip(actual, expected)])
    with open("output_float_index.txt") as f:
        actual = float(f.read().strip())
        expected = values[1:][3]
        assert actual == expected
    with open("output_float_indices.txt") as f:
        actual = [float(x) for x in f.read().strip()[1:-1].split(',')]
        expected = [values[1:][3], values[1:][5]]
        assert len(actual) == len(expected)
        assert all([x == y for x, y in zip(actual, expected)])
    with open("output_all.txt") as f:
        actual = [float(x) for x in f.read().strip()[1:-1].split(',')]
        expected = values
        assert len(actual) == len(expected)
        assert all([x == y for x, y in zip(actual, expected)])
