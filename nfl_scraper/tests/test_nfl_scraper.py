from nfl_scraper import __version__
from nfl_scraper import main


def test_version():
    assert __version__ == '0.1.0'

def test_main():
    assert main.main() == 1