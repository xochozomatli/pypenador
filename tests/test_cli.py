import pytest

from pypenador.cli import parse_args


def test_cli_if():
    """
    Test if '-if' argument is working
    """
    args = parse_args('-if=foo.img -ftype=jpg -outdir=bar'.split())
    print(args.__dict__)
    assert 'if' in args
    assert args.__dict__['if'] == 'foo.img'
    assert 'ftype' in args
    assert args.__dict__['ftype'] == 'jpg'
    assert 'outdir' in args
    assert args.__dict__['outdir'] == 'bar'
    with pytest.raises(SystemExit):
        parse_args([])
