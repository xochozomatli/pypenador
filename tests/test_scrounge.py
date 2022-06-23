import os

import pytest
from pypenador.scrounge import (
    buffer, search_buffer, compile_boundary_lists,
    match, retrieve, find_files)


@pytest.fixture
def foo_img():
    with open('foo.img', 'wb') as f:
        f.write(b'oijwsh00pdawh000pjkd')
    yield
    os.remove('foo.img')


class MockMatch:
    def __init__(self, start, end, group):
        self._start = start
        self._end = end
        self._group = group

    def start(self):
        return self._start

    def end(self):
        return self._end

    def group(self):
        return self._group


def test_buffer():
    buf = buffer('tests/data/test.img', 2**28)
    assert len(buf1 := next(buf)) == 2**28
    assert buf1 != next(buf)


# 11         22     29    35  39      47
TESTSTR = b"hlawefhljwefooaw;oijwefoooow;barjowbarefooo;foebareij"


def test_search_buffer():
    bound_ics = search_buffer(TESTSTR, (b"foo", b"bar"))
    assert [m[0] for m in bound_ics] == [11, 22, 29, 35, 39, 47]


def test_match():
    bml = [
        (1, 2, b"bar"), (3, 4, b"foo"),
        (5, 6, b"bar"), (7, 8, b"foo")
    ]
    assert match(bml, b'foo', b'bar') == [(3, 6)]


def test_retrieve(foo_img):
    with open('foo.img', 'rb') as f:
        data = retrieve(f, 4, 17)
        assert data == b'sh00pdawh000p'


def test_find_files():
    with open('tests/data/test.jpg', 'rb') as f:
        jpg = f.read()
    for s in find_files('tests/data/test.img', 'jpg'):
        if s == jpg:
            assert True
            return
    assert False
