import pytest
import json


@pytest.mark.parametrize("run", ["json.json"], indirect=True)
def test_json(run):
    assert run == 0
    expected = {"dict": {
        "int": -42,
        "float": -3.14,
        "string": "green",
        "bool": True,
        "list": [
            ["-1;-2;-3", "-4;-5;-6"],
            ["-7;-8;-9", "-10;-11;-12"]],
        "sub_dict": {
            "int": -10500,
            "float": -2.72,
            "string": "red",
            "bool": False,
            "list": [
                ["-12;-11;-10", "9;-8;7"],
                ["6;5;4", "3;2;1"]]}}}
    with open('output.json') as f:
        actual = json.load(f)
        assert actual['dict']['int'] == expected['dict']['int']
        assert actual['dict']['float'] == expected['dict']['float']
        assert actual['dict']['string'] == expected['dict']['string']
        assert actual['dict']['bool'] == expected['dict']['bool']
        assert len(actual['dict']['list']) == len(expected['dict']['list'])
        assert all([x == y for x, y in zip(actual['dict']['list'], expected['dict']['list'])])
        assert actual['dict']['sub_dict']['int'] == expected['dict']['sub_dict']['int']
        assert actual['dict']['sub_dict']['float'] == expected['dict']['sub_dict']['float']
        assert actual['dict']['sub_dict']['string'] == expected['dict']['sub_dict']['string']
        assert actual['dict']['sub_dict']['bool'] == expected['dict']['sub_dict']['bool']
        assert len(actual['dict']['sub_dict']['list']) == len(expected['dict']['sub_dict']['list'])
        assert all([x == y for x, y in zip(actual['dict']['sub_dict']['list'], expected['dict']['sub_dict']['list'])])
