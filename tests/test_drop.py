import pytest


@pytest.mark.parametrize("a, b",
                         [(1, 1),
                          (1, 2)])
def test_drop_to(a, b):
    assert a == b
