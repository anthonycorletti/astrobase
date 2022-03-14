from astrobasecloud import __version__


def test_version() -> None:
    assert __version__ is not None
