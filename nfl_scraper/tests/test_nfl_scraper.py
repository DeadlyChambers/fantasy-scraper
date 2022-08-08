from nfl_scraper import __version__
from nfl_scraper.main import main


def test_version():
    assert __version__ == '0.2.0'

def test_main():
    assert main.main() == 1