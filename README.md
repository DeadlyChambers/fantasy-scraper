# fantasy-scraper
Trying to scrape all data from our fantasy league with NFL.com. Since we are moving to Sleeper. It might end up include myfantasyleague as well


## Pipenv and Poetry

Setup

```bash
curl -sSL https://instcurl -sSL https://install.python-poetry.org | python3 -
pipenv install --python=/usr/loca/bin/python3.10
pipenv shell
poetry completions bash >> ~/.bash_completion
#export PIP_PYTHON_PATH="$VIRTUAL_ENV/bin/python3"
poetry new nfl_scraper
poetry new nfl_scraper
#pipenv install --index=pip
#pipenv install --index=distutils
poetry add requests
poetry add html5lib
poetry add bs4


#pip uninstall -y setuptools
#exit
#deactivate 
```

## Running

```bash
pipenv shell
cd nfl_scraper
poetry run python main.py

# Test need to beef these up
poetry run pytest
```