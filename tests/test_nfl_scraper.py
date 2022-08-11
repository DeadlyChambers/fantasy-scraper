from nfl_scraper import main
from nfl_scraper.nfl import __version__



def test_version():
    assert __version__ == '0.2.1'

def test_main():
    assert main(["email=a","password=b","id=c","name=d"]) == 1