import pytest


@pytest.mark.parametrize("run", ["set_default.json"], indirect=True)
def test_set_default(run):
    assert run == 0
    with open('set_default.txt') as f:
        assert 42 == int(f.read().strip())


@pytest.mark.parametrize("run", ["set_route_attr.json"], indirect=True)
def test_set_route_attr(run):
    assert run == 0
    with open('set_attr.txt') as f:
        assert 42 == int(f.read().strip())


@pytest.mark.parametrize("run", ["set_route_attr_list.json"], indirect=True)
def test_set_route_attr_list(run):
    assert run == 0
    with open('set_route_attr_list.txt') as f:
        assert 42 == int(f.read().strip())


@pytest.mark.parametrize("run", ["set_route_attr_dict.json"], indirect=True)
def test_set_route_attr_dict(run):
    assert run == 0
    with open('set_route_attr_dict.txt') as f:
        assert 42 == int(f.read().strip())


@pytest.mark.parametrize("run", ["set_route_attr_dict_num.json"], indirect=True)
def test_set_route_attr_dict_num(run):
    assert run == 0
    with open('set_route_attr_dict_num.txt') as f:
        assert 42 == int(f.read().strip())


@pytest.mark.parametrize("run", ["set_route_attr_mix_num.json"], indirect=True)
def test_set_route_attr_mix_num(run):
    assert run == 0
    with open('set_route_attr_mix_num.txt') as f:
        assert 42 == int(f.read().strip())